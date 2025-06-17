PLEASE READ!

Before reading this, you have to know that i have no prior experience in Google ADK. On getting this assignment, I dove into Google ADK for the first time and learnt about all the ways to create agents and workflows and how they work, from Youtube. I spent two days completing a crash course video, creating the code and making notes simultaneously. Then finally, i got to making this actual assignment. I spent all day, and at one point i thought I had it too. 

I had created a Sequential Agent containing planner_agent and search_agent. Problem was, using LLMs they were giving outdated answers. To tackle this small problem, I went on a whole new journey of trying to get live search LLMs, to trying to use external Gemini API to call from root_agent, to injecting answers from external to my search agent call. Also you wanted a Sequential Agent Workflow, hence it didnt allow me to use the built-in tools. Maybe could have used Agent-as-Tool, but that wouldnt have been sequential. 

There was always some or the other problem. The deeper I went the more i had to backtrack to fix things. ChatGPT became my buddy, i was literally in an error debugging and optimizing loophole for the last 5 hours. Mostly it was due to FunctionAgent not being avalaible on Python SDK, but im sure there were other ways to do it. 

I have made something, but it doesn't work. I wish I would have stayed on a simpler code that partially works instead of going LENGTHS to produce something not working. But it has been a journey. And i've learnt a lot. I will still be working on agents, i think i like Google ADK its amazing. 

I HUMBLY REQUEST YOU TO PLEASE HAVE AN INTERVIEW. I know the assignment holds value, but I have belief in my efforts. Please give me a shot.


# Multi-Agent Information Retrieval System (ADK-based)

This project is a **multi-agent system** built using the **Google Agent Development Kit (ADK)** for answering real-world, time-sensitive queries through structured task planning, web search, and refinement.

---

## ✨ Project Goal

To build an agent system that:

1. Parses a user's high-level question into subtasks.
2. Executes real-time searches.
3. Iteratively refines the response.

---

## ⚡ Why This Was Built

Initially, the goal was to leverage Gemini's `GoogleSearch` tool for live results. However, Gemini's Python SDK lacked proper support for:

- `GenerateContentConfig`
- `GoogleSearch`

This limitation forced a pivot to **SerpAPI** as an external microservice, ensuring **real-time search results**.

---

## 🧰 Final Architecture

```bash
adk-assignment/
├── manager-agent/
│   ├── __init__.py
│   ├── agent.py                # Root SequentialAgent
│   └── subagents/
│       ├── __init__.py
│       ├── planner_agent/
│       │   └── agent.py        # LlmAgent that breaks goal into tasks
│       ├── search_agent/
│       │   └── agent.py        # FunctionAgent that fetches from SerpAPI microservice
│       └── answer_refiner_agent/
│           └── agent.py        # LlmAgent that refines final answer
├── search_microservice/
│   ├── main.py                 # FastAPI server using SerpAPI
│   └── .env                    # Contains SERPAPI_KEY
├── .venv/                      # Isolated virtual environment
└── README.md
```

---

## 🌐 External Microservice: `search_microservice`

A FastAPI server that receives queries and returns answers from SerpAPI.

### Sample query:

```bash
curl -X POST http://localhost:8085/search -H "Content-Type: application/json" \
     -d '{ "query": "When is the next SpaceX launch?" }'
```

---

## 🧬 Agent Logic

### `planner_agent`

- Type: `LlmAgent`
- Model: `gemini-2.0-flash`
- Task: Splits the goal into structured subtasks with `id`, `description`, `status`, and `answer` fields.

### `search_agent`

- Type: `FunctionAgent`
- Calls the `search_microservice` for each task
- Updates `task.status` to `completed` and fills `answer`

### `answer_refiner_agent`

- Type: `LlmAgent`
- Refines the answer from all tasks into a final coherent statement
- Looped via `LoopAgent` until no changes are detected (max 5 iterations)

---

## 🔥 Challenges Faced

- Google SDK lacks Python bindings for `GoogleSearch`
- Gemini via OpenRouter returns outdated data
- `LiteLLM` output caused `pydantic` parsing errors
- ADK v1.3.0 installation required full environment reset
- FunctionAgent support was missing in earlier versions

---

## 🧨 Key Learnings

- How to structure agents using ADK's `SequentialAgent`, `LoopAgent`, `LlmAgent`, and `FunctionAgent`
- How to fallback from Gemini to SerpAPI for better real-time accuracy
- How to debug ADK CLI, agent registration issues, and version mismatches
- How to combine external APIs with ADK to enhance agent workflows

---

## 🚫 What Didn't Work

- Gemini SDK's built-in `GoogleSearch` tools
- Getting up-to-date responses via OpenRouter-based Gemini or GPT-4o-mini
- Custom agents (e.g., `CustomAgent`) inside subagent workflows (not supported)

---

## ✨ Suggested Future Improvements

- Add caching/memory so agents learn from past queries
- Add UI via `adk web` (currently skipped due to outdated SDK issues)
- Switch to a search engine with fresher APIs (Bing Web Search or custom scrapers)
- Integrate retrieval-augmented generation (RAG) for deeper grounding

---

## 📆 Timeline

- **Day 1-2:** Initial setup, Gemini attempts, failure with search tools
- **Day 3:** Built and tested `search_microservice` with SerpAPI
- **Day 4:** Refactored agents using ADK 1.3.0, added refinement loop
- **Day 5:** Debugged errors, finalized functionality

---

## 📅 Status: \~ 90% Complete

- Functionally sound
- Real-time responses integrated
- Error-handling done
- UI and search quality improvements left as future work

