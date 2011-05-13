#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import sprite
import item

class Item(item.Item):
    name = "box"
    can_pick = False
    can_push = True
    block = True
