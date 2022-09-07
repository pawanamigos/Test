import json
import requests
from tests.API_Tests.Utils import convert_images
import os
from jsonschema import validate

#Had issues to start up a local server. SO have cretaed a placeholder for the endpoints and access keys. A few sample smoke tests have been added and is expected to run without mocks and on a real system
image_update_endpoint = ""
images_endpoint = ""
API_Access_Key = ""

schema = {
    "$schema": "https://json-schema.org/draft/2019-09/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "default": {},
    "title": "Root Schema",
    "required": [
        "created_by",
        "created_timestamp",
        "filename",
        "id",
        "size",
        "uploaded_timestamp"
    ],
    "properties": {
        "created_by": {
            "type": "string",
            "default": "",
            "title": "The created_by Schema",
            "examples": [
                "user-id"
            ]
        },
        "created_timestamp": {
            "type": "integer",
            "default": 0,
            "title": "The created_timestamp Schema",
            "examples": [
                1635973200
            ]
        },
        "filename": {
            "type": "string",
            "default": "",
            "title": "The filename Schema",
            "examples": [
                "image-00000.dcm"
            ]
        },
        "id": {
            "type": "integer",
            "default": 0,
            "title": "The id Schema",
            "examples": [
                204
            ]
        },
        "size": {
            "type": "integer",
            "default": 0,
            "title": "The size Schema",
            "examples": [
                53936
            ]
        },
        "uploaded_timestamp": {
            "type": "integer",
            "default": 0,
            "title": "The uploaded_timestamp Schema",
            "examples": [
                1635973200
            ]
        }
    },
    "examples": [{
        "created_by": "user-id",
        "created_timestamp": 1635973200,
        "filename": "image-00000.dcm",
        "id": 204,
        "size": 53936,
        "uploaded_timestamp": 1635973200
    }]
}

converted_image_folder = os.path.join('C:/', 'Users', 'Pawan', 'tagged-image-manager-challenge-main','tests','API_Tests','Test_Files')

##Test validates upload of images from a folder and successfull status is verified for each upload. Schema validation is performed on the returned json response.
def test_verify_image_update():
    headers = {"Content-Type": "application/json"}
    print("Uploading image files from Image repository")
    for filename in os.listdir(converted_image_folder):
        updated_image = filename.split(".", maxsplit=1)[0]
        payload= json.dumps(
            {
                "filename": updated_image,
                "image_data": convert_images.image_to_base64(filename),
                "tags": ["MRI", "Lumbar", "Scan"],
            }
        ),
        try:
            response = requests.post(image_update_endpoint, auth=(API_Access_Key), files=payload, headers=headers)
            try:
                validate(instance=response.json(),schema=schema)
                validate_condition = True
            except Exception as e:
                validate_condition = False
        except Exception as e:
            print(e)
        assert response.status_code == 200
        assert validate_condition == True

def test_verify_total_images_uploaded():
    total_files = len(os.listdir(r'C:\Users\Pawan\PycharmProjects\tagged-image-manager-challenge-main\tests\API_Tests\Test_Files'))
    try:
        response = requests.post(images_endpoint, auth=(API_Access_Key)).json()
    except Exception as e:
        print(e)
    assert response['meta']['total_results'] == total_files

def test_list_all_file_names():
    for filename in os.listdir(converted_image_folder):
            image_url = images_endpoint+ "/" +filename   #Builds an URI for each uploaded image. Note that file name might have to be parsed depending on how the file name is used in the URI
            try:
                response = requests.post(image_url, auth=(API_Access_Key)).json()
                print(response['filename'])
                response_ok_flag = True
            except Exception as e:
                print(e)
                response_ok_flag = False
                assert response_ok_flag == False
    assert response_ok_flag == True


def test_get_all_image_tags():
    for filename in os.listdir(converted_image_folder):
        image_url = images_endpoint + "/" + filename  #Builds an URI for each uploaded image. Note that file name might have to be parsed depending on how the file name is used in the URI
        try:
            response = requests.post(image_url, auth=(API_Access_Key)).json()
            print(response['tags'][0])
            tag_ok_flag = True
        except Exception as e:
            print(e)
            tag_ok_flag = False
            assert tag_ok_flag == False
    assert tag_ok_flag == True

















