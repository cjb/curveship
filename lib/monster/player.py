import pygame
from pygame.locals import *
import os
import sys

import monster
import sprite
from effect import mesg
import util
import terrain

class Mob(monster.Monster):
    name = "player"
    max_hp = 10

    class Sprite(sprite.Monster):
        def __init__(self, monster, display):
            sprite.Monster.__init__(self, monster, display)
            self.depth += 1 # Display in front of all other creatures
            self.old_facing = self.facing

        def animate(self, delay=1, frames=None):
            """Player has more frames and facing."""
            sprite.Monster.animate(self, delay, self.frames[self.facing-1])

        def anim_stand(self):
            """Player is not animated when standing."""
            self.image = self.frames[self.facing-1][0]
            yield None

        def anim_walk(self):
            dx = util.delta_x[self.facing]*3
            dy = util.delta_y[self.facing]*2
            self.move(dx, dy)
            steps = 7
            if self.facing == self.old_facing % 4+1:
                # rotate CW
                self.image = self.frames[self.facing-1+4][0]
                self.frame = 0
                yield None
            elif self.facing == (self.old_facing-2) % 4+1:
                # rotate CCW
                self.image = self.frames[self.old_facing-1+4][0]
                self.frame = 0
                yield None
            elif self.facing == (self.old_facing-3) % 4+1:
                # turn back
                self.image = self.frames[(self.facing+1) % 4+4][0]
                yield None
                self.move(dx, dy)
                self.image = self.frames[self.facing % 4][0]
                yield None
                self.move(dx, dy)
                self.image = self.frames[self.facing % 4+4][0]
                self.frame = 0
                yield None
                steps = 5
            else:
                # just continue walking
                self.animate()
                yield None
            self.old_facing = self.facing
            for step in range(steps):
                self.move(dx, dy)
                self.animate()
                yield None

        def anim_attack(self):
            """Player attacks first, no delay."""
            self.frame = 0
            self.image = self.frames[self.facing-1+4][0]
            dx = util.delta_x[self.facing]*6
            dy = util.delta_y[self.facing]*4
            for step in range(2):
                self.move(dx, dy, 1)
                yield None
            for step in range(2):
                self.move(-dx, -dy, -1)
                self.animate()
                yield None

        def anim_die(self):
            for d in (2, 6, 1, 5, 0, 4, 3, 7, 2):
                self.image = self.frames[d][0]
                yield None
            self.shadow.kill()
            self.kill()


    def __init__(self, pos, level):
        monster.Monster.__init__(self, pos, level)
        self.inventory = []

    def attack(self, facing, monster):
        self.sprite.facing = facing
        self.sprite.anim = self.sprite.anim_attack()
        damage = 1
        mesg.Mesg(self.display, monster.sprite, "%d" % damage,
                  color=(255, 128, 0))
        monster.hit(damage)

    def hit(self, damage=5):
        mesg.Mesg(self.display, self.sprite, "%d" % damage,
                  color=(255, 0, 0), delay=4)
        self.hp -= damage

    def walk(self, facing):
        monster.Monster.walk(self, facing)
        item = self.level.items.get(self.pos, None)
        if item and item.can_pick:
            self.inventory.append(item.pick())
            mesg.Mesg(self.display, item.sprite, item.name, delay=12)

    def act(self, level):
        pass
