import tkinter as tk
from tkinter import messagebox

def generate_code():
    name = name_entry.get()
    job = job_var.get()
    
    # 验证输入的技能值
    try:
        skill = int(skill_entry.get())
        attack_skill = int(attack_skill_entry.get())
        defense_skill = int(defense_skill_entry.get())
        planning_skill = int(planning_skill_entry.get())
        logistics_skill = int(logistics_skill_entry.get())
    except ValueError:
        messagebox.showerror("输入错误", "技能值不能为空。")
        return
    
    if not (1 <= skill <= 10) or not (1 <= attack_skill <= 10) or not (1 <= defense_skill <= 10) or not (1 <= planning_skill <= 10) or not (1 <= logistics_skill <= 10):
        messagebox.showerror("输入错误", "技能值必须是1到10之间的整数。")
        return

    # 生成代码
    code = f"""{name} = {{
    name = {name}
    portraits = {{
        army = {{
            large = GFX_portrait_{name}
            small = GFX_portrait_{name}_small
        }}
    }}
    {job} = {{
        traits = {{ }}
        skill = {skill}
        attack_skill = {attack_skill}
        defense_skill = {defense_skill}
        planning_skill = {planning_skill}
        logistics_skill = {logistics_skill}
        legacy_id = -1
    }}
}}"""

    # 显示结果
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, code)

# 创建主窗口
root = tk.Tk()
root.title("代码生成工具")
root.geometry("500x600")  # 设置窗口长宽

# 添加居中显示的标签
header_label = tk.Label(root, text="请注意将领的名字只能为英语，实际使用时请注意肖像的名称。", font=(12))
header_label.grid(row=0, column=0, columnspan=3, pady=10)  # 使用 grid 并设置 columnspan 使其居中

# 输入字段

tk.Label(root, text="名称:").grid(row=1, column=0)
name_entry = tk.Entry(root)
name_entry.grid(row=1, column=1)

tk.Label(root, text="职业:").grid(row=2, column=0)
job_var = tk.StringVar(value="field_marshal")
tk.Radiobutton(root, text="元帅(Field Marshal)", variable=job_var, value="field_marshal").grid(row=2, column=1, sticky=tk.W)
tk.Radiobutton(root, text="将领(Corps Commander)", variable=job_var, value="corps_commander").grid(row=2, column=2, sticky=tk.W)

tk.Label(root, text="技能 (1-10):").grid(row=3, column=0)
skill_entry = tk.Entry(root)
skill_entry.grid(row=3, column=1)

tk.Label(root, text="攻击技能 (1-10):").grid(row=4, column=0)
attack_skill_entry = tk.Entry(root)
attack_skill_entry.grid(row=4, column=1)

tk.Label(root, text="防御技能 (1-10):").grid(row=5, column=0)
defense_skill_entry = tk.Entry(root)
defense_skill_entry.grid(row=5, column=1)

tk.Label(root, text="计划技能 (1-10):").grid(row=6, column=0)
planning_skill_entry = tk.Entry(root)
planning_skill_entry.grid(row=6, column=1)

tk.Label(root, text="后勤技能 (1-10):").grid(row=7, column=0)
logistics_skill_entry = tk.Entry(root)
logistics_skill_entry.grid(row=7, column=1)

# 生成按钮
generate_button = tk.Button(root, text="生成代码", command=generate_code)
generate_button.grid(row=5, column=2, columnspan=2)

# 显示结果的文本框
result_text = tk.Text(root, height=20, width=50)
result_text.grid(row=9, column=0, columnspan=3)

tk.Label(root, text="A HOI4 Modding Tool, By MangoGong from TCV").grid(row=11, column=0, columnspan=3)
tk.Label(root, text="For more content, go to https://github.com/MangoGong").grid(row=12, column=0, columnspan=3)

# 启动GUI主循环
root.mainloop()
