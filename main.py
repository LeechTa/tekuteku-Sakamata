import pygame as pyg
from pygame import sprite,mixer
import sys
import glob
import random as rand
import constant as cnst
from background import BackGround
from field import FieldBlock,NUM_OF_FIELD_BLOCK
from collision_detector import CollisionDetector
from chara import Player,Enemy
from UI_parts import Button,Text,UI,Layout


pyg.init()


class Game():
    def __init__(self,run=False):
        self.screen = pyg.display.set_mode((cnst.SCREEN_WIDTH,cnst.SCREEN_HEIGHT))
        pyg.display.set_caption(cnst.TITLE)

        self.clock = pyg.time.Clock()
        self.run = run
        self.is_start_screen = False
        self.is_discription_screen = False
        self.is_finished_screen = False
        self.is_results_screen = False

        self.set_parameter()

        
    def set_parameter(self):
        self.enemy_group = sprite.Group()
        self.field_group = []

        self.game_ui = UI(self.screen)
        
        self.detector =CollisionDetector()
        self.player = Player(cnst.CHARA_NAME,cnst.CHARA_INIT_POS[0],cnst.CHARA_INIT_POS[1],cnst.PLAYER_SCALE,self.screen)
        
        self.bg = BackGround(cnst.BG_SCALE,self.screen)
        for i in range(NUM_OF_FIELD_BLOCK):
            fieldblock = FieldBlock(i,self.screen)
            if i>1:
                fieldblock.enemy_generate()
                (fu_x,fu_y) = fieldblock.enemy_generate_area.rect.midtop
                self.enemy_group.add(Enemy(0,fu_x,fu_y,cnst.ENEMY_SCALE,self.screen))
                fieldblock.enemy_generate_area = None
            self.field_group.append(fieldblock)
        

        
        self.bgm = "sound/bgm/bgm.mp3"
        
        voice_path = "sound/voice/"
        self.voice_standby = mixer.Sound(voice_path+"standby.mp3")
        self.voice_jump_list = []
        for i in range(len(glob.glob(voice_path+"jump?.mp3"))):
            self.voice_jump_list.append(mixer.Sound(voice_path+f"jump{i}.mp3"))
        self.voice_defeat = mixer.Sound(voice_path+"defeat.mp3") 
        self.voice_fallout = mixer.Sound(voice_path+"fall_out.mp3") 
        self.voice_damaged = mixer.Sound(voice_path+"damaged.mp3") 
        self.voice_retry = mixer.Sound(voice_path+"retry.mp3")         
            
        

    def start_screen(self):
        layout = Layout(self.screen,8,14)
        start_screen_rect = pyg.Rect(layout.areas[3][2],(layout.width*8,layout.height*3))
        title_text_area = pyg.Rect(layout.areas[3][2],(layout.width*8,layout.height*2))
        title_text = Text("てくてく♪沙花叉",title_text_area.center,size=cnst.TEXT_SIZE_MIDDLE)
        lead_text_area = pyg.Rect(layout.areas[6][4],(layout.width*2,layout.height))
        
        lead_text = Text("--press Enter--",lead_text_area.center,size=cnst.TEXT_SIZE_VERY_SMALL,color=cnst.TEXT_COLOR_WHITE)

        self.is_start_screen=True
        self.bg.draw()
        pyg.draw.rect(self.screen,cnst.START_SCREEN_COLOR,start_screen_rect)
        title_text.draw(self.screen)
        lead_text.draw(self.screen)
        while self.is_start_screen:
            self.clock.tick(cnst.FPS)
            
            pyg.display.update()

            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    self.is_start_screen = False
                if event.type == pyg.KEYDOWN:
                    if event.key != pyg.K_ESCAPE:
                        self.is_start_screen=False
                        self.is_discription_screen = True
                        return
        

        self.run = False
        pyg.quit()
        sys.exit()
    



    def standby_screen(self):
        if self.is_discription_screen:
            layout = Layout(self.screen,16,14)
            
            text = "うじゃうじゃといる飼育員を\nジャンプで避けながら\n沙花叉を沢山歩かせよう!!".split("\n")
            discription_text_area = pyg.Rect(layout.areas[3][4],(layout.width*8,layout.height*2*len(text)))
            discription_text = []
            for i in range(len(text)):
                text_area = pyg.Rect(layout.areas[3][4+2*i],(layout.width*8,layout.height*2))
                discription_text.append(Text(text[i],text_area.center,size=cnst.TEXT_SIZE_VERY_SMALL))
            update_time = pyg.time.get_ticks()
            while self.is_discription_screen:
                self.clock.tick(cnst.FPS)
                self.bg.draw()
                pyg.draw.rect(self.screen,cnst.TEXT_BG_DEFAULT_COLOR,discription_text_area)
                for text in discription_text:
                    text.draw(self.screen)
                pyg.display.update()
                if pyg.time.get_ticks() - update_time > cnst.FPS*200:
                    self.is_discription_screen = False
                for event in pyg.event.get():
                    if event.type == pyg.QUIT:
                        self.is_start_screen = False
                        pyg.quit()
                    if event.type == pyg.KEYDOWN:
                        if event.key != pyg.K_ESCAPE:
                            self.is_discription_screen = False
                    #if event.type == pyg.MOUSEBUTTONDOWN:
                    #    if event.button == 1:
                    #        self.is_discription_screen = False


        mixer.music.load(self.bgm)
        mixer.music.play(-1)
        ANIMATION_COOLDOWN = 1000
        countdown_texts = ["START!!","1","2","3"]
        index = len(countdown_texts)-1
        countdown_text = Text(countdown_texts[index],cnst.SCREEN_CENTER,cnst.TEXT_SIZE_LARGE,cnst.TEXT_COLOR_RED)
        countdown_text.rect.y -=40

        update_time = pyg.time.get_ticks()
        self.player.update_action(1)
        is_player_move_x = True
        while index>=0:
            self.clock.tick(cnst.FPS)
            self.bg.draw()
            self.game_ui.draw()
            self.screen.fill(cnst.TEXT_BG_DEFAULT_COLOR,pyg.Rect(0,countdown_text.rect.top,cnst.SCREEN_WIDTH,int(countdown_text.rect.height*0.9)))
            countdown_text.draw(self.screen)

            self.player.update()
            self.player.draw()
            
            if self.player.rect.x >=cnst.CHARA_DEFAULT_POS[0]:
                self.player.update_action(0)
                is_player_move_x = False
            self.player.is_on_ground,offset_by_collision_p = self.detector.detect_collision_with_ground(self.player,self.field_group)
            self.player.move(offset_by_collision_p,is_move_x=is_player_move_x)
            
            
            pyg.display.update()
            if pyg.time.get_ticks() - update_time > ANIMATION_COOLDOWN:
                update_time = pyg.time.get_ticks()
                index -= 1
                countdown_text.text = countdown_texts[index]
                if index == 1:
                    mixer.stop()
                    self.voice_standby.play()

            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    index = -1
                    pyg.quit()
                if event.type == pyg.KEYDOWN:
                    if event.key == pyg.K_ESCAPE:
                        index = -1
                        pyg.quit()



    
    


