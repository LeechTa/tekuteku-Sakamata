import pygame as pyg
import constant as cnst

pyg.init()

#TODO:bg画像を半分に分割。ループするようにする

BG_UNIT_CATEGORY = ["far","middle","near"] #遠景←-→近景
NUM_OF_PIECE_BY_CATEGORY = 2


class BackGroundUnit():
    def __init__(self,category,scale):
        
        VELOCITY_SCALE = -0.5
        self.category = category
        idx = BG_UNIT_CATEGORY.index(self.category)
        self.vel_x = cnst.NEAR_BG_VELOSITY_X-VELOCITY_SCALE*(len(BG_UNIT_CATEGORY)-1-idx)
        img = pyg.image.load(cnst.BG_UNIT_IMG_PATH+f'{self.category}.png').convert_alpha()
        self.image = pyg.transform.scale(img,(int(img.get_width()*scale),int(img.get_height()*scale)))
        self.rect = self.image.get_rect()
        self._dx_tmp = 0

        BG_POS_OFFSET = 30
        self.rect.bottomleft = cnst.GROUND_POSITION
        self.rect.bottom += BG_POS_OFFSET


    def move(self):
        dx = 0
        dx += self.vel_x + self._dx_tmp
        self._dx_tmp = dx - int(dx)
        self.rect.x += dx



class BackGround():
    def __init__(self,scale,surface):
        self.bg_units = []
        for i in range(len(BG_UNIT_CATEGORY)):
                self.bg_units.append([BackGroundUnit(BG_UNIT_CATEGORY[i],scale) for j in range(NUM_OF_PIECE_BY_CATEGORY)])
        self.surface = surface

    def draw(self):
        self.surface.fill(cnst.BG_SKY_COLOR)
        pyg.draw.rect(self.surface,cnst.BG_FLOOR_COLOR,pyg.Rect(cnst.GROUND_POSITION,(cnst.SCREEN_WIDTH,cnst.BG_FLOOR_HEIGHT)))
        for bg_units_by_category in self.bg_units:
            for bg_unit in bg_units_by_category:
                self.surface.blit(bg_unit.image,bg_unit.rect)
    

    def update(self):
        for bg_units_by_category in self.bg_units:
            if bg_units_by_category[0].rect.right<=0:
                bg_units_by_category.append(bg_units_by_category.pop(0))
            bg_units_by_category[0].move()
            for i in range(1,len(bg_units_by_category)):
                bg_units_by_category[i].rect.left = bg_units_by_category[i-1].rect.right
            
