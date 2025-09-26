import re
from tkinter import *
from tkinter import scrolledtext
from atmosphere import *
from characters import *
from pygame import mixer

font = "Segoe Print"
font_logger = "Cambria"
outline = 'bold'


def create_label(root, text='', x=0, y=0, font_size=14, fg='gold', bg='black', outline=outline, *args, **kwargs):
    text_lbl = Label(root, text=text, font=(font, font_size, outline), fg=fg, bg=bg, *args, **kwargs)
    text_lbl.place(x=x, y=y)
    objects_in_window.append(text_lbl)
    return text_lbl


def create_button(root, text='', x=0, y=0, font_size=14, fg='black', bg='gold', outline=outline,
                  activebackground="#999900", command=None, *args, **kwargs):
    btn = Button(root, text=text, bg=bg, fg=fg, font=(font, font_size, outline), borderwidth=10,
                 activebackground=activebackground, command=command, *args, **kwargs)
    btn.place(x=x, y=y)
    objects_in_window.append(btn)
    return btn


def create_image(path=None, x=0, y=0, scale=1):
    image = PhotoImage(file=path)
    image = image.subsample(scale, scale)
    img_lbl = Label(root)
    img_lbl.image = image
    img_lbl['image'] = img_lbl.image
    img_lbl.place(x=x, y=y)
    objects_in_window.append(img_lbl)


def create_entry(root, font_size=14, fg='gold', outline='bold', x=0, y=0, height=None, width=None):
    entry = Entry(root, font=(font, font_size, outline), fg=fg, justify='center')
    entry.place(x=x, y=y, height=height, width=width)
    objects_in_window.append(entry)
    return entry


def create_logger(x=0, y=0, width=None, height=None):
    class Logger:
        def __init__(self, frame):
            self.frame = frame
            self.custom_font = (font_logger, 13)
            self.text_widget = scrolledtext.ScrolledText(frame, font=self.custom_font, width=width, height=height)
            self.text_widget.pack(fill='both', expand=True)

            self.text_widget.tag_configure("enemy", foreground="red", justify='right')
            self.text_widget.tag_configure("hero", foreground="green", justify='left')
            self.text_widget.tag_configure("neutral", foreground="black", justify='center', font=(font_logger, 16))
            self.text_widget.config(state='disabled')

        def log(self, message, level="INFO"):
            log_message = f"{message}\n"
            self.text_widget.config(state='normal')
            self.text_widget.insert(END, log_message, level)
            self.text_widget.see(END)
            self.text_widget.config(state='disabled')
            self.text_widget.update()

        def destroy(self):
            self.text_widget.destroy()
            self.frame.destroy()

    frame = Frame(root, bg='gold')
    frame.place(x=x, y=y, width=width * 8.5, height=height * 16)

    logger_instance = Logger(frame)
    objects_in_window.append(logger_instance)
    return logger_instance


def clear_window():
    for obj in objects_in_window:
        obj.destroy()


def name_validation(entry_name, selected_class):
    name = entry_name.get()
    clear_window()
    if re.search(r'[^a-zA-Zа-яёА-ЯЁ]', name):
        mistake_text = ('Имя героя содержит запрещённые символы!\n''Разрешено использование только кириллицы'
                        ' и латиницы.')
    elif not (2 <= len(name) <= 12):
        mistake_text = 'Имя героя должно быть не менее 2 символов и не более 12!'
    else:
        global hero
        hero = Hero(name, selected_class)
        return information(hero)
    create_hero()
    create_label(root, text=mistake_text, fg="red", x=220, y=200, font_size=14)


def create_hero():
    clear_window()
    create_label(root, text='Введите имя персонажа:', font_size=30, x=240, y=50)
    create_label(root, text='Выберите класс персонажа', font_size=30, x=240, y=250)
    entry_name = create_entry(root, font_size=32, fg='blue', x=320, y=150, height=50, width=370)
    step_btn = 100
    step_img = 90

    for cl in classes:
        create_button(root, text=cl, x=step_btn, y=660, font_size=24,
                      command=lambda cl=cl: name_validation(entry_name, cl))
        create_image(path=f'images/hero/{cl}.png', x=step_img, y=350, scale=4)
        step_img += 300
        step_btn = (440 + step_btn) * 0.83


