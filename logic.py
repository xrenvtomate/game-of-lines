import pygame as pg
from pygame.math import Vector2
import random

pg.init()

g = 0.5
ball_radius = 20
ball_color = '#D25EFF'
ball_shadow ='#734884'
bg_color = '#170526'
line_color = '#5EFFFB'
newline_color = '#2E7F7D'
linebord_color = '#00C3CD'

parc_group = pg.sprite.Group()
tail_group = pg.sprite.Group()

def get_offset(x, width):
    return width / 2 - x

def offseted(dx, cord):
    return cord[0] + dx, cord[1]

def drawing(sc, ball, width, newxy, linepos, tail):
    dx = get_offset(ball.x, width)
    for el in tail_group: # drawing tail of ball
        pg.draw.circle(sc, tuple(el.color), (el.x + dx, el.y), el.r)
    #drawing parc
    for el in parc_group:
        pg.draw.rect(sc, el.color, (el.x - el.size + dx, el.y - el.size, el.size * 2, el.size * 2))

    # ball
    pg.draw.circle(sc, ball_shadow, (ball.x + dx, ball.y), ball_radius + 3)
    pg.draw.circle(sc, ball_color, (ball.x + dx, ball.y), ball_radius)


    if newxy is not None:
        pg.draw.line(sc, newline_color, offseted(dx, newxy), pg.mouse.get_pos(), 5)

    if linepos != (None, None):
        # line
        pg.draw.line(sc, linebord_color, offseted(dx, linepos[0]), offseted(dx, linepos[1]), 12)
        pg.draw.line(sc, line_color, offseted(dx, linepos[0]), offseted(dx, linepos[1]), 8)

        # line borders
        pg.draw.circle(sc, linebord_color, offseted(dx, linepos[0]), 10)
        pg.draw.circle(sc, linebord_color, offseted(dx, linepos[1]), 10)


def draw_parc(x, y, sc):
        for i in range(30):
            Parc(x, y)

class Ball(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 200
        self.direction = Vector2(0, -10)

    def update(self, linepos, sc):
        self.moving()
        # collision

        if linepos != (None, None):
            rect = pg.Rect(self.x - ball_radius, self.y - ball_radius, 2 * ball_radius, 2 * ball_radius) # ball rect
            if rect.clipline(linepos):
                line_norm = Vector2(-linepos[1][1] + linepos[0][1], linepos[1][0] - linepos[0][0])
                self.direction = self.direction.reflect(line_norm)
                # creat parciples
                for i in range(30):
                    Parc(self.x, self.y, 'p')


            # bug fix
            while rect.clipline(linepos):
                self.moving()
                rect = pg.Rect(self.x - ball_radius, self.y - ball_radius, 2 * ball_radius, 2 * ball_radius)

    def moving(self):
        # moving
        self.x += self.direction.x
        self.y += self.direction.y
        self.direction.y += g
        Tailparticle(int(self.x), int(self.y))
        Tailparticle(int(self.x - self.direction.x / 2), int(self.y - self.direction.y / 2))




class Tailparticle(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(tail_group)
        self.r = 10
        self.x = x
        self.y = y
        self.color = [0, 100, 255]

    def update(self):
        self.r -= 0.3
        self.color[0] = min(255, self.color[0] + 20)
        if self.r < 0:
            self.kill()


class Parc(pg.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__(parc_group)
        if color == 'p':
            self.color = random.choice(('#E25EFF', '#7D00C5', '#C200C5'))
        else:
            self.color = random.choice((line_color, linebord_color))
        self.x, self.y = x, y
        self.vx = random.randint(-10, 10)
        self.vy = random.randint(-10, -1)
        self.size = random.randint(1, 3)

    def update(self): # moving
        self.x += self.vx
        self.y += self.vy
        self.vy += 2 * g
        if self.y > 1500:
            self.kill()


class Line():
    def __init__(self, start, end):
        self.cord = start, end
