from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .router import config, emotion   # ✅ 新增 emotion

def create_app():

    app = FastAPI(
        title="智能语音情感陪伴系统",
        version="1.0.0",
        description="语音情绪识别 + AI对话系统"
    )

    # =========================
    # CORS 配置
    # =========================
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],          # 开发环境
        allow_credentials=False,      # 避免 * + credentials 冲突
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # =========================
    # 路由注册
    # =========================

    # 原有配置模块
    app.include_router(config.router)

    # ✅ 情绪识别模块（新增）
    app.include_router(
        emotion.router,
        prefix="/emotion",
        tags=["情绪识别"]
    )

    # =========================
    # 健康检查
    # =========================
    @app.get("/health")
    def health():
        return {
            "status": "ok",
            "service": "emotion-ai-system"
        }

    return app