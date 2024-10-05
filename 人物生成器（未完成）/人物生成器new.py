import tkinter as tk
from tkinter import ttk

# 创建主窗口
root = tk.Tk()
root.title("代码生成工具")
root.geometry("1000x600")

# 全局数据结构
selected_leaders = {
    "field_marshal": tk.BooleanVar(value=False),
    "navy_leader": tk.BooleanVar(value=False),
    "corps_commander": tk.BooleanVar(value=False),
    "advisor": tk.BooleanVar(value=False),
    "country_leader": tk.BooleanVar(value=False)
}

data = {
    "portraits": {
        "army": {"large": "", "small": ""},
        "navy": {"large": "", "small": ""},
        "civilian": {"large": "", "small": ""}
    },
    "field_marshal": {},
    "navy_leader": {},
    "corps_commander": {},
    "advisor": {},
    "country_leader": {}
}

# 互斥逻辑：field_marshal 和 corps_commander 互斥选择
def toggle_mutex(*args):
    if selected_leaders["field_marshal"].get():
        selected_leaders["corps_commander"].set(False)
    elif selected_leaders["corps_commander"].get():
        selected_leaders["field_marshal"].set(False)
    update_preview()

selected_leaders["field_marshal"].trace_add("write", toggle_mutex)
selected_leaders["corps_commander"].trace_add("write", toggle_mutex)

# 实时更新代码预览
def update_preview():
    instance_name = name_entry.get().strip()
    if not instance_name:
        return

    output = f'characters = {{\n\tname = "{instance_name}"\n\tportraits = {{\n'
    for unit, portrait in data["portraits"].items():
        output += f'\t\t{unit} = {{\n\t\t\tlarge = "{portrait["large"]}"\n\t\t\tsmall = "{portrait["small"]}"\n\t\t}}\n'
    output += "\t}\n"

    for leader_type, selected in selected_leaders.items():
        if selected.get():
            output += f'\t{leader_type} = {{\n'
            for key, widget in data[leader_type].items():
                value = widget.get().strip()
                # 确保 traits 和 visible 字段在花括号内
                if key in ["traits", "visible", "allowed", "ai_will_do"]:
                    output += f'\t\t{key} = {{{value}}}\n'
                else:
                    output += f'\t\t{key} = {value}\n'
            output += '\t}\n'
    
    output += '}\n'

    # 更新右侧预览文本框
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, output)

    # 根据内容动态调整文本框高度
    original_height = result_text.cget('height')  # 获取当前高度
    num_lines = int(result_text.index('end-1c').split('.')[0])  # 获取当前内容的行数
    new_height = min(max(10, num_lines), 30)  # 限制最小10行，最大30行
    if original_height != new_height:  # 只有当高度变化时才更新
        result_text.config(height=new_height)  # 更新高度

# 创建Notebook标签页
notebook = ttk.Notebook(root)
notebook.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')

def create_leader_tab(tab_name, labels):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text=tab_name.replace("_", " ").capitalize())

    # 添加是否启用的复选框
    tk.Checkbutton(frame, text=f"添加{tab_name.replace('_', ' ').capitalize()}", variable=selected_leaders[tab_name], command=update_preview).grid(row=0, column=0, sticky=tk.W)

    for i, (label_text, key) in enumerate(labels):
        tk.Label(frame, text=label_text).grid(row=i + 1, column=0, sticky=tk.W)
        entry = tk.Entry(frame)
        entry.grid(row=i + 1, column=1, sticky=tk.W)
        data[tab_name][key] = entry
        entry.bind("<KeyRelease>", lambda event: update_preview())

# 创建各个标签页
create_leader_tab("field_marshal", [("技能 (1-10):", "skill"), ("攻击技能 (1-10):", "attack_skill"),
                                    ("防御技能 (1-10):", "defense_skill"), ("计划技能 (1-10):", "planning_skill"),
                                    ("后勤技能 (1-10):", "logistics_skill"), ("Traits:", "traits"),
                                    ("Visible:", "visible")])

create_leader_tab("navy_leader", [("技能 (1-10):", "skill"), ("攻击技能 (1-10):", "attack_skill"),
                                  ("防御技能 (1-10):", "defense_skill"), ("机动技能 (1-10):", "maneuvering_skill"),
                                  ("协调技能 (1-10):", "coordination_skill"), ("Traits:", "traits"),
                                  ("Visible:", "visible")])

