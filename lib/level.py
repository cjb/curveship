import pygame
from pygame.locals import *
import os
import re
import sys
import random

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

class CurveshipLevel(Level):
    def __init__(self, Main, preparer, world, discourse, display):
        self.main = Main
        self.world = world
        self.discourse = discourse
        self.preparer = preparer
        self.display = display
        self.w = 30
        self.h = 30
        self.rooms = {}
        self.room_by_pos = {}

        self.map = [[":" for i in range(self.w)] for j in range(self.h)]
        self.room_by_pos = [[None for i in range(self.w)] for j in range(self.h)]
        self.debug_map()
        self.create_map()

        self.blocking = []
        self.terrain = []
        self.monsters = {}
        self.items = {}
        self.map_key = {
            "X": ("terrain.wall",),
            ":": ("terrain.floor",),
            "@": ("terrain.floor", "monster.player"),
            ">": ("terrain.floor", "item.exit"),
        }
        self.place_monsters(self.map)

    def create_room(self, label, tl=[0,0], br=[0,0]):
        print tl, br
        if label in self.rooms:
            # we already created this room
            return

        # If we're called without coords, randomize.
        if not tl[0] and not br[0]:
            room_size = random.randint(2,3)
            if self.direction is "north":
                center_point = (self.pos[0], self.pos[1]-room_size)
            elif self.direction is "south":
                center_point = (self.pos[0], self.pos[1]+room_size)
            elif self.direction is "east":
                center_point = (self.pos[0]+room_size, self.pos[1])
            elif self.direction is "west":
                center_point = (self.pos[0]-room_size, self.pos[1])

            print "new center_point is %s %s" % (center_point[0], center_point[1])
            tl[0] = center_point[0] - room_size
            tl[1] = center_point[1] - room_size
            br[0] = center_point[0] + room_size
            br[1] = center_point[1] + room_size

        print "creating room %s from %s to %s" % (label, tl, br)
        # self.rooms[label] = [(x, y) for x in xrange(tl, br)
        #                             for y in xrange(tl, br)]
        self.rooms[label] = []
        for x in xrange(tl[0], br[0]+1):
            for y in xrange(tl[1], br[1]+1):
                # print "room coord %s %s" % (x, y)
                self.rooms[label].append([x, y])
                self.room_by_pos[x][y] = label

                if x is tl[0] or x is br[0]:
                    # print "edge piece"
                    if not (x is self.pos[0] and y is self.pos[1]):
                        self.map[y][x] = "X"
                if y is br[1] or y is tl[1]:
                    # print "edge piece"
                    if not (x is self.pos[0] and y is self.pos[1]):
                        self.map[y][x] = "X"

        return tl, br
        self.debug_map()

    def create_exit(self, oldlabel, newlabel, direction):
        # Get the midpoint tile of oldlabel's room
        print oldlabel
        room = self.rooms[oldlabel]
        mid = room[int(len(room) / 2)]
        (mid_x, mid_y) = mid

        # First, create a floor space for the character to walk through.
        if direction is "north":
            newloc = (mid_x, room[0][1])
        if direction is "south":
            newloc = (mid_x, room[-1][1])
        if direction is "east":
            newloc = (room[-1][0], mid_y)
        if direction is "west":
            newloc = (room[0][0], mid_y)

        x, y = newloc
        # make it an exit tile
        self.map[y][x] = ">"

    def use_exit(self, pos, direction):
        self.pos = pos
        self.direction = direction

        print "pos is %s %s" % (pos[0], pos[1])
        print "Current room is %s" % self.room_by_pos[pos[0]][pos[1]]
        user_input = self.preparer.tokenize("leave " + direction, self.discourse.separator)

        self.main.handle_input(user_input, self.world, self.discourse, sys.stdin, sys.stdout)
        newroom = self.world.room_of(self.discourse.spin['focalizer'])

        self.create_room(str(newroom), [0,0], [0,0])
        for obj in newroom.children:
            if obj[0] == "part_of":
                room = self.rooms[str(newroom)]
                mid = room[int(len(room) / 2)]
                (mid_x, mid_y) = mid

                # Remove leading "@"
                i = item.create(self, obj[1][1:])
                i.place((mid_x, mid_y))
                self.display.draw_map(self)
                self.display.add_sprite(*(self.monsters.values()))
                self.display.add_sprite(*(self.items.values()))

    def debug_map(self):
        for line in self.map:
            print line

    def create_map(self):
        current_room = str(self.world.room_of(self.discourse.spin['focalizer']))

        # Put first room in the middle.
        tl = [((self.w/2)-4), (self.h/2)-4]
        br = [((self.w/2)+4), (self.h/2)+4]

        print "first room"
        self.pos = (self.w/2, self.h/2)
        self.create_room(current_room, tl, br)
        self.map[self.h/2][self.w/2] = "@"


        exits = self.world._exits(current_room)
        for an_exit in exits:
            self.create_exit(current_room, exits[an_exit], an_exit)
        # self.debug_map()

    def place_blocks(self):
        self.blocking = []
        for line in self.map:
            block_line = []
            for char in line:
                if char in self.map_key:
                    block_line.append(char in 'X*')
            if self.w < len(block_line):
                self.w = len(block_line)
            self.blocking.append(block_line)

    def place_monsters(self, m):
        """Place monsters on the map."""
        self.monsters = {}
        self.items = {}

        self.place_blocks()

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
