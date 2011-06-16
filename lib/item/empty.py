#!/usr/bin/python
# -*- coding: utf-8 -*-

import sprite
import item

class Item(item.Item):
    name = "empty"
    can_pick = False
    is_exit = True
