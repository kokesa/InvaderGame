#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "sasakitomohiro"
__date__ = "$2015/09/09 8:41:57$"

import pygame
import os
from pygame.locals import *
from sys import exit

def main():
    
    pygame.init()
    
    DISPLAY_SIZE = (640, 480)
    
    screen = pygame.display.set_mode(DISPLAY_SIZE, 0)
    pygame.set_caption("Tank Game")
    
    while(True):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
                
        

if __name__ == "__main__":
    main()
