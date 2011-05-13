#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame.sprite
import pygame.rect

def create(pos, kind, display, level=None):
    """Create and place a monster of specified kind."""
    module = __import__("terrain.%s" % kind, globals(), {}, ["Terrain"])
    return module.Terrain(pos, display, level)


class Terrain(pygame.sprite.Sprite):
    def __init__(self, pos, display, level=None):
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.depth = pos[1]
        self.rect.left = pos[0]*24
        self.rect.top = pos[1]*16
        self.rect.move_ip(display.scrollpos[0], display.scrollpos[1])
        self.display = display
        display.tiles.add(self)
        self.image = self.image.subsurface(self.image.get_rect())
#        rect = self.rect.move(
#            -self.display.scrollpos[0],
#            -self.display.scrollpos[1])
#        self.display.background.blit(self.image, rect)
