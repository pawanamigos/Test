import requests
import json
import urllib3
import os
import base64
import time
import sys

urllib3.disable_warnings()

"""Converting Images to be uploaded to Base 64 and to String for Json payload"""


#Currently not using this utility. This could be used to diretcly genarate a json payload to update the image. This could be modified to add fille name and tags to create a json payload and can directly post to the endpoint for updating images
def convert_images():
    os.chdir(r'C:\Users\Pawan\PycharmProjects\tagged-image-manager-challenge-main\tests\API_Tests\Test_Files')
    for image in os.listdir(r'C:\Users\Pawan\PycharmProjects\tagged-image-manager-challenge-main\tests\API_Tests\Test_Files'):
        with open(os.path.join(os.getcwd(), image), 'rb') as image_file:
            json_filename = image.strip(".PNG")
            json_output = open('C:/Users/Pawan/PycharmProjects/tagged-image-manager-challenge-main/tests/API_Tests/Attachments/' + str(json_filename) + '.json', 'w')
            json_data = {"data": image_to_base64(image_file), "filename": image, "contentType": "image/png"}
            json.dump(json_data, json_output)

"""Converting Image to base64"""

def image_to_base64(image):
    encoded_image = base64.b64encode(image.read())
    encoded_image_string = encoded_image.decode("utf-8")
    return encoded_image_string
