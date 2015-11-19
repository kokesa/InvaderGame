import pygame
from pygame import *

PLAYER_NORMAL_HP = 5000

class PlayerShot(object):
    entity_type = "player_shot"
    entity_shape = "rect"
    def __init__(self, player, speed=300):
        self.width = 2
        self.height = 20
        self.x = player.x + player.width / 2 - self.width / 2
        self.y = player.y - 20
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.speed = speed
        
    def is_collide_with(self, entity):
        shot_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        entity_rect = pygame.Rect(entity.x, entity.y, entity.width, entity.height)
        return shot_rect.colliderect(entity_rect)
        
    def move(self, time_passed_seconds):
        self.y -= self.speed * time_passed_seconds
        
    def update(self, time_passed_seconds):
        self.move(time_passed_seconds)
        
    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 100), (self.x, self.y, self.width, self.height))

class PlayerShotManager(object):
    player_shot_list = []
    num_of_shot = 0
    num_of_shot_limitation = 20
    def __init__(self, entity_list):
        self.entity_list = entity_list
    
    def add(self, player, speed=300):
        if self.num_of_shot <= self.num_of_shot_limitation:
            self.player_shot_list.append(PlayerShot(player, speed))
            self.num_of_shot += 1
        
    def remove(self, invaders_manager):
        invaders_list = invaders_manager.get_invaders_list()
        for invader in invaders_list:
            for shot in self.player_shot_list:
                if shot.is_collide_with(invader):
                    invader.damaged(10)
                    self.player_shot_list.remove(shot)
                    self.num_of_shot -= 1
        for shot in self.player_shot_list:
            if shot.y + shot.height <= 0:
                self.player_shot_list.remove(shot)
                self.num_of_shot -= 1
                
    def update(self, time_passed_seconds, invaders_manager):
        for shot in self.player_shot_list:
            shot.update(time_passed_seconds)
        
        self.remove(invaders_manager)
        
    def draw(self, surface):
        for shot in self.player_shot_list:
            shot.draw(surface)

class Player(object):
    entity_type = "player"
    entity_shape = "rect"
    
    flashing = False
    flash_frame_no = None
    
    is_display = True
    def __init__(self, image, init_x, init_y, player_shot_manager, speed=200):
        self.x = init_x
        self.y = init_y
        self.image = image
        self.width, self.height = image.get_size()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.player_shot_manager = player_shot_manager
        self.speed = speed
        self.HP = PLAYER_NORMAL_HP
    
    def update_flash_frame_no(self):
        if self.flash_frame_no == None:
            self.flash_frame_no = 0
        else:
            self.flash_frame_no += 1
            
    def flash(self, interval=5, duration=50):
        self.update_flash_frame_no()
        if self.flashing:
            if self.flash_frame_no % interval == 0:
                if self.is_display:
                    self.is_display = False
                else:
                    self.is_display = True
            if self.flash_frame_no >= duration:
                self.flashing = False
                self.flash_frame_no = None
                self.is_display = True

    def move(self, time_passed_seconds, surface):
        surface_width, surface_height = surface.get_size()
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.y -= self.speed * time_passed_seconds
        if pressed_keys[K_RIGHT]:
            self.x += self.speed * time_passed_seconds
        if pressed_keys[K_DOWN]:
            self.y += self.speed * time_passed_seconds
        if pressed_keys[K_LEFT]:
            self.x -= self.speed * time_passed_seconds
        
        if self.x < 0:
            self.x = 0
        if self.x + self.width > surface_width:
            self.x = surface_width - self.width
        if self.y < 0:
            self.y = 0
        if self.y + self.height > surface_height:
            self.y = surface_height - self.height
    
    def damaged(self, point):
        self.HP -= point
        self.flashing = True
    
    def shot(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_SPACE]:
            self.player_shot_manager.add(self)
           
    def update(self, time_passed_seconds, surface):
        self.move(time_passed_seconds, surface)
        self.shot()
            
    def draw(self, surface):
        if self.is_display:
            surface.blit(self.image, (self.x, self.y))