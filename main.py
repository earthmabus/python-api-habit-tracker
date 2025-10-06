import os
import requests
import json
from pixela_graph import PixelaGraph

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

# create a PixelaGraph
graph = PixelaGraph(pixela_token, pixela_username)

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
    response_create_graph = graph.create_graph(my_running_graph_id, my_running_graph_name, "minute", "int", "shibafu")
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
    graph.post_pixel("20250821", 40)
    graph.post_pixel("20250824", 40)
    graph.post_pixel("20250827", 40)
    graph.post_pixel("20250827", 40)
    graph.post_pixel("20250901", 40)
    graph.post_pixel("20250904", 40)
    graph.post_pixel("20250907", 40)
    graph.post_pixel("20250910", 40)
    graph.post_pixel("20250915", 40)
    graph.post_pixel("20250919", 40)
    graph.post_pixel("20250921", 40)
    graph.post_pixel("20250924", 40)
    graph.post_pixel("20251004", 40)

    graph.update_pixel("20251004", 1000)

    graph.delete_pixel("20251004")
except requests.exceptions.HTTPError as e:
    print(f"Encountered issue when attempting to post data point to id='{my_running_graph_id}; please try again")
    print(e.response.json()['message'])
