#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import monster
import item
import util

class Mob(monster.Monster):
    name = "jello"
    max_hp = 3
    item = None

    def act(self, level):
        direction = random.randint(1, 4)
        try:
            try:
                self.walk(direction)
                if self.item is None:
                    item = self.level.items.get(self.pos)
                    if item and item.can_pick:
                        self.item = item
                        item.pick()
                        # XXX This code should be in monster's sprite!
                        # Superimpose the item image on all the frames
                        frames = self.sprite.frames
                        self.sprite.frames = []
                        item_image = item.sprite.image.copy()
                        item_image.set_alpha(92)
                        for row in frames:
                            line = []
                            for frame in row:
                                new_frame = frame.copy()
                                new_frame.blit(item_image, (0, 0))
                                line.append(new_frame)
                            self.sprite.frames.append(line)
                        del item_image
            except monster.MoveBump, e:
                if e.monster == self.level.player:
                    self.attack(direction, e.monster)
        except monster.MoveError:
            pass

    def die(self):
        monster.Monster.die(self)
        try:
            if self.item:
                self.item.place(self.pos)
                self.drop(i=self.item)
        except item.DropError, e:
            pass
