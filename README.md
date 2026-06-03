# Stellamiss_ai

> 本项目供学习交流使用，如果有问题欢迎联系3545890534@qq.com

## 项目简介

一个基于 AI 的智能语音陪伴系统，通过识别和理解用户情感，提供自然、贴心的语音交互与陪伴。

## 功能特点

- [X] 文字聊天：像微信好友一样聊天
- [X] 语音聊天：和DeepSeek进行语音对话，支持打断
- [X] 自动配置：自动获取 MAC 地址、更新 OTA 版本，避免繁杂的配置流程
- [X] 移动适配：支持移动端配置服务器地址

## 系统要求

- Python 3.9+
- NodeJS 18+
-  npm
- uv (Python 包管理器)
- 支持的操作系统：Windows 10+

## 快速开始

### 一键启动（推荐）

1. 安装前端依赖

```bash
 cd "D:\AI\Stellamiss_ai"
pnpm install
```

    2. 安装后端依赖

```bash
cd backend
uv sync
cd ..
```

> **注意**：如果遇到 WebSocket 连接问题，请确保使用兼容的 `websockets` 库版本。项目使用 `websockets>=15.0.1`。

4. 同时启动前后端

```bash
npm run dev
```

这将使用 `concurrently` 同时启动前端和后端服务，在终端中会看到带颜色区分的前后端日志输出。

> **Windows 用户注意**：如果在控制台看到中文乱码，项目已自动配置 UTF-8 编码。如果仍有问题，请确保：
>
> 1. 使用 PowerShell 或 Windows Terminal（推荐）
> 2. 在 CMD 中手动执行 `chcp 65001` 切换到 UTF-8 编码
> 3. 或使用 VS Code 内置终端

> **停止服务**：使用 `Ctrl+C` 可以优雅地停止前后端服务，系统会自动清理所有进程和连接。

### 浏览页面

在浏览器中访问 `http://localhost:5173` 即可使用

## 项目结构-

d:\AI\Stellamiss_ai
├── .git/                        # Git 版本控制目录
├── .gitignore                   # Git 忽略规则
├── env.d.ts                     # TypeScript 环境类型声明
├── index.html                   # 前端入口 HTML
├── package.json                 # 前端依赖与脚本配置
├── package-lock.json            # npm 锁定版本
├── pnpm-lock.yaml               # pnpm 锁定版本
├── PROJECT_STRUCTURE_DETAILED.md# 项目结构说明文档
├── README.md                    # 项目整体说明
├── tsconfig.app.json            # 前端应用 TypeScript 配置
├── tsconfig.json                # TypeScript 根配置
├── tsconfig.node.json           # Node 环境 TypeScript 配置
├── vite.config.ts               # Vite 构建配置
├── dist/                        # 构建产物输出目录
├── image/                       # 项目使用的图片资源
├── node_modules/                # 前端依赖包
├── public/                      # 静态资源目录
├── backend/                     # 后端代码与模型资源
│   ├── .python-version          # Python 版本配置
│   ├── .venv/                   # Python 虚拟环境
│   ├── main.py                  # 后端服务启动入口
│   ├── pyproject.toml           # Python 项目依赖与配置
│   ├── uv.lock                  # uv dependency lock
│   ├── app/                     # 后端应用源码
│   │   ├── __init__.py
│   │   ├── config.py            # 后端配置逻辑
│   │   ├── constant/            # 常量定义
│   │   │   ├── __init__.py
│   │   │   ├── file.py          # 文件相关常量
│   │   │   └── repsonse.py      # 响应相关常量
│   │   ├── proxy/               # 代理模块
│   │   │   ├── __init__.py
│   │   │   ├── process_handler.py  # 进程代理处理
│   │   │   └── websocket_proxy.py  # WebSocket 代理
│   │   ├── router/              # 路由模块
│   │   │   ├── __init__.py
│   │   │   ├── config.py        # 路由配置
│   │   │   └── emotion.py       # 情感识别接口
│   │   └── utils/               # 工具函数
│   │       ├── __init__.py
│   │       ├── audio.py         # 音频处理工具
│   │       ├── device.py        # 设备信息与控制
│   │       ├── emotion_service.py # 情感服务逻辑
│   │       ├── logger.py        # 日志工具
│   │       └── system_info.py   # 系统信息获取
│   ├── config/                  # 后端配置文件
│   │   └── config.json
│   ├── libs/                    # 依赖库与模型资源
│   │   ├── linux/               # Linux 平台相关资源
│   │   ├── windows/             # Windows 平台相关资源
│   │   └── SpeechEmotionRecognition-Pytorch-master/  # 情感识别模型仓库
│   │       ├── create_data.py
│   │       ├── eval.py
│   │       ├── extract_features.py
│   │       ├── infer.py
│   │       ├── LICENSE
│   │       ├── README.md
│   │       ├── requirements.txt
│   │       ├── setup.py
│   │       ├── train.py
│   │       ├── configs/         # 模型配置
│   │       ├── dataset/         # 数据集与特征文件
│   │       ├── docs/            # 文档与图片
│   │       ├── log/             # 训练日志
│   │       ├── models/          # 模型权重与输出
│   │       ├── mser/            # 自定义情感识别库
│   │       └── output/          # 运行结果输出
│   └── logs/                    # 后端运行日志
└── src/                         # 前端 Vue 应用
    ├── App.vue                  # 根组件
    ├── main.ts                  # 前端入口脚本
    ├── assets/                  # 样式与静态前端资源
    │   ├── base.css
    │   └── main.css
    ├── components/              # Vue 组件
    │   ├── ChatContainer.vue     # 聊天容器组件
    │   ├── InputField.vue        # 输入框组件
    │   ├── Header/               # 头部相关组件
    │   │   ├── ConnectionStatus.vue
    │   │   ├── index.vue
    │   │   └── Title.vue
    │   ├── Setting/              # 设置面板组件
    │   │   ├── index.vue
    │   │   └── SettingButton.vue
    │   └── services/             # 组件内服务目录（可能命名异常）
    ├── services/                # 前端业务逻辑服务
    │   ├── AudioManager.ts
    │   ├── ChatStateManager.ts
    │   ├── VoiceAnimationManager.ts
    │   └── WebSocketManager.ts
    ├── stores/                  # Pinia / 状态管理
    │   └── setting.ts
    └── types/                   # TypeScript 类型定义
        ├── chat.ts
        ├── message.ts
        └── websocket.ts

## 技术栈

**前端**

- 框架： Vue3 + TypeScript + Pinia
- 构建工具：Vite
- 包管理器：pnpm
- UI 组件：Element Plus
- Web API: WebSocket、Web Audio API、AudioWorklet

**后端**

- Python 3.12+ + FastAPI
- 包管理器：uv
- 协议：WebSocket

**开发工具**TypeScript：类型安全

- Less：CSS 预处理器

## 故障排除

### 常见问题

**1. WebSocket 连接错误**
如果看到类似 `BaseEventLoop.create_connection() got an unexpected keyword argument 'extra_headers'` 的错误：

- 确保使用正确版本的 `websockets` 库（建议 >=15.0.1）
- 运行 `cd backend && uv sync` 重新安装依赖

**2. 中文字符显示乱码**

- 使用 PowerShell 或 Windows Terminal
- 在 CMD 中执行 `chcp 65001` 切换编码
- 使用 VS Code 内置终端

**3. 端口占用问题**

- 前端默认端口：5173
- 后端默认端口：5000
- 如有冲突，请在配置文件中修改端口设置
