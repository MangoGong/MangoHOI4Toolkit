import os
from tkinter import filedialog, messagebox
import tkinter as tk
from PIL import Image

def convert_to_dds(image_path, output_path, size):
    try:
        img = Image.open(image_path).convert('RGBA')  # 转换为RGBA格式
        img = img.resize(size, Image.ANTIALIAS)  # 调整图片大小
        img.save(output_path, format='DDS')  # 保存为DDS格式
        messagebox.showinfo("成功！", f"文件已成功转换为DDS格式并被保存在{output_path}")
    except Exception as e:
        messagebox.showerror("错误", f"发生了一个错误: {e}")

def convert_to_tga(image_path, output_path, size):
    try:
        # 打开图像并转换为 RGBA 格式
        img = Image.open(image_path).convert('RGBA')
        # 调整图像大小
        img = img.resize(size, Image.Resampling.LANCZOS)
        # 保存为 TGA 格式
        img.save(output_path, format='TGA')
        messagebox.showinfo("成功！", f"文件已成功转换为TGA格式并被保存在{output_path}")
    except Exception as e:
        messagebox.showerror("错误", f"发生了一个错误: {e}")

def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("图片文件", "*.png;*.jpg;*.jpeg;*.bmp")])
    if file_path:
        return file_path
    else:
        messagebox.showerror("错误", "未选择图片")
        return None

def save_dds(image_path, size, size_str, root):
    if image_path:
        output_path = filedialog.asksaveasfilename(defaultextension=".dds", filetypes=[("DDS文件", "*.dds")])
        if output_path:
            convert_to_dds(image_path, output_path, size)
        else:
            messagebox.showerror("错误", f"No output file selected for {size_str}")

def save_tga(image_path, size, size_str, root):
    if image_path:
        output_path = filedialog.asksaveasfilename(defaultextension=".tga", filetypes=[("TGA文件", "*.tga")])
        if output_path:
            convert_to_tga(image_path, output_path, size)
        else:
            messagebox.showerror("错误", f"No output file selected for {size_str}")

def open_image(root):
    image_path = select_image()
    if image_path:
        # Options to convert to different sizes
        size1 = (82, 52)
        size2 = (41, 26)
        size3 = (10, 7)
        size4 = (96, 96)
        size5 = (68, 68)
        size6 = (156, 208)

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        button1 = tk.Button(button_frame, text="82x52（大尺寸国旗,TGA）", command=lambda: save_tga(image_path, size1, "82x52", root))
        button1.grid(row=0, column=0, padx=5, pady=5)

        button2 = tk.Button(button_frame, text="41x26（中尺寸国旗,TGA）", command=lambda: save_tga(image_path, size2, "41x26", root))
        button2.grid(row=0, column=1, padx=5, pady=5)

        button3 = tk.Button(button_frame, text="10x7（小尺寸国旗,TGA）", command=lambda: save_tga(image_path, size3, "10x7", root))
        button3.grid(row=0, column=2, padx=5, pady=5)

        button3 = tk.Button(button_frame, text="96×96（国策,DDS）", command=lambda: save_dds(image_path, size3, "10x7", root))
        button3.grid(row=1, column=0, padx=5, pady=5)

        button3 = tk.Button(button_frame, text="68×68（民族精神,DDS）", command=lambda: save_dds(image_path, size3, "10x7", root))
        button3.grid(row=1, column=1, padx=5, pady=5)

        button3 = tk.Button(button_frame, text="156x208（领导人肖像,DDS）", command=lambda: save_dds(image_path, size3, "10x7", root))
        button3.grid(row=1, column=2, padx=5, pady=5)


###GUI部分

def create_gui():
    root = tk.Tk()
    root.title("钢丝图片转换器")
    root.geometry("600x300")
    
    label = tk.Label(root, text="请选择要转换格式的图片")
    label.pack(pady=10)

    select_btn = tk.Button(root, text="选择图片文件", command=lambda: open_image(root))
    select_btn.pack(pady=5)

    #root.iconbitmap("LOGO.ico")
    root.mainloop()

if __name__ == "__main__":
    create_gui()



###我需要一个将任意图片格式转换成dds并能够将其调整成82*52 、41*26 、10*7三个尺寸大小的py脚本，输出的图片必须是BGRA格式，且该代码应该能够直接封装成.exe文件，并且写出GUI。