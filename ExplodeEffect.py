import pygame
import collision
from pygame.locals import *
from collision import *

NORMAL_EXPLOSION_DAMAGE = 50

class ExplodeEffect(object):
    entity_type = "explosion"
    entity_shape = "rect"
    frame_no = 0
    image_index = 0
    animation_rate = 2
    def __init__(self, images, invader_x, invader_y, invader_width, invader_height):
        self.images = images
        self.image = images[self.image_index]
        self.width, self.height = self.image.get_size()
        self.x = invader_x - (self.width - invader_width) / 2
        self.y = invader_y - (self.height - invader_height) / 2
        self.num_of_image_index = len(images)
        
    def is_collide_with(self, entity):
        if is_collide_with(self, entity):
            return True
        else:
            return False
        
    def is_end(self):
        if self.image_index + 1 == self.num_of_image_index:
            return True
        else:
            return False      
    
    def update_frame_no(self):
        self.frame_no += 1
        self.image_index = self.frame_no / self.animation_rate
       
    def update_image(self):
        if not self.is_end():
            self.image = self.images[self.image_index]
        
    def update(self):
        self.update_frame_no()
        self.update_image()
        
    def draw_explode_effect(self, surface):
        surface.blit(self.image, (self.x, self.y))

class ExplodeEffectManager(object):
    explode_effect_list = []
    def __init__(self, images, entity_list):
        self.images = images
        self.entity_list = entity_list
    
    def add(self, x, y, w, h):
        explode_effect = ExplodeEffect(self.images, x, y, w, h)
        self.explode_effect_list.append(explode_effect)
        self.entity_list.append(explode_effect)
        
    def collision(self):
        for entity in self.entity_list:
            for explode_effect in self.explode_effect_list:
                if entity.entity_type == "invader":
                    invader = entity
                    if explode_effect.is_collide_with(invader):
                        #invader.damaged(NORMAL_EXPLOSION_DAMAGE)
                       # print "invader explosion damaged"
                       pass
        
    def update(self):
        for explode_effect in self.explode_effect_list:
            explode_effect.update()
            if explode_effect.is_end():
                self.explode_effect_list.remove(explode_effect)
        self.collision()
            
    def draw_explode_effect(self, surface):
        for explode_effect in self.explode_effect_list:
            explode_effect.draw_explode_effect(surface)
            
    
        