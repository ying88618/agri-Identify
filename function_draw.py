import tkinter as tk
from tkinter import ttk
import math
import numpy as np

# 创建主窗口
root = tk.Tk()
root.title("数学函数动态可视化工具")
root.geometry("800x600")
root.resizable(True, True)

# 确保中文正常显示
root.option_add("*Font", "SimHei 10")

# 函数输入框架
input_frame = ttk.Frame(root, padding="10")
input_frame.pack(fill=tk.X)

# 函数输入标签和输入框
ttk.Label(input_frame, text="请输入函数表达式 (例如: x**2 或 sin(x)):").pack(side=tk.LEFT)
func_entry = ttk.Entry(input_frame, width=30)
func_entry.pack(side=tk.LEFT, padx=5)
func_entry.insert(0, "x**2")  # 默认函数

# 范围输入框架
range_frame = ttk.Frame(root, padding="10")
range_frame.pack(fill=tk.X)

# 起始值输入
ttk.Label(range_frame, text="x起始值:").pack(side=tk.LEFT)
x_start_entry = ttk.Entry(range_frame, width=10)
x_start_entry.pack(side=tk.LEFT, padx=5)
x_start_entry.insert(0, "-10")

# 结束值输入
ttk.Label(range_frame, text="x结束值:").pack(side=tk.LEFT)
x_end_entry = ttk.Entry(range_frame, width=10)
x_end_entry.pack(side=tk.LEFT, padx=5)
x_end_entry.insert(0, "10")

# 绘制按钮
def draw_function():
    """绘制用户输入的函数"""
    canvas.delete("all")  # 清除画布
    
    try:
        # 获取用户输入
        func_expr = func_entry.get()
        x_start = float(x_start_entry.get())
        x_end = float(x_end_entry.get())
        
        if x_start >= x_end:
            ttk.messagebox.showerror("错误", "起始值必须小于结束值")
            return
        
        # 绘制坐标轴
        draw_axes()
        
        # 计算函数值并绘制
        x_vals = np.linspace(x_start, x_end, 1000)
        y_vals = []
        
        for x in x_vals:
            # 安全地计算函数值
            try:
                y = eval(func_expr, {"__builtins__": None}, {"x": x, "math": math})
                y_vals.append(y)
            except:
                y_vals.append(None)  # 无法计算时设为None
        
        # 绘制函数曲线
        draw_curve(x_vals, y_vals, x_start, x_end)
        
    except Exception as e:
        ttk.messagebox.showerror("错误", f"绘制失败: {str(e)}")

draw_btn = ttk.Button(root, text="绘制函数", command=draw_function)
draw_btn.pack(pady=5)

# 绘图画布
canvas = tk.Canvas(root, bg="white", width=780, height=500)
canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

def draw_axes():
    """绘制坐标轴和网格"""
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    
    # 计算坐标轴位置 (居中)
    center_x = width // 2
    center_y = height // 2
    
    # 绘制x轴
    canvas.create_line(0, center_y, width, center_y, fill="black", width=2)
    # 绘制y轴
    canvas.create_line(center_x, 0, center_x, height, fill="black", width=2)
    
    # 绘制网格线
    for i in range(0, width, 50):
        canvas.create_line(i, center_y-5, i, center_y+5, fill="gray", width=1)
    for i in range(0, height, 50):
        canvas.create_line(center_x-5, i, center_x+5, i, fill="gray", width=1)

def draw_curve(x_vals, y_vals, x_start, x_end):
    """绘制函数曲线"""
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    center_x = width // 2
    center_y = height // 2
    
    # 计算缩放因子，使图像适合画布
    x_range = x_end - x_start
    x_scale = (width * 0.45) / max(abs(x_start), abs(x_end), 0.1)
    y_scale = (height * 0.45) / max(max([abs(y) for y in y_vals if y is not None] or [1]), 0.1)
    
    # 存储线段坐标
    points = []
    
    for x, y in zip(x_vals, y_vals):
        if y is None:
            continue  # 跳过无法计算的点
        
        # 转换为画布坐标
        canvas_x = center_x + x * x_scale
        canvas_y = center_y - y * y_scale  # y轴反向
        points.append(canvas_x)
        points.append(canvas_y)
    
    # 绘制曲线
    if points:
        canvas.create_line(points, fill="red", width=2)

# 初始绘制默认函数
draw_function()

# 运行主循环
root.mainloop()