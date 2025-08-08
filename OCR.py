import cv2
import os
import pytesseract

def image_to_string(image_path):
    print(f"提取图片中的文字: {os.path.basename(image_path)}")

    Tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    pytesseract.pytesseract.tesseract_cmd = Tesseract_path

    # 读取图片
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 图像预处理优化
    # 调整大小
    image_big = cv2.resize(gray_image, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    
    # 二值化而不是高斯模糊
    _, binary_image = cv2.threshold(image_big, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # 使用指定的PSM模式
    custom_config = f'--psm 4 --oem 3'
    text = pytesseract.image_to_string(binary_image, lang='chi_sim', config=custom_config)

    # print(f"图片{image_path}识别出文字内容:")
    # print(text)
    return text

def get_picture(dir):
    directory = dir
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files

if __name__ == '__main__':
    image_path = r'D:\file_compare_scan\picture\image.png'
    dir = r'D:\file_compare_scan\picture'
    
    image_to_string(image_path)
    # pictures = get_picture(dir)
    # for picture in pictures:
    #     image_to_string(picture)
    #     print("\n\n\n")