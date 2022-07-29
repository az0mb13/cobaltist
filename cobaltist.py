import os
from dotenv import load_dotenv
import requests
import json
import time
import datetime
from todoist_api_python.api import TodoistAPI

load_dotenv()
API_KEY = os.getenv('cobalt_key')
API_URL = 'https://api.cobalt.io'
TODO_API = TodoistAPI(os.getenv('TODO_API'))

Headers = {'Authorization': 'bearer ' + API_KEY}

org_tokens = []
all_pentests = []

def get_all_orgs():
    orgs = requests.get(API_URL + '/orgs?limit=5', headers=Headers)
    json_orgs = orgs.json()
    total_orgs = len(json_orgs['data']) #total number of orgs
    

    for i in range(0, total_orgs):
        org_tokens.append(json_orgs["data"][i]['resource']['token'])


def get_all_pt():
    date_of_today = str(datetime.date.today())
    today_is = datetime.datetime.strptime(date_of_today, "%Y-%m-%d")

    for token in org_tokens:
        pentests = requests.get(API_URL + '/pentests?limit=1000', headers={'Authorization': 'bearer ' + API_KEY, 'X-Org-Token': token})
        json_pentests = pentests.json()

        start_date = json_pentests["data"][0]['resource']['start_date']
        pt_start = datetime.datetime.strptime(start_date, "%b %d %Y")
        
        if(pt_start >= today_is):
            task = TODO_API.add_task(content='Buy Milk', project_id=2290748296, section_id=88110232)
            TODO_API.add_task(content='Update 1', project_id=2290748296, section_id=88110232, parent_id=task.id, due_string='2 days from today at 9 pm')
            TODO_API.add_task(content='Update 2', project_id=2290748296, section_id=88110232, parent_id=task.id, due_string='6 days from today at 9 pm')
            TODO_API.add_task(content='Update 3', project_id=2290748296, section_id=88110232, parent_id=task.id, due_string='10 days from today at 9 pm')
            TODO_API.add_task(content='Update 4', project_id=2290748296, section_id=88110232, parent_id=task.id, due_string='13 days from today at 9 pm')
            TODO_API.add_task(content='Final Update', project_id=2290748296, section_id=88110232, parent_id=task.id, due_string='14 days from today at 9 pm')

def main():
    get_all_orgs()
    get_all_pt()

if __name__ == "__main__":
    main()