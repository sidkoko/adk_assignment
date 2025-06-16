import requests
from google.adk.agents import FunctionAgent
from pydantic import BaseModel, Field
from typing import List

class Task(BaseModel):
    id: int
    description: str
    status: str
    answer: str

class SearchOutput(BaseModel):
    tasks: List[Task]
    answer: str

def search_logic(ctx):
    input_data = ctx.input["result"]
    tasks = input_data.get("tasks", [])
    final_answer = []

    for task in tasks:
        try:
            response = requests.post(
                "http://localhost:8085/search",  # Your microservice endpoint
                json={"query": task["description"]},
                timeout=10
            )
            task["answer"] = response.json().get("answer", "No answer found")
            task["status"] = "completed"
        except Exception as e:
            task["answer"] = f"Error: {str(e)}"
            task["status"] = "completed"
        final_answer.append(task["answer"])

    return {
        "tasks": tasks,
        "answer": " ".join(final_answer)
    }

search_agent = FunctionAgent(
    name="search_agent",
    description="Uses SerpAPI microservice to search and update task answers",
    python_function=search_logic,
    output_schema=SearchOutput,
    output_key="result"
)
