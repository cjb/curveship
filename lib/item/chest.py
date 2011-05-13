#!/usr/bin/python
# -*- coding: utf-8 -*-

import item

class Item(item.Item):
    name = "chest"
    can_pick = False
    can_push = False
    block = False
