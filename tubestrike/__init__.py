from __future__ import division, print_function, unicode_literals

from pkg_resources import resource_filename
import math
import sys

from pygame import display, draw, transform
import pygame
import numpy


DISPLAY_MODES = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE

# colours
WHITE = (255, 255, 255)
LIGHT_COLOUR = (178, 150, 250)
DARK_COLOUR = (153, 125, 225)
BACKGROUND_COLOUR = (128, 100, 200)
BLACK = (0, 0, 0)


def setup():
    """Setup game environment"""
    display.init()
    pygame.font.init()

    pygame.event.set_allowed(None)  # disable all events
    pygame.event.set_allowed((
        pygame.QUIT,
        pygame.VIDEORESIZE,
        pygame.ACTIVEEVENT,
        pygame.KEYDOWN,
    ))  # re-enable some events

    width = 800
    height = 600

    print("Setting game resolution to {} x {}".format(width, height))
    screen = display.set_mode((width, height), DISPLAY_MODES)
    display.set_caption("tubestrike!")

    screen.fill(BLACK)
    display.flip()


def make_track_surface():
    """Paint some tracks onto a surface"""
    track_shape = (640, 5)
    track_shadow = (640, 3)
    sleeper = (10, 40)
    sleeper_shadows = (10, 2)

    surf = pygame.Surface((640, 40), flags=pygame.SRCALPHA | pygame.HWSURFACE)

    # sleepers
    for i in xrange(5, 640, 20):
        draw.rect(surf, LIGHT_COLOUR, pygame.Rect((i, 0), sleeper))
        draw.rect(surf, DARK_COLOUR, pygame.Rect((i, 0), sleeper_shadows))
        draw.rect(surf, DARK_COLOUR, pygame.Rect((i, 25), sleeper_shadows))
        draw.rect(surf, DARK_COLOUR, pygame.Rect((i, 38), sleeper_shadows))

    # tracks
    draw.rect(surf, LIGHT_COLOUR, pygame.Rect((0, 2), track_shape))
    draw.rect(surf, DARK_COLOUR, pygame.Rect((0, 7), track_shadow))
    draw.rect(surf, LIGHT_COLOUR, pygame.Rect((0, 27), track_shape))
    draw.rect(surf, DARK_COLOUR, pygame.Rect((0, 32), track_shadow))

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


class Menu(object):
    def __init__(self, track=None):
        self.canvas = pygame.Surface((640, 200), flags=pygame.HWSURFACE)

        # PyGame 1.9.1 doesn't seem to like file objects
        # TODO: use resource_stream once it works
        title_font = pygame.font.Font(resource_filename("tubestrike", "assets/fonts/Hammersmith_One/HammersmithOne-Regular.ttf"), 40)
        subtitle_font = pygame.font.Font(resource_filename("tubestrike", "assets/fonts/Roboto_Mono/RobotoMono-Regular.ttf"), 15)

        self.title_surface = title_font.render("Tubestrike!", True, WHITE)
        self.subtitle_surface = subtitle_font.render("PRESS SPACE TO START", True, WHITE)

        if track is None:
            self.track_surface = make_track_surface()
        else:
            self.track_surface = track

        self.zoom_val = 1
        self.rot_val = 0
        self.zoom_delta = 0.01
        self.rot_delta = 0.1

        self.next_scene = self

    def render(self):
        self.canvas.fill(BACKGROUND_COLOUR)
        self.canvas.blit(self.track_surface, (0, 148))

        title_copy = transform.rotozoom(self.title_surface, self.rot_val, self.zoom_val)
        title_shadow_copy = transform.rotozoom(self.title_surface, self.rot_val * 2.1, self.zoom_val + 0.5)
        title_center = (
            int(self.canvas.get_size()[0]/2 - title_copy.get_size()[0]/2),
            int(self.canvas.get_size()[1]/3 - title_copy.get_size()[1]/2),
        )

        title_shadow_center = (
            int(self.canvas.get_size()[0]/2 - title_shadow_copy.get_size()[0]/2),
            int(self.canvas.get_size()[1]/3 - title_shadow_copy.get_size()[1]/2),
        )
        subtitle_center = (
            int(self.canvas.get_size()[0]/2 - self.subtitle_surface.get_size()[0]/2),
            int((2*self.canvas.get_size()[1]/3) - self.subtitle_surface.get_size()[1]/2),
        )

        # shadow effect
        pixels_alpha = pygame.surfarray.pixels_alpha(title_shadow_copy)
        pixels_alpha[...] = (pixels_alpha * (50 / 255.0)).astype(numpy.uint8)
        del pixels_alpha  # unlock surface

        self.canvas.blit(title_shadow_copy, title_shadow_center)
        self.canvas.blit(title_copy, title_center)
        self.canvas.blit(self.subtitle_surface, subtitle_center)

        self.rot_val = 15 * math.sin((math.pi * self.rot_delta) + 2)
        self.zoom_val = math.sin(math.pi * self.zoom_delta) + 0.5
        self.zoom_delta = (self.zoom_delta + 0.0039) % 1
        self.rot_delta = (self.rot_delta + 0.008) % 2

    def event_KEYDOWN(self, event):
        if event.key == pygame.K_q:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        elif event.key == pygame.K_SPACE:
            # XXX: should transition to actual game
            self.next_scene = MoveOver(self, Menu(self.track_surface))


