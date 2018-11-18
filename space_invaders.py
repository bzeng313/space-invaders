import curses
import random

screen = curses.initscr()
curses.curs_set(False)
screen_h, screen_w = screen.getmaxyx()
window = curses.newwin(screen_h, screen_w, 0, 0)
window.keypad(True)
window.timeout(100)
curses.noecho()
invaders = [(2*i + 1, screen_w/8 + 2*j) for i in range(0, 4) for j in range(6*screen_w/16)]
blockades = [(screen_h - (10 - i), screen_w/8 + j) for i in range(4) for j in range(6*screen_w/8) if j%5 != 0]
defender = (screen_h - 2, screen_w/2)
invader_fire = []
defender_fire = []

window.addch(defender[0], defender[1], 'Y')


travel_forward = False
travel_right = True

side = 0

score = 0
window.addstr(screen_h - 1, 0, 'Score: %d'%score)
delay = 0
while True:
    moved_invaders = []
    for y, x in invaders:
        window.addch(y, x, ' ')
        moved_invaders.append((y + travel_forward, x + (2*travel_right - 1)))
    for y, x in moved_invaders:
        window.addch(y, x, 'T')
        if (y, x) in blockades:
            blockades.remove((y, x))
    invaders = moved_invaders

    side += 1
    if side % 5 == 0 and side % 10 != 0:
        travel_right = not travel_right
    if travel_forward:
        travel_forward = False
    if side == 150:
        side = 0
        travel_forward = True
    

    for y, x in blockades:
        window.addch(y, x, '=')

    moved_defender_fire = []
    for y, x in defender_fire:
        if y != 0:
            window.addch(y, x, '^')
        if (y + 1, x) != defender:
            window.addch(y + 1, x, ' ')
        if (y, x) in blockades:
            window.addch(y, x, ' ')
            blockades.remove((y, x))
        elif (y, x) in invaders:
            window.addch(y, x, ' ')
            invaders.remove((y, x))
            score += 100
        else:
            if y != 0:
                moved_defender_fire.append((y - 1, x))
    defender_fire = moved_defender_fire


    moved_invader_fire = []
    for y, x in invader_fire:
        if y != screen_h - 1 and (y, x) not in invaders:
            window.addch(y, x, 'V')
        if y - 1 >= 0:
            window.addch(y - 1, x, ' ')

        if (y, x) in blockades:
            window.addch(y, x, ' ')
            blockades.remove((y, x))
        else:
            if y != screen_h - 1:
                moved_invader_fire.append((y + 1, x))
    invader_fire = moved_invader_fire

    key = window.getch()

    if key == curses.KEY_RIGHT and defender[1] != 7*screen_w/8 + 2:
        window.addch(defender[0], defender[1], ' ')
        defender = (defender[0], defender[1] + 1)
    elif key == curses.KEY_LEFT and defender[1] != screen_w/8 - 3:
        window.addch(defender[0], defender[1], ' ')
        defender = (defender[0], defender[1] - 1)
    elif key == curses.KEY_UP:
        if delay == 0:
            defender_fire.append((defender[0] - 1, defender[1]))
        delay += 1
        if delay == 3:
            delay = 0
    if random.randint(0, 5) == 0:
        invader_fire.append(random.choice(invaders))
    window.addch(defender[0], defender[1], 'Y')

    window.addstr(screen_h - 1, 0, 'Score: %d'%score)

    if defender in invaders or defender in invader_fire:
        break
curses.endwin()
