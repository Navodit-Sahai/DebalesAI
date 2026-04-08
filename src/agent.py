from typing import TypedDict, Optional
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END

from .llm import get_llm
from .rag import retrieve_context
from . import rag as _rag
from .tools import search_web
from .prompts import (
    ROUTER_PROMPT, RAG_PROMPT, SERP_PROMPT, MIXED_PROMPT, UNKNOWN_PROMPT
)


class AgentState(TypedDict):
    query: str
    route: Optional[str]
    rag_context: Optional[str]
    serp_results: Optional[str]
    answer: Optional[str]


llm = get_llm()


def route_node(state: AgentState) -> AgentState:
    prompt = ROUTER_PROMPT.format(query=state["query"])
    route = llm.invoke([HumanMessage(content=prompt)]).content.lower().strip()

    if route not in ("rag", "serp", "mixed", "unknown"):
        route = "rag" if "debales" in state["query"].lower() else "serp"

    print(f"[Route]: {route}")
    return {**state, "route": route}


def rag_node(state: AgentState) -> AgentState:
    return {
        **state,
        "rag_context": retrieve_context(state["query"], store=_rag.store)
    }


def serp_node(state: AgentState) -> AgentState:
    return {
        **state,
        "serp_results": search_web(state["query"])
    }


def mixed_node(state: AgentState) -> AgentState:
    return {
        **state,
        "rag_context": retrieve_context(state["query"], store=_rag.store),
        "serp_results": search_web(state["query"])
    }


PROMPT_MAP = {
    "rag": lambda s: RAG_PROMPT.format(context=s["rag_context"], query=s["query"]),
    "serp": lambda s: SERP_PROMPT.format(results=s["serp_results"], query=s["query"]),
    "mixed": lambda s: MIXED_PROMPT.format(
        rag_context=s["rag_context"],
        serp_results=s["serp_results"],
        query=s["query"],
    ),
    "unknown": lambda s: UNKNOWN_PROMPT.format(query=s["query"]),
}


def answer_node(state: AgentState) -> AgentState:
    prompt = PROMPT_MAP.get(state["route"], PROMPT_MAP["unknown"])(state)
    answer = llm.invoke([HumanMessage(content=prompt)]).content.strip()
    return {**state, "answer": answer}


def dispatch(state: AgentState) -> str:
    return {
        "rag": "rag_node",
        "serp": "serp_node",
        "mixed": "mixed_node"
    }.get(state["route"], "answer_node")


def _build_graph() -> StateGraph:
    g = StateGraph(AgentState)

    nodes = {
        "route_node": route_node,
        "rag_node": rag_node,
        "serp_node": serp_node,
        "mixed_node": mixed_node,
        "answer_node": answer_node,
    }

    for name, fn in nodes.items():
        g.add_node(name, fn)

    g.set_entry_point("route_node")
    g.add_conditional_edges("route_node", dispatch)

    for node in ("rag_node", "serp_node", "mixed_node"):
        g.add_edge(node, "answer_node")

    g.add_edge("answer_node", END)

    return g.compile()


_graph = _build_graph()


def run_agent(query: str, history=None) -> str:
    result = _graph.invoke({
        "query": query,
        "route": None,
        "rag_context": None,
        "serp_results": None,
        "answer": None
    })
    return result["answer"]