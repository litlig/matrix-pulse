from typing import Union
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import db
import matrix
import quotes

scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()
    repo = db.Repo("test.DB")
    mat = matrix.Matrix(repo, "http://192.168.1.117:7000/api/v3/customapp")
    poller = quotes.Poller("api_key", repo)
    scheduler.add_job(poller.run, IntervalTrigger(minutes=10))
    scheduler.add_job(mat.run, IntervalTrigger(minutes=10))
    app.state.repo = repo
    yield


app = FastAPI(lifespan=lifespan)


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/ticks")
def read_ticks():
    return app.state.repo.get_ticks()


@app.get("/matrix")
def read_matrix():
    return app.state.repo.get_matrix()


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