def change_weapon(hero, new_weapon):
    hero.weapon = new_weapon
    hero.weapon_damage = weapons[new_weapon][0]
    hero.type_weapon = weapons[new_weapon][1]
    validation_overthrown_monsters(hero)


def validation_overthrown_monsters(hero):
    if overthrown_monsters == 5:
        completed_the_game(hero)
    else:
        information(hero)


def asking_change_weapon(hero, new_weapon):
    clear_window()
    create_label(root, text=f'У поверженного существа Вы находите "{new_weapon}"',
                 font_size=20, x=100, y=100, justify='center', fg='#8b00ff')
    hero_weapon_str = f'Ваше оружие:\n\n\n\n\n\n{hero.weapon} (+⚔️{hero.weapon_damage} ед.)\nТип оружия: "{hero.type_weapon}"'
    new_weapon_str = f'Найденное оружие:\n\n\n\n\n\n{new_weapon} (+⚔️{weapons[new_weapon][0]} ед.)\nТип оружия: "{weapons[new_weapon][1]}"'
    create_label(root, text=hero_weapon_str, font_size=20, x=10, y=200, justify='center', width=28)
    create_label(root, text=new_weapon_str, font_size=20, x=510, y=200, justify='center', width=28)
    create_label(root, text='--->', font_size=30, x=440, y=320, justify='center')
    create_image(path=f'images/weapons/{hero.weapon}.png', x=145, y=260, scale=5)
    create_image(path=f'images/weapons/{new_weapon}.png', x=645, y=260, scale=5)
    create_label(root, text='Хотите сменить оружие?', font_size=20, x=275, y=600, justify='center', fg='red')
    create_button(root, text='Да', x=300, y=670, font_size=18, command=lambda: change_weapon(hero, new_weapon))
    create_button(root, text='Нет', x=550, y=670, font_size=18, command=lambda: validation_overthrown_monsters(hero))


def change_class(hero, loser, cl):
    hero.add_class(cl)
    asking_change_weapon(hero, loser.reward)


def get_reward(winner, loser):
    clear_window()
    play_music(f'music/events/win.mp3', loops=-1)
    create_label(root, text=f'🎉💥Вы одержали победу!🎉💥', fg='#1f75fe', font_size=30, x=150, y=20)
    create_image(path='images/congratulations/Ура1.png', x=765, y=500, scale=4)
    create_image(path='images/congratulations/Ура2.png', x=5, y=500, scale=4)
    if winner.hp < winner.max_hp:
        winner.hp = winner.max_hp
        create_label(root, text=f'Вы чувствуете прилив энергии!\n'
                                f'Ваше здоровье полностью восстановлено до ❤{winner.max_hp} ед.\n',
                     font_size=20, x=130, y=100, fg='#52a8ff', justify='center')
    else:
        create_label(root, text='🔥Ого! Вас даже не задело!🔥', fg='#52a8ff', font_size=20, x=260, y=120,
                     justify='center')
    if hero.lvl >= 3:
        create_label(root, text=f'🔥У Вас максимально возможный уровень!🔥', font_size=20, x=170, y=250, justify='center')
        create_label(root, text=f'Вы покорили {overthrown_monsters} монстров! ', font_size=20, x=300, y=300,
                     justify='center')
        create_label(root, text=f'Да Вы уже сам как монстр 👻😈👾', font_size=20, x=210, y=350, justify='center')
        create_button(root, text='Далее', x=430, y=680, font_size=18,
                      command=lambda: asking_change_weapon(hero, loser.reward))
        return
    hero.lvl += 1
    create_label(root, text=f'🔝Вы повысили уровень🔝\n Теперь у Вас {hero.lvl} уровень!\n', fg='#c53dff', font_size=20,
                 x=310, y=200, justify='center')
    if hero.lvl == 3:
        create_label(root, text='🔥Это максимально возможный уровень🔥\n', fg='#ff4d00', font_size=20, x=190, y=300,
                     justify='center')
    create_label(root, text=f'Ваше здоровье повышено на +❤{hero.endurance} ед. выносливости!', fg='#19ff19',
                 font_size=20, x=120, y=350, justify='center')
    hero.hp = hero.max_hp = hero.max_hp + hero.endurance
    create_label(root, text='Вы можете прокачать класс и получить новый бонус!', font_size=20, x=100, y=400,
                 justify='center')
    create_label(root, text='Выберите класс для прокачки', font_size=18, x=300, y=630, justify='center')
    selected_classes = [f'{key}: {value} уровня' for key, value in hero.selected_classes.items()]
    strig_classes = ",\n".join(selected_classes)
    create_label(root, text=f'Ваш(и) класс(ы):\n{strig_classes}', font_size=16, x=380, y=450, justify='center')
    step_btn = 50
    for cl in classes:
        step_btn = (420 + step_btn) * 0.65
        create_button(root, text=f'{cl}', x=step_btn, y=700, font_size=14,
                      command=lambda cl=cl: change_class(hero, loser, cl))


