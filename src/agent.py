from langchain_core.messages import HumanMessage
from .llm import get_llm
from .rag import retrieve_context,store
from .tools import search_web
from .prompts import *

def route_query(query):
    llm = get_llm()
    prompt = ROUTER_PROMPT.format(query=query)
    route = llm.invoke([HumanMessage(content=prompt)]).content.lower().strip()

    if route not in ["rag", "serp", "mixed", "unknown"]:
        return "rag" if "debales" in query.lower() else "serp"

    return route


def run_agent(query, history=None):
    llm = get_llm()

    route = route_query(query)
    print(f"[Route]: {route}")

    rag_context = ""
    serp_results = ""

    if route in ["rag", "mixed"]:
        rag_context = retrieve_context(query,store=store)

    if route in ["serp", "mixed"]:
        serp_results = search_web(query)

    if route == "rag":
        prompt = RAG_PROMPT.format(context=rag_context, query=query)

    elif route == "serp":
        prompt = SERP_PROMPT.format(results=serp_results, query=query)

    elif route == "mixed":
        prompt = MIXED_PROMPT.format(
            rag_context=rag_context,
            serp_results=serp_results,
            query=query
        )
    else:
        prompt = UNKNOWN_PROMPT.format(query=query)

    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip()