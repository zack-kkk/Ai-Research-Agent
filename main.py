from fastapi import FastAPI
from pydantic import BaseModel
from agent import run_agent
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str


@app.post("/research")
def research(data: QueryRequest):
    return run_agent(data.query)