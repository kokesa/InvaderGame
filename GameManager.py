invaders_image_name = "invaders.png"
white_invader_image_name = "whiteinvader.png"
yellow_invader_image_name = "yellowinvader.png"
red_invader_image_name = "redinvader.png"
blue_invader_image_name = "blueinvader.png"
black_invader_image_name = "blackinvader.png"
purple_invader_image_name = "purpleinvader.png"
player_image_name = "player.png"
explode_image_name = "explosion.png"
blue_shot_image_name = "blueshot.png"
red_shot_image_name = "redshot.png"
green_shot_image_name = "greenshot.png"
orange_shot_image_name = "orangeshot.png"
purple_shot_image_name = "purpleshot.png"
raser_image_name = "raser.png"
bg_image_name = "space.jpeg"

import pygame
import os
import random
import PatternMovement
import invader
import player
import ExplodeEffect
import collision
from pygame.locals import *
from PatternMovement import PatternMovement
from invader import *
from player import *
from ExplodeEffect import *
from collision import *
from sys import exit

DISPLAY_SIZE = (480, 640)

def split_image(image_name, num_of_col, num_of_row, init_col=0, init_row=0):
    """it divide image along with column and row"""
    splited_image_surf_list = []
    image_surf = pygame.image.load(os.path.join("images", image_name))
    image_surf = image_surf.convert_alpha()
    image_width, image_height = image_surf.get_size()
    splited_image_width = image_surf.get_width() / num_of_col
    splited_image_height = image_surf.get_height() / num_of_row
    splited_image_init_x = splited_image_width * init_col
    splited_image_init_y = splited_image_height * init_row
    
    for i in range(0, image_height, splited_image_height):
        for j in range(0, image_width, splited_image_width):
            init_x = splited_image_init_x + j
            init_y = splited_image_init_y + i
            splited_image_width = splited_image_width
            splited_image_height = splited_image_height
            tmp_surf = pygame.Surface((splited_image_width, splited_image_height))
            tmp_surf.blit(image_surf, (0, 0),(init_x, init_y, splited_image_width , splited_image_height))
            color_key = tmp_surf.get_at((0, 0,))
            tmp_surf.set_colorkey(color_key, RLEACCEL)
            splited_image_surf_list.append(tmp_surf)
            
    return splited_image_surf_list
 
def make_invaders_dictionary():    
    dictionary = {}
    white_invader_list = split_image(white_invader_image_name, 2, 4)
    yellow_invader_list = split_image(yellow_invader_image_name, 2, 4)
    red_invader_list = split_image(red_invader_image_name, 2, 4)
    blue_invader_list = split_image(blue_invader_image_name, 2, 4)
    black_invader_list = split_image(black_invader_image_name, 2, 4)
    purple_invader_list = split_image(purple_invader_image_name, 2, 4)
    dictionary["white"] = tuple(white_invader_list)
    dictionary["yellow"] = tuple(yellow_invader_list)
    dictionary["red"] = tuple(red_invader_list)
    dictionary["blue"] = tuple(blue_invader_list)
    dictionary["black"] = tuple(black_invader_list)
    dictionary["purple"] = tuple(purple_invader_list)
    return dictionary

def make_shot_image_dictionary():
    dictionary = {}
    blue_shot_list = split_image(blue_shot_image_name, 3, 1)
    red_shot_list = split_image(red_shot_image_name, 3, 1)
    green_shot_list = split_image(green_shot_image_name, 3, 1)
    orange_shot_list = split_image(orange_shot_image_name, 3, 1)
    purple_shot_list = split_image(purple_shot_image_name, 3, 1)
    dictionary["blue"] = tuple(blue_shot_list)
    dictionary["red"] = tuple(red_shot_list)
    dictionary["green"] = tuple(green_shot_list)
    dictionary["orange"] = tuple(orange_shot_list)
    dictionary["purple"] = tuple(purple_shot_list)
    return dictionary
 
