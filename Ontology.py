from abc import ABC, abstractmethod

# Абстрактный базовый класс для всех сущностей
class Entity(ABC):
    def __init__(self, name):
        self.name = name
        self.references = {}

    def add_references(self, **kwargs):
        for key, value in kwargs.items():
            self.references[key] = value

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name})"


# Классы для героев
class Hero(Entity):
    def __init__(self, name, health, mana, gender, role):
        super().__init__(name)
        self.health = health
        self.mana = mana
        self.gender = gender
        self.role = role


class HeroStrength(Hero):
    pass


class HeroAgility(Hero):
    pass


class HeroIntelligence(Hero):
    pass


# Класс для ролей
class Role(Entity):
    def __init__(self, name, required_item=None):
        super().__init__(name)
        self.required_item = required_item


# Класс для предметов
class Item(Entity):
    def __init__(self, name, recommended_role=None, recommended_hero=None):
        super().__init__(name)
        self.recommended_role = recommended_role
        self.recommended_hero = recommended_hero


# Функция для выполнения запросов
def query(entities, cls, slot, flag, value):
    filtered_entities = [entity for entity in entities if isinstance(entity, cls)]

    if hasattr(filtered_entities[0], slot):
        return [entity for entity in filtered_entities if getattr(entity, slot) == value]

    search_result = []
    for entity in filtered_entities:
        names = [ref.name for ref in entity.references.get(slot, [])]
        if value in names:
            search_result.append(entity)

    return search_result if flag else [entity for entity in filtered_entities if entity not in search_result]


# Вспомогательные функции для вывода

def obj_output(obj):
    if isinstance(obj, list):
        return [(x.name, x.__class__.__name__) for x in obj]
    else:
        return obj.name, obj.__class__.__name__


def references_output(obj):
    output = f"{obj.name} references:\n"
    for slot, references in obj.references.items():
        if isinstance(references, list):
            names = [obj_output(ref) for ref in references]
            output += f"{slot.upper()}: {names}\n"
        else:
            output += f"{slot.upper()}: {obj_output(references)}\n"
    return output


def get_reference(obj, slot, index=0):
    if isinstance(obj.references[slot], list):
        return obj.references[slot][index]
    return obj.references[slot]


# Создание объектов
carry = Role("Carry")
offlaner = Role("Offlaner")
support = Role("Support")

axe = HeroStrength("Axe", health=700, mana=300, gender="Male", role=offlaner)
phantom_assassin = HeroAgility("Phantom Assassin", health=500, mana=200, gender="Female", role=carry)
crystal_maiden = HeroIntelligence("Crystal Maiden", health=450, mana=600, gender="Female", role=support)
warlock = HeroIntelligence("Warlock", health=500, mana=500, gender="Male", role=support)

belt_of_strength = Item("Belt of Strength", recommended_role=offlaner)
blade_of_alacrity = Item("Blade of Alacrity", recommended_role=carry)
mantle_of_intelligence = Item("Mantle of Intelligence", recommended_role=support)
ogre_axe = Item("Ogre Axe", recommended_role=offlaner)
parasma = Item("Parasma", recommended_role=[support, carry])
slippers_of_agility = Item("Slippers of Agility", recommended_role=carry)
staff_of_wizardry = Item("Staff of Wizardry", recommended_role=support)

# Добавление связей
axe.add_references(items=[belt_of_strength, ogre_axe], synergies=[crystal_maiden], plays_role=offlaner)
phantom_assassin.add_references(items=[blade_of_alacrity, slippers_of_agility, parasma], synergies=[crystal_maiden, warlock], plays_role=carry)
crystal_maiden.add_references(items=[parasma, mantle_of_intelligence, staff_of_wizardry], synergies=[phantom_assassin, axe], plays_role=support)
warlock.add_references(items=[parasma, mantle_of_intelligence, staff_of_wizardry], synergies=[phantom_assassin], plays_role=support)

carry.add_references(required_items=[parasma, slippers_of_agility], recommended_items=[blade_of_alacrity])
offlaner.add_references(required_items=[ogre_axe], recommended_items=[belt_of_strength])
support.add_references(required_items=[staff_of_wizardry], recommended_items=[mantle_of_intelligence])

belt_of_strength.add_references(recommended_roles=offlaner)
blade_of_alacrity.add_references(recommended_roles=carry)
mantle_of_intelligence.add_references(recommended_roles=support)
ogre_axe.add_references(recommended_roles=offlaner)
parasma.add_references(recommended_roles=[support, carry])
slippers_of_agility.add_references(recommended_roles=carry)
staff_of_wizardry.add_references(recommended_roles=support)

# Список всех объектов
instances = [
    carry, offlaner, support,
    axe, phantom_assassin, crystal_maiden, warlock,
    belt_of_strength, blade_of_alacrity, mantle_of_intelligence, ogre_axe, parasma, slippers_of_agility, staff_of_wizardry
]

# Пример вывода связей один-к-одному
print("\n--- Один к одному ---")
print(references_output(belt_of_strength))
print(references_output(blade_of_alacrity))

# Пример вывода связей один-ко-многим
print("\n--- Один ко многим ---")
print(references_output(parasma))
print(references_output(phantom_assassin))

# Пример вывода с ролями и обязательными предметами
print("\n--- Роли и обязательные предметы ---")
print(f"{carry.name}: обязательный предмет: {carry.references.get('required_items')}")
print(f"{offlaner.name}: обязательный предмет: {offlaner.references.get('required_items')}")
print(f"{support.name}: обязательный предмет: {support.references.get('required_items')}")

# Пример запроса
query_heroes = query(instances, Role, 'required_items', True, 'Parasma')
print("\n--- Запрос ролей с required_items 'Parasma' ---")
print(obj_output(query_heroes))
print(references_output(query_heroes[0]))

ref_items = get_reference(query_heroes[0], 'recommended_items')
print("\n--- Рекомендуемый предмет ---")
print(obj_output(ref_items))
print(references_output(ref_items))

# Пример вывода ссылок на роли для героев
print("\n--- Герои и их роли ---")
print(references_output(axe))
print(references_output(phantom_assassin))
print(references_output(crystal_maiden))
print(references_output(warlock))
