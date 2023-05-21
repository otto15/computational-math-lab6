from dto.request import ODUTo
from dto.response import ODUViewTo, ODUResultTo
from service import odu_service

from fastapi import FastAPI

import config
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = config.origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/odu")
async def get_all_odu() -> list[ODUViewTo]:
    return odu_service.get_all()


@app.post("/odu")
async def solve(odus: ODUTo) -> ODUResultTo:
    return odu_service.solve(odus)
