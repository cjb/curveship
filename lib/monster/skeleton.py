#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import monster
import item

class Mob(monster.Monster):
    name = "skeleton"
    max_hp = 3

    def act(self, level):
        direction = random.randint(1, 4)
        try:
            try:
                self.walk(direction)
            except monster.MoveBump, e:
                if e.monster == level.player:
                    self.attack(direction, e.monster)
        except monster.MoveError:
            pass

    def die(self):
        monster.Monster.die(self)
        try:
            self.drop("bones")
        except item.DropError, e:
            pass

