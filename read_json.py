import json
import os

folder_path = "D:/JSON_sample1"

# 폴더 내 파일 목록 가져오기
# if os.path.isdir(folder_path):
files = os.listdir(folder_path)

labels = []

labels_dict = {'traffic_light':0, 'traffic_sign':1, 'traffic_information':2}

for file_name in files:
    # 파일 확장자가 .json인 파일만 처리
    if file_name.endswith('.json'):
        file_path = os.path.join(folder_path, file_name)

        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            # 클래스 값을 추출
            classes = [item['class'] for item in data['annotation']]
            # 클래스 이름에 따라 0~2의 숫자로 변환
            classes = [labels_dict[label] for label in classes]
            labels.append(classes)

# with open("JSON_sample_practice1.txt", 'w', encoding='utf-8') as f:
#     for data in json_data_list:
#         f.write(str(data))
#         f.write('\n')