#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import pygame.sprite
import os

class Shadow(pygame.sprite.Sprite):
    """Display a transparent shadow."""

    image = pygame.image.load(os.path.join("lib", "effect", "shadow.png")).convert()

    def __init__(self, sprite):
        pygame.sprite.Sprite.__init__(self)
        self.sprite = sprite
        self.image.set_alpha(64)
        self.rect = self.image.get_rect()
        self.offset = 0

    def update(self):
        x, y = self.sprite.rect.center
        self.rect.center = (x, y+4+self.sprite.height-self.offset)
