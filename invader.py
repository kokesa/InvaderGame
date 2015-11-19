import pygame
import abc
import PatternMovement
import collision
import math
from Vector2D import *
from GameManager import *
from pygame.locals import *
from abc import ABCMeta, abstractmethod
from PatternMovement import *
from collision import *

INVADER_NORMAL_MOVE_SPEED = 110
INVADER_NORMAL_SHOT_SPEED = 100
INVADER_NORMAL_SHOT_RATE = 50
INVADER_NORMAL_SHOT_POWER = 10
INVADER_NORMAL_HP = 10
INVADER_NORMAL_REST_SHOT = 50

NORMAL_RASER_DURATION_TIME = 60
NORMAL_RASER_INTERVAL = [200, 300]
NORMAL_RASER_POWER = 10

STEERING_FORCE = 0.3

class InvaderShot(object):
    entity_type = "invader_shot"
    entity_shape = "circle"
    frame_no = 0
    animation_rate = 2
    def __init__(self, image_list, x, y, speed, power):
        self.image_list = image_list
        self.num_of_frame = len(image_list)
        self.image = image_list[self.frame_no]
        self.width, self.height = image_list[0].get_size()
        self.radius = self.height / 2
        self.move_speed = speed
        self.shot_power = power
        self.x = x + self.width / 2 + 2.5
        self.y = y + self.height / 2
       
    def set_shot_power(self, power):
        self.shot_power = power
        
    def set_shot_speed(self, speed):
        self.shot_speed = speed
       
    def move(self, time_passed_seconds):
        self.y += self.move_speed * time_passed_seconds
    
    def is_collide_with(self, entity):
        if is_collide_with(self, entity):
            if entity.entity_type == "player":
                player = entity
                player.damaged(self.shot_power)
                return True
        else:
            return False
    
    def update_frame(self):
        self.frame_no += 1
        self.image = self.image_list[self.frame_no/self.animation_rate%self.num_of_frame]
        
    def update(self, time_passed_seconds):
        self.update_frame()
        self.move(time_passed_seconds)
    
    def draw(self, surface):
        surface.blit(self.image, (self.x - self.width / 2 - 2.5, self.y - self.height / 2))
      
class ChaseInvaderShot(InvaderShot):
    entity_type = "chase_shot"
    def __init__(self, image_list, x, y, speed, power):
        InvaderShot.__init__(self, image_list, x, y, speed, power)
        self.heading = Vector2D(0, 1)
    
    def set_target(self, target):
        self.target = target
    
    def calculate_force(self):
        self.force = 0
        steering_force = STEERING_FORCE
        position = Vector2D(self.x, self.y)
        target_position = Vector2D(self.target.x, self.target.y)
        r_position = target_position - position
        heading_angle = get_angle_from_vector(self.heading)
        r_angle = get_angle_from_vector(r_position)
        diff_angle = abs(r_angle - heading_angle)
        local_position = rotate_vector(r_position, 90-heading_angle)
        if local_position.y > 0:
            if local_position.x > 0:
                m = +1
            elif local_position.x < 0:
                m = -1
            else:
                m = 0
            self.force = m * diff_angle * steering_force
        
    def move(self, time_passed_seconds):
        self.x += self.heading.x * self.move_speed * time_passed_seconds
        self.y += self.heading.y * self.move_speed * time_passed_seconds
        
    def update_heading(self):
        self.calculate_force()
        self.heading.x += self.force
        self.heading.normalize()
        
    def update(self, time_passed_seconds):
        self.update_frame()
        self.update_heading()
        self.move(time_passed_seconds)
        
