""""""
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
        return f"Hero(name={self.name}, role={self.role.name})"


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


# Запросы
class QuerySystem:
    def __init__(self, heroes, roles, items):
        self.heroes = heroes
        self.roles = roles
        self.items = items

    def heroes_by_role(self, role_name):
        """Поиск героев по роли"""
        return [hero for hero in self.heroes if hero.role.name.lower() == role_name.lower()]

    def heroes_by_item(self, item_name):
        """Поиск героев по предмету"""
        return [hero for hero in self.heroes if any(item.name.lower() == item_name.lower() for item in hero.items)]

    def heroes_by_synergy(self, synergy_name):
        """Поиск героев по синергии"""
        return [hero for hero in self.heroes if any(synergy.name.lower() == synergy_name.lower() for synergy in hero.synergies)]

    def items_by_role(self, role_name):
        """Поиск предметов по роли"""
        return [item for item in self.items if any(role.name.lower() == role_name.lower() for role in item.recommended_roles)]

    def roles_by_item(self, item_name):
        """Поиск ролей по предмету"""
        return [role for role in self.roles if any(item.name.lower() == item_name.lower() for item in role.required_items + role.recommended_items)]


# Запросы с выбором доступных опций
class UserInterface:
    def __init__(self, query_system):
        self.query_system = query_system

    def list_available_heroes(self):
        return [hero.name for hero in self.query_system.heroes]

    def list_available_roles(self):
        return [role.name for role in self.query_system.roles]

    def list_available_items(self):
        return [item.name for item in self.query_system.items]

    def heroes_by_role(self, role_name):
        return self.query_system.heroes_by_role(role_name)

    def heroes_by_item(self, item_name):
        return self.query_system.heroes_by_item(item_name)

    def heroes_by_synergy(self, synergy_name):
        return self.query_system.heroes_by_synergy(synergy_name)

    def items_by_role(self, role_name):
        return self.query_system.items_by_role(role_name)

    def roles_by_item(self, item_name):
        return self.query_system.roles_by_item(item_name)

    def user_interface(self):
        print("Добро пожаловать в систему запросов!\n")
        while True:
            print("\nЧто вы хотите найти?")
            print("1. Герои по роли")
            print("2. Герои по предмету")
            print("3. Герои по синергии")
            print("4. Предметы по роли")
            print("5. Роли по предмету")
            print("6. Выход")

            choice = input("Введите номер вашего выбора: ")

            if choice == "4":
                print("\nДоступные роли: ", ", ".join(self.list_available_roles()))
                role_name = input("Введите роль: ")
                items = self.items_by_role(role_name)
                if items:
                    print(f"\nПредметы для роли '{role_name}':")
                    for item in items:
                        print(item.name)

                    # Выбор предмета для вывода связей
                    item_name = input("\nВведите название предмета для отображения связей: ")
                    selected_item = next((item for item in items if item.name.lower() == item_name.lower()), None)
                    if selected_item:
                        # Находим всех героев, связанных с этим предметом
                        related_heroes = self.heroes_by_item(item_name)
                        print(f"\nГерои, связанные с предметом '{item_name}':")
                        for hero in related_heroes:
                            print(f"\nГерой: {hero.name}")
                            print(f"  Роль: {hero.role.name}")
                            print(f"  Подкласс: {hero.__class__.__name__}")
                            print(f"  Предметы: {[item.name for item in hero.items]}")
                            print(f"  Синергии: {[synergy.name for synergy in hero.synergies]}")
                    else:
                        print("Такого предмета не найдено.")
                else:
                    print("Предметы для этой роли не найдены.")

            elif choice == "6":
                print("Выход из программы.")
                break

            else:
                print("Неверный выбор, попробуйте снова.")


# Пример создания объектов
carry = Role("Carry")
offlaner = Role("Offlaner")
support = Role("Support")

axe = HeroStrength("Axe", health=700, mana=300, gender="Male", role=offlaner)
phantom_assassin = HeroAgility("Phantom Assassin", health=500, mana=200, gender="Female", role=carry)
crystal_maiden = HeroIntelligence("Crystal Maiden", health=450, mana=600, gender="Female", role=support)
warlock = HeroIntelligence("Warlock", health=500, mana=500, gender="Male", role=support)

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

# Создание системы запросов
query_system = QuerySystem(
    heroes=[axe, phantom_assassin, crystal_maiden, warlock],
    roles=[carry, offlaner, support],
    items=[belt_of_strength, blade_of_alacrity, mantle_of_intelligence, ogre_axe, parasma, slippers_of_agility, staff_of_wizardry]
)

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

# Запуск интерфейса
user_interface = UserInterface(query_system)
user_interface.user_interface()