#------------------------------------------------------------------------
#------------------------------------------------------------------------

    def game(self):
        discription_text_area = pyg.Rect(0,0,cnst.SCREEN_WIDTH//3,cnst.TEXT_SIZE_VERY_SMALL)
        discription_text_area.bottomright = (cnst.SCREEN_WIDTH,cnst.SCREEN_HEIGHT)
        discription_text = Text("操作方法:マウス左クリックでジャンプ",discription_text_area.center,size=int(cnst.TEXT_SIZE_VERY_SMALL*0.6))
        mixer.music.load(self.bgm)
        mixer.music.play(-1)
        self.player.is_moving = True
        while self.run:
            self.clock.tick(cnst.FPS)
            if self.player.is_alive:
                self.bg.update()
            self.bg.draw()
            for field_block in self.field_group:
                field_block.update()
                if field_block.enemy_generate_area:
                    (fu_x,fu_y) = field_block.enemy_generate_area.rect.midtop
                    self.enemy_group.add(Enemy(rand.randrange(0,cnst.NUM_OF_ENEMY_TYPE),fu_x,fu_y,cnst.ENEMY_SCALE,self.screen))
                    field_block.enemy_generate_area = None
            self.game_ui.update(self.player.hp)
            
            self.player.update()

            self.game_ui.draw()
            discription_text.draw(self.screen)

            self.player.draw()

            
            if self.player.is_alive:
                if self.player.damaged_cooldown:
                    self.player.update_action(2)
                elif self.player.is_moving:
                    self.player.update_action(1)
                else:
                    self.player.update_action(0)
                self.player.is_on_ground,offset_by_collision_p = self.detector.detect_collision_with_ground(self.player,self.field_group)
                if self.player.is_jump:
                    mixer.stop()
                    self.voice_jump_list[rand.randrange(0,len(self.voice_jump_list))].play()
                self.player.move(offset_by_collision_p)
                self.player.is_crashing_chara = self.detector.detect_collision_with_chara(self.player,self.enemy_group)
                if self.player.is_crashing_chara:
                    mixer.stop()
                    self.voice_damaged.play()
            else:
                self.game_ui.hpgauge.update(0)
                mixer.stop()
                mixer.music.stop()
                self.run = False
                
                self.game_ui.draw()
                pyg.display.update()
                
                for field_block in self.field_group:
                    field_block.change_place_of_units([[1,0,0],[1,0,0],[1,0,0]])
                self.player.vel_x *=-1.5
                if self.player.rect.top >= cnst.SCREEN_HEIGHT:
                    self.voice_fallout.play()
                else:
                    self.voice_defeat.play()
                    while self.player.rect.right > 0:
                        self.clock.tick(cnst.FPS)
                        self.bg.draw()
                        for field_block in self.field_group:
                            field_block.update(is_move=False)
                        
                        if self.player.is_on_ground:
                            self.player.update_action(3)
                        self.player.update_animation()
                        self.player.is_on_ground,offset_by_collision_p = self.detector.detect_collision_with_ground(self.player,self.field_group)
                        self.player.move(offset_by_collision_p,is_move_x=True)
                        self.player.draw()
                        self.game_ui.draw()
                        pyg.display.update()
                        for event in pyg.event.get():
                            if event.type == pyg.QUIT:
                                pyg.quit()
                                sys.exit()
                        
                return
            
            for enemy in self.enemy_group:
                enemy.update()
                enemy.draw()
                if enemy.is_alive:
                    enemy.is_on_ground,offset_by_collision_e = self.detector.detect_collision_with_ground(enemy,self.field_group)
                    if enemy.fall_avoidance_enabled and enemy.is_on_ground:
                        if (enemy.vel_x < 0) and not(self.detector.detect_collision_between_obj_and_ground(enemy.collider.rect_left_bottom,self.field_group)):
                            enemy.vel_x = -1*cnst.ENEMY_VELOSITY_X
                        elif (enemy.vel_x > 0) and not(self.detector.detect_collision_between_obj_and_ground(enemy.collider.rect_right_bottom,self.field_group)):
                            enemy.vel_x = cnst.ENEMY_VELOSITY_X
                    
                    enemy.move(offset_by_collision_e)
                else:
                    #enemy.update_action(1)
                    if self.player.damaged_cooldown<=0:
                        enemy.kill()
            

            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    self.run = False
                if event.type == pyg.KEYDOWN:
                    if event.key == pyg.K_ESCAPE:
                        self.run == False
                    if self.player.is_on_ground and event.key == pyg.K_SPACE:
                        self.player.is_jump = True
                if event.type == pyg.MOUSEBUTTONDOWN:
                    if self.player.is_on_ground and event.button == 1:
                        self.player.is_jump = True


            pyg.display.update()

        mixer.music.stop()
        pyg.quit()
        sys.exit()



    def results_screen(self):
            ANIMATION_COOLDOWN = 100
            text = Text("Finish!!",cnst.SCREEN_CENTER,cnst.TEXT_SIZE_LARGE,cnst.TEXT_COLOR_RED)
            screen_center_x = cnst.SCREEN_CENTER[0]
            dx = (screen_center_x+cnst.FPS-1)/cnst.FPS
            text.rect.x -= cnst.FPS*dx

            update_time = pyg.time.get_ticks()

            self.is_finished_screen = True
            self.is_results_screen = True

            while self.is_finished_screen:
                self.screen.fill(cnst.TEXT_BG_DEFAULT_COLOR,pyg.Rect(0,text.rect.top,cnst.SCREEN_WIDTH,text.rect.height))
                text.draw(self.screen)
                if pyg.time.get_ticks() - update_time > ANIMATION_COOLDOWN and text.rect.centerx < screen_center_x:
                    text.rect.x += dx

                
                for event in pyg.event.get():
                    if event.type == pyg.QUIT:
                        self.is_finished_screen = False
                        self.is_results_screen = False
                    if event.type == pyg.KEYDOWN:
                        if event.key == pyg.K_ESCAPE:
                            self.is_finished_screen = False
                            self.is_results_screen = False
                        if text.rect.centerx >= screen_center_x and event.key:
                            self.is_finished_screen = False
                    if event.type == pyg.MOUSEBUTTONDOWN:
                        if text.rect.centerx >= screen_center_x and event.button:
                            self.is_finished_screen = False
                pyg.display.update()
            
            layout = Layout(self.screen,12,16)
            text2_area = pyg.Rect(layout.areas[2][1],(layout.width*6,layout.height*2))
            text2 = Text("歩いた距離...",text2_area.center,cnst.TEXT_SIZE_MIDDLE,color=cnst.TEXT_COLOR_WHITE)
            
            score_area = pyg.Rect(layout.areas[4][3],(layout.width*8,layout.height*6))
            score = Text(f"{self.game_ui.get_distance()}m",score_area.center,cnst.TEXT_SIZE_LARGE)
            effect_image = pyg.image.load(cnst.UI_IMG_PATH+f'score_effect.png').convert_alpha()
            effect_image_scale = score_area.height/effect_image.get_height()
            effect_image = pyg.transform.scale(effect_image,(int(effect_image.get_width()*effect_image_scale),int(effect_image.get_height()*effect_image_scale)))
            retry_button_area = pyg.Rect(layout.areas[10][9],(layout.width*4,layout.height*2))
            retry_button = Button("リトライ(press R)",retry_button_area,self.screen,text_scale=0.3)
            exit_button_area = pyg.Rect(layout.areas[2][9],(layout.width*4,layout.height*2))
            exit_button = Button("終了(press Q)",exit_button_area,self.screen,text_scale=0.3)

            is_black_screen = False
            while self.is_results_screen:
                self.screen.fill(cnst.RESULTS_SCREEN_COLOR)
                text2.draw(self.screen)
                self.screen.blit(effect_image,score_area)
                score.draw(self.screen)
                
                retry_button.draw()
                exit_button.draw()

                pyg.display.update()
                
                for event in pyg.event.get():
                    if event.type == pyg.QUIT:
                        self.is_results_screen = False
                        pyg.quit()
                        sys.exit()
                    if event.type == pyg.KEYDOWN:
                        if event.key == pyg.K_ESCAPE:
                            self.is_results_screen = False
                            pyg.quit()
                            sys.exit()
                        if event.key == pyg.K_r:
                            self.voice_retry.play()
                            self.is_results_screen = False
                            self.run = True
                            self.set_parameter()
                        if event.key == pyg.K_q:
                            self.is_results_screen = False
                            is_black_screen = True

                    if event.type == pyg.MOUSEBUTTONDOWN:
                        if retry_button.button_rect.collidepoint(event.pos):
                            self.voice_retry.play()
                            self.is_results_screen = False
                            self.run = True
                            self.set_parameter()
                        if exit_button.button_rect.collidepoint(event.pos):
                            self.is_results_screen = False
                            is_black_screen = True
            
            if is_black_screen:
                comment_text_area = pyg.Rect(layout.areas[2][6],(layout.width*12 ,layout.height*2))
                text26810 = ["風呂入れ！！！！","家の外に出たね？風呂入れ！！","たくさん歩いたね！風呂入れ！！"]
                if self.game_ui.get_distance() < 50:
                    idx = 0
                elif self.game_ui.get_distance() < 100:
                    idx = 1
                else:
                    idx = 2
                comment_text = Text(text26810[idx],comment_text_area.center,int(cnst.TEXT_SIZE_VERY_SMALL*0.2),color=cnst.TEXT_COLOR_WHITE)
                update_time = pyg.time.get_ticks()
                while is_black_screen:
                    self.screen.fill((0,0,0))
                    
                    comment_text.draw(self.screen)
                    pyg.display.update()
                    if pyg.time.get_ticks() - update_time > cnst.FPS and comment_text.size < 47:
                        comment_text.size = comment_text.size + 2
                        update_time = pyg.time.get_ticks()
                    for event in pyg.event.get():
                        if event.type == pyg.QUIT:
                            is_black_screen = False
                            pyg.quit()
                            sys.exit()
                        if event.type == pyg.KEYDOWN and event.key:
                            is_black_screen = False
                            pyg.quit()
                            sys.exit()
                    
            


    def mainloop(self):
        self.start_screen()
        while self.run:
            self.standby_screen()
            self.game()
            self.results_screen()


if __name__ == "__main__":
    run=True
    game = Game(run)
    game.mainloop()

