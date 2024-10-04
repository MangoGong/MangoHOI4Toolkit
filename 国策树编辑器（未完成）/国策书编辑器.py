import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

class FocusTreeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("钢铁雄心4国策树编辑器")
        self.root.geometry("1000x700")
        
        # 配置格子的大小
        self.grid_width = 50
        self.grid_height = 25
        
        # 初始化画布
        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # 绑定事件
        self.canvas.bind("<ButtonPress-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<Configure>", self.on_canvas_resize)

        # 工具栏
        self.toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_focus_btn = tk.Button(self.toolbar, text="添加国策", command=self.add_focus)
        self.add_focus_btn.pack(side=tk.LEFT, padx=2, pady=2)

        self.load_img_btn = tk.Button(self.toolbar, text="加载图片", command=self.load_image)
        self.load_img_btn.pack(side=tk.LEFT, padx=2, pady=2)

        self.save_btn = tk.Button(self.toolbar, text="保存国策树", command=self.save_focus_tree)
        self.save_btn.pack(side=tk.LEFT, padx=2, pady=2)

        self.add_prereq_btn = tk.Button(self.toolbar, text="设置需求", command=self.set_prerequisite)
        self.add_prereq_btn.pack(side=tk.LEFT, padx=2, pady=2)

        self.add_mutex_btn = tk.Button(self.toolbar, text="设置互斥", command=self.set_mutex)
        self.add_mutex_btn.pack(side=tk.LEFT, padx=2, pady=2)

        self.preview_btn = tk.Button(self.toolbar, text="预览国策树", command=self.preview_tree)
        self.preview_btn.pack(side=tk.LEFT, padx=2, pady=2)

        # 初始化
        self.focus_list = []  # 保存国策信息的列表
        self.current_focus = None  # 当前被选中的国策
        self.drag_data = {"x": 0, "y": 0, "item": None}  # 用于拖动功能

        # 绘制初始格子
        self.draw_grid()

    def on_canvas_click(self, event):
        """检测是否点击了国策，并开始拖动"""
        closest_item = self.canvas.find_closest(event.x, event.y)
        focus_id = closest_item[0]
        focus = self.find_focus_by_item(focus_id)
        if focus:
            self.current_focus = focus
            self.drag_data["item"] = focus_id
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

    def on_canvas_drag(self, event):
        """拖动国策框时，保证其只能在格子线的交点移动"""
        if self.drag_data["item"]:
            # 将当前鼠标坐标调整到最近的格子交点
            grid_x = round(event.x / self.grid_width) * self.grid_width
            grid_y = round(event.y / self.grid_height) * self.grid_height

            # 更新画布上国策的移动
            item_id = self.drag_data["item"]
            self.canvas.coords(item_id, grid_x, grid_y, grid_x + self.grid_width, grid_y + self.grid_height)
            
            # 同步移动文字，使其保持在灰框中央
            text_id = self.current_focus["text_item"]
            self.canvas.coords(text_id, grid_x + self.grid_width // 2, grid_y + self.grid_height // 2)

            # 更新国策的位置信息
            self.current_focus["x"] = grid_x
            self.current_focus["y"] = grid_y

    def on_canvas_resize(self, event):
        """当窗口大小改变时，重新绘制格子"""
        self.canvas.delete("grid_line")
        self.draw_grid()

    def draw_grid(self):
        """绘制画布中的格子线"""
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        for i in range(0, width, self.grid_width):
            self.canvas.create_line(i, 0, i, height, tag="grid_line", fill="lightgray")

        for i in range(0, height, self.grid_height):
            self.canvas.create_line(0, i, width, i, tag="grid_line", fill="lightgray")

    def add_focus(self):
        focus_name = simpledialog.askstring("国策名称", "请输入国策名称：")
        if focus_name:
            # 初始位置为最近的格子交点
            grid_x = 100 // self.grid_width * self.grid_width
            grid_y = 100 // self.grid_height * self.grid_height
            focus = {
                "name": focus_name,
                "image": None,
                "x": grid_x,
                "y": grid_y,
                "prerequisites": [],
                "mutually_exclusive": []
            }
            self.focus_list.append(focus)
            self.draw_focus(focus)

    def load_image(self):
        file_path = filedialog.askopenfilename(title="选择国策图片", filetypes=[("图片文件", "*.png;*.jpg")])
        if file_path and self.current_focus:
            self.current_focus['image'] = file_path
            self.canvas.create_image(self.current_focus['x'], self.current_focus['y'], image=tk.PhotoImage(file=file_path))

    def set_prerequisite(self):
        if not self.current_focus:
            messagebox.showerror("错误", "请选择一个国策。")
            return
        prereq_name = simpledialog.askstring("需求国策", "请输入需求国策名称：")
        prereq_focus = self.find_focus_by_name(prereq_name)
        if prereq_focus:
            self.current_focus['prerequisites'].append(prereq_name)
            messagebox.showinfo("成功", f"{self.current_focus['name']} 已设置 {prereq_name} 作为需求国策。")
        else:
            messagebox.showerror("错误", "找不到该国策！")

    def set_mutex(self):
        if not self.current_focus:
            messagebox.showerror("错误", "请选择一个国策。")
            return
        mutex_name = simpledialog.askstring("互斥国策", "请输入互斥国策名称：")
        mutex_focus = self.find_focus_by_name(mutex_name)
        if mutex_focus:
            self.current_focus['mutually_exclusive'].append(mutex_name)
            messagebox.showinfo("成功", f"{self.current_focus['name']} 已设置 {mutex_name} 作为互斥国策。")
        else:
            messagebox.showerror("错误", "找不到该国策！")

    def find_focus_by_name(self, name):
        for focus in self.focus_list:
            if focus['name'] == name:
                return focus
        return None

    def find_focus_by_item(self, item):
        for focus in self.focus_list:
            if focus.get('item') == item or focus.get('text_item') == item:
                return focus
        return None

    def draw_focus(self, focus):
        # 将国策绘制在格子线上，灰框大小为一个格子
        focus_id = self.canvas.create_rectangle(focus["x"], focus["y"], focus["x"]+self.grid_width, focus["y"]+self.grid_height, fill="lightgrey")
        text_id = self.canvas.create_text(focus["x"] + self.grid_width // 2, focus["y"] + self.grid_height // 2, text=focus["name"])

        # 记录画布中的国策项ID
        focus['item'] = focus_id
        focus['text_item'] = text_id

    def save_focus_tree(self):
        save_path = filedialog.asksaveasfilename(title="保存国策树", defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if save_path:
            with open(save_path, 'w') as file:
                for focus in self.focus_list:
                    file.write(f"国策名称: {focus['name']}\n")
                    if focus['image']:
                        file.write(f"图片路径: {focus['image']}\n")
                    file.write(f"位置: {focus['x']}, {focus['y']}\n")
                    if focus['prerequisites']:
                        file.write(f"需求: {', '.join(focus['prerequisites'])}\n")
                    if focus['mutually_exclusive']:
                        file.write(f"互斥: {', '.join(focus['mutually_exclusive'])}\n")
                    file.write("\n")
            messagebox.showinfo("保存成功", f"国策树已保存至 {save_path}")

    def preview_tree(self):
        """预览当前国策树结构"""
        preview_window = tk.Toplevel(self.root)
        preview_window.title("国策树预览")
        preview_window.geometry("600x400")
        preview_canvas = tk.Canvas(preview_window, bg="white")
        preview_canvas.pack(fill=tk.BOTH, expand=True)

        for focus in self.focus_list:
            preview_canvas.create_rectangle(focus["x"], focus["y"], focus["x"]+self.grid_width, focus["y"]+self.grid_height, fill="lightgrey")
            preview_canvas.create_text(focus["x"]+self.grid_width//2, focus["y"]+self.grid_height//2, text=focus["name"])
            for prereq_name in focus['prerequisites']:
                prereq_focus = self.find_focus_by_name(prereq_name)
                if prereq_focus:
                    preview_canvas.create_line(focus["x"]+self.grid_width//2, focus["y"], prereq_focus["x"]+self.grid_width//2, prereq_focus["y"]+self.grid_height, arrow=tk.LAST)

# 启动应用
if __name__ == "__main__":
    root = tk.Tk()
    app = FocusTreeEditor(root)
    root.mainloop()
