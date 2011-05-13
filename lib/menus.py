#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import sys

class Menu(object):
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.saved = self.screen.copy()
        self.background = self.screen.copy()
        self.clock = pygame.time.Clock()

    def fade_out(self):
        black = pygame.Surface(self.screen.get_size())
        black.fill((0, 0, 0))
        for step in range(0, 192, 30):
            self.clock.tick(20)
            self.background.blit(self.saved, (0, 0))
            black.set_alpha(step)
            self.background.blit(black, (0, 0))
            self.update()
            self.refresh()

    def fade_in(self):
        black = pygame.Surface(self.screen.get_size())
        black.fill((0, 0, 0))

        for step in range(0, 192, 30):
            self.clock.tick(20)
            self.background.blit(self.saved, (0, 0))
            black.set_alpha(192-step)
            self.background.blit(black, (0, 0))
            self.update()
            self.refresh()


    def run(self):
        self.fade_out()
        pygame.event.clear(pygame.locals.KEYDOWN)
        self.exit = False
        while not self.exit:
            self.update()
            self.clock.tick(20)
            for event in pygame.event.get():
                if event.type==pygame.locals.QUIT:
                    sys.exit(0)
                elif event.type==pygame.locals.KEYDOWN:
                    self.key(event.key)
        while pygame.event.wait().type != pygame.locals.KEYUP:
            pass
        self.fade_in()

    def key(self, key):
        if key==pygame.locals.K_x:
            self.exit = True
        elif key == pygame.locals.K_ESCAPE:
            sys.exit(0)

    def update(self):
        pass

    def refresh(self):
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()
