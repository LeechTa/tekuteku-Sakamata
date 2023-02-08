import pygame as pyg
import constant as cnst
import glob

DEFAULT_BUTTON_COLLOR = (240,240,240)
DEFAULT_TEXT_COLLOR = (0,0,0)
DEFAULT_TEXT_SIZE = 25

class Text():
    def __init__(self,text,rect_center,size=DEFAULT_TEXT_SIZE,color=DEFAULT_TEXT_COLLOR,font='uddigikyokashonkb'):
        
        self.font_name = font
        self.font = pyg.font.SysFont(font,size)
        self.color = color
        self.__size = size
        self.__str_text = text
        self.__text = self.font.render(text,True,self.color)
        (text_rect_w,text_rect_h) = self.font.size(text)
        self.rect = pyg.Rect(0,0,text_rect_w,text_rect_h)
        self.rect.center = rect_center


    @property
    def text(self):
        return self.__str_text

    @text.setter
    def text(self,text):
        self.__str_text = text
        self.__text = self.font.render(text,True,self.color)
        (text_rect_w,text_rect_h) = self.font.size(text)
        rect_center = self.rect.center
        self.rect = pyg.Rect(0,0,text_rect_w,text_rect_h)
        self.rect.center = rect_center

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self,size):
        self.__size = size
        self.font = pyg.font.SysFont(self.font_name,size)
        self.__text = self.font.render(self.text,True,self.color)
        (text_rect_w,text_rect_h) = self.font.size(self.text)
        rect_center = self.rect.center
        self.rect = pyg.Rect(0,0,text_rect_w,text_rect_h)
        self.rect.center = rect_center
        
    def draw(self,surface):
        surface.blit(self.__text,self.rect)

TEXT_SCALE = 0.75
class Button():
    def __init__(self,text,rect,surface,button_color = DEFAULT_BUTTON_COLLOR,text_color=DEFAULT_TEXT_COLLOR,text_size = None,text_scale=TEXT_SCALE):
        self.button_rect = rect
        self.surface = surface
        self.button_color = button_color

        
        text_size = text_size if text_size else int(rect.height*text_scale)
        self.text = Text(text,rect.center,text_size,text_color)
        
    def draw(self):
        pyg.draw.rect(self.surface,self.button_color,self.button_rect)
        self.text.draw(self.surface)

class Layout():
    def __init__(self,surface,row,column):
        
        self.surface = surface
        self.width = surface.get_width()//column
        self.height = surface.get_height()//row
        self.areas = [[(self.width*r,self.height*c) for c in range(column)] for r in range(row)]


class HpGaugeDisplay():
    def __init__(self,surface,x,y,chara_hp):
        #Screen上の位置を含んだrectは、ここでは書かない。
        # UIクラスでrect作成する。
        #ここでは、HPgaugeの挙動とレイアウト
        self.name_area = pyg.Rect(x,y,cnst.HP_GAUGE_WIDTH//2,cnst.HP_GAUGE_HEIGHT)
        hpgauge_split_width = cnst.HP_GAUGE_WIDTH//(2*chara_hp)
        self.hpgauge_area = pyg.Rect(x+self.name_area.width,y,hpgauge_split_width*chara_hp,cnst.HP_GAUGE_HEIGHT)
        
        self.hpgauge_split_area = [pyg.Rect(self.hpgauge_area.x+i*hpgauge_split_width,self.hpgauge_area.y,hpgauge_split_width,cnst.HP_GAUGE_HEIGHT) for i in range(cnst.PLAYER_HP)]
        self.surface = surface

        img_path = cnst.UI_IMG_PATH
        self.img_list = []
        
        for i in range(len(glob.glob(img_path+"hp_gauge?.png"))):
            img = pyg.image.load(img_path+f'hp_gauge{i}.png').convert_alpha()
            hpgauge_scale = self.hpgauge_area.height/img.get_height()
            img = pyg.transform.scale(img,(int(img.get_width()*hpgauge_scale),int(img.get_height()*hpgauge_scale)))
            self.img_list.append(img)

        self.hp_gauge = [1 for i in range(chara_hp)]
        self.text = Text("体力：",self.name_area.center,cnst.TEXT_SIZE_SMALL)
    
    def update(self,chara_hp):
        gauge_now = sum(self.hp_gauge)
        if gauge_now != chara_hp:
            for i in range(chara_hp,gauge_now):
                self.hp_gauge[i] = 0
    
    def draw(self):
        self.text.draw(self.surface)
        pyg.draw.rect(self.surface,(255,255,255),self.hpgauge_area)
        for idx,x in enumerate(self.hp_gauge):
            self.surface.blit(self.img_list[x],self.hpgauge_split_area[idx])

class DistanceGaugeDisplay():
    def __init__(self,surface,x,y):
        self.name_area = pyg.Rect(x,y,cnst.DISTANCE_DISPLAY_WIDTH//2,cnst.DISTANCE_DISPLAY_HEIGHT)
        self.distance_area = pyg.Rect(x+self.name_area.width,y,cnst.DISTANCE_DISPLAY_WIDTH//2,cnst.DISTANCE_DISPLAY_HEIGHT)
        self.distance = 0

        self.surface = surface
        self.text = Text("歩行距離：",self.name_area.center,cnst.TEXT_SIZE_SMALL)
        self.dist_gauge_text = Text(f"{self.distance:>3}m",self.distance_area.center,cnst.TEXT_SIZE_SMALL)
        self.update_time = pyg.time.get_ticks()

    def update(self):
        if pyg.time.get_ticks() - self.update_time > cnst.DISTANCE_ANIMATION_COOLDOWN:
            self.update_time = pyg.time.get_ticks()
            self.distance += 1
            self.dist_gauge_text.text = f"{self.distance:>3}m"
    
    def draw(self):
        self.text.draw(self.surface)
        self.dist_gauge_text.draw(self.surface)



class UI():
    def __init__(self,surface):
        self.surface = surface
        self.layout = Layout(surface,4,2)
        self.rect = pyg.Rect(0,0,cnst.SCREEN_WIDTH,cnst.UI_HEIGHT)
        
        offset_y = self.layout.height //17
        hpgauge_area = self.layout.areas[0][0]
        self.hpgauge = HpGaugeDisplay(surface,hpgauge_area[0],hpgauge_area[1]+offset_y,3)

        distgauge_area = self.layout.areas[1][0]
        self.distgauge = DistanceGaugeDisplay(surface,distgauge_area[0],distgauge_area[1])

        
    def draw(self):
        pyg.draw.rect(self.surface,cnst.UI_COLOR,self.rect)
        self.hpgauge.draw()
        self.distgauge.draw()
    
    def update(self,chara_hp):
        
        self.hpgauge.update(chara_hp)
        self.distgauge.update()
    
    def get_distance(self):
        return self.distgauge.distance
