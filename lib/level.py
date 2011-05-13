import pygame
from pygame.locals import *
import os
import re

import item
import monster

class Level(object):
    def __init__(self):
        self.items = []
        self.monsters = []
        self.terrain = []

    def is_floor(self, pos):
        """Used by the wall tiles to tell whether neighbouring
           squares contain floor tiles.
        """
        return not self.is_blocked(pos)

    def is_blocked(self, pos):
        """Used by the creatures to check whether they can move there"""
        x, y = pos
        if x < 0 or y < 0:
            return True
        try:
            return self.blocking[y][x]
        except IndexError:
            return True

class StaticLevel(Level):
    def __init__(self):
        self.static_map()
        self.place_monsters(self.map)

    def place_monsters(self, m):
        """Place monsters on the map."""

        self.monsters = {}
        self.items = {}
        for y, line in enumerate(m):
            for x, tile in enumerate(line):
                urls = self.map_key[tile]
                if urls:
                    for url in urls[1:]:
                        kind, name = url.split(".", 1)
                        if kind == "monster":
                            m = monster.create(self, (x, y), name)
                            if name == 'player':
                                self.player = m
                            m.place((x, y))
                        elif kind == "item":
                            i = item.create(self, name)
                            i.place((x, y))
                        elif kind == "status":
                            self.monsters[(x, y)].add_status(name)

    def static_map(self):
        """A mockup of a level map."""
        self.map_key = {
            "X": ("terrain.wall",),
            "*": ("terrain.cliff",),
            ":": ("terrain.floor",),
            ".": ("terrain.ground",),
            ",": ("terrain.corridor",),
            "O": ("terrain.floor", "monster.eye"),
            "S": ("terrain.floor", "monster.skeleton"),
            "M": ("terrain.floor", "monster.jello"),
            "Z": ("terrain.floor", "monster.zombie"),
            "R": ("terrain.ground", "monster.robot"),
            "B": ("terrain.floor", "monster.beast", "status.asleep"),
            "C": ("terrain.floor", "monster.cat"),
            "V": ("terrain.floor", "monster.bat"),
            "@": ("terrain.floor", "monster.player", "item.up"),
            "&": ("terrain.floor", "item.box"),
            "%": ("terrain.floor", "item.chest"),
            "/": ("terrain.floor", "item.wrench"),
            "!": ("terrain.floor", "item.hammer"),
            "~": ("terrain.floor", "item.chainsaw"),
            "+": ("terrain.floor", "item.firstaid"),
            ">": ("terrain.floor", "item.down"),
        }
        self.map = (
            "XXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXX::::::XXX::::::X",
            "XX::::XXXX:::R::X..::M:::X",
            "XX:V::XXXX::V:::X.*::::::X",
            "XX::::XXXX::::::X.*::::::X",
            "XX~::@....::/:::..*::::::X",
            "XX::::XXXX::::::***:::Z::X",
            "XXX.XXXXXXXXX.*****::::::X",
            "XXX...XXXXXXX.*******.XXXX",
            "XXXXX.XXXX:%:::::****.XXXX",
            "X:::::::XX:::::::**:::::XX",
            "X:::::::XX::V::::..::!::XX",
            "X::%::::XX::::>::XXO::::XX",
            "X::::+::..:::::::XX:::&:XX",
            "X:::::::XXXXX.XXXXX:::::XX",
            "X:::::::XXXXX.XXXXX:::::XX",
            "X:::::M:XXXXX.XXXXXXXX.XXX",
            "XX.XXXXXXXXX..XXXXXXXX.XXX",
            "XX.XXXXXXXXX.XXXXXXX:::::X",
            "X::::::XXX::::XXXXXX:::::X",
            "X::::::...::::XXXXXX:::::X",
            "X::::::XXX::::....XX::S::X",
            "XC:::::XXX::B:XXX.XX:::::X",
            "X::::::XXXXXXXXXX...:::::X",
            "X::::::XXXXXXXXXXXXX:::::X",
            "XXXXXXXXXXXXXXXXXXXXXXXXXX",
        )
        self.blocking = []
        self.terrain = []
        self.w = 0
        for line in self.map:
            block_line = []
            for char in line:
                if char in self.map_key:
                    block_line.append(char in 'X*')
            if self.w < len(block_line):
                self.w = len(block_line)
            self.blocking.append(block_line)
        self.h = len(self.map)

    def get_content(self, pos):
        """List all objects on given map square"""
        x, y = pos
        if x < 0 or y < 0:
            return ()
        try:
            m = self.map[y][x]
        except IndexError:
            return ()
        return self.map_key.get(m, ())
