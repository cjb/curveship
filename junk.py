#!/usr/bin/env python

#
#    Junk Jungle, an exploration game
#    Copyright (C) 2008  Radomir Dopieralski <junk@sheep.art.pl>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import os
import sys

# Make sure we are in the correct directory to load images
# and modules.
base_path = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(base_path, "lib"))
if base_path:
    os.chdir(base_path)

from game import Game

if __name__ == "__main__":
    Game().play_level()

