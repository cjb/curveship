#!/usr/bin/python
# -*- coding: utf-8 -*-

import sprite
import item

class Item(item.Item):
    name = "up"
    can_pick = False

    class Sprite(sprite.Item):
        def place(self, pos):
            sprite.Item.place(self, pos)
            self.depth = self.y*16-16
            self.shadow.offset = 5
