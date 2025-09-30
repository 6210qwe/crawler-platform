from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.api_v1.api import api_router
import logging
import json
import os

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="爬虫逆向学习平台 API",
    openapi_url="/openapi.json",
    docs_url="/swagger",
    redoc_url="/docs"
)

# 设置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含API路由
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "爬虫逆向学习平台 API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# 在启动时尝试预生成 OpenAPI，若失败会在控制台打印详细异常
@app.on_event("startup")
async def _generate_openapi_on_startup():
    try:
        schema = app.openapi()
        try:
            out_path = os.path.join(os.path.dirname(__file__), "..", "openapi.json")
            out_path = os.path.abspath(out_path)
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(schema, f, ensure_ascii=False, indent=2)
        except Exception as io_err:
            logging.getLogger("uvicorn.error").warning("Failed to write openapi.json: %s", io_err)
    except Exception as e:
        logging.getLogger("uvicorn.error").exception("OpenAPI generation failed: %s", e)

# 便于排查：直接返回内存中的 OpenAPI schema
@app.get("/schema.json")
async def get_schema():
    return app.openapi()

