import os
import requests
import time
import random
import json

pixela_token = os.environ.get("PIXELA_TOKEN")
pixela_username = os.environ.get("PIXELA_USERNAME")

def create_account():
    '''creates an account on pixe.la'''
    # this is the request that is sent to pixela
    # curl -X POST https://pixe.la/v1/users -d '{"token":"thisissecret", "username":"a-know", "agreeTermsOfService":"yes", "notMinor":"yes"}'
    # {"message":"Success.","isSuccess":true}
    #
    # this is the response that's sent from pixela
    # {"message": "Success. Let's visit https://pixe.la/@earthmabus , it is your profile page!", "isSuccess": true}

    params = { "token": pixela_token, "username": pixela_username, "agreeTermsOfService": "yes", "notMinor": "yes" }
    response = requests.post(url="https://pixe.la/v1/users", json=params)
    #response.raise_for_status()

    # this is the response that's sent from pixela
    # {"message": "Success. Let's visit https://pixe.la/@earthmabus , it is your profile page!", "isSuccess": true}
    return json.loads(response.text)

# create a graph
def create_graph(graph_id, graph_name, unit, type, color):
    '''visit https://pixe.la/v1/users/earthmabus/graphs/graph1.html afterwards'''
    headers = { "X-USER-TOKEN": pixela_token }
    payload = {
        "id": graph_id,
        "name": graph_name,
        "unit": unit,
        "type": type,
        "color": color
    }
    response = requests.post(url=f"https://pixe.la/v1/users/{pixela_username}/graphs", json=payload, headers=headers)
    if response.status_code == 409:
        return json.loads(response.text)
    response.raise_for_status()
    return json.loads(response.text)

def post_pixel(graph_id, date_str, quantity):
    '''posts a pixel on the graph'''
    num_retries = 7
    except_to_return: BaseException = None
    while num_retries > 0:
        try:
            print(f"trying {num_retries}")
            headers = { "X-USER-TOKEN": pixela_token }
            payload = {
                "date": date_str,
                "quantity": str(quantity)
            }
            response = requests.post(url=f"https://pixe.la/v1/users/{pixela_username}/graphs/{graph_id}", json=payload, headers=headers)

            # did we experience any issues?
            response.raise_for_status()

            # there were no issues, exit this loop and return
            return json.loads(response.text)
        except requests.exceptions.HTTPError as e:
            if "not a Pixela supporter" in e.response.json()['message']:
                except_to_return = e
                num_retries -= 1
                time.sleep(random.randint(1, 3))
                print(f"retrying ({graph_id}, {date_str}, {quantity}) due to not being pixela supporter")
            else:
                raise e

    # if we're here, that means we've failed on all of our attempts to post this pixel due to not being a pixela
    # supporter... raise the exception
    print(f"Unable to create pixel for ({graph_id}, {date_str}, {quantity}) -- Raising exception")
    raise except_to_return

# create a pixela account
try:
    response_create_acct = create_account()
    if not response_create_acct['isSuccess']:
        print("You account was NOT successfully created; please try again")
        print(response_create_acct['message'])
    else:
        print(f"Successfully created account '{pixela_username}'")
except requests.exceptions.HTTPError as e:
    print(e)
    print(f"Your account with username='{pixela_username}' with token='{pixela_token}' was NOT successfully created; please try again")
    print(e.response.json()['message'])

# create a new graph
# afterwards, can visit: https://pixe.la/v1/users/earthmabus/graphs/graph1.html
my_running_graph_id = "graph1"
my_running_graph_name = "Running Graph"
try:
    response_create_graph = create_graph(my_running_graph_id, my_running_graph_name, "minute", "int", "shibafu")
    if not response_create_graph['isSuccess']:
        print(f"Your graph id='{my_running_graph_id}' with name='{my_running_graph_name}' was NOT successfully created; {response_create_graph["message"]}")
    else:
        print(f'Successfully created "{my_running_graph_name}"!')
except requests.exceptions.HTTPError as e:
    print(e)
    print(f"Your graph id='{my_running_graph_id}' with name='{my_running_graph_name}' was NOT successfully created; please try again")
    print(e.response.json()['message'])

# post data to the graph
try:
    post_pixel(my_running_graph_id, "20250821", 40)
    post_pixel(my_running_graph_id, "20250824", 40)
    post_pixel(my_running_graph_id, "20250827", 40)
    post_pixel(my_running_graph_id, "20250827", 40)
    post_pixel(my_running_graph_id, "20250901", 40)
    post_pixel(my_running_graph_id, "20250904", 40)
    post_pixel(my_running_graph_id, "20250907", 40)
    post_pixel(my_running_graph_id, "20250910", 40)
    post_pixel(my_running_graph_id, "20250915", 40)
    post_pixel(my_running_graph_id, "20250919", 40)
    post_pixel(my_running_graph_id, "20250921", 40)
    post_pixel(my_running_graph_id, "20250924", 40)
    post_pixel(my_running_graph_id, "20251004", 40)
except requests.exceptions.HTTPError as e:
    print(f"Encountered issue when attempting to post data point to id='{my_running_graph_id}; please try again")
    print(e.response.json()['message'])
    exit(-1)
