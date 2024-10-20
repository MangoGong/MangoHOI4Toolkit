import tkinter as tk

def redirect_print(*args, **kwargs):
    output = ""
    for arg in args:
        output += str(arg) + " "
    text_box.insert(tk.END, output + "\n")
    text_box.see(tk.END)  # 滚动到文本框底部

root = tk.Tk()
text_box = tk.Text(root)
text_box.pack()

# 重定向print()函数的输出
print = redirect_print

# 测试输出
print("Hello, World!")
print("This is a test.")

root.mainloop()