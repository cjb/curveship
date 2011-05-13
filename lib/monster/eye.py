#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import monster
import util

class Mob(monster.Monster):
    name = "eye"
    max_hp = 4

    def act(self, level):
        player = level.player
        dirs = util.dir_of(self.pos, player.pos)
        for direction in dirs:
            try:
                try:
                    self.walk(direction)
                    return
                except monster.MoveBump, e:
                    if e.monster == player:
                        self.attack(direction, e.monster)
                        return
            except monster.MoveError:
                pass
