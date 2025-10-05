import tkinter as tk
from tkinter import ttk, messagebox

# ---------- Ontology Model ----------

class Instance:
    def __init__(self, name):
        self.name = name


class Role(Instance):
    def __init__(self, name):
        super().__init__(name)
        self.plays = []          # Heroes
        self.mandatory_items = []


class Item(Instance):
    def __init__(self, name):
        super().__init__(name)
        self.recommended = []          # Heroes
        self.recommended_for_role = [] # Roles


class Hero(Instance):
    def __init__(self, name, health, mana, gender):
        super().__init__(name)
        self.health = health
        self.mana = mana
        self.gender = gender
        self.owns = []            # Items
        self.role = None          # Role
        self.effective_with = []  # Heroes


class HeroIntelligence(Hero):
    pass


class HeroAgility(Hero):
    pass


class HeroStrength(Hero):
    pass


# ---------- Create Objects ----------

# Roles
role_support = Role("Support")
role_carry = Role("Carry")
role_tank = Role("Tank")

# Items
item_staff = Item("Staff of Wizardry")
item_blade = Item("Blade of Alacrity")
item_belt = Item("Belt of Strength")

# Heroes
hero_cm = HeroIntelligence("Crystal Maiden", 500, 400, "Female")
hero_pa = HeroAgility("Phantom Assasin", 700, 300, "Female")
hero_axe = HeroStrength("Axe", 1000, 200, "Male")

# Relationships
hero_cm.role = role_support
hero_pa.role = role_carry
hero_axe.role = role_tank

hero_cm.owns = [item_staff]
hero_pa.owns = [item_blade]
hero_axe.owns = [item_belt]

hero_cm.effective_with = [hero_pa, hero_axe]
hero_pa.effective_with = [hero_cm]
hero_axe.effective_with = [hero_cm]

item_staff.recommended = [hero_cm]
item_blade.recommended = [hero_pa]
item_belt.recommended = [hero_axe]

item_staff.recommended_for_role = [role_support]
item_blade.recommended_for_role = [role_carry]
item_belt.recommended_for_role = [role_tank]

role_support.plays = [hero_cm]
role_carry.plays = [hero_pa]
role_tank.plays = [hero_axe]

role_support.mandatory_items = [item_staff]
role_carry.mandatory_items = [item_blade]
role_tank.mandatory_items = [item_belt]

# ---------- Data Structure for GUI ----------

classes = {
    "Hero": {
        "slots": ["owns", "health", "mana", "gender", "role", "effective_with", "name"],
        "instances": [hero_cm, hero_pa, hero_axe]
    },
    "Item": {
        "slots": ["name", "recommended", "recommended_for_role"],
        "instances": [item_staff, item_blade, item_belt]
    },
    "Role": {
        "slots": ["plays", "name", "mandatory_items"],
        "instances": [role_support, role_carry, role_tank]
    }
}


# ---------- GUI Implementation ----------

root = tk.Tk()
root.title("Ontology Query Interface")
root.geometry("700x500")
root.configure(bg="#1e1e1e")

style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#1e1e1e", foreground="white", font=("Segoe UI", 11))
style.configure("TButton", font=("Segoe UI", 11, "bold"))
style.configure("TCombobox", font=("Segoe UI", 11))

# --- Layout blocks ---
frm = ttk.Frame(root, padding=20)
frm.pack(fill="both", expand=True)

# Class dropdown
ttk.Label(frm, text="Class:").grid(row=0, column=0, sticky="w")
class_cb = ttk.Combobox(frm, values=list(classes.keys()), state="readonly")
class_cb.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

# Slot dropdown
ttk.Label(frm, text="Slot:").grid(row=1, column=0, sticky="w")
slot_cb = ttk.Combobox(frm, state="readonly")
slot_cb.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

# Condition dropdown
ttk.Label(frm, text="Condition:").grid(row=2, column=0, sticky="w")
condition_cb = ttk.Combobox(frm, values=["contains", "does not contain"], state="readonly")
condition_cb.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

# String entry with autocompletion
ttk.Label(frm, text="String:").grid(row=3, column=0, sticky="w")
string_cb = ttk.Combobox(frm)
string_cb.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

# Search button
def perform_search():
    cls_name = class_cb.get()
    slot = slot_cb.get()
    condition = condition_cb.get()
    query_str = string_cb.get().lower()

    if not (cls_name and slot and condition and query_str):
        messagebox.showwarning("Missing info", "Please fill in all fields before searching.")
        return

    instances = classes[cls_name]["instances"]
    results = []

    for inst in instances:
        value = getattr(inst, slot, None)

        if isinstance(value, list):
            names = [v.name.lower() if isinstance(v, Instance) else str(v).lower() for v in value]
            match = query_str in names
        else:
            val_str = value.name.lower() if isinstance(value, Instance) else str(value).lower()
            match = query_str in val_str

        if (condition == "contains" and match) or (condition == "does not contain" and not match):
            results.append(inst)

    result_text.delete(1.0, tk.END)
    if results:
        for r in results:
            result_text.insert(tk.END, f"{r.name} ({cls_name})\n")
            for s in classes[cls_name]["slots"]:
                val = getattr(r, s, None)
                if val:
                    if isinstance(val, list):
                        val_str = [v.name if isinstance(v, Instance) else str(v) for v in val]
                    elif isinstance(val, Instance):
                        val_str = val.name
                    else:
                        val_str = val
                    result_text.insert(tk.END, f"  {s}: {val_str}\n")
            result_text.insert(tk.END, "-"*60 + "\n")
    else:
        result_text.insert(tk.END, "No results found.\n")


find_btn = ttk.Button(frm, text="Find", command=perform_search)
find_btn.grid(row=4, column=1, sticky="ew", pady=10)

# Search results area
ttk.Label(frm, text="Search Results:").grid(row=5, column=0, sticky="w", pady=(10,0))
result_text = tk.Text(frm, height=12, wrap="word", bg="#252526", fg="white", insertbackground="white")
result_text.grid(row=6, column=0, columnspan=2, sticky="nsew", pady=5)

frm.columnconfigure(1, weight=1)
frm.rowconfigure(6, weight=1)

# --- Autocomplete logic ---
def update_slots(event):
    cls_name = class_cb.get()
    if cls_name:
        slot_cb["values"] = classes[cls_name]["slots"]
        slot_cb.set("")
        string_cb.set("")
        string_cb["values"] = []

def update_string_values(event):
    cls_name = class_cb.get()
    slot_name = slot_cb.get()
    if not cls_name or not slot_name:
        return
    instances = classes[cls_name]["instances"]
    values = set()
    for inst in instances:
        val = getattr(inst, slot_name, None)
        if isinstance(val, list):
            for v in val:
                if isinstance(v, Instance):
                    values.add(v.name)
                else:
                    values.add(str(v))
        elif isinstance(val, Instance):
            values.add(val.name)
        elif val is not None:
            values.add(str(val))
    string_cb["values"] = sorted(values)

class_cb.bind("<<ComboboxSelected>>", update_slots)
slot_cb.bind("<<ComboboxSelected>>", update_string_values)

root.mainloop()
