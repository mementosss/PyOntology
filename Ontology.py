# Классы для разных типов героев
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

    def __repr__(self):
        return f"Role(name={self.name})"


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
belt_of_strength = "Belt of Strength"
blade_of_alacrity = "Blade of Alacrity"
mantle_of_intelligence = "Mantle of Intelligence"
ogre_axe = "Ogre Axe"
parasma = "Parasma"
slippers_of_agility = "Slippers of Agility"
staff_of_wizardry = "Staff of Wizardry"

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

# Вывод данных
print("\nRoles:", carry, offlaner, support)
print("Heroes:", axe, phantom_assassin, crystal_maiden, warlock)
print("Items:", belt_of_strength, blade_of_alacrity, mantle_of_intelligence, ogre_axe, parasma, slippers_of_agility, staff_of_wizardry)

print("\nHero Details:")
for hero in [axe, phantom_assassin, crystal_maiden, warlock]:
    # Выводим информацию о подклассе
    print(f"{hero.name} -> Subclass: [{hero.__class__.__name__}]")
    print(f"  Health={hero.health}, Mana={hero.mana}, Gender={hero.gender}, Role={hero.role.name}")
    print(f"  Items: {[item for item in hero.items]}")
    print(f"  Synergies: {[synergy.name for synergy in hero.synergies]}\n")
