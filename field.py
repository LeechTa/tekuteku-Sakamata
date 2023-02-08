import pygame as pyg
from pygame import sprite
import os
import random as rand
import constant as cnst

pyg.init()


NUM_OF_FIELD_UNITS = 3
NUM_OF_FIELD_BLOCK = 4

class Obstruction(sprite.Sprite):
    def __init__(self,x,y,scale,img):
        sprite.Sprite.__init__(self)
        self.image = pyg.transform.scale(img,(int(img.get_width()*scale), int(img.get_height()*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.is_existence = True
        self.is_enemy_appear = False
        

    def draw(self,surface):
        if self.is_existence:
            surface.blit(self.image,self.rect)



class FieldUnit():
    def __init__(self,id,surface,left,width): #TODO:scaleの必要性
        self.id = id
        self.width = width
        self.obstruction_group = []
        OBSTRUCTION_DRAW_AREA = [cnst.SCREEN_HEIGHT-int(cnst.SCREEN_HEIGHT/(cnst.NUM_OF_OBSTRUCTION_PER_FIELDUNIT*2))*(i+1) for i in range(0,cnst.NUM_OF_OBSTRUCTION_PER_FIELDUNIT*2-1,cnst.NUM_OF_OBSTRUCTION_PER_FIELDUNIT-1)]
        
        self.rect = pyg.Rect(left,0,self.width,cnst.SCREEN_HEIGHT)
        self.rect.x += self.width*self.id
        
        num_of_obstruction = len(os.listdir(cnst.OBSTRUCTION_IMG_PATH))
        for i in range(num_of_obstruction):
            img = pyg.image.load(cnst.OBSTRUCTION_IMG_PATH+f'{i}.png').convert_alpha()
            scale = self.width/img.get_width()
            self.obstruction_group.append(Obstruction(self.rect.left,OBSTRUCTION_DRAW_AREA[i],scale,img))
        self.surface = surface
        

    def update(self):
        right = self.rect.right
        for obstruction in self.obstruction_group:
            obstruction.rect.right = right
            obstruction.draw(self.surface)
    
    


class FieldBlock():
    def __init__(self,id,surface):
        
        self.id = id
        self.rect = pyg.Rect(cnst.FIELD_BLOCK_WIDTH*self.id,0,cnst.FIELD_BLOCK_WIDTH,cnst.SCREEN_HEIGHT)
        self.field_unit_group = []
        self.obstruction_group = []
        field_unit_width = cnst.FIELD_BLOCK_WIDTH//NUM_OF_FIELD_UNITS
        for i in range(NUM_OF_FIELD_UNITS):
            field_unit = FieldUnit(i,surface,self.rect.left,field_unit_width)
            self.field_unit_group.append(field_unit)
            self.obstruction_group += field_unit.obstruction_group
        self.is_out_of_frame = False
        self.is_existence_of_all = []
        self.change_place_of_units([[1,0,0],[1,0,0],[1,0,0]])
        
        self.enemy_generate_area = None
        
        self.vel_x = cnst.NEAR_BG_VELOSITY_X
        self._dx_tmp = 0
        

    
    def change_place_of_units(self,is_existence_of_all=None):
        
        self.is_existence_of_all = is_existence_of_all
        if not(is_existence_of_all):
            pos_10 = bool(rand.randint(0,3))
            [pos_01,pos_02,pos_11,pos_21] = [bool(rand.randint(0,1)) for i in range(4)]
            self.is_existence_of_all = [
                [True,pos_01,pos_02],
                [pos_10,pos_11,not(pos_10)|pos_11],
                [not(pos_10|(pos_11&pos_21))| bool(rand.random()),pos_21,not(pos_21)] #[not(pos_10|(pos_11&pos_21))| bool(rand.randint(0,3)),pos_21,not(pos_21)]
                ]
        for idx_funit,field_unit in enumerate(self.field_unit_group):
            is_existence_of_units = self.is_existence_of_all[idx_funit]
            for idx_obst,obstruction in enumerate(field_unit.obstruction_group):
                try:
                    obstruction.is_existence = is_existence_of_units[idx_obst]
                except TypeError:
                    self.is_existence_of_all[idx_obst] = bool(self.is_existence_of_all[idx_obst])
                    obstruction.is_existence = is_existence_of_units[idx_obst]
            
    

    def move(self):
        dx = 0
        dx += self.vel_x + self._dx_tmp
        self._dx_tmp = dx - int(dx)
        if self.rect.right < 0:
            dx += self.rect.width*NUM_OF_FIELD_BLOCK
            self.is_out_of_frame = True
        self.rect.right += dx
        
    
    def update(self,is_move=True):
        
        if is_move:
            self.move()
        if self.is_out_of_frame:
            self.change_place_of_units()
            self.enemy_generate()
            self.is_out_of_frame = False
        left = self.rect.left
        for field_unit in self.field_unit_group:
            field_unit.rect.left = left
            field_unit.update()
            left = field_unit.rect.right

    def enemy_generate(self):
        area_indexes = []
        for idx_x,is_existence_of_unit in enumerate(self.is_existence_of_all):
            
            for idx_y,val in enumerate(is_existence_of_unit):
                if val:
                    area_indexes.append(idx_x*3+idx_y)
        self.enemy_generate_area = self.obstruction_group[rand.choice(area_indexes)]
