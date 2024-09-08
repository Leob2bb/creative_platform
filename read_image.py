# import cv2
import tensorflow as tf
import os
import numpy as np

from read_json import labels

# 이미지 폴더 경로
folder_path = "D:/image_sample1"

image_paths = []
# image_data_list = []

# 이미지 정보 불러오기 및 정렬
files = os.listdir(folder_path)

for file_name in files:
    if file_name.endswith('.jpg'):
        file_path = os.path.join(folder_path, file_name)
        image_paths.append(file_path)

# 이미지 처리 함수
def load_and_preprocess_image(path):

    image = tf.io.read_file(path)
    image = tf.image.decode_jpeg(image, channels=1)  # 흑백 이미지 # 일단 하라는 대로 해보자
    image = tf.image.resize(image, [500, 333])  # 크기 조절
    image /= 255.0  # 정규화
    return image

# 이미지 데이터셋 생성
path_ds = tf.data.Dataset.from_tensor_slices(image_paths)
image_ds = path_ds.map(load_and_preprocess_image, num_parallel_calls=tf.data.AUTOTUNE)

# label_ds = tf.data.Dataset.from_tensor_slices(labels)

# 이미지와 라벨 결합
image_label_ds = tf.data.Dataset.zip((image_ds, labels))

# DATASET_SIZE = len(image_paths)
# TRAIN_SIZE = int(0.8 * DATASET_SIZE)
# SHUFFLE_BUFFER_SIZE = 1000

# # 데이터셋 셔플
# shuffled_ds = image_label_ds.shuffle(SHUFFLE_BUFFER_SIZE)

# # 훈련 데이터셋
# train_ds = shuffled_ds.take(TRAIN_SIZE)

# # 테스트 데이터셋
# test_ds = shuffled_ds.skip(TRAIN_SIZE)

# # NumPy 배열로 변환
# train_images = np.array([image.numpy() for image, _ in train_ds])
# train_labels = np.array([label.numpy() for _, label in train_ds])
# test_images = np.array([image.numpy() for image, _ in test_ds])
# test_labels = np.array([label.numpy() for _, label in test_ds])

# # npz 파일로 저장
# np.savez_compressed('datasets.npz', 
#                     train_images=train_images, train_labels=train_labels,
#                     test_images=test_images, test_labels=test_labels)


