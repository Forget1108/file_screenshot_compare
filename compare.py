from clean_text import clean_ocr_text, parse_file_info, format_file_list
from OCR import image_to_string
import os
import difflib

def string_similarity_ratio(str1, str2):
    """计算两个字符串的相似度比率 (0-1之间)"""
    return difflib.SequenceMatcher(None, str1, str2).ratio()
def compare_two_image(image1, image2):
    # 从图片中提取文字
    text1 = image_to_string(image1)
    text2 = image_to_string(image2)

    # 将文字简单处理
    clean_text1 = clean_ocr_text(text1)
    clean_text2 = clean_ocr_text(text2)

    # 格式化文字
    parse_text1 = parse_file_info(clean_text1)
    parse_text2 = parse_file_info(clean_text2)

    formatted_output1 = format_file_list(parse_text1)
    print(f"\n{'='*80}")
    print(f"将从图片中的提取的文字格式化展示: {os.path.basename(image1)}")
    print('='*80)
    print(formatted_output1)
    print("\n\n")

    formatted_output2 = format_file_list(parse_text2)
    print(f"\n{'='*80}")
    print(f"将从图片中的提取的文字格式化展示: {os.path.basename(image2)}")
    print('='*80)
    print(formatted_output2)
    print("\n\n")
    
    print("两个文件夹下的相同文件：")
    print("-" * 160)
    print(f"{'截图1文件':<50}{'截图2文件':<50}{'相似度信息'}")
    print("-" * 160)
    for i in parse_text1:
        for j in parse_text2:
            if i['date'] == j['date'] and i['size'] == j['size']:
                similarity = string_similarity_ratio(i['name'], j['name'])
                if similarity >= 0.8:
                    print(f"{i['name']:<50}{j['name']:<50}名称相似度：{similarity:.2f},修改日期：{i['date']},文件大小：{i['size']}")

if __name__ == '__main__':
    image1 = r'D:\file_compare_scan\picture\test1.jpg'
    image2 = r'D:\file_compare_scan\picture\test2.jpg'
    compare_two_image(image1, image2)