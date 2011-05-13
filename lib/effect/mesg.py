#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import pygame.font


class Mesg(pygame.sprite.Sprite):
    """Messages float up and disappear."""

    font = pygame.font.SysFont(None, 18)

    def __init__(self, display, sprite, text, color=None, delay=0):
        pygame.sprite.Sprite.__init__(self)
        if color is None:
            color = (255, 255, 255)
        self.dh = 10
        self.image = self.font.render(text, False, color).convert()
        self.alpha = 255
        self.rect = self.image.get_rect()
        self.image.set_alpha(0)
        self.rect.center = sprite.rect.midtop
        self.sprite = sprite
        self.delay = delay
        display.effects.add(self)

    def update(self):
        if self.delay>0:
            self.delay -= 1
        else:
            if self.alpha <= 0:
                self.kill()
                return
            self.dh -= 1
            self.rect.move_ip(0, -self.dh)
            self.image.set_alpha(self.alpha)
            self.alpha -= 20

