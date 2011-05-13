#!/usr/bin/python
# -*- coding: utf-8 -*-

import sprite
import util
import monster

class DropError(Exception):
    def __init__(self, pos, item):
        self.pos = pos
        self.item = item

def create(level, kind):
    """Create an item object of specified kind."""
    module = __import__("item.%s" % kind, globals(), {}, ["Item"])
    return module.Item(level)

class Item(object):
    can_pick = True
    can_push = False
    block = False
    Sprite = sprite.Item

    def __init__(self, level):
        self.pos = None
        self.level = level
        self.sprite = None

    def place(self, pos):
        """Put the item on specified map square"""
        try:
            del self.level.items[self.pos]
        except KeyError:
            pass
        if pos in self.level.items:
            raise DropError(pos, self)
        self.pos = pos
        self.level.items[pos] = self
        if self.sprite and not self.sprite.on_floor:
            self.sprite.place(pos)

    def drop(self, pos):
        """Drop the item on specified map square, with animation"""
        self.place(pos)
        # XXX Evil hack
        self.level.player.display.add_sprite(self)
        self.sprite.anim = self.sprite.anim_drop()

    def pick(self):
        """Pick up the item"""
        try:
            del self.level.items[self.pos]
        except KeyError:
            pass
        self.sprite.anim = self.sprite.anim_pick()
        self.sprite.on_floor = False
        return self

    def push(self, facing):
        """Push the item in specified direction."""
        pos = (self.pos[0]+util.delta_x[facing],
               self.pos[1]+util.delta_y[facing])
        if (self.level.is_blocked(pos) or self.level.items.get(pos)
            or self.level.monsters.get(pos)):
            raise monster.MoveBlocked(pos)
        self.sprite.anim = self.sprite.anim_push(facing)
        self.place(pos)
