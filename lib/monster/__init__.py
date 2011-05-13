#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import pygame.locals as pg
import os

import item
import sprite
import util
import effect.status

class MoveError(Exception):
    """Parent of all movement-related exceptions"""
    pass

class MoveBump(MoveError):
    """Exception risen when the visited location contains another monster"""
    def __init__(self, pos, monster):
        self.pos = pos
        self.monster = monster

    def __repr__(self):
        return "bump (%d, %d), %s" % (self.pos[0], self.pos[1], repr(self.monster))

class MoveBlocked(MoveError):
    """Exception risen when the visited location is blocking movement"""
    def __init__(self, pos):
        self.pos = pos

    def __repr__(self):
        return "block (%d, %d)" % (self.pos[0], self.pos[1])

class MovePush(MoveBlocked):
    """Exception risen when the visited location contains pushable object"""
    def __init__(self, pos, item):
        self.pos = pos
        self.item = item

    def __repr__(self):
        return "push (%d, %d), %s" % (self.pos[0], self.pos[1], self.item)


def create(level, pos, kind):
    """Create and place a monster of specified kind."""

    module = __import__("monster.%s" % kind, globals(), {}, ["Mob"])
    return module.Mob(pos, level)


class Monster(object):
    """Logical representation of the creature, stored on the map."""

    max_hp = 5
    Sprite = sprite.Monster

    def __init__(self, pos, level):
        self.hp = self.max_hp
        self.pos = pos
        self.level = level
        self.sprite = None
        self.asleep = False
        self.wounded = False

    def add_status(self, status):
        if status == 'asleep':
            self.asleep = True
        elif status == 'wounded':
            self.wounded = True

    def place(self, pos):
        """Place the monster on specified map square"""
        if self.level.is_blocked(pos):
            raise MoveBlocked(pos)
        item = self.level.items.get(pos, None)
        if item and item.can_push:
            raise MovePush(pos, item)
        monster = self.level.monsters.get(pos, None)
        if monster:
            raise MoveBump(pos, monster)
        try:
            del self.level.monsters[self.pos]
        except KeyError:
            pass
        self.pos = pos
        self.level.monsters[pos] = self

    def die(self):
        """Kill the monster"""
        try:
            del self.level.monsters[self.pos]
            self.sprite.anim = self.sprite.anim_die()
        except KeyError:
            pass

    def hit(self, damage=5):
        """Cause damage to the monster"""

        self.hp -= damage
        if not self.wounded:
            self.wounded = True
            effect.status.Wounded(self.sprite)
        if self.asleep:
            self.asleep = False
            try:
                self.sprite.bubbles['asleep'].kill()
                del self.sprite.bubbles['asleep']
            except KeyError:
                pass
        if self.hp <= 0:
            self.die()

    def wait(self):
        """Make the monster wait one turn"""
        self.sprite.anim = self.sprite.anim_stand()

    def walk(self, facing):
        """Make the monster walk in specified direction"""
        self.place((self.pos[0]+util.delta_x[facing],
                    self.pos[1]+util.delta_y[facing]))
        self.sprite.facing = facing
        self.sprite.anim = self.sprite.anim_walk()

    def attack(self, facing, monster):
        """Make the monster attack another monster in specified direction"""
        self.sprite.facing = facing
        self.sprite.anim = self.sprite.anim_attack()
        monster.hit()

    def drop(self, item_name="goo", i=None):
        """Make the monster drop a specified item"""
        if i is None:
            i = item.create(self.level, item_name)
        i.drop(self.pos)

    def act(self, level):
        if self.asleep:
            return True
