#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

from display import Display
from level import StaticLevel
from level import CurveshipLevel
from effect import mesg
import monster
import util
import item
import sys

class Game(object):
    def __init__(self):
        self.game_over = False
        self.display = Display()
        self.level = None

    def wait_for_command(self, player):
        """Wait for a single command from the player."""

        while True:
            key_pressed = self.display.key_pressed
            self.display.key_pressed = None
            keys = pygame.key.get_pressed()
            key = lambda k: keys[k] or key_pressed == k
            if key(K_SPACE):
                player.wait()
                return
            if key(K_ESCAPE):
                player.die()
                self.game_over = True
                return
            try:
                try:
                    if key(K_UP):
                        d = 1
                        player.walk(d)
                        return
                    elif key(K_DOWN):
                        d = 3
                        player.walk(d)
                        return
                    elif key(K_LEFT):
                        d = 4
                        player.walk(d)
                        return
                    elif key(K_RIGHT):
                        d = 2
                        player.walk(d)
                        return
                    elif key(K_x):
                        import menus
                        menus.Menu().run()
                        self.display.refresh()
                except monster.MoveBump, bump:
                    player.attack(d, bump.monster)
                    return
                except monster.MovePush, pushed:
                    pushed.item.push(d)
                    player.walk(d)
                    return
            except monster.MoveError:
                mesg.Mesg(self.display, player.sprite, "blocked")
            self.display.show_frame()

    def static_level(self):
        """Play a Static level."""
        self.level = StaticLevel()
        self.play_level()

    def curve_level(self, Main, preparer, world, discourse):
        """Play a Curveship level."""

        self.level = CurveshipLevel(Main, preparer, world, discourse, self.display)
        self.play_level()

    def play_level(self):
        """Play a single level."""

        self.display.draw_map(self.level)
        self.display.add_sprite(*(self.level.monsters.values()))
        self.display.add_sprite(*(self.level.items.values()))
        # XXX The player character needs display for messages
        self.level.player.display = self.display
        self.display.refresh()
        while not self.game_over:
            self.wait_for_command(self.level.player)
            for monster in self.level.monsters.values():
                monster.act(self.level)
            for step in range(8): # Animate single turn
                self.display.scroll_after(self.level.player.sprite.rect)
                self.display.show_frame()
        sys.exit()


