from random import randint, choice
from bonuses import *

classes = {
    'Разбойник': (4, 'Кинжал', hidden_attack, dexterity_up, poison),
    'Воин': (5, 'Меч', rush, shield, power_up),
    'Варвар': (6, 'Дубина', rage, stone_skin, endurance_up),
}

weapons = {
    'Меч': (3, 'Рубящий'),
    'Дубина': (3, 'Дробящий'),
    'Кинжал': (2, 'Колющий'),
    'Топор': (4, 'Рубящий'),
    'Копье': (3, 'Колющий'),
    'Легендарный Меч': (10, 'Рубящий'),
}


class Hero:
    def __init__(self, name, selected_class):
        hp, weapon, bonus = classes[selected_class][:3]
        self.name = name
        self.power = randint(1, 3)
        self.dexterity = randint(1, 3)
        self.endurance = randint(1, 3)
        self.hp = hp + self.endurance
        self.max_hp = self.hp
        self.weapon = weapon
        self.weapon_damage = weapons[weapon][0]
        self.type_weapon = weapons[weapon][1]
        self.selected_classes = {selected_class: 1}
        bonus(attacker=self, type_bonus="one_time_bonus")
        self.bonuses = [bonus]
        self.lvl = 1
        self.type = 'hero'

    def add_class(self, cl):
        if cl in self.selected_classes:
            self.selected_classes[cl] += 1
        else:
            self.selected_classes[cl] = 1
        bonus = classes[cl][self.selected_classes[cl] + 1]
        bonus(attacker=self, type_bonus="one_time_bonus")
        self.bonuses.append(bonus)


class Enemy:
    enemies = {
        'Гоблин': (5, 2, 1, 1, 1, None, 'Кинжал'),
        'Скелет': (10, 2, 2, 2, 1, fear_crushing, 'Дубина'),
        'Слайм': (8, 1, 3, 1, 2, immune_chopping, 'Копье'),
        'Призрак': (6, 3, 1, 3, 1, hidden_attack, 'Меч'),
        'Голем': (10, 1, 3, 1, 3, stone_skin, 'Топор'),
        'Дракон': (20, 4, 3, 3, 3, breath_fire, 'Легендарный Меч'),
    }

    def __init__(self):
        enemy = choice(list(self.enemies.keys()))
        self.name = enemy
        hp, weapon_damage, power, dexterity, endurance, bonus, reward = self.enemies[enemy]
        self.max_hp = self.hp = hp
        self.power = power
        self.dexterity = dexterity
        self.endurance = endurance
        self.weapon_damage = weapon_damage
        self.bonuses = [bonus] if bonus else []
        self.reward = reward
        self.type = 'enemy'
