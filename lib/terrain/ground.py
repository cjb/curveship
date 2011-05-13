#!/usr/bin/python
# -*- coding: utf-8 -*-
import sprite
import pygame.image
import os

import terrain

class Terrain(terrain.Terrain):
    image = pygame.image.load(os.path.join("lib", "terrain", "ground.png"))
