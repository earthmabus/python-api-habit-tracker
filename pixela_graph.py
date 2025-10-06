import requests
import time
import random
import datetime as dt
import json

# number of maximum retries when issuing a request against pixela
MAX_RETRIES = 7

class PixelaGraph:

    def __init__(self, pixela_token: str, pixela_username: str):
        self.m_pixela_token = pixela_token
        self.m_pixela_username =pixela_username
        self.m_graph_id = -1

    # create a graph
    def create_graph(self, graph_id, graph_name, unit, type, color):
        '''visit https://pixe.la/v1/users/earthmabus/graphs/graph1.html afterwards'''
        self.m_graph_id = graph_id

        headers = {"X-USER-TOKEN": self.m_pixela_token}
        payload = {
            "id": self.m_graph_id,
            "name": graph_name,
            "unit": unit,
            "type": type,
            "color": color
        }
        response = requests.post(url=f"https://pixe.la/v1/users/{self.m_pixela_username}/graphs", json=payload, headers=headers)
        if response.status_code == 409:
            return json.loads(response.text)
        response.raise_for_status()
        return json.loads(response.text)

    def post_pixel(self, date_str, quantity):
        '''posts a pixel on the graph'''
        num_retries = MAX_RETRIES
        except_to_return: BaseException = None
        while num_retries > 0:
            try:
                headers = {"X-USER-TOKEN": self.m_pixela_token}
                payload = {
                    "date": date_str,
                    "quantity": str(quantity)
                }
                response = requests.post(url=f"https://pixe.la/v1/users/{self.m_pixela_username}/graphs/{self.m_graph_id}", json=payload, headers=headers)

                # did we experience any issues?
                response.raise_for_status()

                # there were no issues, exit this loop and return
                return json.loads(response.text)
            except requests.exceptions.HTTPError as e:
                if "not a Pixela supporter" in e.response.json()['message']:
                    except_to_return = e
                    num_retries -= 1
                    time.sleep(random.randint(1, 3))
                    print(
                        f"post_pixel: retrying ({self.m_graph_id}, {date_str}, {quantity}) due to not being pixela supporter")
                else:
                    raise e

        # if we're here, that means we've failed on all of our attempts to post this pixel due to not being a pixela
        # supporter... raise the exception
        print(f"post_pixel: unable to create pixel for ({self.m_graph_id}, {date_str}, {quantity}) -- raising exception")
        raise except_to_return

    def update_pixel(self, date_str, quantity):
        '''updates a pixel on the graph'''
        num_retries = MAX_RETRIES
        except_to_return: BaseException = None
        while num_retries > 0:
            try:
                headers = {"X-USER-TOKEN": self.m_pixela_token}
                payload = {
                    "quantity": str(quantity)
                }
                time_now = dt.datetime.now()
                time_now_as_string = time_now.strftime("%Y%m%d")
                response = requests.put(
                    url=f"https://pixe.la/v1/users/{self.m_pixela_username}/graphs/{self.m_graph_id}/{time_now_as_string}",
                    json=payload, headers=headers)

                # did we experience any issues?
                response.raise_for_status()

                # there were no issues, exit this loop and return
                return json.loads(response.text)
            except requests.exceptions.HTTPError as e:
                if "not a Pixela supporter" in e.response.json()['message']:
                    except_to_return = e
                    num_retries -= 1
                    time.sleep(random.randint(1, 3))
                    print(
                        f"update_pixel: retrying ({self.m_graph_id}, {date_str}, {quantity}) due to not being pixela supporter")
                else:
                    raise e

        # if we're here, that means we've failed on all of our attempts to post this pixel due to not being a pixela
        # supporter... raise the exception
        print(f"update_pixel: unable to create pixel for ({self.m_graph_id}, {date_str}, {quantity}) -- raising exception")
        raise except_to_return

    def delete_pixel(self, date_str):
        '''deletes a pixel from the graph'''
        num_retries = MAX_RETRIES
        except_to_return: BaseException = None
        while num_retries > 0:
            try:
                headers = {"X-USER-TOKEN": self.m_pixela_token}
                time_now = dt.datetime.now()
                time_now_as_string = time_now.strftime("%Y%m%d")
                response = requests.delete(
                    url=f"https://pixe.la/v1/users/{self.m_pixela_username}/graphs/{self.m_graph_id}/{time_now_as_string}",
                    headers=headers)

                # did we experience any issues?
                response.raise_for_status()

                # there were no issues, exit this loop and return
                return json.loads(response.text)
            except requests.exceptions.HTTPError as e:
                if "not a Pixela supporter" in e.response.json()['message']:
                    except_to_return = e
                    num_retries -= 1
                    time.sleep(random.randint(1, 3))
                    print(
                        f"delete_pixel: retrying ({self.m_graph_id}, {date_str}) due to not being pixela supporter")
                else:
                    raise e

        # if we're here, that means we've failed on all of our attempts to post this pixel due to not being a pixela
        # supporter... raise the exception
        print(f"delete_pixel: unable to create pixel for ({self.m_graph_id}, {date_str}) -- raising exception")
        raise except_to_return
