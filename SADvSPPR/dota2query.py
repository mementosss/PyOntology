from abc import ABC, abstractmethod


class Hero(ABC):
    @abstractmethod
    def __init__(self, name, health, role, real_name, mana, gender):
        self.name = name              # String
        self.health = health          # Integer
        self.role = role              # Instance (Role)
        self.real_name = real_name    # String
        self.mana = mana              # Integer
        self.gender = gender          # String
        self.owns = []                # Instance, multiple
        self.effective_with = []      # Instance, multiple

    def add_references(self, owns=None, effective_with=None):
        if owns:
            self.owns.extend(owns)
        if effective_with:
            self.effective_with.extend(effective_with)

# -------------------------
# Concrete классы Герой
# -------------------------
class IntelligenceHero(Hero):
    def __init__(self, name, health, role, real_name, mana, gender):
        super().__init__(name, health, role, real_name, mana, gender)

class AgilityHero(Hero):
    def __init__(self, name, health, role, real_name, mana, gender):
        super().__init__(name, health, role, real_name, mana, gender)

class StrengthHero(Hero):
    def __init__(self, name, health, role, real_name, mana, gender):
        super().__init__(name, health, role, real_name, mana, gender)

# -------------------------
# Concrete класс Предмет
# -------------------------
class Item:
    def __init__(self, name):
        self.name = name             # String
        self.recommended_for = []    # Instance, multiple
        self.recommended_role = []   # Instance, multiple

    def add_references(self, recommended_for=None, recommended_role=None):
        if recommended_for:
            self.recommended_for.extend(recommended_for)
        if recommended_role:
            self.recommended_role.extend(recommended_role)

# -------------------------
# Concrete класс Роль
# -------------------------
class Role:
    def __init__(self, name):
        self.name = name             # String
        self.plays = []              # Instance, multiple
        self.mandatory_item = []     # Instance, multiple

    def add_references(self, plays=None, mandatory_item=None):
        if plays:
            self.plays.extend(plays)
        if mandatory_item:
            self.mandatory_item.extend(mandatory_item)

# -------------------------
# Вспомогательные функции
# -------------------------
def obj_output(obj):
    if isinstance(obj, list):
        return [(x.name, x.__class__.__name__) for x in obj]
    else:
        return obj.name, obj.__class__.__name__

def references_output(obj):
    output = f'{obj.name} references:\n'

    # ----------------- Герой -----------------
    if isinstance(obj, Hero):
        output += f'ROLE: {obj_output(obj.role)}\n'

        # Рекомендованные предметы для героя
        recommended_items = [item for item in instances if isinstance(item, Item) and obj in item.recommended_for]
        if recommended_items:
            output += f'RECOMMENDED ITEMS: {obj_output(recommended_items)}\n'

        # Эффективнее вместе
        if obj.effective_with:
            output += f'EFFECTIVE_WITH: {obj_output(obj.effective_with)}\n'

    # ----------------- Предмет -----------------
    elif isinstance(obj, Item):
        # Герои, у которых предмет есть в owns
        owned_by = [hero for hero in instances if isinstance(hero, Hero) and obj in hero.owns]
        output += f'OWNED_BY: {obj_output(owned_by) if owned_by else "None"}\n'

        # Роли, для которых предмет обязательный
        mandatory_roles = [role for role in instances if isinstance(role, Role) and obj in role.mandatory_item]
        output += f'MANDATORY_FOR_ROLE: {obj_output(mandatory_roles) if mandatory_roles else "None"}\n'

    # ----------------- Роль -----------------
    elif isinstance(obj, Role):
        # Герои, которые играют роль
        if obj.plays:
            output += f'PLAYS: {obj_output(obj.plays)}\n'

        # Находим все предметы, у которых эта роль есть в recommended_role
        recommended_items = [item for item in instances if isinstance(item, Item) and obj in item.recommended_role]
        if recommended_items:
            output += f'RECOMMENDED ITEMS: {obj_output(recommended_items)}\n'

    # ----------------- Остальные объекты -----------------
    else:
        for slot, references in obj.__dict__.items():
            if isinstance(references, list) and references and hasattr(references[0], 'name'):
                output += f'{slot.upper()}: {obj_output(references)}\n'
            elif hasattr(references, 'name'):
                output += f'{slot.upper()}: {obj_output(references)}\n'

    return output


def query(objects, cls, slot, flag, value):
    filtered_instances = [obj for obj in objects if isinstance(obj, cls)]
    search_result = []
    for obj in filtered_instances:
        refs = getattr(obj, slot, [])
        if isinstance(refs, list):
            names = [x.name for x in refs]
            if value in names:
                search_result.append(obj)
        else:
            if getattr(obj, slot, None) and getattr(obj, slot).name == value:
                search_result.append(obj)
    if flag:
        return search_result
    else:
        return [obj for obj in filtered_instances if obj not in search_result]

