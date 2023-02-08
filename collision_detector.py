import pygame as pyg

pyg.init()


class CollisionDetector():

    def detect_collision_with_ground(self,chara,field_group):
        field_rect = []
        if isinstance(field_group,pyg.Rect):
            field_rect.append(field_group)
        else:
            for field in field_group:
                for obstruction in field.obstruction_group:
                    if obstruction.is_existence:
                        field_rect.append(obstruction.rect)
        
        is_collision = False
        for rect in chara.collider.rects_bottom():
            collision_object_index = rect.collidelist(field_rect)
            collision_object_left = chara.rect.left
            collision_object_bottom = chara.rect.bottom
            if collision_object_index>=0:
                if chara.collider.rect_right_top.colliderect(field_rect[collision_object_index]):
                    is_collision = False
                    break
                is_collision |= True
                collision_object_left=field_rect[collision_object_index].left
                collision_object_bottom=field_rect[collision_object_index].top
            else:
                is_collision |= False

        return is_collision, [collision_object_left,collision_object_bottom]

    def detect_collision_between_obj_and_ground(self,rect,field_group):
        field_rect = []

        if isinstance(field_group,pyg.Rect):
            field_rect.append(field_group)
        else:
            for field in field_group:
                for obstruction in field.obstruction_group:
                    if obstruction.is_existence:
                        field_rect.append(obstruction.rect)
        
        collide_object_index = rect.collidelist(field_rect)
        is_collision = True if collide_object_index>=0 else False
        return is_collision #, field_rect[collide_object_index]

    def detect_collision_with_chara(self,chara,other_group):
        others = []
        other_collider_rects = []
        for other in other_group:
            others.append(other)
            other_collider_rects.append(other.collider.rects)
            
        for rect in chara.collider.rects:
            for idx,rects in enumerate(other_collider_rects):
                if rect.collidelist(rects)>=0:
                    collision_object = others[idx]
                    collision_object.is_crashing_chara = True
                    return True
            
        return False
    



class Collider():
    def __init__(self,chara_rect,surface):
        COLLIDER_HEIGHT = chara_rect.height//2
        COLLIDER_WIDTH = chara_rect.width//4

        self.rect_left_top = pyg.Rect(0,0,COLLIDER_WIDTH,COLLIDER_HEIGHT)
        self.rect_right_top = pyg.Rect(0,0,COLLIDER_WIDTH,COLLIDER_HEIGHT)
        self.rect_left_bottom = pyg.Rect(0,0,COLLIDER_WIDTH,COLLIDER_HEIGHT)
        self.rect_right_bottom = pyg.Rect(0,0,COLLIDER_WIDTH,COLLIDER_HEIGHT)

        self.rects = [
            self.rect_left_top,
            self.rect_right_top,
            self.rect_left_bottom,
            self.rect_right_bottom
            ]
        self.surface = surface
        self.update(chara_rect)


    def update(self,chara_rect):
        chara_center = chara_rect.center
        self.rect_left_top.bottomright = chara_center
        self.rect_right_top.bottomleft = chara_center
        self.rect_left_bottom.topright = chara_center
        self.rect_right_bottom.topleft = chara_center


    def rects_top(self):
        return [self.rect_left_top, self.rect_right_top]


    def rects_bottom(self):
        return [self.rect_left_bottom, self.rect_right_bottom]


    def rects_left(self):
        return [self.rect_left_top, self.rect_left_bottom]


    def rects_right(self):
        return [self.rect_right_top, self.rect_right_bottom]
