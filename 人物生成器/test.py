import tkinter as tk
from tkinter import Button, ttk
from tkcalendar import DateEntry  # 导入tkcalendar库

def update_output():
    var.get()

import tkinter as tk

def redirect_print(*args, **kwargs):
    output = ""
    for arg in args:
        output += str(arg) + " "
    text_box.insert(tk.END, output + "\n")
    text_box.see(tk.END)  # 滚动到文本框底部

root = tk.Tk()
root.title("人物生成工具")
root.geometry("825x400")
root.resizable(False,False)

namelable = tk.Label(root, text='名字:', relief=tk.FLAT)
namelable.grid(row=0, column=0)

var = tk.StringVar()
name = tk.Entry(root, width=25)
name.grid(row=0, column=1)

keylabel = tk.Label(root, text='键名:', relief=tk.FLAT)
keylabel.grid(row=1, column=0)

var = tk.StringVar()
key = tk.Entry(root, width=25)
key.grid(row=1, column=1)

notebook = ttk.Notebook(root)
notebook.grid(row=2, columnspan=3, rowspan=6)

frame1 = tk.Frame()
frame2 = tk.Frame()
frame3 = tk.Frame()
frame4 = tk.Frame()
frame5 = tk.Frame()

notebook.add(frame1, text="field_marshal")
notebook.add(frame2, text="navy_leader")
notebook.add(frame3, text="corps_commander")
notebook.add(frame4, text="advisor")
notebook.add(frame5, text="country_leader")

switch1 = tk.Checkbutton(frame1, text="是否启用")
switch1.grid(row=0, column=0)

skill_label1 = ttk.Label(frame1, text="技能:")
skill_label1.grid(row=1, column=0)
skill1 = tk.Entry(frame1, width=25)
skill1.grid(row=1, column=1, sticky=tk.W)

attack_skill_label1 = ttk.Label(frame1, text="攻击技能:")
attack_skill_label1.grid(row=2, column=0)
attack_skill1 = tk.Entry(frame1, width=25)
attack_skill1.grid(row=2, column=1)

defense_skill_label1 = ttk.Label(frame1, text="防御技能:")
defense_skill_label1.grid(row=3, column=0)
defense_skill1 = tk.Entry(frame1, width=25)
defense_skill1.grid(row=3, column=1)

planning_skill_label1 = ttk.Label(frame1, text="计划技能:")
planning_skill_label1.grid(row=4, column=0)
planning_skill1 = tk.Entry(frame1, width=25)
planning_skill1.grid(row=4, column=1)

logistics_skill_label1 = ttk.Label(frame1, text="后勤技能:")
logistics_skill_label1.grid(row=5, column=0)
logistics_skill1 = tk.Entry(frame1, width=25)
logistics_skill1.grid(row=5, column=1)

switch2 = tk.Checkbutton(frame2, text="是否启用")
switch2.grid(row=0, column=0)

skill_label2 = ttk.Label(frame2, text="技能:")
skill_label2.grid(row=1, column=0)
skill2 = tk.Entry(frame2, width=25)
skill2.grid(row=1, column=1, sticky=tk.W)

attack_skill_label2 = ttk.Label(frame2, text="攻击技能:")
attack_skill_label2.grid(row=2, column=0)
attack_skill2 = tk.Entry(frame2, width=25)
attack_skill2.grid(row=2, column=1)

defense_skill_label1 = ttk.Label(frame2, text="防御技能:")
defense_skill_label1.grid(row=3, column=0)
defense_skill1 = tk.Entry(frame2, width=25)
defense_skill1.grid(row=3, column=1)

maneuvering_skill_label2 = ttk.Label(frame2, text="机动技能:")
maneuvering_skill_label2.grid(row=4, column=0)
maneuvering_skill2 = tk.Entry(frame2, width=25)
maneuvering_skill2.grid(row=4, column=1)

coordination_skill_label2 = ttk.Label(frame2, text="协作技能:")
coordination_skill_label2.grid(row=5, column=0)
coordination_skill2 = tk.Entry(frame2, width=25)
coordination_skill2.grid(row=5, column=1)

switch3 = tk.Checkbutton(frame3, text="是否启用")
switch3.grid(row=0, column=0)

skill_label3 = ttk.Label(frame3, text="技能:")
skill_label3.grid(row=1, column=0)
skill3 = tk.Entry(frame3, width=25)
skill3.grid(row=1, column=1, sticky=tk.W)

attack_skill_label3 = ttk.Label(frame3, text="攻击技能:")
attack_skill_label3.grid(row=2, column=0)
attack_skill3 = tk.Entry(frame3, width=25)
attack_skill3.grid(row=2, column=1)

defense_skill_label3 = ttk.Label(frame3, text="防御技能:")
defense_skill_label3.grid(row=3, column=0)
defense_skill3 = tk.Entry(frame3, width=25)
defense_skill3.grid(row=3, column=1)

planning_skill_label3 = ttk.Label(frame3, text="计划技能:")
planning_skill_label3.grid(row=4, column=0)
planning_skill3 = tk.Entry(frame3, width=25)
planning_skill3.grid(row=4, column=1)

logistics_skill_label3 = ttk.Label(frame3, text="后勤技能:")
logistics_skill_label3.grid(row=5, column=0)
logistics_skill3 = tk.Entry(frame3, width=25)
logistics_skill3.grid(row=5, column=1)

switch4 = tk.Checkbutton(frame4, text="是否启用")
switch4.grid(row=0, column=0)

cost_label = ttk.Label(frame4, text="花费:")
cost_label.grid(row=2, column=0)
cost = tk.Entry(frame4, width=25)
cost.grid(row=2, column=1)

allowed_label = ttk.Label(frame4, text="Allowed:")
allowed_label.grid(row=3, column=0)
allowed = tk.Entry(frame4, width=25)
allowed.grid(row=3, column=1)

traits_label = ttk.Label(frame4, text="Traits:")
traits_label.grid(row=4, column=0)
traits = tk.Entry(frame4, width=25)
traits.grid(row=4, column=1)

ai_will_do_label = ttk.Label(frame4, text="AI will do:")
ai_will_do_label.grid(row=5, column=0)
ai_will_do = tk.Entry(frame4, width=25)
ai_will_do.grid(row=5, column=1)

switch5 = tk.Checkbutton(frame5, text="是否启用")
switch5.grid(row=0, column=0)

ideology_label = ttk.Label(frame5, text="意识形态:")
ideology_label.grid(row=2, column=0)
ideology = tk.Entry(frame5, width=25)
ideology.grid(row=2, column=1)

allowed_label = ttk.Label(frame5, text="描述:")
allowed_label.grid(row=3, column=0)
allowed = tk.Entry(frame5, width=25)
allowed.grid(row=3, column=1)

desc_label = ttk.Label(frame5, text="到期日期:")
desc_label.grid(row=4, column=0)
desc = tk.Entry(frame5, width=25)
desc.grid(row=4, column=1)

id_label = ttk.Label(frame5, text="ID:")
id_label.grid(row=5, column=0)
id = tk.Entry(frame5, width=25)
id.grid(row=5, column=1)

text_box = tk.Text(root)
text_box.grid(row=8, column=1)

# 重定向print()函数的输出
print = redirect_print

root.mainloop()

