import os
import time
import json
import requests
import sys

API_URL = os.getenv("API_URL", "http://microcks:8080/api/jobs")
JOBS_FILE = os.getenv("JOBS_FILE", "jobs.json")

def load_jobs_from_file(path):
    with open(path, "r") as f:
        return json.load(f)

POST_PAYLOAD_TEMPLATE = {
    "metadata": {
        "labels": {}
    }
}

def activate(job_id):
    activate_url = f"{API_URL}/{job_id}/activate"
    activate_resp = requests.put(activate_url)
    if activate_resp.ok:
        print(f"Activated job '{job_id}' successfully.")
    else:
        print(f"Failed to activate job '{job_id}': {activate_resp.status_code}")

def start(job_id):
    activate_url = f"{API_URL}/{job_id}/start"
    activate_resp = requests.put(activate_url)
    if activate_resp.ok:
        print(f"Started job '{job_id}' successfully.")
    else:
        print(f"Failed to start job '{job_id}': {activate_resp.status_code}")

def post_and_activate_jobs(jobs):
    for job in jobs:
        payload = POST_PAYLOAD_TEMPLATE.copy()
        payload.update(job)
        payload["metadata"] = POST_PAYLOAD_TEMPLATE["metadata"]

        post_resp = requests.post(API_URL, json=payload)
        if post_resp.ok:
            job_id = post_resp.json().get("id")
            if job_id:
                activate(job_id)
                start(job_id)
            else:
                print(f"No ID returned for job '{job['name']}'")
        else:
            print(f"Failed to post job '{job['name']}': {post_resp.status_code}")
        

def main():
    try:
        resp = requests.get(API_URL, timeout=10)
        if resp.ok:
            jobs = resp.json()
            if jobs:
                print("Jobs already exist, doing nothing.")
            else:
                print(f"No jobs found, posting and activating jobs from file. '{JOBS_FILE}'")
                job_definitions = load_jobs_from_file(JOBS_FILE)
                post_and_activate_jobs(job_definitions)
        else:
            print(f"GET failed: {resp.status_code}")
    except:
        sys.exit("Microcks not available")



if __name__ == "__main__":
    main()