def meeting_enemy(hero):
    global enemy
    clear_window()
    enemy = Enemy()
    play_music(f'music/enemies/{enemy.name}.wav', loops=0)
    create_label(root, text='Перед Вами появляется', font_size=30, x=245, y=60)
    create_label(root, text=f'{enemy.name}', fg="red", font_size=40, x=135, y=120, width=21)
    create_image(path=f'images/enemies/{enemy.name}.png', x=340, y=220, scale=3)
    create_button(root, text='В бой!', x=420, y=650, font_size=24, command=lambda: battle(hero, enemy))


def quit():
    clear_window()
    create_label(root, text='Спасибо за игру!\nУдачи!', font_size=34, x=290, y=280)
    root.after(2000, lambda: exit())


def before_battle(hero):
    clear_window()
    creepy_sounds = ['creepy1.MP3', 'creepy2.wav', 'creepy3.mp3', 'creepy4.wav', 'creepy5.wav']
    play_music(f'music/environment/{choice(creepy_sounds)}', loops=0)
    words = choice(words_before_fight)
    create_label(root, text=f'{words}', font_size=26, x=13, y=200, width=44)
    root.after(6000, lambda: meeting_enemy(hero))


def battle(hero, enemy):
    clear_window()
    play_music(f'music/environment/fight.MP3', loops=-1)
    create_label(root, text=f'⚔️БОЙ⚔️', font_size=30, x=385, y=0)
    global hero_char, enemy_char
    hero_char = create_characteristic(hero, x=25, y=350)
    enemy_char = create_characteristic(enemy, x=735, y=350)
    create_label(root, text=hero.name, font_size=18, fg="#19ff19", x=0, y=0, width=20)
    create_label(root, text=enemy.name, font_size=18, fg="red", x=700, y=0, width=20)
    hero_class = "".join(sorted(hero.selected_classes.keys()))
    create_image(path=f'images/hero/{hero_class}.png', x=40, y=50, scale=4)
    create_image(path=f'images/enemies/{enemy.name}.png', x=740, y=50, scale=4)
    hero_bonuses = '\n      '.join([func.__doc__ for func in hero.bonuses])
    enemy_bonuses = '\n      '.join([func.__doc__ for func in enemy.bonuses])
    string_bonuses = f"Ваши бонусы:\n      {hero_bonuses}\n"
    string_bonuses = string_bonuses + (f'Особенности противника:\n      '
                                       f'{enemy_bonuses}') if enemy_bonuses else string_bonuses
    text_bonuses = create_label(root, text=string_bonuses, font_size=11, x=25, y=620, justify='left', fg='#cc99ff')
    logger = create_logger(x=288, y=80, width=51, height=33)
    if hero.dexterity >= enemy.dexterity:
        attacker, defender, level = hero, enemy, 'hero'
    else:
        attacker, defender, level = enemy, hero, "enemy"
    logger.log(f'Первым ходит {attacker.name}\n', "neutral")
    loser, winner = fight(attacker, defender, 1, True, logger=logger, level=level)
    text_bonuses.destroy()
    if loser == hero:
        play_music(f'music/events/die.wav', loops=0)
        create_image(path='images/hero/Мёртвый.png', x=40, y=50, scale=4)
        create_label(root, text='Вы проиграли...Не расстраивайтесь!', font_size=20, x=240, y=615)
        create_button(root, text='Сыграть ещё', x=300, y=690, font_size=18, command=lambda: hello_player(), bg="green",
                      fg="black", activebackground='#008000')
        create_button(root, text='Уйти', x=600, y=690, font_size=18, command=lambda: quit(), bg="red", fg="black",
                      activebackground='#8b0000')
    else:
        global overthrown_monsters
        overthrown_monsters += 1
        play_music(f'music/events/victory.wav', loops=0)
        create_image(path='images/enemies/Мёртвый.png', x=740, y=50, scale=4)
        create_button(root, text='К награде!', x=420, y=670, font_size=18, command=lambda: get_reward(winner, loser))


