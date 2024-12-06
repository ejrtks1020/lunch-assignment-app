from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.session import engine
from model.base_model import Base
from configs.api_config import api_router
from contextlib import asynccontextmanager
from icecream import ic
from util.sqladmin_util import set_admin
from util.dummy_data_util import add_dummy_data
ic.configureOutput(includeContext=True)

async def init_models():
  async with engine.begin() as conn:
    # await conn.run_sync(Base.metadata.drop_all)
    await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("start")
    await init_models()
    await add_dummy_data()
    yield

app = FastAPI(title="Lunch", version="0.1.0", lifespan=lifespan)

set_admin(app=app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8070, reload=True)
