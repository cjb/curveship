#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import monster

class Mob(monster.Monster):
    name = "bat"
    max_hp = 3

    def act(self, level):
        direction = random.randint(1, 4)
        try:
            try:
                self.walk(direction)
            except monster.MoveBump, e:
                if e.monster == self.level.player:
                    self.attack(direction, e.monster)
        except monster.MoveError:
            pass

    def die(self):
        monster.Monster.die(self)
