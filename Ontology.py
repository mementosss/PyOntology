class Hero:
    def __init__(self, name, health, mana, gender, role):
        self.name = name
        self.health = health
        self.mana = mana
        self.gender = gender
        self.role = role
        self.items = []
        self.synergies = []

    def add_item(self, item):
        self.items.append(item)

    def add_synergy(self, *heroes):
        self.synergies.extend(heroes)

    def __repr__(self):
        return f"Hero(name={self.name}, role={self.role})"


class HeroStrength(Hero):
    def __init__(self, name, health, mana, gender, role):
        super().__init__(name, health, mana, gender, role)


class HeroAgility(Hero):
    def __init__(self, name, health, mana, gender, role):
        super().__init__(name, health, mana, gender, role)


class HeroIntelligence(Hero):
    def __init__(self, name, health, mana, gender, role):
        super().__init__(name, health, mana, gender, role)


# Класс для ролей
class Role:
    def __init__(self, name):
        self.name = name
        self.required_items = []  # Обязательные предметы для этой роли
        self.recommended_items = []  # Рекомендуемые предметы для этой роли

    def add_required_item(self, *items):
        """Добавляет обязательные предметы для этой роли"""
        self.required_items.extend(items)

    def add_recommended_item(self, *items):
        """Добавляет рекомендуемые предметы для этой роли"""
        self.recommended_items.extend(items)

    def __repr__(self):
        return f"Role(name={self.name})"


# Класс для предметов
class Item:
    def __init__(self, name):
        self.name = name
        self.recommended_roles = []  # Список ролей, для которых предмет рекомендован

    def add_recommended_role(self, *roles):
        """Добавляет роли, для которых данный предмет рекомендован"""
        self.recommended_roles.extend(roles)

    def __repr__(self):
        return f"Item(name={self.name})"


# Пример ролей
carry = Role("Carry")
offlaner = Role("Offlaner")
support = Role("Support")

# Пример героев
axe = HeroStrength("Axe", health=700, mana=300, gender="Male", role=offlaner)
phantom_assassin = HeroAgility("Phantom Assassin", health=500, mana=200, gender="Female", role=carry)
crystal_maiden = HeroIntelligence("Crystal Maiden", health=450, mana=600, gender="Female", role=support)
warlock = HeroIntelligence("Warlock", health=500, mana=500, gender="Male", role=support)

# Пример предметов
belt_of_strength = Item("Belt of Strength")
blade_of_alacrity = Item("Blade of Alacrity")
mantle_of_intelligence = Item("Mantle of Intelligence")
ogre_axe = Item("Ogre Axe")
parasma = Item("Parasma")
slippers_of_agility = Item("Slippers of Agility")
staff_of_wizardry = Item("Staff of Wizardry")

# Привязка предметов к героям
axe.add_item(belt_of_strength)
axe.add_item(ogre_axe)
phantom_assassin.add_item(blade_of_alacrity)
phantom_assassin.add_item(slippers_of_agility)
phantom_assassin.add_item(parasma)
crystal_maiden.add_item(parasma)
crystal_maiden.add_item(mantle_of_intelligence)
crystal_maiden.add_item(staff_of_wizardry)
warlock.add_item(parasma)
warlock.add_item(mantle_of_intelligence)
warlock.add_item(staff_of_wizardry)

# Синергии
axe.add_synergy(crystal_maiden)
phantom_assassin.add_synergy(crystal_maiden, warlock)
crystal_maiden.add_synergy(phantom_assassin, axe)
warlock.add_synergy(phantom_assassin)

# Добавляем обязательные предметы для ролей
carry.add_required_item(parasma, slippers_of_agility)
offlaner.add_required_item(ogre_axe)
support.add_required_item(staff_of_wizardry)

# Добавляем рекомендованные предметы для ролей
carry.add_recommended_item(blade_of_alacrity)
offlaner.add_recommended_item(belt_of_strength)
support.add_recommended_item(mantle_of_intelligence)

# Добавляем рекомендованные роли для предметов
belt_of_strength.add_recommended_role(offlaner)
blade_of_alacrity.add_recommended_role(carry)
mantle_of_intelligence.add_recommended_role(support)
ogre_axe.add_recommended_role(offlaner)
parasma.add_recommended_role(support, carry)
slippers_of_agility.add_recommended_role(carry)
staff_of_wizardry.add_recommended_role(support)

# Вывод данных
print("\nRoles and Required/Recommended Items:")
for role in [carry, offlaner, support]:
    print(f"{role.name} (Required Items: {[item.name for item in role.required_items]}, Recommended Items: {[item.name for item in role.recommended_items]})")

print("\nItems and Recommended Roles:")
for item in [belt_of_strength, blade_of_alacrity, mantle_of_intelligence, ogre_axe, parasma, slippers_of_agility, staff_of_wizardry]:
    print(f"{item.name} (Recommended Roles: {[role.name for role in item.recommended_roles]})")

print("\nHero Details:")
for hero in [axe, phantom_assassin, crystal_maiden, warlock]:
    print(f"{hero.name} -> Subclass: [{hero.__class__.__name__}]")
    print(f"  Health={hero.health}, Mana={hero.mana}, Gender={hero.gender}, Role={hero.role.name}")
    print(f"  Items: {[item for item in hero.items]}")
    print(f"  Synergies: {[synergy.name for synergy in hero.synergies]}\n")