def create_characteristic(target, x, y):
    characterictik = (
        f'❤Здоровье: {target.hp}/{target.max_hp} ед.'
        f'\n⚔️Урон: {target.power + target.weapon_damage} ед.'
        f'\n\nСила: {target.power} ед.\nЛовкость: {target.dexterity} ед.'
        f'\nВыносливость: {target.endurance} ед.')
    if target.type == 'hero':
        characterictik += f'\nОружие: {hero.weapon}\nТип оружия: "{hero.type_weapon}"'
    return create_label(root, text=characterictik, font_size=14, justify='left', x=x, y=y)


def update_characteristics(hero, enemy):
    global hero_char, enemy_char
    x_h, y_h = hero_char.winfo_x(), hero_char.winfo_y()
    x_e, y_e = enemy_char.winfo_x(), enemy_char.winfo_y()
    hero_char.destroy()
    enemy_char.destroy()
    hero_char = create_characteristic(hero, x=x_h, y=y_h)
    enemy_char = create_characteristic(enemy, x=x_e, y=y_e)


def fight(attacker, defender, turn_counter, first_attacker, logger, level):
    delay()
    logger.log(f'{attacker.name} замахивается...\n', level)
    hit_chance = randint(1, attacker.dexterity + defender.dexterity)
    delay()
    if hit_chance <= defender.dexterity:
        logger.log('Промах...\n', level)
        return fight(defender, attacker, turn_counter + 1 if not first_attacker else turn_counter, not first_attacker,
                     logger, level='enemy' if level == 'hero' else 'hero')
    logger.log('🎯Есть попадание!🎯\n', level)
    delay()
    damage = attacker.weapon_damage + attacker.power
    logger.log(f'Урон от оружия ⚔️+{attacker.weapon_damage} ед.\nУрон от силы ⚔️+{attacker.power} ед.', level)
    delay()
    if attacker.bonuses:
        for bonus in attacker.bonuses:
            damage = bonus(damage=damage, attacker=attacker, defender=defender,
                           turn_counter=turn_counter, type_bonus="damage_bonus", logger=logger, level=level)
    if defender.bonuses:
        for bonus in defender.bonuses:
            damage = bonus(damage=damage, attacker=attacker, defender=defender,
                           turn_counter=turn_counter, type_bonus="protection_bonus", logger=logger, level=level)

    delay()
    if damage <= 0:
        logger.log('Урона недостаточно...', level)
    else:
        defender.hp = defender.hp - damage if (defender.hp - damage) > 0 else 0
        logger.log(f'\nВ итоге: {attacker.name} наносит {defender.name} ⚔️{damage} ед. урона\n', level)

        update_characteristics(*((attacker, defender) if level == 'hero' else (defender, attacker)))

        if level == 'enemy':
            logger.log(f'У героя {defender.name} осталось ❤️{defender.hp} ед. здоровья\n', level)
        else:
            logger.log(f'У существа {defender.name} осталось ❤️{defender.hp} ед. здоровья\n', level)

    if defender.hp <= 0:
        logger.log(f'💀{defender.name} поражён💀\n', 'neutral')
        return defender, attacker

    return fight(defender, attacker, turn_counter + 1 if not first_attacker else turn_counter, not first_attacker,
                 logger=logger, level='enemy' if level == 'hero' else 'hero')


