from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field

class RefinedOutput(BaseModel):
    answer: str = Field(..., description="Cleaned and improved final answer")

answer_refiner_agent = LlmAgent(
    name="answer_refiner_agent",
    model="gemini-2.0-flash",
    description="Refines the final answer to ensure accuracy and tone",
    instruction="""
You are an Answer Refinement Agent.

Review the current 'answer' and check if it reflects all task answers in detail.

Only improve clarity, completeness, and eliminate contradictions.

You must return:
{
  "answer": "...your refined version..."
}
""",
    output_schema=RefinedOutput,
    output_key="result"
)
