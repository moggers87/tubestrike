from __future__ import division, print_function, unicode_literals

from pkg_resources import resource_filename
import math
import sys
import threading

from pygame import display, transform
import pygame


def setup(width=800, height=600):
    """Setup game environment"""
    display.init()
    pygame.font.init()

    print("Setting game resolution to {} x {}".format(width, height))
    screen = display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE)
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

    pygame.event.set_allowed([pygame.QUIT, pygame.VIDEORESIZE])

    def render_text(text, colour, antialiasing=True):
        # PyGame 1.9.1 doesn't seem to like file objects
        # TODO: use resource_stream once it works
        font = pygame.font.Font(resource_filename("tubestrike", "assets/fonts/Hammersmith_One/HammersmithOne-Regular.ttf"), 40)

        title = font.render(text, antialiasing, colour)
        return title

    def event_ticker():
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                print("Quitting...")
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                setup(event.dict["w"], event.dict["h"])

    event_thread = threading.Thread(target=event_ticker)
    event_thread.start()

    title_surface = render_text("Tubestrike!", (255, 255, 255))
    title_center = (
        int(canvas.get_size()[0]/2 - title_surface.get_size()[0]/2),
        int(canvas.get_size()[1]/2 - title_surface.get_size()[1]/2),
    )

    zoom_val = 1
    rot_val = 0
    zoom_delta = 0.01
    rot_delta = 0.1

    print("Entering main game loop...")
    while event_thread.is_alive():
        pygame.event.pump()
        title_copy = transform.rotozoom(title_surface, rot_val, zoom_val)
        title_center = (
            int(canvas.get_size()[0]/2 - title_copy.get_size()[0]/2),
            int(canvas.get_size()[1]/2 - title_copy.get_size()[1]/2),
        )
        canvas.fill((128, 100, 200))
        canvas.blit(title_copy, title_center)

        rot_val = 15 * math.sin((math.pi * rot_delta) + 2)
        zoom_val = math.sin(math.pi * zoom_delta) + 0.5
        zoom_delta = (zoom_delta + 0.005) % 1
        rot_delta = (rot_delta + 0.01) % 2

        paint_canvas_onto_screen(screen, canvas)
        display.flip()
        clock.tick(24)


def main():
    setup()
    loop()
