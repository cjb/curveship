#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import pygame.font


class Inventory(pygame.sprite.Sprite):
    """Messages float up and disappear."""

    font = pygame.font.SysFont(None, 18)

    def __init__(self, display, text, color=None, delay=0):
        pygame.sprite.Sprite.__init__(self)
        if color is None:
            color = (255, 255, 255)
        self.dh = 10
        self.image = self.font.render(text, False, color).convert()
        self.alpha = 255
        self.rect = self.image.get_rect()
        self.image.set_alpha(0)
