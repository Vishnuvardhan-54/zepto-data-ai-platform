import os
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from app.ingestion import collection, embedding_model

# Define the data shared between all LangGraph nodes
class SupportState(TypedDict, total=False):
    query: str
    intent: str
    context: list[str]
    answer: str
    sources: list[str]
    confidence: float

# Check whether the required offline mock mode is enabled
def mock_llm_enabled() -> bool:
    return os.getenv("MOCK_LLM", "1") == "1"

# Classify the user query using the required keyword-based rule
def classify_intent(state: SupportState) -> SupportState:
    query = state["query"].lower()

    # Keywords that indicate a Zepto policy question
    policy_keywords = [
        "delivery",
        "return",
        "refund",
        "membership",
        "tracking",
        "cancel",
        "gift card",
        "support hours",
    ]

    if mock_llm_enabled():
        # In mock mode, classify using keywords without an LLM call
        intent = (
            "policy_question"
            if any(keyword in query for keyword in policy_keywords)
            else "general_question"
        )

    return {
        **state,
        "intent": intent,
    }

# Retrieve the most relevant policy documents and create the mock answer
def retrieve_and_answer(state: SupportState) -> SupportState:
    query = state["query"]
    # Convert the user query into an embedding
    query_embedding = embedding_model.encode([query],normalize_embeddings=True).tolist()[0]

    # Retrieve the top 3 most similar documents from ChromaDB
    results = collection.query( query_embeddings=[query_embedding],n_results=3,include=["documents"],)

    documents = results["documents"][0]
    source_ids = results["ids"][0]

    # Handle the case where no relevant document is found
    if not documents:
        return {
            **state,
            "context": [],
            "answer": "No relevant policy information was found.",
            "sources": [],
            "confidence": 0.0,
        }

    # Use the most similar document for the required mock response
    top_chunk = documents[0]
    top_snippet = top_chunk[:200]

    if mock_llm_enabled():
        answer = f"Based on the retrieved context: {top_snippet}"

    return {
        **state,
        "context": documents,
        "answer": answer,
        "sources": source_ids,
        "confidence": 1.0,
    }

# Return a fixed response for questions outside the Zepto policy corpus
def direct_answer(state: SupportState) -> SupportState:

    # In mock mode, do not make any LLM call
    if mock_llm_enabled():
        answer = "I can only answer questions about Zepto policies right now."

    return {
        **state,
        "answer": answer,
        "sources": [],
        "confidence": 1.0,
    }

# Decide which node should handle the query
def route_intent(state: SupportState) -> str:
    if state["intent"] == "policy_question":
        return "retrieve_and_answer"

    return "direct_answer"

# Create the LangGraph workflow
workflow = StateGraph(SupportState)

# Add the three required nodes
workflow.add_node("classify_intent", classify_intent)
workflow.add_node("retrieve_and_answer", retrieve_and_answer)
workflow.add_node("direct_answer", direct_answer)

# Start the workflow with intent classification
workflow.add_edge(START, "classify_intent")

# Route the query based on the detected intent
workflow.add_conditional_edges(
    "classify_intent",
    route_intent,
    {
        "retrieve_and_answer": "retrieve_and_answer",
        "direct_answer": "direct_answer",
    },
)

# End the workflow after generating the response
workflow.add_edge("retrieve_and_answer", END)
workflow.add_edge("direct_answer", END)

# Compile the graph so it can be executed
graph = workflow.compile()