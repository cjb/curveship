#!/usr/bin/python
# -*- coding: utf-8 -*-

#import sprite
#import pygame.transform

import item

class Item(item.Item):
    name = "firstaid"

# Make it super-huge
#    class Sprite(sprite.Item):
#        def __init__(self, *args, **kw):
#            sprite.Item.__init__(self, *args, **kw)
#            self.image = pygame.transform.scale2x(self.image)
#            self.rect = self.image.get_rect()