class MoveOver(object):
    def __init__(self, from_scene, to_scene):
        self.canvas = pygame.Surface((640, 200), flags=pygame.HWSURFACE)
        self.track_surface = from_scene.track_surface
        self.remains = from_scene.canvas.get_size()[0]

        self.from_scene = from_scene
        self.to_scene = to_scene

        self.next_scene = self

    def render(self):
        self.canvas.fill(BACKGROUND_COLOUR)
        if self.remains > 0 and self.from_scene is not None:
            self.canvas.blit(self.track_surface, (self.remains, 148))
            self.from_scene.render()

            self.canvas.blit(self.from_scene.canvas, ((self.remains - self.from_scene.canvas.get_size()[0]), 0))
            self.remains -= 3
        elif self.remains > 0 and self.from_scene is None:
            self.canvas.blit(self.to_scene.canvas, (self.remains, 0))
            self.to_scene.render()

            self.canvas.blit(self.track_surface, (self.remains - self.to_scene.canvas.get_size()[0], 148))
            self.remains -= 3
        elif self.from_scene is not None:
            self.canvas.blit(self.track_surface, (self.remains, 148))
            self.from_scene = None
            self.remains = self.to_scene.canvas.get_size()[0] + self.remains
        else:
            self.canvas = self.to_scene.canvas
            self.to_scene.render()
            self.next_scene = self.to_scene

    def event_KEYDOWN(self, event):
        if event.key == pygame.K_q:
            pygame.event.post(pygame.event.Event(pygame.QUIT))


def loop():
    """Main gameloop"""
    clock = pygame.time.Clock()
    screen = display.get_surface()  # the "display"

    size = None

    current_scene = Menu()

    print("Entering main game loop...")
    while True:
        for event in pygame.event.get():
            event_key = "event_%s" % pygame.event.event_name(event.type).upper()
            if event.type == pygame.QUIT:
                print("Quitting...")
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                size = event.dict["size"]
            elif event.type == pygame.ACTIVEEVENT:
                if event.dict["state"] == 2:
                    # we might be resizing, set this to prevent mode setting
                    # see issue #2
                    resizing = event.dict["gain"] == 0
            elif hasattr(current_scene, event_key):
                getattr(current_scene, event_key)(event)

        # work around for gnomeshell/sdl bug
        # see issue #2
        if size is not None and not resizing:
            print("Setting game resolution to {} x {}".format(*size))
            screen = display.set_mode(size, DISPLAY_MODES)
            size = None
        current_scene.render()
        paint_canvas_onto_screen(screen, current_scene.canvas)
        display.flip()
        current_scene = current_scene.next_scene
        clock.tick(24)


def main():
    setup()
    loop()
