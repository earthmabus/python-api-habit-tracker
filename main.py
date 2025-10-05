import os
import requests

def create_account():
    '''creates an account on pixe.la'''
    # this is the request that is sent to pixela
    # curl -X POST https://pixe.la/v1/users -d '{"token":"thisissecret", "username":"a-know", "agreeTermsOfService":"yes", "notMinor":"yes"}'
    # {"message":"Success.","isSuccess":true}
    #
    # this is the response that's sent from pixela
    # {"message": "Success. Let's visit https://pixe.la/@earthmabus , it is your profile page!", "isSuccess": true}

    pixela_token = os.environ.get("PIXELA_TOKEN")
    pixela_username = os.environ.get("PIXELA_USERNAME")

    params = { "token": pixela_token, "username": pixela_username, "agreeTermsOfService": "yes", "notMinor": "yes" }
    response = requests.post(url="https://pixe.la/v1/users", json=params)

    # this is the response that's sent from pixela
    # {"message": "Success. Let's visit https://pixe.la/@earthmabus , it is your profile page!", "isSuccess": true}
    print(response.text)
    return response.text

# create a pixela account
successfully_created_account = create_account()
if successfully_created_account['isSuccess'] == "false":
    print("You account was NOT successfully created; please try again")
    print(successfully_created_account['message'])
    exit(-1)

