import argparse
import functools

from mser.trainer import MSERTrainer
from mser.utils.utils import add_arguments, print_arguments

parser = argparse.ArgumentParser(description=__doc__)
add_arg = functools.partial(add_arguments, argparser=parser)

add_arg('configs', str, 'configs/bi_lstm.yml', '配置文件')

# 保存特征路径（建议固定）
add_arg('save_dir', str, 'dataset/features', '特征保存路径')

# ⚠ CASIA 不建议 100 秒，这里改为合理值
add_arg('max_duration', int, 5, '最大音频长度（秒）')

args = parser.parse_args()
print_arguments(args=args)

# 初始化训练器
trainer = MSERTrainer(configs=args.configs)

# ==========================
# 1️⃣ 提取特征
# ==========================
trainer.extract_features(
    save_dir=args.save_dir,
    max_duration=args.max_duration
)

# ==========================
# 2️⃣ 生成标准化文件
# ==========================
trainer.get_standard_file(max_duration=args.max_duration)