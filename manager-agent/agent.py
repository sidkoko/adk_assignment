from google.adk.agents import SequentialAgent, LoopAgent
from .subagents.planner_agent import planner_agent
from .subagents.search_agent import search_agent
from .subagents.answer_refiner_agent import answer_refiner_agent

refinement_loop = LoopAgent(
    name="AnswerRefinementLoop",
    max_iterations=3,
    sub_agents=[answer_refiner_agent],
    description="Refines the answer iteratively until no further changes are needed."
)

root_agent = SequentialAgent(
    name="manager_agent",
    sub_agents=[
        planner_agent,
        search_agent,
        refinement_loop
    ],
    description="Orchestrates planning, search, and iterative answer refinement"
)
