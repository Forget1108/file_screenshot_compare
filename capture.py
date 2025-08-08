# capture.py 的修改建议
import tkinter as tk
from PIL import Image, ImageGrab
import os
import time

class ScreenCapture:
    def __init__(self):
        self.root = None
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.rect = None
        self.drawing = False
        
    def capture_image(self, save_path=None):
        """捕获屏幕区域"""
        print("请开始选择截图区域...")
        time.sleep(0.5)
        
        # 确保之前的Tk实例完全关闭
        if tk._default_root:
            try:
                tk._default_root.destroy()
            except:
                pass
            tk._default_root = None
        
        # 创建新的截图选择器
        selector = RegionSelector()
        coords = selector.select_region()
        data_dir = 'picture'
        os.makedirs(data_dir, exist_ok=True)
        
        if coords:
            left, top, right, bottom = coords
            # 截取选定区域
            screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
            
            # 生成带时间戳的文件名
            if save_path is None:
                import datetime
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                save_path = os.path.join(data_dir, f"region_screenshot_{timestamp}.png")
            
            screenshot.save(save_path)
            print(f"截图已保存为: {save_path}")
            return save_path
        return None

class RegionSelector:
    def __init__(self):
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.rect = None
        self.drawing = False
        self.coords = None
        
    def select_region(self):
        """选择屏幕区域"""
        # 创建全屏选择窗口
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.3)  # 半透明
        self.root.configure(cursor="crosshair")
        self.root.title("选择截图区域 - 按ESC退出")
        
        # 创建画布
        self.canvas = tk.Canvas(self.root, bg='gray')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # 绑定事件
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.root.bind('<Escape>', self.on_escape)
        
        # 运行事件循环
        self.root.mainloop()
        
        return self.coords
    
    def on_mouse_down(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.drawing = True
        
    def on_mouse_drag(self, event):
        if self.drawing:
            # 删除之前的矩形
            if self.rect:
                self.canvas.delete(self.rect)
            
            # 绘制新的选择矩形
            self.rect = self.canvas.create_rectangle(
                self.start_x, self.start_y, event.x, event.y,
                outline='red', width=2, fill='blue', stipple='gray25'
            )
    
    def on_mouse_up(self, event):
        self.end_x = event.x
        self.end_y = event.y
        self.drawing = False
        
        if self.start_x and self.end_x:
            left = min(self.start_x, self.end_x)
            top = min(self.start_y, self.end_y)
            right = max(self.start_x, self.end_x)
            bottom = max(self.start_y, self.end_y)
            self.coords = (left, top, right, bottom)
        
        self.root.quit()
        self.root.destroy()
    
    def on_escape(self, event):
        self.coords = None
        self.root.quit()
        self.root.destroy()

# 全局函数
def capture_image():
    """捕获屏幕图像"""
    capture = ScreenCapture()
    return capture.capture_image()