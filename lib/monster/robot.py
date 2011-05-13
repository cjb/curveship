#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import monster

class Mob(monster.Monster):
    name = "robot"
    max_hp = 7

    def __init__(self, pos, level):
        monster.Monster.__init__(self, pos, level)
        self.facing = random.randint(1, 4)

    def act(self, level):
        keep_trying = True
        while keep_trying:
            try:
                try:
                    self.walk(self.facing)
                    keep_trying = False
                except monster.MoveBump, e:
                    self.attack(self.facing, e.monster)
                    keep_trying = False
                    self.facing = random.randint(1, 4)
            except monster.MoveError:
                self.facing = random.randint(1, 4)

    def hit(self, damage=5):
        monster.Monster.hit(self, damage)
        self.facing = random.randint(1, 4)
