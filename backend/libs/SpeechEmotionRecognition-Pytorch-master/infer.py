import argparse
import functools
import os

from mser.predict import MSERPredictor
from mser.utils.utils import add_arguments, print_arguments

parser = argparse.ArgumentParser(description=__doc__)
add_arg = functools.partial(add_arguments, argparser=parser)

add_arg('configs', str, 'configs/bi_lstm.yml', '配置文件')

# 如果你本地已经训练好模型，这个设为 None
add_arg('use_ms_model', str, None, '是否使用ModelScope上的Emotion2Vec模型')

add_arg('use_gpu', bool, True, '是否使用GPU预测')

add_arg('audio_path', str, 'dataset/test.wav', '预测音频路径')

# ⚠ 必须是你四分类训练生成的模型路径
add_arg('model_path', str,
        'models/BiLSTM_Emotion2Vec/best_model/',
        '预测模型路径')

args = parser.parse_args()
print_arguments(args=args)

# 检查音频是否存在
if not os.path.exists(args.audio_path):
    raise FileNotFoundError(f"音频文件不存在: {args.audio_path}")

# 初始化预测器
predictor = MSERPredictor(
    configs=args.configs,
    use_ms_model=args.use_ms_model,
    model_path=args.model_path,
    use_gpu=args.use_gpu
)

# 开始预测
label, score = predictor.predict(audio_data=args.audio_path)

print(f"\n音频: {args.audio_path}")
print(f"预测情绪: {label}")
print(f"置信度: {score:.4f}")