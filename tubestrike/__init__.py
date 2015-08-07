from __future__ import division, print_function, unicode_literals

import sys

from pygame import display
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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(24)


def main():
    setup()
    loop()
