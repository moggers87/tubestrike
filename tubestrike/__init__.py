from __future__ import division, print_function, unicode_literals

from pkg_resources import resource_filename
import math
import random
import sys

from pygame import display, draw, transform
import pygame


DISPLAY_MODES = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE


def setup():
    """Setup game environment"""
    display.init()
    pygame.font.init()

    pygame.event.set_allowed(None)  # disable all events
    pygame.event.set_allowed((pygame.QUIT, pygame.VIDEORESIZE))  # re-enable some events

    width = 800
    height = 600

    print("Setting game resolution to {} x {}".format(width, height))
    screen = display.set_mode((width, height), DISPLAY_MODES)
    display.set_caption("tubestrike!")

    screen.fill((0, 0, 0))
    display.flip()


def make_track_surface():
    """Paint some tracks onto a surface"""
    track_shape = (640, 5)
    track_shadow = (640, 3)
    sleeper = (10, 40)
    surf = pygame.Surface((640, 40), flags=pygame.SRCALPHA | pygame.HWSURFACE)
    # sleepers
    for i in xrange(5, 640, 20):
        draw.rect(surf, (178, 150, 250), pygame.Rect((i, 0), sleeper))

    # tracks
    draw.rect(surf, (178, 150, 250), pygame.Rect((0, 2), track_shape))
    draw.rect(surf, (153, 125, 225), pygame.Rect((0, 7), track_shadow))
    draw.rect(surf, (178, 150, 250), pygame.Rect((0, 27), track_shape))
    draw.rect(surf, (153, 125, 225), pygame.Rect((0, 32), track_shadow))

    return surf


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
    canvas = pygame.Surface((640, 200), flags=pygame.HWSURFACE)
    canvas.fill((128, 100, 200))

    # PyGame 1.9.1 doesn't seem to like file objects
    # TODO: use resource_stream once it works
    font = pygame.font.Font(resource_filename("tubestrike", "assets/fonts/Hammersmith_One/HammersmithOne-Regular.ttf"), 40)

    title_surface = font.render("Tubestrike!", True, (255, 255, 255))
    title_center = (
        int(canvas.get_size()[0]/2 - title_surface.get_size()[0]/2),
        int(canvas.get_size()[1]/2 - title_surface.get_size()[1]/2),
    )

    track_surface = make_track_surface()

    zoom_val = 1
    rot_val = 0
    zoom_delta = 0.01
    rot_delta = 0.1

    # screen resize stuff
    size = None
    cool_down = 0
    print("Entering main game loop...")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quitting...")
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                size = (event.dict["w"], event.dict["h"])
                cool_down = 5

        canvas.fill((128, 100, 200))
        canvas.blit(track_surface, (0, 148))

        title_copy = transform.rotozoom(title_surface, rot_val, zoom_val)
        title_center = (
            int(canvas.get_size()[0]/2 - title_copy.get_size()[0]/2),
            int(canvas.get_size()[1]/2 - title_copy.get_size()[1]/2),
        )
        canvas.blit(title_copy, title_center)

        rot_val = 15 * math.sin((math.pi * rot_delta) + 2)
        zoom_val = math.sin(math.pi * zoom_delta) + 0.5
        zoom_delta = (zoom_delta + 0.005) % 1
        rot_delta = (rot_delta + 0.01) % 2

        # work around for gnomeshell/sdl bug
        if size is not None and cool_down == 0:
            print("Setting game resolution to {} x {}".format(*size))
            screen = display.set_mode(size, DISPLAY_MODES)
            size = None
        elif cool_down > 0:
            cool_down = cool_down - 1

        paint_canvas_onto_screen(screen, canvas)
        display.flip()
        clock.tick(24)


def main():
    setup()
    loop()
