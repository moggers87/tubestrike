from __future__ import division, print_function, unicode_literals

import pygame

def setup():
    width = 800
    height = 600

    print("Setting game resolution to {} x {}".format(width, height))
    screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)
    pygame.display.set_caption("tubestrike!")

    screen.fill((0, 0, 0))
    pygame.display.flip()


def main():
    setup()
    input()  # for testing, remove later