# -------------------------
# Создание объектов
# -------------------------

# Роли
role_carry = Role("Carry")
role_offlaner = Role("Offlaner")
role_support = Role("Support")

# Предметы
belt_of_strength = Item("Belt of Strength")
blade_of_alacrity = Item("Blade of Alacrity")
mantle_of_intelligence = Item("Mantle of Intelligence")
ogre_axe = Item("Ogre Axe")
parasma = Item("Parasma")
slippers_of_agility = Item("Slippers of Agility")
staff_of_wizardry = Item("Staff of Wizardry")

# Герои
crystal_maiden = IntelligenceHero(
    name="Crystal Maiden", health=800, role=role_support,
    real_name="Crystal Maiden", mana=800, gender="female"
)
crystal_maiden.add_references(
    owns=[mantle_of_intelligence, staff_of_wizardry]
)

warlock = IntelligenceHero(
    name="Warlock", health=900, role=role_support,
    real_name="Warlock", mana=300, gender="male"
)
warlock.add_references(
    owns=[parasma]
)

phantom_assasin = AgilityHero(
    name="Phantom Assasin", health=700, role=role_carry,
    real_name="Phantom Assasin", mana=400, gender="female"
)
phantom_assasin.add_references(
    owns=[slippers_of_agility, blade_of_alacrity]
)

axe = StrengthHero(
    name="Axe", health=900, role=role_offlaner,
    real_name="Axe", mana=300, gender="male"
)
axe.add_references(
    owns=[ogre_axe, belt_of_strength]
)

# Связи effective_with
crystal_maiden.effective_with = [phantom_assasin, axe]
warlock.effective_with = [phantom_assasin]
phantom_assasin.effective_with = [crystal_maiden, warlock]
axe.effective_with = [crystal_maiden]

# Связи recommended_for и recommended_role для предметов
belt_of_strength.add_references(recommended_for=[axe], recommended_role=[role_offlaner])
blade_of_alacrity.add_references(recommended_for=[phantom_assasin], recommended_role=[role_carry])
mantle_of_intelligence.add_references(recommended_for=[crystal_maiden, warlock], recommended_role=[role_support])
ogre_axe.add_references(recommended_for=[axe], recommended_role=[role_offlaner])
parasma.add_references(recommended_for=[crystal_maiden, warlock, phantom_assasin], recommended_role=[role_support, role_carry])
slippers_of_agility.add_references(recommended_for=[phantom_assasin], recommended_role=[role_carry])
staff_of_wizardry.add_references(recommended_for=[warlock, crystal_maiden], recommended_role=[role_support])

# Связи plays и mandatory_item для ролей
role_carry.plays = [phantom_assasin]
role_carry.mandatory_item = [parasma, slippers_of_agility]

role_offlaner.plays = [axe]
role_offlaner.mandatory_item = [ogre_axe]

role_support.plays = [crystal_maiden, warlock]
role_support.mandatory_item = [staff_of_wizardry]

# Список всех объектов
instances = [
    crystal_maiden, warlock, phantom_assasin, axe,
    belt_of_strength, blade_of_alacrity, mantle_of_intelligence,
    ogre_axe, parasma, slippers_of_agility, staff_of_wizardry,
    role_carry, role_offlaner, role_support
]

# ----------------- Функции для запросов -----------------

def query_1():
    print("=== Запрос 1: Герои роли Support и связанные объекты ===")
    heroes_support = query(instances, Hero, "role", True, "Support")
    print('Search Results: ')
    print(obj_output(heroes_support))
    print('')
    print(references_output(crystal_maiden))
    print(references_output(parasma))


def query_2():
    print("=== Запрос 2: Роль героя Warlock и связанные объекты ===")
    roles_of_warlock = query(instances, Role, "plays", True, "Warlock")
    print('Search Results: ')
    print(obj_output(roles_of_warlock))
    print('')
    print(references_output(role_support))
    print(references_output(staff_of_wizardry))

def query_3():
    print("=== Запрос 3: Предметы рекомендованные Axe и связанные объекты ===")
    axe_items = query(instances, Item, "recommended_for", True, "Axe")
    print('Search Results: ')
    print(obj_output(axe_items))
    print('')
    print(references_output(ogre_axe))
    print(references_output(axe))

while True:
    print("\nВыберите номер запроса:")
    print("1 - Запрос 1")
    print("2 - Запрос 2")
    print("3 - Запрос 3")
    print("0 - Выход")
    choice = input("Введите номер запроса: ").strip()

    if choice == "1":
        query_1()
    elif choice == "2":
        query_2()
    elif choice == "3":
        query_3()
    elif choice == "0":
        print("Выход...")
        break
    else:
        print("Неверный ввод. Попробуйте снова.")