def completed_the_game(hero):
    clear_window()
    play_music(f'music/events/completed_the_game.mp3', loops=-1)
    create_label(root, text=f'🎉💥Вы прошли игру!🎉💥', font_size=30, x=180, y=20)
    create_image(path='images/congratulations/Ура1.png', x=765, y=350, scale=4)
    create_image(path='images/congratulations/Ура2.png', x=5, y=350, scale=4)
    create_image(path='images/congratulations/Ура3.png', x=330, y=595, scale=4)
    name_image = "".join(sorted(hero.selected_classes.keys()))
    create_image(path=f'images/hero/{name_image}.png', x=350, y=100, scale=3)
    create_label(root, text=f'Победитель {hero.name}', font_size=20, x=240, y=500, width=30)
    create_button(root, text='Сыграть ещё', x=20, y=690, font_size=18, command=lambda: hello_player(), bg="green",
                  fg="black", activebackground='#008000')
    create_button(root, text='Уйти', x=800, y=690, font_size=18, command=lambda: quit(), bg="red", fg="black",
                  activebackground='#8b0000')


def parting_speech(hero, last_word=None):
    clear_window()
    choised_word = choice([w for w in parting_words if w != last_word])
    create_label(root, text=f'"{choised_word}"', font_size=26, x=12, y=200, width=44)

    create_button(root, text='В путь', x=150, y=660, font_size=24, command=lambda: before_battle(hero))
    create_button(root, text='Герой', x=365, y=660, font_size=24, command=lambda: information(hero))
    create_button(root, text='Ещё напутствие', x=550, y=660, font_size=24,
                  command=lambda: parting_speech(hero, last_word=choised_word))


def information(hero):
    clear_window()
    classes_lvl = [f'    {key}: {value} уровня' for key, value in hero.selected_classes.items()]
    string_bonuses = "\n  ".join([func.__doc__ for func in hero.bonuses])
    string_classes = ",\n".join(classes_lvl)
    characterictik = (
        f'👑Герой {hero.lvl} уровня\nКласс(ы): \n{string_classes}\n❤Здоровье: {hero.hp} ед.'
        f'       ⚔️Урон: {hero.power + hero.weapon_damage} ед.\nСила: {hero.power} ед.\nЛовкость: {hero.dexterity} ед.'
        f'\nВыносливость: {hero.endurance} ед.')
    weapon = f'Оружие:\n\n\n\n\n\n\n{hero.weapon} (+⚔️{hero.weapon_damage} ед.)\nТип оружия: "{hero.type_weapon}"'
    create_label(root, text='Характеристики', font_size=32, x=100, y=20, fg='#00ff00')
    create_label(root, text=f'\nБонусы:\n  {string_bonuses}', font_size=11, fg='#cc99ff', x=330, y=500, justify='left')
    create_label(root, text=weapon, font_size=14, x=30, y=485, fg='#ff4d00', justify='center')
    create_image(path=f'images/weapons/{hero.weapon}.png', x=60, y=530, scale=6)
    create_label(root, text=hero.name, font_size=26, x=475, y=450, width=25)
    create_label(root, text=characterictik, font_size=18, x=50, y=100, justify='left')
    create_button(root, text='В путь', x=400, y=660, font_size=24, command=lambda: before_battle(hero))
    create_button(root, text='Напутствие', x=650, y=660, font_size=24, command=lambda: parting_speech(hero))
    name_image = "".join(sorted(hero.selected_classes.keys()))
    create_image(path=f'images/hero/{name_image}.png', x=600, y=60, scale=3)


def play_music(path, loops):
    mixer.music.load(path)
    mixer.music.play(loops=loops)


def hello_player():
    clear_window()
    play_music("music/environment/menu.mp3", loops=-1)
    create_label(root, text='Приветствую Вас в игре!', font_size=32, x=220, y=200)
    create_button(root, text='Создать персонажа', x=320, y=550, font_size=24, command=create_hero)


def start_game():
    global root, delay, objects_in_window, overthrown_monsters
    root = Tk()
    root.title("РПГ")
    root["bg"] = 'black'
    w = 1000
    h = 800
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    delay = lambda: root.after(2000)
    mixer.init()
    objects_in_window = []
    overthrown_monsters = 0
    hello_player()
    root.mainloop()


if __name__ == '__main__':
    start_game()


