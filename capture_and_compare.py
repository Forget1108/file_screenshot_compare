from capture import capture_image
from compare import compare_two_image
import time

def main():
    print("截取第一个文件夹的目录图片")
    image1_path = capture_image()
    time.sleep(5)
    print("截取第二个文件夹的目录图片")
    image2_path = capture_image()
    print("开始对比两个文件夹")
    compare_two_image(image1_path, image2_path)

main()
