from fastapi import FastAPI
from dotenv import load_dotenv
from pydantic import BaseModel
from datetime import datetime

from services.orchestrator_service import OrchestratorService

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()


# Define a Pydantic model for the request body
class TranscriptionRequest(BaseModel):
    transcription: str

@app.post("/orchestrator")
async def orchestrator(request: TranscriptionRequest):
    """
    OpenAI Response Orchestrator Endpoint
    """
    try:
        if not request.transcription or request.transcription == "":
            raise Exception("Transcription is empty")

        orchestrator = OrchestratorService(request.transcription)

        start = datetime.now()
        query = orchestrator.query_extractor_bot()
        relevant_docs = orchestrator.get_relavent_docs(query)
        response = orchestrator.response_generator_bot(query, relevant_docs)
        end = datetime.now()

        return {"message": response, "time_taken": str(end - start)}
    except Exception as e:
        return {"message": f"Error in orchestrating a response: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)