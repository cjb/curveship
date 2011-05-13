#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import monster
import util
import item

class Mob(monster.Monster):
    name = "zombie"
    max_hp = 5

    def act(self, level):
        player = level.player
        dirs = util.dir_of(self.pos, player.pos)
        # Randomly try horizontal or vertical movement
        direction = random.choice(dirs)
        try:
            try:
                self.walk(direction)
            except monster.MoveBump, e:
                if e.monster == player:
                    self.attack(direction, e.monster)
        except monster.MoveError:
            pass

    def die(self):
        monster.Monster.die(self)
        try:
            self.drop("firstaid")
        except item.DropError, e:
            pass
