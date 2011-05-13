#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import pygame.sprite

import os

class Gauge(pygame.sprite.Sprite):
    """Display a gauge. Used to show hitpoints."""

    base_image = pygame.image.load(os.path.join("lib", "effect", "gauge.png")).convert()
    
    def __init__(self, display):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.base_image.copy()
        self.image.set_alpha(200)
        self.rect = self.image.get_rect()
        self.rect.bottom = display.screen.get_rect().bottom
        self.image.fill((128, 200, 0), Rect(3, 3, 18, 2))