create_leader_tab("corps_commander", [("技能 (1-10):", "skill"), ("攻击技能 (1-10):", "attack_skill"),
                                      ("防御技能 (1-10):", "defense_skill"), ("计划技能 (1-10):", "planning_skill"),
                                      ("后勤技能 (1-10):", "logistics_skill"), ("Traits:", "traits"),
                                      ("Visible:", "visible")])

# 添加 advisor 标签页
def update_leger_options(*args):
    slot = data["advisor"]["slot"].get()
    if slot in ["theorist", "high_command"]:
        leger_combobox.config(values=["army", "air", "navy"], state="readonly")
    elif slot == "army_chief":
        leger_combobox.config(values=["army"], state="readonly")
    elif slot == "navy_chief":
        leger_combobox.config(values=["navy"], state="readonly")
    elif slot == "air_chief":
        leger_combobox.config(values=["air"], state="readonly")
    else:
        leger_combobox.config(values=["Civilian"], state="readonly")
    update_preview()

create_leader_tab("advisor", [("Cost (0+):", "cost"), ("Allowed:", "allowed"),
                              ("Traits:", "traits"), ("AI Will Do (0-1):", "ai_will_do")])

advisor_frame = notebook.children['!frame4']  # 获取 advisor 页面的 frame

# 添加 slot 和 leger
tk.Label(advisor_frame, text="Slot:").grid(row=5, column=0, sticky=tk.W)
slot_combobox = ttk.Combobox(advisor_frame, values=["political_advisor", "theorist", "army_chief", "navy_chief", "air_chief", "high_command"], state="readonly")
slot_combobox.grid(row=5, column=1, sticky=tk.W)
data["advisor"]["slot"] = slot_combobox
slot_combobox.bind("<<ComboboxSelected>>", update_leger_options)

tk.Label(advisor_frame, text="Leger:").grid(row=6, column=0, sticky=tk.W)
leger_combobox = ttk.Combobox(advisor_frame, state="readonly")
leger_combobox.grid(row=6, column=1, sticky=tk.W)
data["advisor"]["leger"] = leger_combobox
slot_combobox.bind("<<ComboboxSelected>>", lambda e: update_preview())  # 确保 slot 变化反映到代码中
leger_combobox.bind("<<ComboboxSelected>>", lambda e: update_preview())  # 确保 leger 变化反映到代码中

# 添加 country_leader 标签页
create_leader_tab("country_leader", [("意识形态:", "ideology"), ("描述:", "desc"),
                                     ("Traits:", "traits"), ("到期日期:", "expire"),
                                     ("ID:", "id")])

country_leader_frame = notebook.children['!frame5']

# 监听名称输入框并自动生成desc字段
def update_desc_field(*args):
    desc_entry.delete(0, tk.END)
    desc_entry.insert(0, name_entry.get() + "_desc")

desc_entry = data["country_leader"]["desc"]  # 定义 desc_entry

# 输入实例名称（固定在标签页上方并居中）
name_frame = tk.Frame(root)
name_frame.grid(row=0, column=0, sticky=tk.W+tk.E)

tk.Label(name_frame, text="名称:").pack(side=tk.LEFT)
name_entry = tk.Entry(name_frame)
# 使输入框可扩展填满剩余空间，并居中
name_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
name_entry.bind("<KeyRelease>", lambda event: update_preview())  # 绑定事件

tk.Label(name_frame, text="名称:").pack(side=tk.LEFT)
name_entry = tk.Entry(name_frame)
name_entry.pack(side=tk.LEFT)
name_entry.bind("<KeyRelease>", lambda event: update_preview() and update_desc_field())  # 合并事件处理函数

#绑定名称更新事件以生成描述
name_entry.bind("<KeyRelease>", update_desc_field)

#输出结果的文本框在右侧
result_text = tk.Text(root, height=20, width=50)
result_text.grid(row=0, column=3, rowspan=3, padx=10, pady=10, sticky="nsew")

# 在程序启动时调用update_preview函数以生成初始的输出代码
update_preview()

#启动主循环
root.mainloop()