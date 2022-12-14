import json
from typing import List, Optional
from unittest import mock

import pytest
from chalice.test import Client
from freezegun import freeze_time
from sqlalchemy.orm.session import Session

from app import app
from chalicelib.db import get_or_create
from chalicelib.models import Image, Tag
from tests.helpers import dict_assert


def build_image(
    db_session: Session,
    id: Optional[int] = None,
    created_by: str = "test-user",
    created_timestamp: int = 1635926694,
    size=256000,
    upload_timestamp: Optional[int] = 1635926694,
    prefix: Optional[str] = None,
    tags: Optional[List[str]] = ["foo", "bar", "baz"],
) -> Image:
    filename = f"sample-{id}.dcm"
    if prefix is None and upload_timestamp is not None:
        prefix = "archive/2021/11/03/19-06-{id}/"

    image = Image(
        id=id,
        filename=filename,
        created_by=created_by,
        created_timestamp=created_timestamp,
        size=size,
        upload_timestamp=upload_timestamp,
        prefix=prefix,
    )

    if tags is not None:
        for tag in tags:
            tag_rec: Tag = get_or_create(db_session, Tag, name=tag)
            image.tags.append(tag_rec)

    db_session.add(image)
    db_session.commit()
    return image


@freeze_time("2021-11-03 21:00:00")
def test_images(db_session: Session, snapshot):
    for i in range(1, 200):
        build_image(db_session=db_session, id=i)

    with Client(app) as client:
        response = client.http.get("/v1/images").json_body
        assert response.get("meta") is not None
        print(type(response))


        dict_assert(response, snapshot, "page-1")
        # get second page
        response = client.http.get("/v1/images?page=1").json_body
        dict_assert(response, snapshot, "page-2")
        assert response.get("meta") is not None


@freeze_time("2021-11-03 21:00:00")
def test_post_image(db_session: Session, snapshot):
    with Client(app) as client:
        response = client.http.post(
            "/v1/images",
            headers={"Content-Type": "application/json"},
            body=json.dumps(
                {"filename": "test.dcm", "size": 1234, "tags": ["bar", "baz"]}
            ),
        ).json_body

        assert isinstance(response["id"], int)
        assert response["upload_url"].startswith("http")
        image = db_session.query(Image).first()
        assert len(image.tags) > 0


@freeze_time("2021-11-03 21:00:00")
def test_image(db_session):
    build_image(db_session=db_session)

    with Client(app) as client:
        response = client.http.get("/v1/images/1").json_body
        del response["url"]
        assert response == {
            "created_by": "test-user",
            "created_timestamp": 1635926694,
            "filename": "sample-1.dcm",
            "id": 1,
            "size": 256000,
            "tags": [
                {"id": 1, "name": "foo"},
                {"id": 2, "name": "bar"},
                {"id": 3, "name": "baz"},
            ],
            "uploaded_timestamp": 1635926694,
        }


@freeze_time("2021-11-03 21:00:00")
def test_image_update(db_session, snapshot):
    image = build_image(db_session=db_session, tags=["foo"])

    with Client(app) as client:
        response = client.http.put(
            f"/v1/images/{image.id}",
            headers={"Content-Type": "application/json"},
            body=json.dumps({"tags": ["foo", "bar", "baz"]}),
        ).json_body
        del response["url"]
        del response["filename"]
        dict_assert(response, snapshot)

    assert "foo" in [t.name for t in image.tags]


def test_image_delete(db_session, snapshot):
    image = build_image(db_session=db_session, tags=["foo"])
    id = image.id

    with Client(app) as client:
        response = client.http.delete("/v1/images/1").json_body
        assert response == {}

    db_session.query(Image).filter_by(id=id).count() == 0
