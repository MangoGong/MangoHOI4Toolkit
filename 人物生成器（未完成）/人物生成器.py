import tkinter as tk
from tkinter import ttk
from tkinter import Spinbox, filedialog

class CodeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Generator")

        self.data = {
            "portraits": {
                "army": {"large": "", "small": ""},
                "navy": {"large": "", "small": ""},
                "civilian": {"large": "", "small": ""}
            },
            "field_marshal": {"skill": 2, "attack_skill": 3, "defense_skill": 3, "planning_skill": 2, "logistics_skill": 3},
            "navy_leader": {"skill": 2, "attack_skill": 3, "defense_skill": 3, "maneuvering_skill": 3, "coordination_skill": 2},
            "corps_commander": {"skill": 2, "attack_skill": 2, "defense_skill": 2, "planning_skill": 2, "logistics_skill": 2},
            "advisor": {"cost": 100, "slot": "army_chief", "ledger": "army", "idea_token": "", "allowed": "", "traits": "", "ai_will_do": 0.5},
            "country_leader": {"ideology": "", "desc": "", "traits": "", "expire": "1965.1.1"}
        }

        self.selected_leaders = {
            "field_marshal": tk.BooleanVar(),
            "navy_leader": tk.BooleanVar(),
            "corps_commander": tk.BooleanVar(),
            "advisor": tk.BooleanVar(),
            "country_leader": tk.BooleanVar()
        }

        self.ideologies = {}  # 保存解析的母意识形态和子意识形态
        self.create_widgets()
        self.update_output()

    def create_widgets(self):
        name_frame = ttk.Frame(self.root)
        name_frame.pack(fill="x")
        ttk.Label(name_frame, text="Instance Name: ").pack(side="left")
        self.instance_name = tk.Entry(name_frame, width=20)
        self.instance_name.insert(0, "instances")
        self.instance_name.pack(side="left")

        # 导入意识形态按钮
        import_button = ttk.Button(self.root, text="Import Ideologies", command=self.import_ideologies)
        import_button.pack(pady=5)

        self.menu_frames = {}  # 用于存储各个菜单的Frame
        for leader_type in self.selected_leaders:
            parent_frame = ttk.Frame(self.root)
            parent_frame.pack(fill="x", pady=5)
            leader_check = ttk.Checkbutton(parent_frame, text=leader_type.replace('_', ' ').title(), variable=self.selected_leaders[leader_type], command=self.update_output)
            leader_check.pack(side="left", anchor="w")

            expand_button = ttk.Button(parent_frame, text="▼", command=lambda lt=leader_type: self.toggle_menu(lt))
            expand_button.pack(side="right")

            menu_frame = self.create_menu(leader_type)  # 生成对应的菜单
            self.menu_frames[leader_type] = menu_frame  # 保存菜单frame

        self.output_box = tk.Text(self.root, height=20, width=80)
        self.output_box.pack(fill="both", expand=True)

    def create_menu(self, leader_type):
        menu_frame = ttk.Frame(self.root)
        if leader_type in ["field_marshal", "navy_leader", "corps_commander"]:
            for label, key in [("Skill", "skill"), ("Attack Skill", "attack_skill"), ("Defense Skill", "defense_skill"),
                               ("Planning Skill", "planning_skill"), ("Logistics Skill", "logistics_skill")]:
                frame = ttk.Frame(menu_frame)
                frame.pack(fill="x", pady=2)
                ttk.Label(frame, text=label).pack(side="left")
                spinbox = tk.Spinbox(frame, from_=1, to=10, width=5, command=self.update_output)
                spinbox.pack(side="right")
                self.data[leader_type][key] = spinbox  # 将输入的spinbox与data关联

        elif leader_type == "advisor":
            frame = ttk.Frame(menu_frame)
            frame.pack(fill="x", pady=2)
            ttk.Label(frame, text="Cost").pack(side="left")
            cost_spinbox = tk.Spinbox(frame, from_=0, to=1000, width=5, command=self.update_output)
            cost_spinbox.pack(side="right")
            self.data[leader_type]["cost"] = cost_spinbox  # 将输入的spinbox与data关联

            frame = ttk.Frame(menu_frame)
            frame.pack(fill="x", pady=2)
            ttk.Label(frame, text="Slot").pack(side="left")
            slot_options = ["political_advisor", "theorist", "army_chief", "navy_chief", "air_chief", "high_command"]
            self.slot_combobox = ttk.Combobox(frame, values=slot_options, state="readonly")
            self.slot_combobox.pack(side="right")
            self.slot_combobox.bind("<<ComboboxSelected>>", self.update_ledger)

            frame = ttk.Frame(menu_frame)
            frame.pack(fill="x", pady=2)
            ttk.Label(frame, text="Ledger").pack(side="left")
            self.ledger_combobox = ttk.Combobox(frame, values=["Civilian", "Army", "Navy", "Air"], state="readonly")
            self.ledger_combobox.pack(side="right")
            self.data[leader_type]["ledger"] = self.ledger_combobox  # 将输入的combobox与data关联

            self.data[leader_type]["idea_token"] = self.instance_name

            frame = ttk.Frame(menu_frame)
            frame.pack(fill="x", pady=2)
            ttk.Label(frame, text="Allowed").pack(side="left")
            allowed_entry = tk.Entry(frame, width=10)
            allowed_entry.pack(side="right")
            self.data[leader_type]["allowed"] = allowed_entry  # 将输入的Entry与data关联

            frame = ttk.Frame(menu_frame)
            frame.pack(fill="x", pady=2)
            ttk.Label(frame, text="Traits").pack(side="left")
            traits_entry = tk.Entry(frame, width=10)
            traits_entry.pack(side="right")
            self.data[leader_type]["traits"] = traits_entry  # 将输入的Entry与data关联

            frame = ttk.Frame(menu_frame)
            frame.pack(fill="x", pady=2)
            ttk.Label(frame, text="AI Will Do (0-1)").pack(side="left")
            ai_spinbox = tk.Spinbox(frame, from_=0.0, to=1.0, increment=0.01, width=5, command=self.update_output)
            ai_spinbox.pack(side="right")
            self.data[leader_type]["ai_will_do"] = ai_spinbox  # 将输入的spinbox与data关联

        elif leader_type == "country_leader":
            frame = ttk.Frame(menu_frame)
            frame.pack(fill="x", pady=2)
            ttk.Label(frame, text="Ideology").pack(side="left")
            self.ideology_combobox = ttk.Combobox(frame, values=[], state="readonly")
            self.ideology_combobox.pack(side="right")
            self.data[leader_type]["ideology"] = self.ideology_combobox  # 将输入的combobox与data关联

            frame = ttk.Frame(menu_frame)
            frame.pack(fill="x", pady=2)
            ttk.Label(frame, text="Expire").pack(side="left")
            expire_entry = tk.Entry(frame, width=10)
            expire_entry.insert(0, self.data["country_leader"]["expire"])
            expire_entry.pack(side="right")
            self.data[leader_type]["expire"] = expire_entry  # 将输入的Entry与data关联

        return menu_frame  # 返回生成的菜单frame

    def toggle_menu(self, leader_type):
        menu_frame = self.menu_frames[leader_type]
        if menu_frame.winfo_ismapped():
            menu_frame.pack_forget()
        else:
            menu_frame.pack(fill="x")

    def update_ledger(self, event=None):
        slot = self.slot_combobox.get()
        if slot == "political_advisor":
            self.ledger_combobox.config(values=["Civilian"])
        elif slot == "theorist":
            self.ledger_combobox.config(values=["Army", "Air", "Navy"])
        elif slot == "army_chief":
            self.ledger_combobox.config(values=["Army"])
        elif slot == "navy_chief":
            self.ledger_combobox.config(values=["Navy"])
        elif slot == "air_chief":
            self.ledger_combobox.config(values=["Air"])
        elif slot == "high_command":
            self.ledger_combobox.config(values=["Army", "Air", "Navy"])

    def import_ideologies(self):
        filepath = filedialog.askopenfilename(title="Select Ideology File", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if filepath:
            with open(filepath, "r") as file:
                self.parse_ideologies(file)

    def parse_ideologies(self, file):
        current_mother = None
        for line in file:
            stripped_line = line.strip()
            if stripped_line.endswith('= {'):
                if 'types' not in stripped_line:
                    current_mother = stripped_line.split('=')[0].strip()
                    self.ideologies[current_mother] = []
                else:
                    current_mother = None
            elif current_mother:
                child_ideology = stripped_line.split('=')[0].strip()
                self.ideologies[current_mother].append(child_ideology)

        self.update_ideology_combobox()

    def update_ideology_combobox(self):
        values = [f"{mother}:{child}" for mother, children in self.ideologies.items() for child in children]
        self.ideology_combobox.config(values=values)

    def update_output(self):
        # 处理互斥逻辑
        if self.selected_leaders["corps_commander"].get():
            self.selected_leaders["field_marshal"].set(False)
        if self.selected_leaders["field_marshal"].get():
            self.selected_leaders["corps_commander"].set(False)

        # 生成代码
        output = f'characters = {{\n\tname = "{self.instance_name.get()}"\n\tportraits = {{\n'
        for unit, portrait in self.data["portraits"].items():
            output += f"\t\t{unit} = {{\n\t\t\tlarge = {portrait['large']}\n\t\t\tsmall = {portrait['small']}\n\t\t}}\n"
        output += "\t}\n"

        for leader_type, selected in self.selected_leaders.items():
            if selected.get():
                output += f"\t{leader_type} = {{\n"
                for key, value in self.data[leader_type].items():
                    # 读取用户输入
                    if isinstance(value, tk.Entry):
                        output += f"\t\t{key} = {value.get()}\n"
                    elif isinstance(value, tk.Spinbox):
                        output += f"\t\t{key} = {value.get()}\n"
                    elif isinstance(value, ttk.Combobox):
                        output += f"\t\t{key} = {value.get()}\n"
                output += "\t}\n"

        output += "}\n"

        # 更新输出框
        self.output_box.delete(1.0, tk.END)
        self.output_box.insert(tk.END, output)

        # 动态调整输出框的高度
        lines = output.count('\n')
        self.output_box.config(height=lines + 5)

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeGenerator(root)
    root.mainloop()
