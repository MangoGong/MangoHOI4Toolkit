import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry  # 导入tkcalendar库

# 创建主窗口
root = tk.Tk()
root.title("代码生成工具")
root.geometry("825x400")

# 添加居中显示的标签
header_label = tk.Label(root, text="A HOI4 Modding Tool, By MangoGong from TCV")
header_label.grid(row=3, column=0, columnspan=3, pady=5)  # 使用 grid 并设置 columnspan 使其居中

header_label = tk.Label(root, text="For more content, go to https://github.com/MangoGong")
header_label.grid(row=4, column=0, columnspan=3)  # 使用 grid 并设置 columnspan 使其居中

# 全局数据结构
selected_leaders = {
    "field_marshal": tk.BooleanVar(),
    "navy_leader": tk.BooleanVar(),
    "corps_commander": tk.BooleanVar(),
    "advisor": tk.BooleanVar(),
    "country_leader": tk.BooleanVar()
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
    output = f'characters = {{\n\tname = "{instance_name}"\n\tportraits = {{\n'
    for unit, portrait in data["portraits"].items():
        output += f'\t\t{unit} = {{\n\t\t\tlarge = {portrait["large"]}\n\t\t\tsmall = {portrait["small"]}\n\t\t}}\n'
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

# 创建Notebook标签页
notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0, padx=10, pady=10)

def create_leader_tab(tab_name, labels):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text=tab_name.replace("_", " ").capitalize())

    # 添加是否启用的复选框
    tk.Checkbutton(frame, text=f"添加{tab_name.replace('_', ' ').capitalize()}", variable=selected_leaders[tab_name], command=update_preview).grid(row=0, column=0, sticky=tk.W)

    for i, (label_text, key) in enumerate(labels):
        tk.Label(frame, text=label_text).grid(row=i + 1, column=0, sticky=tk.W)

        # 根据字段类型决定使用 Spinbox 还是 Entry
        if key in ["skill", "attack_skill", "defense_skill", "planning_skill", "logistics_skill", "maneuvering_skill", "coordination_skill"]:
            # 使用 Spinbox 创建技能输入框
            spinbox = tk.Spinbox(frame, from_=0, to=10, width=5)
            spinbox.grid(row=i + 1, column=1, sticky=tk.W)
            data[tab_name][key] = spinbox
            spinbox.bind("<KeyRelease>", lambda event: update_preview())
        else:
            # 使用 Entry 创建其他输入框
            entry = tk.Entry(frame, width=25)  # 设置宽度与其他输入框对齐
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

# 创建 advisor 标签页
advisor_frame = ttk.Frame(notebook)
notebook.add(advisor_frame, text="Advisor")

# 添加复选框
tk.Checkbutton(advisor_frame, text="添加 Advisor", variable=selected_leaders["advisor"], command=update_preview).grid(row=0, column=0, sticky=tk.W)

# 为 Cost 添加 Entry 和 Spinbox，调整位置，按钮在文本框右侧
tk.Label(advisor_frame, text="Cost (0+):").grid(row=1, column=0, sticky=tk.W)

cost_frame = tk.Frame(advisor_frame)
cost_frame.grid(row=1, column=1, sticky=tk.W)

cost_spinbox = tk.Spinbox(cost_frame, from_=0, to=100, width=23)
cost_spinbox.pack(side=tk.RIGHT)  # Spinbox on the right
cost_spinbox.bind("<KeyRelease>", lambda event: update_preview())

data["advisor"]["cost"] = cost_spinbox

# 其余输入框
tk.Label(advisor_frame, text="Allowed:").grid(row=2, column=0, sticky=tk.W)
allowed_entry = tk.Entry(advisor_frame, width=25)
allowed_entry.grid(row=2, column=1, sticky=tk.W)
data["advisor"]["allowed"] = allowed_entry
allowed_entry.bind("<KeyRelease>", lambda event: update_preview())

tk.Label(advisor_frame, text="Traits:").grid(row=3, column=0, sticky=tk.W)
traits_entry = tk.Entry(advisor_frame, width=25)
traits_entry.grid(row=3, column=1, sticky=tk.W)
data["advisor"]["traits"] = traits_entry
traits_entry.bind("<KeyRelease>", lambda event: update_preview())

tk.Label(advisor_frame, text="AI Will Do (0-1):").grid(row=4, column=0, sticky=tk.W)
ai_will_do_entry = tk.Entry(advisor_frame, width=25)
ai_will_do_entry.grid(row=4, column=1, sticky=tk.W)
data["advisor"]["ai_will_do"] = ai_will_do_entry
ai_will_do_entry.bind("<KeyRelease>", lambda event: update_preview())

# 添加 country_leader 标签页
create_leader_tab("country_leader", [("意识形态:", "ideology"), ("描述:", "desc"),
                                     ("Traits:", "traits"), ("到期日期:", "expire"),
                                     ("ID:", "id")])

country_leader_frame = notebook.children['!frame5']

# 添加 expire_date 的日历控件，设置宽度
tk.Label(country_leader_frame, text="到期日期:").grid(row=3, column=0, sticky=tk.W)
expire_date_entry = DateEntry(country_leader_frame, date_pattern='yyyy.MM.dd', width=22)  # 设置宽度
expire_date_entry.grid(row=3, column=1, sticky=tk.W)
data["country_leader"]["expire"] = expire_date_entry


# 监听名称输入框并自动生成desc字段
def update_desc_field(*args):
    desc_entry.delete(0, tk.END)
    desc_entry.insert(0, name_entry.get() + "_desc")

desc_entry = data["country_leader"]["desc"]

# 输入实例名称
name_frame = tk.Frame(root)
name_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

tk.Label(name_frame, text="名称:").pack(side=tk.LEFT)
name_entry = tk.Entry(name_frame)
name_entry.pack(side=tk.LEFT)
name_entry.bind("<KeyRelease>", lambda event: update_preview())

# 绑定名称更新事件以生成描述
name_entry.bind("<KeyRelease>", update_desc_field)

# 输出结果的文本框在右侧
result_text = tk.Text(root, height=20, width=50)
result_text.grid(row=0, column=3, rowspan=3, padx=10, pady=10)

# 启动主循环
root.mainloop()