class InvaderShotManager(object):
    shot_list = []
    def __init__(self, shot_image_dictionary, entity_list):
        self.shot_image_dictionary = shot_image_dictionary
        self.entity_list = entity_list
    
    def add(self, invader, speed, power):
        x, y = invader.get_position()
        if invader.invader_color == "white":
            shot_image_list = self.shot_image_dictionary["green"]
            invader_shot = InvaderShot(shot_image_list, x+5, y+invader.height-5, speed, power)
        elif invader.invader_color == "yellow":
            shot_image_list = self.shot_image_dictionary["orange"]
            invader_shot = InvaderShot(shot_image_list, x+5, y+invader.height-5, speed, power)
        elif invader.invader_color == "red":
            shot_image_list = self.shot_image_dictionary["red"]
            invader_shot = InvaderShot(shot_image_list, x+5, y+invader.height-5, speed, power)
        elif invader.invader_color == "blue":
            shot_image_list = self.shot_image_dictionary["blue"]
            invader_shot = InvaderShot(shot_image_list, x+5, y+invader.height-5, speed, power)
        elif invader.invader_color == "purple":
            shot_image_list = self.shot_image_dictionary["purple"]
            invader_shot = ChaseInvaderShot(shot_image_list, x+5, y+invader.height-5, speed, power)
            self.set_target(invader_shot)
        elif invader.invader_color == "black":
            shot_image_list = self.shot_image_dictionary["purple"]
            invader_shot = ChaseInvaderShot(shot_image_list, x+5, y+invader.height-5, speed, power)
            self.set_target(invader_shot)
        self.shot_list.append(invader_shot)
        
    def remove(self, entity, surface):
        surface_height = surface.get_height()
        for shot in self.shot_list:
            if shot.is_collide_with(entity):
                self.shot_list.remove(shot)
            elif shot.y - shot.height >= surface_height:
                self.shot_list.remove(shot)
    
    def collision(self):
        for entity in self.entity_list:
            for shot in self.shot_list:
                if entity.entity_type == "player":
                    player = entity
                    if shot.is_collide_with(player):
                        player.damaged(shot.shot_power)
                       # print "shot damaged"
                
    def set_target(self, chase_shot):
        for entity in self.entity_list:
            if entity.entity_type == "player":
                player = entity
                break
        chase_shot.set_target(player)        
                
    def update(self, entity, surface, time_passed_seconds):
        for shot in self.shot_list:
            shot.update(time_passed_seconds)
            if shot.entity_type == "chase_shot":
                self.set_target(shot)
        self.collision()
        self.remove(entity, surface)
            
    def draw(self, surface):
        for shot in self.shot_list:
            shot.draw(surface)
            
class Raser(object):
    entity_type = "raser"
    entity_shape = "rect"
    frame_no = 0
    animation_rate = 2
    image_index = 0
    duration_time = NORMAL_RASER_DURATION_TIME
    power = NORMAL_RASER_POWER
    def __init__(self, images, invader):
        self.images = images
        self.image = images[self.image_index]
        self.num_of_images = len(images)
        self.invader = invader
        self.width, self.height = self.image.get_size()
        self.x = invader.x - (self.width - invader.width) / 2
        self.y = invader.y + invader.height
    
    def is_collide_with(self, entity):
        if self.image_index == self.num_of_images - 2:
            if entity.entity_shape == "rect":
                if self.y <= entity.y:
                    if self.x <= entity.x and entity.x + entity.width <= self.x + self.width:
                        return True
                else:
                    return False
    
    def update_frame_no(self):
        self.frame_no += 1
        self.image_index = self.frame_no/self.animation_rate
        if self.image_index >= self.num_of_images - 2:
            self.image_index = self.num_of_images - 2
            self.image = self.images[self.image_index]
    
    def update_raser_position(self):
        self.x = self.invader.x - (self.width - self.invader.width) / 2
        self.y = self.invader.y + self.invader.height
    
    def update(self):
        self.update_frame_no()
        self.update_raser_position()
        
    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

class RaserManager(object):
    raser_list = []
    def __init__(self, images, entity_list):
        self.images = images
        self.raser_width = images[0].get_width()
        self.raser_height = images[1].get_height()
        self.entity_list = entity_list
    
    def add(self, invader):
        raser = Raser(self.images, invader)
        self.raser_list.append(raser)
        self.entity_list.append(raser)

    def remove(self):
        for raser in self.raser_list:
            if raser.frame_no >= raser.duration_time:
                self.raser_list.remove(raser)
     
    def collision(self):
        for entity in self.entity_list:
            for raser in self.raser_list:
                if raser.is_collide_with(entity):
                    if entity.entity_type == "player":
                        player = entity
                        player.damaged(raser.power)
                       # print "raser damaged"
                
    def update(self):
        for raser in self.raser_list:
            raser.update()
        self.collision()
        self.remove()

    def draw(self, surface):
        for raser in self.raser_list:
            raser.draw(surface)

