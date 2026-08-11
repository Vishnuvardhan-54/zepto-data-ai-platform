from fastapi import FastAPI

from app.graph import graph
from app.models import AskRequest, AskResponse


# Create the FastAPI application
app = FastAPI(
    title="Zepto Support Assistant",
    description="Policy-based customer support assistant",
    version="1.0.0",
)

# Handle customer questions through the /ask endpoint
@app.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    # Send the user's query through the LangGraph workflow
    result = graph.invoke({"query": request.query})

    # Return only the fields required by the response schema
    return AskResponse(
        answer=result["answer"],
        sources=result.get("sources", []),
        confidence=result.get("confidence", 0.0),
    )