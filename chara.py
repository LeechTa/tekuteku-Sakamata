import pygame as pyg
from pygame import sprite
import os
from constant import SCREEN_HEIGHT,FPS,GRAVITY
from collision_detector import Collider
import constant as cnst

pyg.init()



class Chara(sprite.Sprite):
    def __init__(self,name,x,y,scale,hp,animation_types,surface):
        sprite.Sprite.__init__(self)
        self.name = name
        self.hp = hp
        self.surface = surface
        self.vel_x = 0
        self.vel_y = 0
        
        self.is_crashing_chara = False
        self.is_alive = True
        self.is_moving = False #移動中フラグ
        self.is_on_ground = False
        self.is_jump = False

        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        
        self.update_time = pyg.time.get_ticks()
        
        for animation in animation_types:
            tmp_list = []
            animation_img_path = f'{cnst.ANIMATION_IMG_PATH}{self.name}/{animation}/'
            num_of_frames = len(os.listdir(animation_img_path))
            for i in range(num_of_frames):
                img = pyg.image.load(animation_img_path+f'{self.name}_{animation}{i}.png').convert_alpha()
                img = pyg.transform.scale(img,(int(img.get_width()*scale),int(img.get_height()*scale)))
                tmp_list.append(img)
            self.animation_list.append(tmp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        
        self.rect.center = (x,y)
        self.collider = Collider(self.rect,surface)


    def draw(self):
        self.surface.blit(self.image, self.rect)


    def update(self):
        self.update_animation()
        self.check_damaged()
        self.check_alive()


    def move(self,offset_by_collision,is_move_x=True,is_move_y=True,relative_velosity=cnst.NEAR_BG_VELOSITY_X):
        if is_move_x:
            dx = 0
            if self.is_crashing_chara:
                dx = offset_by_collision[0] - self.rect.left -1
                
            else:
                dx = self.vel_x 
            self.rect.x += dx + relative_velosity
            if self.rect.right < 0:
                self.is_alive = False
                return 0
        
        if is_move_y:
            dy = 0
            if self.is_jump:
                self.jump()

            #空中での落下
            if self.is_on_ground:
                self.vel_y = 0
                dy = offset_by_collision[1] - self.rect.bottom +1
            else:
                self.vel_y += GRAVITY
            dy += self.vel_y
            
            self.rect.y += dy
            if self.rect.top > SCREEN_HEIGHT:  #上に行く分には下に落ちてきてくれれば良い
                self.is_alive = False
                return 0

        self.collider.update(self.rect)


    def update_animation(self): #アニメーションの更新

        self.image = self.animation_list[self.action][self.frame_index]

        if pyg.time.get_ticks() - self.update_time > cnst.ANIMATION_COOLDOWN:
            self.update_time = pyg.time.get_ticks() #更新時刻の更新
            self.frame_index += 1

            #frame_indexはanimation_list[action]の要素数を超えてはならない
            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0
            

    def update_action(self, new_action): #アクションの更新
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pyg.time.get_ticks()
    

    def check_alive(self):
        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False
            

    
    def check_damaged(self):
        if self.is_crashing_chara:
            self.hp -= 1
            self.is_crashing_chara=False
        

    def jump(self):
        self.vel_y = -13
        self.is_jump = False
        self.is_on_ground = False
    


class Player(Chara):
    def __init__(self,name,x,y,scale,surface):
        
        PLAYER_VELOSITY_X = 1
        
        ANIMATION_TYPES = ["Idle","Moving","Damaged","Defeat"]
        super().__init__(name,x,y,scale,cnst.PLAYER_HP,ANIMATION_TYPES,surface)
        self.damaged_cooldown = 0
        self.vel_x = PLAYER_VELOSITY_X
        
    
    def move(self,offset_by_collision,is_move_x=False,is_move_y=True,relative_velosity=0):
        super().move(offset_by_collision,is_move_x,is_move_y,relative_velosity)

    def check_damaged(self):
        if self.is_crashing_chara and self.damaged_cooldown <= 0:
            self.damaged_cooldown = FPS
            super().check_damaged()


    def update(self):
        super().update()
        if self.damaged_cooldown > 0:
            self.damaged_cooldown -=1

    def check_alive(self):
        super().check_alive()
        if self.hp<=0:
            self.update_action(3)

class Enemy(Chara):
    def __init__(self,id,x,y,scale,surface):
        
        ANIMATION_TYPES = ["Moving"]#,"Damaged"]
        self.id = id*2 #現在はenemyの種類が1種類のみなので自動的にenemy0に割り当てられる
        name = "enemy"+f"{int(self.id%cnst.NUM_OF_ENEMY_TYPE)}"
        super().__init__(name,x,y,scale,cnst.ENEMY_HP,ANIMATION_TYPES,surface)
        
        self.vel_x = cnst.ENEMY_VELOSITY_X
        self.fall_avoidance_enabled = True
        
    
    def draw(self):
        flip = True if self.vel_x > 0 else False
        self.surface.blit(pyg.transform.flip(self.image,flip,False),self.rect)