class Invader(object):
    __metaclass__ = ABCMeta
    entity_type = "invader"
    entity_shape = "rect" 
    frame_no = 0
    frame_change_rate = 30
    move_direction = "down" 
    invader_direction_dictionary = {}
    wait_frame_no = None
    is_display = True
    flashing = False
    flash_frame_no = None
    def __init__(self, invaders_dictionary, x, y, surface, pattern_movement_type="right_to_left"):
        self.invader_direction_dictionary["up"] = invaders_dictionary[0:2]
        self.invader_direction_dictionary["right"] = invaders_dictionary[2:4]
        self.invader_direction_dictionary["down"] = invaders_dictionary[4:6]
        self.invader_direction_dictionary["left"] = invaders_dictionary[6:8]
        self.image = self.invader_direction_dictionary[self.move_direction][0]
        self.width, self.height = self.image.get_size()
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.pattern_movement = PatternMovement(x, y, surface, pattern_movement_type)
        self.HP = INVADER_NORMAL_HP
        self.move_speed = INVADER_NORMAL_MOVE_SPEED
        self.shot_speed = INVADER_NORMAL_SHOT_SPEED
        self.shot_rate = INVADER_NORMAL_SHOT_RATE
        self.shot_power = INVADER_NORMAL_SHOT_POWER
        self.rest_shot_rate = INVADER_NORMAL_REST_SHOT
    
    def set_move_speed(self, move_speed):
        self.move_speed = move_speed
    
    def set_shot_speed(self, shot_speed):
        self.shot_speed = shot_speed
        
    def set_shot_rate(self, shot_rate):
        self.shot_rate = shot_rate
        
    def set_shot_power(self, shot_power):
        self.shot_power = shot_power
        
    def set_HP(self, HP):
        self.HP = HP
    
    def damaged(self, num):
        self.HP -= num
        self.flashing = True
        
    def get_position(self):
        return (self.x, self.y)
                
    def update_frame_no(self):
        self.frame_no += 1
        self.image = self.invader_direction_dictionary[self.move_direction][self.frame_no/self.frame_change_rate%2]
    
    def update_wait_frame_no(self):
        if self.wait_frame_no == None:
            self.wait_frame_no = 0
        else:
            self.wait_frame_no += 1
            
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
         
    def is_collide_with(self, entity):
        if is_collide_with(self, entity):
            return True
        else:
            return False
            
    def move(self, time_passed_seconds, surface):
        behavior = self.pattern_movement.pattern[self.pattern_movement.pattern_movement_id]
        self.move_direction = behavior.keys()[0]
        surface_width, surface_height = surface.get_size()
        if behavior.has_key("wait"):
            self.update_wait_frame_no()
            self.move_direction = "down"
            if not self.wait_frame_no <= behavior["wait"]:
                self.pattern_movement.pattern_movement_id += 1
                self.wait_frame_no = None
        if behavior.has_key("up"):
            self.y -= self.move_speed * time_passed_seconds
            if not abs(self.y - self.patern_movement.init_y) <= behavior["up"]:
                self.pattern_movement.pattern_movement_id += 1
            if self.y <= 0:
                self.y = 0
                self.pattern_movement.pattern_movement_id += 1
        if behavior.has_key("right"):
            self.x += self.move_speed * time_passed_seconds
            if not abs(self.x - self.pattern_movement.init_x) <= behavior["right"]:
                self.pattern_movement.init_x = self.x
                self.pattern_movement.pattern_movement_id += 1
            if self.x + self.width >= surface_width:
                self.x = surface_width - self.width
                self.pattern_movement.pattern_movement_id += 1
        if behavior.has_key("down"):
            self.y += self.move_speed * time_passed_seconds
            if not abs(self.y - self.pattern_movement.init_y) <= behavior["down"]:
                self.pattern_movement.pattern_movement_id += 1
            if self.y + self.height >= surface_height:
                self.y = surface_height - self.height
                self.pattern_movement.pattern_movement_id += 1
        if behavior.has_key("left"):
            self.x -= self.move_speed * time_passed_seconds
            if not abs(self.x - self.pattern_movement.init_x) <= behavior["left"]:
                self.pattern_movement.init_x = self.x
                self.pattern_movement.pattern_movement_id += 1
            if self.x <= 0:
                self.x = 0
                self.pattern_movement.pattern_movement_id += 1
        if self.pattern_movement.pattern_movement_id >= self.pattern_movement.pattern_length:
            self.pattern_movement.pattern_movement_id = 0
    
    def update(self, time_passed_seconds, surface):
        self.update_frame_no()
        self.move(time_passed_seconds, surface)
        self.flash()
        
    @abstractmethod
    def shot(self):
        pass
        
    def draw(self, surface):
        if self.is_display:
            surface.blit(self.image, (self.x, self.y), (0, 12, self.width, self.height))

