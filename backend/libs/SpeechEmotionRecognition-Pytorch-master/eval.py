import argparse
import functools
import time
import os

from mser.trainer import MSERTrainer
from mser.utils.utils import add_arguments, print_arguments

parser = argparse.ArgumentParser(description=__doc__)
add_arg = functools.partial(add_arguments, argparser=parser)

add_arg('configs', str, 'configs/bi_lstm.yml', "配置文件")
add_arg("use_gpu", bool, True, "是否使用GPU评估模型")

# 混淆矩阵保存路径
add_arg('save_matrix_path', str, 'output/images/', "保存混淆矩阵路径")

# ⚠ 改成你实际训练后的模型目录
add_arg('resume_model', str,
        'models/BiLSTM_Emotion2Vec/best_model/',
        "模型路径")

add_arg('overwrites', str, None,
        '覆盖配置文件参数，例如"train_conf.max_epoch=100"')

args = parser.parse_args()
print_arguments(args=args)

# 如果目录不存在自动创建
if not os.path.exists(args.save_matrix_path):
    os.makedirs(args.save_matrix_path)

# 初始化训练器
trainer = MSERTrainer(
    configs=args.configs,
    use_gpu=args.use_gpu,
    overwrites=args.overwrites
)

# 开始评估
start = time.time()

loss, accuracy = trainer.evaluate(
    resume_model=args.resume_model,
    save_matrix_path=args.save_matrix_path
)

end = time.time()

print('评估耗时：{}s | loss：{:.5f} | accuracy：{:.5f}'
      .format(int(end - start), loss, accuracy))