from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field
from typing import List


class Task(BaseModel):
    id: int = Field(..., description="Unique numeric task ID")
    description: str = Field(..., description="Actionable task instruction")
    status: str = Field(..., description="'pending' or 'completed'")
    answer: str = Field(..., description="Answer for this task")

class PlanningOutput(BaseModel):
    tasks: List[Task]
    answer: str = ""

planner_agent = LlmAgent(
    name="planner_agent",
    model="gemini-2.0-flash",
    description="Breaks down user query into actionable subtasks",
    instruction="""
You are a Planner Agent. Your job is to break a user's query into smaller subtasks.

Respond in the following format (JSON only, no backticks, no explanations):

{
  "tasks": [
    {
      "id": 1,
      "description": "...",
      "status": "pending",
      "answer": ""
    }
  ],
  "answer": ""
}
""",
    output_schema=PlanningOutput,
    output_key="result"
)
