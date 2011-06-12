#!/usr/bin/python
# -*- coding: utf-8 -*-

import sprite
import item

class Item(item.Item):
    name = "exit"
    can_pick = False
    is_exit = True

    class Sprite(sprite.Item):
        def place(self, pos):
            sprite.Item.place(self, pos)
            self.depth = self.y*16-10
            self.shadow.offset = 5
