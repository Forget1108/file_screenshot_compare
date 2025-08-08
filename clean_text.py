import re
import os
from OCR import get_picture, image_to_string

def clean_ocr_text(text):
    """
    清理OCR识别出的文本，去除无效字符并统一格式
    """
    # 按行分割文本
    lines = text.split('\n')
    cleaned_lines = []
    
    # 定义需要过滤的无效字符和符号
    invalid_chars = r'[^\w\s./:\\\-_年月日时分秒KB\d\u4e00-\u9fff]'
    
    for line in lines:
        # 去除首尾空白字符
        line = line.strip()
        
        # 跳过空行
        if not line:
            continue
            
        # 去除常见的无效符号
        line = re.sub(invalid_chars, '', line)
        
        # 标准化空格（将多个空格替换为单个空格）
        line = re.sub(r'\s+', ' ', line)
        
        # 修复常见的OCR识别错误
        line = line.replace('口', '')  
        line = line.replace('国', '')  
        line = line.replace('人', '')  
        line = line.replace('I〕', '') 
        line = line.replace('弘', '')  
        line = line.replace('图', '')  
        line = line.replace('岩', '')  
        line = line.replace('奂', '')  
        line = line.replace('蜀', '')  
        line = line.replace('盈', '')  
        line = line.replace('盟', '')  
        line = line.replace('司', '')  
        line = line.replace('吾', '')  
        line = line.replace('咏', '')  
        line = line.replace('公', '')  
        line = line.replace('一', '')  
        line = line.replace('切', '')  
        line = line.replace('小', '')  
        line = line.replace('湘', '')  
        line = line.replace('澳', '')  
        line = line.replace('濑', '')  
        line = line.replace('濡', '')  
        line = line.replace('渡', '')  
        line = line.replace('震', '')  
        line = line.replace('前', '')  
        line = line.replace('温', '')  
        line = line.replace('园', '')
        line = line.replace('闯', '')
        line = line.replace('门', '')
        line = line.replace('嚎', '')
        line = line.replace('十', '')
        line = line.replace('固', '')
        line = line.replace('牛', '')
        line = line.replace('生', '')
        line = line.replace('文 件 夷', '文 件 夹')
        
        # 修复文件扩展名
        line = re.sub(r'(?<!\.)dll(?=\s|$)', '.dll', line)
        line = re.sub(r'(?<!\.)exe(?=\s|$)', '.exe', line)
        line = re.sub(r'(?<!\.)pdb(?=\s|$)', '.pdb', line)
        line = re.sub(r'(?<!\.)xml(?=\s|$)', '.xml', line)
        line = re.sub(r'(?<!\.)py(?=\s|$)', '.py', line)
        line = re.sub(r'(?<!\.)ini(?=\s|$)', '.ini', line)
        line = re.sub(r'(?<!\.)config(?=\s|$)', '.config', line)
        line = re.sub(r'(?<!\.)yml(?=\s|$)', '.yml', line)
        line = re.sub(r'(?<!\.)jar(?=\s|$)', '.jar', line)
        
        # 去除多余的空白
        line = line.strip()
        
        # 只保留非空行
        if line:
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

def parse_file_info(cleaned_text):
    """
    解析文件信息，提取结构化数据
    """
    lines = cleaned_text.split('\n')
    file_info_list = []
    
    # 匹配文件信息的正则表达式
    file_pattern = r'(.+?)\s+(\d{4}/\d{1,2}/\d{1,2}\s+\d{1,2}:\d{2})\s*(.*?)\s*(\d+)\s*(KB)?'
    
    for line in lines:
        match = re.match(file_pattern, line)
        if match:
            file_name = match.group(1).strip()
            file_date = match.group(2).strip()
            file_type = match.group(3).strip() if match.group(3) else "未知"
            file_size = match.group(4).strip()
            size_unit = match.group(5) if match.group(5) else "KB"
            
            file_info = {
                'name': file_name,
                'date': file_date,
                'type': file_type,
                'size': f"{file_size} {size_unit}"
            }
            file_info_list.append(file_info)
    
    return file_info_list

def format_file_list(file_info_list):
    """
    格式化文件列表输出
    """
    if not file_info_list:
        return "未识别到有效的文件信息"
    
    # 计算列宽
    max_name_len = max(len(info['name']) for info in file_info_list) if file_info_list else 20
    max_type_len = max(len(info['type']) for info in file_info_list) if file_info_list else 15
    
    # 确保最小宽度
    max_name_len = max(max_name_len, 20)
    max_type_len = max(max_type_len, 15)
    
    # 输出表头
    header = f"{'文件名':<{max_name_len}} {'修改时间':<16} {'类型':<{max_type_len}} {'大小':<10}"
    separator = "-" * (max_name_len + 16 + max_type_len + 12)
    
    formatted_output = [header, separator]
    
    # 输出文件信息
    for info in file_info_list:
        line = f"{info['name']:<{max_name_len}} {info['date']:<16} {info['type']:<{max_type_len}} {info['size']:<10}"
        formatted_output.append(line)
    
    return '\n'.join(formatted_output)

if __name__ == '__main__':
    image_path = r'D:\file_compare_scan\picture\1754546015687.jpg'
    dir = r'D:\file_compare_scan\picture'
    
    # image_to_string(image_path)
    pictures = get_picture(dir)
    for picture in pictures:
        print(f"\n{'='*80}")
        print(f"处理图片: {os.path.basename(picture)}")
        print('='*80)
        
        text = image_to_string(picture)
        
        # 清理文本
        cleaned_text = clean_ocr_text(text)
        
        # 解析文件信息
        file_info_list = parse_file_info(cleaned_text)
        
        # 格式化输出
        formatted_output = format_file_list(file_info_list)
        
        print("清理后的文本:")
        print(cleaned_text)
        print("\n结构化文件列表:")
        print(formatted_output)
        print("\n\n")