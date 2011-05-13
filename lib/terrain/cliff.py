#!/usr/bin/python
# -*- coding: utf-8 -*-
import sprite
import pygame.image
import os

import pygame.sprite
import terrain

class Terrain(terrain.Terrain):
    frames = sprite.read_frames(os.path.join("lib", "terrain",
                                                  "cliff.png"), 24, 16)
    def __init__(self, pos, display, level=None):
        self.image = self.frames[1][1]
        self.level = level
        terrain.Terrain.__init__(self, pos, display, level)

    def update(self):
        x, y = self.pos
        level = self.level
        if level.is_floor((x, y+1)):
            if level.is_floor((x+1, y)) and level.is_floor((x-1, y)):
                self.image = self.frames[3][2]
            elif level.is_floor((x+1, y)):
                self.image = self.frames[2][2]
            elif level.is_floor((x-1, y)):
                self.image = self.frames[0][2]
            else:
                self.image = self.frames[1][2]
        else:
            if level.is_floor((x+1, y+1)) and level.is_floor((x-1, y+1)):
                self.image = self.frames[3][1]
            elif level.is_floor((x+1, y+1)):
                self.image = self.frames[2][1]
            elif level.is_floor((x-1, y+1)):
                self.image = self.frames[0][1]
            else:
                self.image = self.frames[1][1]
        if level.is_floor((x, y-1)):
            overlay = pygame.sprite.Sprite(self.display.overlay)
            overlay.rect = pygame.rect.Rect(x*24, y*16-16, 24, 26)
            if level.is_floor((x+1, y)) and level.is_floor((x-1, y)):
                overlay.image = self.frames[3][0]
            elif level.is_floor((x+1, y)):
                overlay.image = self.frames[2][0]
            elif level.is_floor((x-1, y)):
                overlay.image = self.frames[0][0]
            else:
                overlay.image = self.frames[1][0]