def make_images_dictionary():
    dictionary = {}
    explode_images = split_image(explode_image_name, 8, 1)
    dictionary["explode"] = explode_images
    invaders_dictionary = make_invaders_dictionary()
    dictionary["invader"] = invaders_dictionary
    shot_image_dictionary = make_shot_image_dictionary()
    dictionary["shot"] = shot_image_dictionary
    raser_image = split_image(raser_image_name, 7, 1)
    dictionary["raser"] = raser_image
    player_image = pygame.image.load(os.path.join("images", player_image_name))
    player_image = player_image.convert_alpha()
    dictionary["player"] = player_image
    bg_image = pygame.image.load(os.path.join("images", bg_image_name))
    bg_image = bg_image.convert_alpha()
    dictionary["back_ground"] = bg_image
    return dictionary
 
def get_random_color():
    num = random.randint(0, 5)
    if num == 0:
        return "white"
    elif num == 1:
        return "yellow"
    elif num == 2:
        return "red"
    elif num == 3:
        return "blue"
    elif num == 4:
        return "purple"
    elif num == 5:
        return "black"

class GameManager(object):
    entity_list = []
    def __init__(self, surface, images_dictionary):
        self.screen = surface
        self.images_dictionary = images_dictionary
        self.screen_width, self.screen_height = self.screen.get_size()
        self.bg_image = images_dictionary["back_ground"]
        self.sys_font = pygame.font.SysFont("systemfont", 30, True)
        self.game_over_message = self.sys_font.render("Game Over", True, (255,255,255))
        self.game_start_message = self.sys_font.render("Press Space Key to Start", True, (255,255,255))
        self.is_game_continue_message = self.sys_font.render('If you wanna play Again. Press "space" key.' ,True,(255,255,255))
        self.invaders_list = ["white","yellow","red","blue","purple","black"]
        self.score = 0
        self.isGameStart = False
        self.isGameOver = False
        self.isGameClear = False
    
    def timer_draw(self):
        self.passed_time = (pygame.time.get_ticks() - self.start_time) / 1000.0
        passed_time_surface = self.sys_font.render("Timer:%03.1f"%self.passed_time, True, (255,255,255))
        self.screen.blit(passed_time_surface, (0,0))
        
    def HP_draw(self):
        HP_surface = self.sys_font.render("HP:%03.f"%self.player.HP, True, (255,255,255))
        self.screen.blit(HP_surface,(0,20))
        
    def score_draw(self):
        score_surface = self.sys_font.render("Score:%0.f"%self.score, True, (255,255,255))
        self.screen.blit(score_surface, (10,DISPLAY_SIZE[1]))
    
    def calculate_score(self):
        for invader in self.invaders_manager.removed_invaders_list:
            color = invader.invader_color
            if color == "white":
                self.score += 10 / self.passed_time
            elif color == "yellow" or color == "red" or color == "blue":
                self.score += 30 / self.passed_time
            elif color == "purple":
                self.score += 50 / self.passed_time
            elif color == "black":
                self.score += 100 / self.passed_time
        self.score += self.player.HP
     
    def get_num_of_invaders(self):
        return len(self.invaders_manager.invaders_list)
        
    def game_start(self):
        self.timer = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        self.explode_effect_manager = ExplodeEffectManager(self.images_dictionary["explode"], self.entity_list)
        self.invader_shot_manager = InvaderShotManager(self.images_dictionary["shot"], self.entity_list)
        self.raser_manager = RaserManager(self.images_dictionary["raser"], self.entity_list)
        self.player_shot_manager = PlayerShotManager(self.entity_list)
        self.invaders_manager = InvadersManager(self.images_dictionary["invader"], self.explode_effect_manager,
                                                self.invader_shot_manager, self.raser_manager, self.entity_list)
        self.player = Player(self.images_dictionary["player"], DISPLAY_SIZE[0]/2, DISPLAY_SIZE[1]-50,
                             self.player_shot_manager, 200)
        self.entity_list.append(self.player)
        self.socre = 0
        self.isGameStart = False
        self.isGameOver = False
        self.isGameClear = False
        self.invader_type_index = 0
        self.make_stage(self.invaders_list[self.invader_type_index])
        
    def make_stage(self, invader_type):
        interval = random.randint(50,55)
        plumi = random.randint(-1,1)
        for i in range(0, 5):
            for j in range(0, 6):
                self.invaders_manager.add(invader_type, 10 + interval*j + i * plumi, 35 + 30*i, self.screen)
    
        
    def clear_screen(self):
        self.screen.fill((0, 0, 0))
        
    def update_timer(self):
        self.time_passed = self.timer.tick(60)
        self.time_passed_seconds = self.time_passed / 1000.0
        
    def update(self):
        
        if (not self.isGameStart):
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_SPACE]:
                pygame.time.wait(1000)
                self.game_start()
                self.isGameStart = True
            return
        
        if (self.isGameOver or self.isGameClear):
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_SPACE]:
                pygame.time.wait(1000)
                self.isGameStart = False
                self.isGameOver = False
                self.isGameClear = False
            return
        
        self.update_timer()
        self.invaders_manager.update(self.time_passed_seconds, self.screen)
        self.explode_effect_manager.update()
        self.invader_shot_manager.update(self.player, self.screen, self.time_passed_seconds)
        self.raser_manager.update()
        self.player.update(self.time_passed_seconds, self.screen)
        self.player_shot_manager.update(self.time_passed_seconds, self.invaders_manager)
        
        if (self.player.HP <= 0):
            self.isGameOver = True
            self.explode_effect_manager.add(self.player.x, self.player.y, self.player.width, self.player.height)
            self.game_end()
            return
            
        if (len(self.invaders_manager.invaders_list) == 0):
            self.invader_type_index += 1
            if (self.invader_type_index == len(self.invaders_list)):
                self.isGameClear = True
                self.calculate_score()
                self.game_end()
                return
            self.make_stage(self.invaders_list[self.invader_type_index])
        
    def under_draw(self):
        self.screen.unlock()
        self.screen.blit(self.bg_image, (0, 0))
        
    def draw(self):
        if not self.isGameStart:
            return
        self.invaders_manager.draw(self.screen)
        self.invader_shot_manager.draw(self.screen)
        self.raser_manager.draw(self.screen)
        self.player.draw(self.screen)
        self.player_shot_manager.draw(self.screen)
        self.explode_effect_manager.draw_explode_effect(self.screen)
        
    def over_draw(self):
        if (self.isGameOver):
            self.screen.blit(self.game_over_message,(180, DISPLAY_SIZE[1] / 2))
            self.screen.blit(self.is_game_continue_message,(25,DISPLAY_SIZE[1] / 2 + 20))
        elif (self.isGameClear):
 #           self.screen.blit(self.game_clear_message,(150, DISPLAY_SIZE[1] / 2))
            self.score_draw()
            self.screen.blit(self.is_game_continue_message,(25,DISPLAY_SIZE[1] / 2 + 10))
        elif (not self.isGameStart):
            #width, height = self.game_start_message.size
            self.screen.blit(self.game_start_message,(110, DISPLAY_SIZE[1] / 2))
        elif (self.isGameStart):
            self.timer_draw()
            self.HP_draw()
        
    def game_end(self):
        del self.entity_list[:]
        del self.invaders_manager.invaders_list[:]
        del self.invaders_manager.removed_invaders_list[:]
        del self.invader_shot_manager.shot_list[:]
        del self.player_shot_manager.player_shot_list[:]
        del self.explode_effect_manager.explode_effect_list[:]
        del self.raser_manager.raser_list[:]

def main():
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY_SIZE, 0, 32)
    pygame.display.set_caption("Invader Game")
    images_dictionary = make_images_dictionary()
    game_manager = GameManager(screen, images_dictionary)
    #game_manager.game_start()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
        game_manager.clear_screen()
        game_manager.update()
        game_manager.under_draw()
        game_manager.draw()
        game_manager.over_draw()
        pygame.display.update()
        
        
    
if __name__ == "__main__":
    main()