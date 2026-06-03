import os
from mser.trainer import MSERTrainer


def create_casia_4class_list(audio_dir, list_path):
    """
    目录结构:
    audio/
        └── speaker/
              └── emotion/
                    └── *.wav

    四分类映射:
    0 -> neutral
    1 -> happy
    2 -> sad
    3 -> angry
    """

    emotion_map = {
        "neutral": 0,
        "happy": 1,
        "sad": 2,
        "angry": 3
    }

    label_names = ["中性", "快乐", "悲伤", "愤怒"]

    # 写标签文件
    with open(os.path.join(list_path, 'label_list.txt'), 'w', encoding='utf-8') as f:
        for name in label_names:
            f.write(name + "\n")

    data_dict = {0: [], 1: [], 2: [], 3: []}

    # 遍历 speaker 文件夹
    for speaker in os.listdir(audio_dir):
        speaker_path = os.path.join(audio_dir, speaker)

        if not os.path.isdir(speaker_path):
            continue

        # 遍历情绪文件夹
        for emotion in os.listdir(speaker_path):
            if emotion not in emotion_map:
                continue

            emotion_path = os.path.join(speaker_path, emotion)

            for file in os.listdir(emotion_path):
                if file.endswith('.wav'):
                    full_path = os.path.join(emotion_path, file).replace('\\', '/')
                    label_id = emotion_map[emotion]
                    data_dict[label_id].append(full_path)

    # 生成 train/test
    train_file = os.path.join(list_path, 'train_list.txt')
    test_file = os.path.join(list_path, 'test_list.txt')

    with open(train_file, 'w', encoding='utf-8') as f_train, \
         open(test_file, 'w', encoding='utf-8') as f_test:

        for label_id in data_dict:
            files = data_dict[label_id]

            for i, file_path in enumerate(files):
                if i % 10 == 0:
                    f_test.write(f"{file_path}\t{label_id}\n")
                else:
                    f_train.write(f"{file_path}\t{label_id}\n")

    print("✅ CASIA 四分类数据列表生成完成！")


def create_standard(config_file):
    trainer = MSERTrainer(configs=config_file)
    trainer.get_standard_file()


if __name__ == '__main__':
    create_casia_4class_list('dataset/audio', 'dataset')
    create_standard('configs/bi_lstm.yml')