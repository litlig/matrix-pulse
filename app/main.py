from typing import Union
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import os
import db
import matrix
import quotes

scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()
    repo = db.Repo(os.getenv("DB_PATH", "test.db"))
    mat = matrix.Matrix(
        repo, os.getenv("MATRIX_ENDPOINT", "http://192.168.1.117:7000/api/v3/customapp")
    )
    poller = quotes.Poller(os.getenv("FINNHUB_API_KEY", ""), repo, mat)
    scheduler.add_job(poller.run, IntervalTrigger(minutes=1))
    scheduler.add_job(mat.run, IntervalTrigger(minutes=1))
    scheduler.start()
    app.state.repo = repo
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/ticks")
def read_ticks():
    return app.state.repo.get_ticks()


@app.put("/ticks/{tick}/{ath}")
def update_ticks(tick: str, ath: float):
    app.state.repo.upsert_tick(tick, ath)
    return {"ok": True}


@app.delete("/ticks/{tick}")
def delete_ticks(tick: str):
    app.state.repo.delete_tick(tick)
    return {"ok": True}


@app.get("/matrix")
def read_matrix():
    return app.state.repo.get_matrix()


@app.put("/matrix/{matrix_id}")
def add_matrix(matrix_id: int):
    app.state.repo.insert_matrix(str(matrix_id))
    return {"ok": True}


@app.delete("/matrixmatrix/{matrix_id}")
def delete_matrix(matrix_id: int):
    app.state.repo.delete_matrix(str(matrix_id))
    return {"ok": True}
