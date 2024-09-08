import json
import xml.etree.ElementTree as ET
import os

# Reference: ChatGPT

# XML 생성 함수
def create_voc_xml(json_data, json_name):
    annotation = ET.Element("annotation")
    
    # 이미지 정보
    filename = ET.SubElement(annotation, "filename")
    filename.text = json_data['image']['filename']
    
    size = ET.SubElement(annotation, "size")
    width = ET.SubElement(size, "width")
    height = ET.SubElement(size, "height")
    depth = ET.SubElement(size, "depth")
    
    width.text = str(json_data['image']['imsize'][0])
    height.text = str(json_data['image']['imsize'][1])
    depth.text = "3"  # Assume RGB image
    
    # 객체 정보 추가
    for obj in json_data['annotation']:
        obj_element = ET.SubElement(annotation, "object")
        
        # class 정보
        name = ET.SubElement(obj_element, "name")
        name.text = obj['class']

        # 위 json에는 추가로 shape, **color, kind, text, type 등의 정보가 있음. (이후 신호등 색깔 판정하는 데 확인)
        # 바운딩 박스 정보
        bndbox = ET.SubElement(obj_element, "bndbox")
        xmin = ET.SubElement(bndbox, "xmin")
        ymin = ET.SubElement(bndbox, "ymin")
        xmax = ET.SubElement(bndbox, "xmax")
        ymax = ET.SubElement(bndbox, "ymax")
        
        # 바운딩 박스 좌표
        xmin.text = str(obj['box'][0])
        ymin.text = str(obj['box'][1])
        xmax.text = str(obj['box'][2])
        ymax.text = str(obj['box'][3])
    
    # XML 문자열로 변환
    tree = ET.ElementTree(annotation)
    # xml 파일 이름을 jpg, json 파일 이름과 동일하게 작성.
    xml_name = filename.text.replace(".jpg", ".xml")
    print(xml_name)
    tree.write("D:/XML_sample1/" + xml_name)

# JSON 파일 읽기

folder_path = "D:/JSON_sample1"

files = os.listdir(folder_path)

for file_name in files:
    # 파일 확장자가 .json인 파일만 처리
    if file_name.endswith('.json'):
        file_path = os.path.join(folder_path, file_name)

        with open(file_path, 'r', encoding='utf-8') as json_file:
            json_data = json.loads(json_file.read())
            # XML 생성
            create_voc_xml(json_data, file_name)
