import asyncio
import signal
import websockets
import json
import numpy as np
import requests
from ..utils.device import get_mac_address, get_local_ip
from ..utils.logger import get_logger
from ..utils.audio import pcm_to_opus, decoder, AudioProcessor
from app.utils.emotion_service import emotion_service
import tempfile
import wave

logger = get_logger(__name__)


class WebSocketProxy:
    def __init__(
        self,
        device_id: str,
        client_id: str,
        websocket_url: str,
        ota_version_url: str,
        proxy_host: str | None,
        proxy_port: int | None,
        token_enable: bool,
        token: str,
    ):
        self.device_id= device_id
        self.client_id= client_id
        self.websocket_url= websocket_url
        self.ota_version_url= ota_version_url
        self.proxy_host= proxy_host
        self.proxy_port= proxy_port
        self.token_enable= token_enable
        self.token= token
        self.emotion_result = None  # 用于存储最新的情绪分析结果
        self.user_audio_buffer = bytearray()
        self.user_total_samples = 0

        self.audio_processor = AudioProcessor(960)
        self.decoder = decoder
        self.audio_buffer: bytearray = bytearray()  # 用于存储解码后的音频数据
        self.is_first_audio: bool = True  # 用于判断是否创建 Wave 头信息
        self.total_samples: int = 0  # 跟踪总采样数
        self.audio_lock = asyncio.Lock()  # 保证音频按顺序发送
        self.shutdown_event = asyncio.Event()  # 用于优雅退出

        self.headers = {
            "Device-Id": self.device_id,
            "Client-Id": self.client_id,
            "Protocol-Version": "1",
        }
        if self.token_enable and self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"

        self._update_ota_address()

    def _update_ota_address(self):
        MAC_ADDR = get_mac_address()

        headers = {"Device-Id": MAC_ADDR, "Content-Type": "application/json"}

        # 构建设备信息 payload
        payload = {
            "version": 2,
            "flash_size": 16777216,  # 闪存大小 (16MB)
            "psram_size": 0,
            "minimum_free_heap_size": 8318916,  # 最小可用堆内存
            "mac_address": MAC_ADDR,  # 设备 MAC 地址
            "uuid": self.client_id,
            "chip_model_name": "esp32s3",  # 芯片型号
            "chip_info": {"model": 9, "cores": 2, "revision": 2, "features": 18},
            "application": {
                "name": "xiaozhi",
                "version": "1.1.2",
                "idf_version": "v5.3.2-dirty",
            },
            "partition_table": [],  # 省略分区表信息
            "ota": {"label": "factory"},
            "board": {
                "type": "bread-compact-wifi",
                "ip": get_local_ip(),
                "mac": MAC_ADDR,
            },
        }

        try:
            # 发送请求到 OTA 服务器
            response = requests.post(
                self.ota_version_url,
                headers=headers,
                json=payload,
                timeout=10,  # 设置超时时间，防止请求卡死
                # proxies={"http": None, "https": None},  # 禁用代理
            )

            # 检查 HTTP 状态码
            if response.status_code != 200:
                logger.error(f"OTA 服务器错误: HTTP {response.status_code}")
                raise ValueError(f"OTA 服务器返回错误状态码: {response.status_code}")

            # 解析 JSON 数据
            response_data = response.json()

            # 确保 MQTT 信息存在
            if "mqtt" in response_data:
                logger.debug(f"MQTT 信息已更新:\n{json.dumps(response_data, indent=2, ensure_ascii=False)}")
                return response_data["mqtt"]
            else:
                logger.error(
                    f"OTA 服务器返回的数据无效: 没有 MQTT 信息: {response_data}"
                )
                raise ValueError(
                    "OTA 服务器返回的数据无效，请检查服务器状态或 MAC 地址"
                )

        except requests.Timeout:
            logger.error("OTA 请求超时")
            raise ValueError("OTA 请求超时，请稍后重试")

        except requests.RequestException as e:
            logger.error(f"OTA 请求失败: {e}")
            raise ValueError("无法连接到 OTA 服务器，请检查网络连接")

    def create_wav_header(self, total_samples):
        """
        创建 Wave 文件头, https://blog.csdn.net/shulianghan/article/details/117351966

        参数:
            total_samples (int): 音频数据的总采样数

        返回:
            bytearray: Wave 文件头的字节数组

        """
        header = bytearray(44)

        # ========== The "RIFF" chunk descriptor ==========
        header[0:4] = b"RIFF"
        header[4:8] = (total_samples * 2 + 36).to_bytes(4, "little")
        header[8:12] = b"WAVE"

        # ========== The "fmt" sub-chunk ==========
        header[12:16] = b"fmt "
        header[16:20] = (16).to_bytes(4, "little")
        header[20:22] = (1).to_bytes(2, "little")
        header[22:24] = (1).to_bytes(2, "little")
        header[24:28] = (16000).to_bytes(4, "little")
        header[28:32] = (32000).to_bytes(4, "little")
        header[32:34] = (2).to_bytes(2, "little")
        header[34:36] = (16).to_bytes(2, "little")

        # ========== The "data" sub-chunk ==========
        header[36:40] = b"data"
        header[40:44] = (total_samples * 2).to_bytes(4, "little")

        return header

    async def proxy_handler(self, websocket):
        """来自浏览器的 WebSocket 连接"""
        try:
            logger.info(
                f"正在创建新的客户端 websocket 连接: {websocket.remote_address}"
            )
            # 使用正确的参数名称 additional_headers (websockets 11.0+)
            async with websockets.connect(
                self.websocket_url, additional_headers=self.headers
            ) as server_ws:
                logger.info(f"已连接至 websocket 服务器，请求头: {self.headers}")
                await self._handle_proxy_communication(websocket, server_ws)

        except Exception as e:
            logger.error(f"代理失败: {e}")
        finally:
            logger.info("客户端连接关闭")

    async def _handle_proxy_communication(self, websocket, server_ws):
        """处理代理通信"""
        # 创建任务
        client_to_server = asyncio.create_task(
            self.handle_client_messages(websocket, server_ws)
        )
        server_to_client = asyncio.create_task(
            self.handle_server_messages(server_ws, websocket)
        )

        # 等待任意一个任务完成
        done, pending = await asyncio.wait(
            [client_to_server, server_to_client],
            return_when=asyncio.FIRST_COMPLETED,
        )

        # 取消其他任务
        for task in pending:
            task.cancel()

    async def handle_server_messages(self, server_ws, client_ws):
        logger.info("handle_server_messages 已启动")
        """处理来自 WebSocket 服务器的消息"""
        try:
            async for message in server_ws:
                logger.info(f"收到服务端消息: {type(message)}")
                # ---------- 文本消息 ----------
                if isinstance(message, str):
                    logger.info(f"服务端文本消息: {message}")
                    try:
                        msg_data = json.loads(message)

                        # ===============================
                        # 🎯 1️⃣ ASR 只在 stop 时处理
                        # ===============================
                        if (
                            msg_data.get("type") == "asr"
                            and msg_data.get("state") == "stop"
                        ):

                            user_text = msg_data.get("text", "")
                            logger.info(f"ASR完整文本: {user_text}")

                            # ============================
                            # 🎯 ① 如果累计音频足够，做情绪识别
                            # ============================

                            if self.user_total_samples > 16000 * 0.5:  # 至少0.5秒

                                try:
                                    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_wav:

                                        with wave.open(tmp_wav.name, "wb") as wf:
                                            wf.setnchannels(1)
                                            wf.setsampwidth(2)
                                            wf.setframerate(16000)
                                            wf.writeframes(self.user_audio_buffer)

                                        emotion_result = emotion_service.predict(tmp_wav.name)

                                        self.emotion_result = emotion_result

                                        logger.info(f"检测到情绪: {emotion_result}")

                                except Exception as e:
                                    logger.error(f"情绪识别失败: {e}")

                            # ============================
                            # ② 重置音频缓存
                            # ============================

                            self.user_audio_buffer = bytearray()
                            self.user_total_samples = 0

                            # ============================
                            # ③ 注入 prompt
                            # ============================

                            if self.emotion_result:

                                emotion = self.emotion_result.get("emotion")
                                confidence = self.emotion_result.get("confidence")

                                if confidence is not None and confidence >= 0.6:

                                    enhanced_text = (
                                        f"用户当前情绪为：{emotion}（置信度：{confidence:.2f}）。"
                                        f"请根据该情绪采用合适语气进行回应。\n\n"
                                        f"用户原话：{user_text}"
                                    )

                                    msg_data["text"] = enhanced_text

                                    logger.info("情绪已注入 ASR 文本")

                                self.emotion_result = None

                            message = json.dumps(msg_data, ensure_ascii=False)

                        # ===============================
                        # 🎧 2️⃣ TTS start
                        # ===============================
                        if (
                            msg_data.get("type") == "tts"
                            and msg_data.get("state") == "start"
                        ):
                            if len(self.audio_buffer) > 44:
                                async with self.audio_lock:
                                    chunk_size = (
                                        self.total_samples * 2 + 36
                                    ).to_bytes(4, "little")

                                    subchunk2_size = (
                                        self.total_samples * 2
                                    ).to_bytes(4, "little")

                                    self.audio_buffer[4:8] = chunk_size
                                    self.audio_buffer[40:44] = subchunk2_size

                                    await client_ws.send(bytes(self.audio_buffer))

                            self.audio_buffer = bytearray()
                            self.is_first_audio = True
                            self.total_samples = 0

                        # ===============================
                        # 🎧 3️⃣ TTS stop
                        # ===============================
                        elif (
                            msg_data.get("type") == "tts"
                            and msg_data.get("state") == "stop"
                        ):
                            if len(self.audio_buffer) > 44:
                                async with self.audio_lock:
                                    chunk_size = (
                                        self.total_samples * 2 + 36
                                    ).to_bytes(4, "little")

                                    subchunk2_size = (
                                        self.total_samples * 2
                                    ).to_bytes(4, "little")

                                    self.audio_buffer[4:8] = chunk_size
                                    self.audio_buffer[40:44] = subchunk2_size

                                    await client_ws.send(bytes(self.audio_buffer))

                            self.audio_buffer = bytearray()
                            self.is_first_audio = True
                            self.total_samples = 0

                        # ===============================
                        # 🔁 转发给客户端
                        # ===============================
                        await client_ws.send(message)

                    except json.JSONDecodeError:
                        await client_ws.send(message)

                # ---------- 二进制音频 ----------
                else:
                    async with self.audio_lock:
                        try:
                            pcm_data = self.decoder.decode(message, 960)

                            if pcm_data:

                                samples = len(pcm_data) // 2
                                self.total_samples += samples

                                if self.is_first_audio:
                                    self.audio_buffer.extend(
                                        self.create_wav_header(self.total_samples)
                                    )
                                    self.is_first_audio = False

                                self.audio_buffer.extend(pcm_data)

                                # 缓冲发送
                                if len(self.audio_buffer) >= 64044:

                                    chunk_size = (
                                        self.total_samples * 2 + 36
                                    ).to_bytes(4, "little")

                                    subchunk2_size = (
                                        self.total_samples * 2
                                    ).to_bytes(4, "little")

                                    self.audio_buffer[4:8] = chunk_size
                                    self.audio_buffer[40:44] = subchunk2_size

                                    await client_ws.send(bytes(self.audio_buffer))

                                    self.audio_buffer = bytearray()
                                    self.is_first_audio = True
                                    self.total_samples = 0

                        except Exception as e:
                            logger.error(f"音频处理错误: {e}")

        except Exception as e:
            logger.error(f"服务端消息处理异常: {e}")
        

    async def handle_client_messages(self, client_ws, server_ws):
        """处理来自客户端的消息"""
        try:
            async for message in client_ws:

                # =========================
                # 1️⃣ 文字消息
                # =========================
                if isinstance(message, str):
                    await server_ws.send(message)

                # =========================
                # 2️⃣ 音频消息
                # =========================
                else:
                    try:
                        audio_data = np.frombuffer(message, dtype=np.int16)

                        if len(audio_data) > 0:

                            chunks = self.audio_processor.process_audio(
                                audio_data.tobytes()
                            )

                            for chunk in chunks if chunks else []:

                        
                                opus_data = pcm_to_opus(chunk)
                                await server_ws.send(opus_data)

                                # ===== ② 累积音频（用于情绪识别）=====
                                self.user_audio_buffer.extend(chunk)
                                self.user_total_samples += len(chunk) // 2

                        else:
                            logger.warning("音频数据为空")

                    except Exception as e:
                        logger.error(f"音频处理错误: {e}")

        except Exception as e:
            logger.error(f"客户端信息处理异常: {e}")


    async def main(self):
        """启动代理服务器"""
        # 设置信号处理器
        def signal_handler():
            logger.info("收到退出信号，开始优雅关闭代理服务器...")
            self.shutdown_event.set()

        # 在 Windows 和 Unix 系统上设置信号处理
        if hasattr(signal, 'SIGTERM'):
            signal.signal(signal.SIGTERM, lambda s, f: signal_handler())
        if hasattr(signal, 'SIGINT'):
            signal.signal(signal.SIGINT, lambda s, f: signal_handler())

        try:
            logger.info(f"代理服务器启动在 {self.proxy_host}:{self.proxy_port}")
            async with websockets.serve(
                self.proxy_handler, self.proxy_host, self.proxy_port
            ) as server:
                # 等待关闭信号
                await self.shutdown_event.wait()
                logger.info("代理服务器正在关闭...")
                
        except asyncio.CancelledError:
            logger.info("代理服务器被取消，正在退出...")
        except Exception as e:
            logger.error(f"代理服务器异常: {e}")
        finally:
            logger.info("代理服务器已关闭")
