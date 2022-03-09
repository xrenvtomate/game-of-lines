from logic import *


font = pg.font.Font(None, 100) # font settings
WIDTH, HEIGHT = 1600, 900
tail = []
clock = pg.time.Clock()
sc = pg.display.set_mode((WIDTH, HEIGHT))

max_v = (2 * g * HEIGHT) ** 0.5
newxy = None
ball = Ball()
line = Line(None, None)
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            if newxy is None:
                newxy = offseted(-get_offset(ball.x, WIDTH), event.pos)
            else:
                line = Line(newxy, offseted(-get_offset(ball.x, WIDTH), event.pos))
                for _ in range(10):
                    Parc(*newxy, 'b')
                for _ in range(10):
                    Parc(*offseted(-get_offset(ball.x, WIDTH), event.pos), 'b')
                newxy = None
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            elif event.key == pg.K_r:
                # clear all
                tail = []
                newxy = None
                ball = Ball()
                line = Line(None, None)




    ball.update(line.cord, sc)

    tail_group.update()
    parc_group.update()
    sc.fill(bg_color)
    drawing(sc, ball, WIDTH, newxy, line.cord, tail)
    if ball.y > HEIGHT + 50:
        sc.blit(font.render('press R to restart', 1, '#58FF8D'), (100, 100))
    pg.display.flip()
    clock.tick(60)
