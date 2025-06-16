import requests
import json

SEARCH_ENDPOINT = "http://localhost:8085/search"

def call_microservice(query):
    try:
        resp = requests.post(SEARCH_ENDPOINT, json={"query": query})
        return resp.json().get("answer", "No answer found.")
    except Exception as e:
        return f"Search error: {e}"

def update_tasks(session_state_file):
    with open(session_state_file, "r") as f:
        session = json.load(f)

    tasks = session["result"]["tasks"]
    new_answer = []

    for task in tasks:
        result = call_microservice(task["description"])
        task["answer"] = result
        task["status"] = "completed"
        new_answer.append(result)

    session["result"]["tasks"] = tasks
    session["result"]["answer"] = " ".join(new_answer)

    with open("updated_state.json", "w") as f:
        json.dump(session, f, indent=2)

    print("✅ Answers injected. Saved to 'updated_state.json'.")

# Usage
update_tasks("planner_output.json")  # Replace with actual output file from planner agent