class WhiteInvader(Invader):
    invader_color = "white"
    shot_frame = 0
    shotting = True
    def __init__(self, invader_image, x, y, surface):
        Invader.__init__(self, invader_image, x, y, surface)

    def shot(self, shot_manager):
        ranNum = random.randint(0,100)
        if self.shotting and ranNum > self.rest_shot_rate:
            self.shot_frame += 1
            if self.shot_frame%self.shot_rate == 0:
                shot_manager.add(self, self.shot_speed, self.shot_power)
            
class YellowInvader(Invader):
    invader_color = "yellow"
    shot_frame = 0
    shotting = True
    def __init__(self, invader_image, x, y, surface):
        Invader.__init__(self, invader_image, x, y, surface)
        self.move_speed = INVADER_NORMAL_MOVE_SPEED / 3
        self.shot_spedd = INVADER_NORMAL_SHOT_SPEED * 1 / 2
        self.HP = INVADER_NORMAL_HP * 5
        
    def shot(self, shot_manager):
        ranNum = random.randint(0,100)
        if self.shotting and ranNum > self.rest_shot_rate:
            self.shot_frame += 1
            if self.shot_frame%self.shot_rate == 0:
                shot_manager.add(self, self.shot_speed, self.shot_power)
                
class RedInvader(Invader):
    invader_color = "red"
    shot_frame = 0
    shotting = True
    def __init__(self, invader_image, x, y, surface):
        Invader.__init__(self, invader_image, x, y, surface)
        self.move_speed = INVADER_NORMAL_MOVE_SPEED * 3
        self.shot_speed = INVADER_NORMAL_SHOT_SPEED * 3
        self.shot_power = INVADER_NORMAL_SHOT_POWER * 2
        self.HP = INVADER_NORMAL_HP / 2 * 3
        self.rest_shot_rate = 40
        self.shot_rate = INVADER_NORMAL_SHOT_RATE * 2 / 3

    def shot(self, shot_manager):
        ranNum = random.randint(0,100)
        if self.shotting and ranNum > self.rest_shot_rate:
            self.shot_frame += 1
            if self.shot_frame%self.shot_rate == 0:
                shot_manager.add(self, self.shot_speed, self.shot_power)
                
class BlueInvader(Invader):
    invader_color = "blue"
    shot_frame = 0
    shotting = True
    def __init__(self, invader_image, x, y, surface):
        Invader.__init__(self, invader_image, x, y, surface)
        self.shot_rate = INVADER_NORMAL_SHOT_RATE / 4
        self.shot_power = INVADER_NORMAL_SHOT_POWER / 2

    def shot(self, shot_manager):
        if self.shotting:
            self.shot_frame += 1
            if self.shot_frame%self.shot_rate == 0:
                shot_manager.add(self, self.shot_speed, self.shot_power)
                
class PurpleInvader(Invader):
    invader_color = "purple"
    shot_frame = 0
    shotting = True
    def __init__(self, invader_image, x, y, surface):
        Invader.__init__(self, invader_image, x, y, surface)
        self.HP = INVADER_NORMAL_HP * 3

    def shot(self, shot_manager):
        if self.shotting:
            self.shot_frame += 1
            if self.shot_frame%self.shot_rate == 0:
                shot_manager.add(self, self.shot_speed, self.shot_power)
                
