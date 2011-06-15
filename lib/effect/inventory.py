#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import pygame.font


class Inventory(pygame.sprite.Sprite):
    """List inventory."""

    def __init__(self, screen, text, color=None, delay=0):
        font = pygame.font.SysFont(None, 18)
        pygame.sprite.Sprite.__init__(self)
        if color is None:
            color = (255, 255, 255)
        self.alpha = 255
        print text
        self.image = font.render(text, 1, (255,255,255))
        self.rect = self.image.get_rect()
        self.rect.bottom = screen.get_rect().bottom - 70
        screen.blit(self.image, (50, 100))
