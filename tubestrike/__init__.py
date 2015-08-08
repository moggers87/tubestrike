from __future__ import division, print_function, unicode_literals

import sys

from pygame import draw, display
import pygame


def setup():
    """Setup game environment"""
    width = 800
    height = 600

    print("Setting game resolution to {} x {}".format(width, height))
    screen = display.set_mode((width, height), pygame.DOUBLEBUF)
    display.set_caption("tubestrike!")

    screen.fill((0, 0, 0))
    display.flip()


def loop():
    """Main gameloop"""
    clock = pygame.time.Clock()
    screen = display.get_surface()  # the "display"
    canvas = pygame.Surface((1024, 512))
    canvas.fill((128, 0, 128))

    block = pygame.Rect(5, 5, 1014, 502)
    draw.rect(canvas, (255, 255, 255), block)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quitting...")
                pygame.quit()
                sys.exit()

        screen_res = screen.get_size()
        screen_ratio = screen_res[0]/screen_res[1]
        canvas_res = canvas.get_size()
        canvas_ratio = canvas_res[0]/canvas_res[1]

        if screen_ratio > canvas_ratio:
            canvas_copy_res = (screen_res[0], int(screen_res[0] / canvas_ratio))
        else:
            canvas_copy_res = (int(canvas_ratio * screen_res[1]), screen_res[1])

        canvas_copy = pygame.transform.smoothscale(canvas, canvas_copy_res)
        screen.blit(canvas_copy, (0, 0))

        display.flip()
        clock.tick(24)


def main():
    setup()
    loop()
