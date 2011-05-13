#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import pygame.sprite
import os

class Bubble(pygame.sprite.Sprite):
    """Base class for all status bubbles."""

    offset = 0

    def __init__(self, sprite):
        self.image.set_alpha(128)
        self.sprite = sprite
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.y = 0.0
        self.dy = 0.0
        self.ddy = 0.33
        sprite.display.effects.add(self)
        try:
            sprite.bubbles[self.name].kill()
            del sprite.bubbles[self.name]
        except KeyError:
            pass
        sprite.bubbles[self.name] = self

    def update(self):
        self.y += self.dy
        self.dy += self.ddy
        x, y = self.sprite.rect.center
        self.rect.center = (x+self.offset, y-24+self.y)
        if self.dy>1 or self.dy<-1:
            self.ddy = -self.ddy

class Asleep(Bubble):
    """A 'sleeping' bubble."""

    name = 'asleep'
    offset = 9
    image = pygame.image.load(os.path.join("lib", "effect",
                                           "asleep.png")).convert()


class Wounded(Bubble):
    """A 'bandaid' bubble."""

    name = 'wounded'
    offset = -9
    image = pygame.image.load(os.path.join("lib", "effect",
                                           "wounded.png")).convert()


