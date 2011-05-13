#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Group the helper function and classes for sprite handling, and
the base classes for monster, item and effect sprites. Tightly
coupled with the display.py module and the sprites of particular
monsters items and effects.
"""

import pygame
from pygame.locals import *
import os

import effect.shadow
import effect.status
import util

FRAMES_CACHE = {}

def read_frames(filename, size=24, ysize=None):
    """Read an image and split it into frames. Cache results. """
    if ysize is None:
        ysize = size
    key = (size, ysize, filename)
    try:
        return FRAMES_CACHE[key]
    except KeyError:
        image = pygame.image.load(filename).convert()
        w, h = image.get_size()
        frames = []
        for x in range(0, w/size):
            frames.append([])
            for y in range(0, h/ysize):
                frames[x].append(image.subsurface((x*size, y*ysize, size, ysize)))
        FRAMES_CACHE[key] = frames
        return frames

class SortedUpdates(pygame.sprite.RenderUpdates):
    """Sprite group with a depth for controlling drawing order."""

    def sprites(self):
        """Return list of sprites sorted by depth"""
        sprite_list = self.spritedict.keys()
        sprite_list.sort(lambda a, b: a.depth-b.depth)
        return sprite_list


class Monster(pygame.sprite.Sprite):
    """Display the animated representation of a creature."""

    def __init__(self, monster, display):
        pygame.sprite.Sprite.__init__(self)
        self.display = display
        self.monster = monster
        self.name = monster.name
        pos = monster.pos
        self.frames = read_frames(os.path.join("lib", "monster",
                                               "%s.png" % self.name))
        self.frame = 0
        self.delay = 0
        self.facing = 3
        self.height = 0
        self.anim = self.anim_stand()
        self.image = self.frames[0][0]
        self.rect = self.image.get_rect()
        self.shadow = effect.shadow.Shadow(self)
        self.bubbles = {}
        self.place(pos)
        self.update()
        monster.sprite = self
        if monster.asleep:
            effect.status.Asleep(self)
        if monster.wounded:
            effect.status.Bandaid(self)

    def place(self, pos):
        """Place the sprite in specified square of map."""
        self.x, self.y = pos
        self.depth = self.y*16-12
        self.rect.midbottom = (self.x*24+12, self.y*16+12)
        #self.shadow.center(self)

    def move(self, dx, dy, dz=0):
        """Move the sprite by specified amount of pixels."""
        self.rect.move_ip(dx, dy-dz)
        self.depth += dy
        self.height += dz
        #self.shadow.center(self)

    def rotate(self, facing):
        """Change the animation frames to reflect facing."""
        self.old_facing = self.facing
        self.facing = facing

    def update(self):
        """Called for every frame before display"""
        try:
            self.anim.next()
        except StopIteration:
            self.anim = self.anim_stand()
            self.anim.next()

    def animate(self, delay=4, frames=None):
        if not frames:
            frames = self.frames[0]
        if self.delay >= delay:
            self.delay = 0
            self.frame += 1
            if self.frame >= len(frames):
                self.frame = 0
        else:
            self.delay += 1
            self.image = frames[self.frame]

    def anim_stand(self):
        """Animation of the monster standing in place."""
        while True:
            self.animate()
            yield None

    def anim_walk(self):
        """Animation of the monster walking around"""
        dx = util.delta_x[self.facing]*3
        dy = util.delta_y[self.facing]*2
        for step in range(8):
            self.move(dx, dy)
            self.animate()
            yield None

    def anim_attack(self):
        """Aniamtion of the monster attacking something"""
        dx = util.delta_x[self.facing]*6
        dy = util.delta_y[self.facing]*4
        # Wait for the player attack.
        for step in range(4):
            self.animate()
            yield None
        for step in range(2):
            self.move(dx, dy, 1)
            self.animate()
            yield None
        for step in range(2):
            self.move(-dx, -dy, -1)
            self.animate()
            yield None

    def anim_die(self):
        """Animation of the monster dying"""
        saved = self.image
        self.shadow.kill()
        for bubble in self.bubbles.itervalues():
            bubble.kill()
        for a, z in zip(range(255, 0, -34), range(8)):
            self.image = saved.subsurface((0, 0, 24, 24-z*3))
            self.image.set_alpha(a)
            self.move(0, 0, -3)
            yield None
        self.image = saved
        self.kill()

class Item(pygame.sprite.Sprite):
    """Display the representation of an item."""

    def __init__(self, item, display):
        pygame.sprite.Sprite.__init__(self)
        self.display = display
        self.item = item
        pos = item.pos
        self.name = item.name
        self.frames = read_frames(os.path.join("lib", "item",
                                               "%s.png" % self.name))
        self.image = self.frames[0][0]
        self.rect = self.image.get_rect()
        self.anim = None
        self.delay = 0
        self.frame = 0
        self.height = -8
        self.on_floor = False
        self.shadow = effect.shadow.Shadow(self)
        self.bubbles = {}
        self.update()
        if pos:
            self.place(pos)

    def place(self, pos):
        """Place the sprite on specified map square."""
        self.x, self.y = pos
        self.depth = self.y*16-20
        self.on_floor = True
        self.rect.center = (self.x*24+12, self.y*16+3)
        #self.shadow.center(self)

    def move(self, dx, dy, dz=0):
        """Move sprite by specified amount of pixels."""
        self.rect.move_ip(dx, dy-dz)
        self.depth += dy
        self.height += dz
        #self.shadow.center(self)

    def update(self):
        """Called for every frame"""
        if self.anim:
            try:
                self.anim.next()
            except StopIteration:
                self.anim = None

    def anim_pick(self):
        """Animation of the item being picked up"""
        self.kill()
        self.add(self.display.effects)
        saved = self.image
        self.image = self.image.subsurface(self.image.get_rect())
        self.shadow.kill()

        for a, dz in zip(range(256, 0, -17), range(-7, 8)):
            self.move(0, 0, -dz)
            self.image.set_alpha(a)
            yield None
        self.kill()
        self.image = saved

    def anim_drop(self):
        """Animation of the item being dropped"""
        for a, dz in zip(range(256, 0, -17), range(-4, 5)):
            self.move(0, 0, -dz)
            yield None

    def anim_push(self, facing):
        """Animation of the item being pushed around"""
        dx = util.delta_x[facing]*3
        dy = util.delta_y[facing]*2
        for step in range(8):
            self.move(dx, dy, 0)
            yield None

