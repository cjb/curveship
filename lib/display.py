#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import itertools
import pygame
from pygame.locals import *

# Initialize global libs. Must be done before importing other modules.
pygame.init()
pygame.font.init()
pygame.display.set_mode((384, 384))
pygame.display.set_caption("Junk Jungle")
pygame.display.set_icon(pygame.image.load(os.path.join("lib", "effect", "icon.png")))

import sprite
import effect.gauge
import terrain
import effect.status


class Display:
    """Display-related code"""

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.get_surface()
        self.tiles = pygame.sprite.RenderUpdates()
        self.sprites = sprite.SortedUpdates()
        self.shadows = pygame.sprite.RenderUpdates()
        self.overlay = pygame.sprite.RenderUpdates()
        self.effects = pygame.sprite.RenderUpdates()
        self.hud = pygame.sprite.RenderUpdates()
        self.scrollpos = [0, 0]
        self.key_pressed = None
        self.hud.add(effect.gauge.Gauge(self))

    def draw_map(self, level, rect=None):
        """Draw the background based on the provided map."""
        cache = {}
        background = pygame.Surface((level.w*24, level.h*16))
        background.fill((0, 0, 0))
        if rect is None:
            rect = Rect(0, 0, level.w, level.h)
        for y in range(rect.top, rect.bottom+1):
            for x in range(rect.left, rect.right+1):
                urls = level.get_content((x, y))
                for url in urls:
                    kind, name = url.split(".", 1)
                    if kind == 'terrain':
                        t = terrain.create((x, y), name, self, level)
                x += 1
            x = 0
            y += 1
        self.tiles.update()
        self.tiles.draw(background)
        self.background = background

    def add_sprite(self, *args):
        """Place a sprite taking scrolling into account"""

        for thing in args:
            try:
                sprite = thing.sprite
            except AttributeError:
                sprite = None
            if sprite is None:
                sprite = thing.Sprite(thing, self)
                thing.sprite = sprite
            self.sprites.add(sprite)
            self.shadows.add(sprite.shadow)
            #for bubble in sprite.bubbles.itervalues():
            #    self.effects.add(bubble)
            sprite.rect.move_ip(self.scrollpos[0], self.scrollpos[1])

    def scroll_after(self, rect):
        """Scrolls to keep the specified rectangle visible"""

        hscroll = 0
        vscroll = 0
        if rect.left < 48:
            hscroll = 3
        if rect.right > self.screen.get_width()-48:
            hscroll = -3
        if rect.top < 48:
            vscroll = 2
        if rect.bottom > self.screen.get_height()-48:
            vscroll = -2
        if hscroll or vscroll:
            self.scroll(hscroll, vscroll)
            self.refresh()

    def scroll(self, dx, dy):
        """Scroll the map by specified amount"""

        self.scrollpos[0] += dx
        self.scrollpos[1] += dy
        sprites = itertools.chain(self.tiles, self.sprites, self.effects,
                                  self.shadows, self.overlay)
        for sprite in sprites:
            sprite.rect.move_ip(dx, dy)

    def clear_func(self, screen, rect):
        """
        Clean up after sprites, taking scrolling into account and
        handling sprites that are out of map.
        """

        source = rect.move(-self.scrollpos[0], -self.scrollpos[1])
        if not self.background.get_rect().contains(source):
            screen.fill((0, 0, 0), rect)
        screen.blit(self.background, rect, source)

    def refresh(self):
        """Redraw the whole level"""

        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, self.scrollpos)
        self.shadows.draw(self.screen)
        self.sprites.draw(self.screen)
        self.overlay.draw(self.screen)
        self.effects.draw(self.screen)
        self.hud.draw(self.screen)
        pygame.display.flip()

    def update(self):
        """Redraw and update all the animated parts"""

#        self.hud.clear(self.screen, self.clear_func)
        self.effects.clear(self.screen, self.clear_func)
        self.sprites.clear(self.screen, self.clear_func)
        self.shadows.clear(self.screen, self.clear_func)
        self.sprites.update()
        self.shadows.update()
        self.effects.update()
#        self.hud.update()
        dirty = []
        dirty += self.shadows.draw(self.screen)
        dirty += self.sprites.draw(self.screen)
        self.overlay.draw(self.screen)
        dirty += self.effects.draw(self.screen)
#        dirty += self.hud.draw(self.screen)
        pygame.display.update(dirty)

    def show_frame(self):
        """Process a single frame of the game loop."""

        # Update the screen
        self.update()
        self.clock.tick(20)
        # Process input
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN:
                self.key_pressed = event.key

