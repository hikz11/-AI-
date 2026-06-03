from mser.predict import MSERPredictor
import os


class EmotionService:

    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        
        project_dir = os.path.join(
            base_dir,
            "libs",
            "SpeechEmotionRecognition-Pytorch-master"
        )
        project_dir = os.path.abspath(project_dir)

        # ⭐ 关键：切换工作目录
        os.chdir(project_dir)

        self.model = MSERPredictor(
            configs=os.path.join(project_dir, "configs/bi_lstm.yml"),
            model_path=os.path.join(project_dir, "models/BiLSTM_Emotion2Vec/best_model/"),
            use_gpu=False
        )

    def predict(self, audio_path: str):
        label, score = self.model.predict(audio_data=audio_path)
        return {
            "emotion": label,
            "confidence": float(score)
        }


emotion_service = EmotionService()