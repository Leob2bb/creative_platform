import os
import xml.etree.ElementTree as ET
import tensorflow as tf

# Reference: ChatGPT

# PASCAL VOC XML 파일이 있는 폴더 경로
voc_xml_folder = 'D:/XML_sample1'

# 클래스 이름과 클래스 인덱스를 매핑 (PASCAL VOC 20개의 클래스)
class_mapping = {'traffic_light': 0, 'traffic_sign': 1, 'traffic_information': 2}

# XML 파일을 파싱하여 바운딩 박스 및 클래스 정보를 추출하는 함수
def parse_voc_xml(xml_file):
    # if not os.path.exists(xml_file):
    #     raise FileNotFoundError(f"File not found: {xml_file}")
    
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # 이미지 정보
    filename = root.find('filename').text
    size = root.find('size')
    width = int(size.find('width').text)
    height = int(size.find('height').text)

    # 객체 정보
    objects = []
    for obj in root.findall('object'):
        class_name = obj.find('name').text
        bbox = obj.find('bndbox')
        
        xmin = float(bbox.find('xmin').text) / width
        ymin = float(bbox.find('ymin').text) / height
        xmax = float(bbox.find('xmax').text) / width
        ymax = float(bbox.find('ymax').text) / height
        
        objects.append({
            'bbox': [ymin, xmin, ymax, xmax],  # VOC에서 tfds 포맷으로 변환
            'label': class_mapping[class_name]
        })

    return filename, width, height, objects

# 모든 XML 파일을 파싱하여 TensorFlow Dataset 형식으로 변환
def load_voc_dataset(voc_xml_folder):
    image_paths = []
    bboxes = []
    labels = []
    
    for file_name in os.listdir(voc_xml_folder):
        if file_name.endswith('.xml'):
            xml_path = os.path.join(voc_xml_folder, file_name)
            filename, width, height, objects = parse_voc_xml(xml_path)
            
            # 이미지 경로 저장
            image_path = os.path.join('D:/image_sample1', filename)  # 이미지 파일 경로 설정
            image_paths.append(image_path)
            
            # 바운딩 박스 및 레이블 정보 저장
            img_bboxes = [obj['bbox'] for obj in objects]
            img_labels = [obj['label'] for obj in objects]
            
            bboxes.append(img_bboxes)
            labels.append(img_labels)

    return image_paths, bboxes, labels

# 이미지와 어노테이션 정보를 tf.data.Dataset으로 변환
def create_tf_dataset(image_paths, bboxes, labels):
    def load_image_and_annotation(image_path, bbox, label):
        # 이미지 읽기
        image = tf.io.read_file(image_path)
        image = tf.image.decode_jpeg(image, channels=3)
        image = tf.image.resize(image, [500, 333])  # 크기 조정 (VOC 2007과 비슷하게)
        
        # tf.Tensor 형식으로 변환
        bbox = tf.convert_to_tensor(bbox, dtype=tf.float32)
        label = tf.convert_to_tensor(label, dtype=tf.int64)
        
        return {
            'image': image,
            'objects': {
                'bbox': bbox,
                'label': label
            }
        }

    dataset = tf.data.Dataset.from_tensor_slices((image_paths, bboxes, labels))
    dataset = dataset.map(lambda image_path, bbox, label: load_image_and_annotation(image_path, bbox, label))
    
    return dataset

# XML 파일에서 데이터 추출 및 tf.data.Dataset 생성
image_paths, bboxes, labels = load_voc_dataset(voc_xml_folder)
voc_dataset = create_tf_dataset(image_paths, bboxes, labels)

# 데이터 확인
for example in voc_dataset.take(1):
    print(example)


#     parse_voc_xml 함수:

# 주어진 XML 파일에서 이미지 파일 이름, 이미지 크기, 객체 정보(바운딩 박스와 클래스 레이블)를 파싱합니다.
# 바운딩 박스는 상대 좌표로 변환하여 [ymin, xmin, ymax, xmax] 순서로 반환됩니다.
# load_voc_dataset 함수:

# 폴더 내의 모든 XML 파일을 읽고, 이미지 경로와 바운딩 박스, 레이블을 추출합니다.
# 이미지 파일 경로는 별도로 지정된 이미지 폴더에 기반하여 설정됩니다.
# create_tf_dataset 함수:

# 추출한 이미지 경로, 바운딩 박스, 레이블 데이터를 tf.data.Dataset 형식으로 변환합니다.
# 이미지 파일을 읽고, 크기를 조정하며, 각 이미지에 대해 바운딩 박스와 레이블을 텐서 형식으로 변환합니다.