class BlackInvader(Invader):
    invader_color = "black"
    shot_frame = 0
    shotting = True
    raser_shot_interval = NORMAL_RASER_INTERVAL[1]
    last_raser_shot_time = 0
    raser_duration_time = NORMAL_RASER_DURATION_TIME
    def __init__(self, invader_image, x, y, surface):
        Invader.__init__(self, invader_image, x, y, surface)
        self.shot_rate = INVADER_NORMAL_SHOT_RATE / 2
        self.shot_power = INVADER_NORMAL_SHOT_POWER * 2
        self.shot_speed = INVADER_NORMAL_SHOT_SPEED * 2
        self.move_speed = INVADER_NORMAL_MOVE_SPEED * 4
        self.HP = INVADER_NORMAL_HP * 5

    def shot(self, shot_manager):
        ranNum = random.randint(0,100)
        if self.shotting and ranNum > self.rest_shot_rate:
            self.shot_frame += 1
            if self.shot_frame%self.shot_rate == 0:
                shot_manager.add(self, self.shot_speed, self.shot_power)
                
    def shot_raser(self ,raser_manager):
        if self.frame_no - self.last_raser_shot_time >= self.raser_shot_interval:
            self.shotting = False
            raser_manager.add(self)
            self.last_raser_shot_time = self.frame_no
           # self.raser_shot_interval = random.randint(NORMAL_RASER_INTERVAL[0],NORMAL_RASER_INTERVAL[1])
            
    def update(self, time_passed_seconds, surface):
        Invader.update(self, time_passed_seconds, surface)
        if self.frame_no - self.last_raser_shot_time >= self.raser_duration_time:
            self.shotting = True
    
class InvadersManager(object):
    invaders_list = []
    removed_invaders_list = []
    def __init__(self, invaders_dictionary, explode_effect_manager, invader_shot_manager, raser_manager, entity_list):
        self.invaders_dictionary = invaders_dictionary
        self.explode_effect_manager = explode_effect_manager
        self.invader_shot_manager = invader_shot_manager
        self.raser_manager = raser_manager
        self.entity_list = entity_list
    
    def add(self, invader_type, x, y, surface):
        if invader_type == "white":
            invader = WhiteInvader(self.invaders_dictionary[invader_type], x, y, surface)
        elif invader_type == "yellow":
            invader = YellowInvader(self.invaders_dictionary[invader_type], x, y, surface)
        elif invader_type == "red":
            invader = RedInvader(self.invaders_dictionary[invader_type], x, y, surface)
        elif invader_type == "blue":
            invader = BlueInvader(self.invaders_dictionary[invader_type], x, y, surface)
        elif invader_type == "black":
            invader = BlackInvader(self.invaders_dictionary[invader_type], x, y, surface)
        elif invader_type == "purple":
            invader = PurpleInvader(self.invaders_dictionary[invader_type], x, y, surface)  
        self.invaders_list.append(invader)
        self.entity_list.append(invader)
    
    def collision(self):
        for entity in self.entity_list:
            for invader in self.invaders_list:
                if entity.entity_type == "player":
                    player = entity
                    if invader.is_collide_with(player):
                        player.damaged(10)
                        #print "collide invader and player"
                        
    def remove(self):
        for invader in self.invaders_list:
            if invader.HP <= 0:
                self.explode_effect_manager.add(invader.x, invader.y, invader.width, invader.height)
                self.removed_invaders_list.append(invader)
                self.invaders_list.remove(invader)
    
    def shot(self):
        for invader in self.invaders_list:
            invader.shot(self.invader_shot_manager)
            if invader.invader_color == "black":
                invader.shot_raser(self.raser_manager)
    
    def get_invaders_list(self):
        return self.invaders_list
    
    def update(self, time_passed_seconds, surface):
        for invader in self.invaders_list:
            invader.update(time_passed_seconds, surface)
        self.shot()
        self.collision()
        self.remove()
            
    def draw(self, surface):
        for invader in self.invaders_list:
            invader.draw(surface)
            