def hidden_attack(damage=None, attacker=None, defender=None, type_bonus=None, logger=None, level=None, *args, **kwargs):
    '"Скрытая атака": +1 к урону если ловкость персонажа выше ловкости цели'
    if type_bonus == 'damage_bonus':
        if attacker.dexterity > defender.dexterity:
            logger.log('Бонус от "Скрытой атаки": ⚔️+1 ед.', level)
            damage += 1
    return damage


def dexterity_up(damage=None, attacker=None, type_bonus=None, logger=None, level=None, *args, **kwargs):
    'Ваша ловкость увеличивается на 1 ед.'
    if type_bonus == 'one_time_bonus':
        attacker.dexterity += 1
    return damage


def poison(damage=None, turn_counter=None, type_bonus=None, logger=None, level=None, *args, **kwargs):
    '"Яд": наносит дополнительные +1 урона на втором ходу, +2 на третьем и т.д.'
    if type_bonus == 'damage_bonus':
        if turn_counter > 1:
            logger.log(f'Бонус от "Яд": ⚔️+{turn_counter - 1} ед. на {turn_counter} ходу', level)
            damage += turn_counter - 1
    return damage


def rush(damage=None, attacker=None, turn_counter=None, type_bonus=None, logger=None, level=None, *args, **kwargs):
    '"Порыв к действию": в первый ход наносит двойной урон оружием'
    if type_bonus == 'damage_bonus':
        if turn_counter == 1:
            logger.log(f'Бонус от "Порыв к действию": x2 урона от оружие: ⚔️+{attacker.weapon_damage} ед.', level)
            damage += attacker.weapon_damage
    return damage


def shield(damage=None, attacker=None, defender=None, type_bonus=None, logger=None, level=None, *args, **kwargs):
    '"Щит": -3 к получаемому урону если сила персонажа выше силы атакующего'
    if type_bonus == 'protection_bonus':
        if attacker.power < defender.power:
            logger.log(f'Бонус у {defender.name} от "Щит": заблокировано ⛊3 ед.', level)
            damage -= 3
    return damage


def power_up(damage=None, attacker=None, type_bonus=None, logger=None, level=None, *args, **kwargs):
    'Ваша сила увеличивается на 1 ед.'
    if type_bonus == 'one_time_bonus':
        attacker.power += 1
    return damage


def rage(damage=None, turn_counter=None, type_bonus=None, logger=None, level=None, *args, **kwargs):
    '"Ярость": +2 к урону в первые 3 хода, потом -1 к урону'
    if type_bonus == 'damage_bonus':
        delta = 2 if turn_counter <= 3 else -1
        logger.log(f'Бонус от "Ярость": ⚔️+{delta} ед. урона на {turn_counter} ходу', level)
        damage += delta
    return damage


def stone_skin(damage=None, defender=None, type_bonus=None, logger=None, level=None, *args, **kwargs):
    '"Каменная кожа": Получаемый урон снижается на значение выносливости'
    if type_bonus == 'protection_bonus':
        delta = defender.endurance
        logger.log(f'Бонус у {defender.name} от "Каменная кожа": заблокировано ⛊{delta} ед. урона', level)
        damage -= delta
    return damage


def endurance_up(damage=None, attacker=None, type_bonus=None, logger=None, level=None, *args, **kwargs):
    'Ваша выносливость увеличивается на 1 ед.'
    if type_bonus == 'one_time_bonus':
        attacker.endurance += 1
    return damage


def fear_crushing(damage=None, attacker=None, defender=None, type_bonus=None, logger=None, level=None, *args, **kwargs):
    'Получает вдвое больше урона, если его бьют дробящим оружием'
    if type_bonus == 'protection_bonus':
        if attacker.type_weapon == 'Дробящий':
            logger.log(f'{defender.name} боится дробящего оружия, урон увеличивается вдвое!!! ⚔️x2', level)
            damage *= 2
    return damage


def immune_chopping(damage=None, attacker=None, defender=None, type_bonus=None, logger=None, level=None,
                    *args, **kwargs):
    'Рубящее оружие не наносит ему урона(но урон от силы и прочих особенностей работает)'
    if type_bonus == 'protection_bonus':
        if attacker.type_weapon == 'Рубящий':
            logger.log(f'Иммунитет на рубящее оружие у {defender.name} блокирует 🛡{attacker.weapon_damage} ед. урона',
                       level)
            damage -= attacker.weapon_damage
    return damage


def breath_fire(damage=None, turn_counter=None, type_bonus=None, logger=None, level=None, *args, **kwargs):
    'Каждый 3-й ход дышит огнём, нанося дополнительно 3 урона'
    if type_bonus == 'damage_bonus':
        if turn_counter % 3 == 0:
            logger.log(f'В груди зарождается первородно пламя\nРёбра чёрным узором проступают под кожей...'
                       f'\nИз пасти вырывается жидкий огонь,\nнанося дополнительно ⚔️+3 ед. урона', level)
            damage += 3
    return damage
