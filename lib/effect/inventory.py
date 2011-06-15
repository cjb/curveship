#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import pygame.font


class Inventory(pygame.sprite.Sprite):
    """List inventory."""

    def __init__(self, screen, text, x, y):
        font = pygame.font.SysFont(None, 18)
        pygame.sprite.Sprite.__init__(self)
        color = (255, 255, 255)
        self.alpha = 255
        self.image = font.render(text, 1, color)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.bottom = y
        screen.blit(self.image, (50, 100))
