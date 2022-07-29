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
project_id = os.getenv('project_id')
section_id = os.getenv('section_id')

Headers = {'Authorization': 'bearer ' + API_KEY}

org_tokens = []

def get_all_orgs():
    orgs = requests.get(API_URL + '/orgs?limit=1000', headers=Headers)
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
        pt_name = json_pentests["data"][0]['resource']['title']

        if(pt_start >= today_is):
            task = TODO_API.add_task(content=pt_name, project_id=project_id, section_id=section_id)
            dd1 = (datetime.datetime.strptime(start_date, "%b %d %Y") + datetime.timedelta(days=2)).date()
            TODO_API.add_task(content='Update 1', project_id=project_id, section_id=section_id, parent_id=task.id, due_string=f'{dd1} at 10 pm')
            dd2 = (datetime.datetime.strptime(start_date, "%b %d %Y") + datetime.timedelta(days=6)).date()
            TODO_API.add_task(content='Update 2', project_id=project_id, section_id=section_id, parent_id=task.id, due_string=f'{dd2} at 10 pm')
            dd3 = (datetime.datetime.strptime(start_date, "%b %d %Y") + datetime.timedelta(days=10)).date()
            TODO_API.add_task(content='Update 3', project_id=project_id, section_id=section_id, parent_id=task.id, due_string=f'{dd3} at 10 pm')
            dd4 = (datetime.datetime.strptime(start_date, "%b %d %Y") + datetime.timedelta(days=13)).date()
            TODO_API.add_task(content='Update 4', project_id=project_id, section_id=section_id, parent_id=task.id, due_string=f'{dd4} at 10 pm')
            dd5= (datetime.datetime.strptime(start_date, "%b %d %Y") + datetime.timedelta(days=14)).date()
            TODO_API.add_task(content='Final Update', project_id=project_id, section_id=section_id, parent_id=task.id, due_string=f'{dd5} at 11 pm')

def main():
    get_all_orgs()
    get_all_pt()

if __name__ == "__main__":
    main()