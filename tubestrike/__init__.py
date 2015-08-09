from __future__ import division, print_function, unicode_literals

from pkg_resources import resource_listdir, resource_stream, resource_filename
import random
import sys

from pygame import draw, display, transform
import pygame


def setup():
    """Setup game environment"""
    display.init()
    pygame.font.init()

    pygame.event.set_allowed(pygame.QUIT)

    width = 800
    height = 600

    print("Setting game resolution to {} x {}".format(width, height))
    screen = display.set_mode((width, height), pygame.DOUBLEBUF)
    display.set_caption("tubestrike!")

    screen.fill((0, 0, 0))
    display.flip()


def paint_canvas_onto_screen(screen, canvas):
    """Paints (and scales) `canvas` onto `screen`"""
    screen_res = screen.get_size()
    screen_ratio = screen_res[0]/screen_res[1]
    canvas_res = canvas.get_size()
    canvas_ratio = canvas_res[0]/canvas_res[1]

    if screen_ratio > canvas_ratio:
        canvas_copy_res = (screen_res[0], int(screen_res[0] / canvas_ratio))
    else:
        canvas_copy_res = (int(canvas_ratio * screen_res[1]), screen_res[1])

    canvas_offset = (
        -int((canvas_copy_res[0] - screen_res[0]) / 2),
        -int((canvas_copy_res[1] - screen_res[1]) / 2),
    )

    canvas_copy = transform.smoothscale(canvas, canvas_copy_res)
    screen.blit(canvas_copy, canvas_offset)


def loop():
    """Main gameloop"""
    clock = pygame.time.Clock()
    screen = display.get_surface()  # the "display"
    canvas = pygame.Surface((640, 200))
    canvas.fill((128, 100, 200))

    n = 0
    font_sets = [(asset, resource_listdir("tubestrike", "assets/fonts/" + asset)) for asset in resource_listdir("tubestrike", "assets/fonts")]
    fonts = []
    for asset, font_names in font_sets:
        for name in font_names:
            if name.endswith(".ttf"):
                fonts.append("{}/{}".format(asset, name))
    fonts.sort()

    print("Entering main game loop...")
    def render_text(font, text, colour, antialiasing=True):
        print("Font: {}".format(font))
        font = pygame.font.Font(resource_filename("tubestrike", "assets/fonts/" + font), 40)

        title = font.render(text, antialiasing, colour)
        return title

    title_surface = render_text(fonts[n], "Tubestrike!", (255, 255, 255))
    title_center = (
        int(canvas.get_size()[0]/2 - title_surface.get_size()[0]/2),
        int(canvas.get_size()[1]/2 - title_surface.get_size()[1]/2),
    )

    c = 0
    zoom_val = 1
    rot_val = 0
    zoom_delta = 0
    rot_delta = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quitting...")
                pygame.quit()
                sys.exit()

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE] and c == 0:
            n = (n + 1) % len(fonts)
            c = 12

            title_surface = render_text(fonts[n], "Tubestrike!", (255, 255, 255))
            title_center = (
                int(canvas.get_size()[0]/2 - title_surface.get_size()[0]/2),
                int(canvas.get_size()[1]/2 - title_surface.get_size()[1]/2),
            )

        title_copy = transform.rotozoom(title_surface, 10, zoom_val)
        title_center = (
            int(canvas.get_size()[0]/2 - title_copy.get_size()[0]/2),
            int(canvas.get_size()[1]/2 - title_copy.get_size()[1]/2),
        )
        canvas.fill((128, 100, 200))
        canvas.blit(title_copy, title_center)

        rot_val = rot_val + random.gauss(rot_delta, 1)
        zoom_val = zoom_val + random.gauss(zoom_delta, 0.01)
        if zoom_val > 1.25:
            zoom_delta = zoom_delta - 0.1
        elif zoom_val < 0.75:
            zoom_delta = zoom_delta + 0.1

        if c > 0:
            c = c - 1
        paint_canvas_onto_screen(screen, canvas)
        display.flip()
        clock.tick(24)


def main():
    setup()
    loop()
