import os

from gi.repository import  Gtk
import pygame

import utils
import consts
from engine import MegamenteData

WIN = 1
LOSS = 2
INCOMPLETE = 3

WIN_MESSAGE = "GANASTE"
LOSS_MESSAGE = "PERDISTE"

class DeduccionScreen(utils.ScreenBaseClass):
    QUESTION_SIZE = (1096, 125)
    MESSAGE_SIZE = (400, 200)
    current_question = None
    active_sprite = None

    def __init__(self, screen):
        self.screen = screen
        self.background_src =  consts.DEDUCCION_ASSETS.get('background')
        self.drop_areas = pygame.sprite.Group()
        self.drop_objects = pygame.sprite.Group()
        self.used_objects = pygame.sprite.Group()
        self.text_font = pygame.font.Font(consts.FONT_PATH, 20)
        self.data = MegamenteData()

    def show_message(self, message):
        pos = self.translate_percent(30, 30)
        surface = self.show_text_rect(message,
                                      self.text_font, self.MESSAGE_SIZE,
                                      pos, consts.COLORS['grey'], consts.COLORS['white'],
                                      justification=1, alpha=191,
                                      parent_background=consts.COLORS['yellow'],
                                      parent_alpha=191)
        pygame.display.update()
        pygame.time.wait(1000)
        #clearing the message
        rect = surface.get_rect()
        #limpian
        self.refresh_background()
        pygame.display.update()

    def run(self):
        self.set_background()

        #dibujamos el rectangulito para question
        question_surface = utils.SurfaceSprite(consts.COLORS['white'],
                                               (1120, 150),
                                               location=self.translate_percent(3.5, 31.7),
                                               alpha=170
                                              )
        question_surface.paint(self.background)
        question_area = utils.ImageSprite(
                                          consts.DEDUCCION_ASSETS.get('horizontal_panel'),
                                          location=self.translate_percent(4.5, 33)
                                         )
        question_area.paint(self.background)

        #area de respuestas
        answer_surface = utils.SurfaceSprite(consts.COLORS['white'],
                                               (1120, 410),
                                               location=self.translate_percent(3.5, 52),
                                               alpha=170
                                              )
        answer_surface.paint(self.background)

        loc_x, loc_y= self.translate_percent(4.5, 53)
        arrow = utils.ImageSprite(consts.DEDUCCION_ASSETS.get('arrow'))
        arrow.rect.top = loc_y + 170

        for x in xrange(5):
            answer_area = utils.ImageSprite(consts.DEDUCCION_ASSETS.get('vertical_panel'),
                                            location=(loc_x, loc_y),
                                            name=str(x)
                                        )
            if x < 4:
                arrow.rect.left = loc_x + 170
                arrow.paint(self.background)
            self.drop_areas.add(answer_area)
            loc_x += 231

        self.drop_areas.draw(self.background)

        self.refresh_background()
        self.next_question()

    def draw_question(self, question):
        location = self.translate_percent(4.5, 33)
        question = '\n'.join(self.current_question['pistas'])
        question = '%s\n%s' %  (question, self.current_question['pregunta'])
        self.show_text_rect(question, self.text_font, self.QUESTION_SIZE,
                            location, consts.COLORS['black'], 0, alpha=255)

    def next_question(self):
        #limpiando
        self.active_sprite = None
        self.used_objects.clear(self.screen, self.background)
        self.used_objects.empty()

        for s in self.drop_areas:
            s.filled = False

        self.current_question = self.data.get_random_question()
        self.draw_question(self.current_question)

        #pintando los objetos
        loc_x, loc_y= self.translate_percent(4.5, 15)
        object_list = self.data.get_question_objects(self.current_question)

        for obj in object_list:
            name = obj.split('/')[3]
            name = name.split('.')[0]
            if '-' in name:
                name = name.split('-')[1]
            #TODO: quitar esto cuando tenga todos los recursos
            if not os.path.exists(obj):
                obj = 'assets/img/deduccion/notfound.png'

            obj_sprite = utils.ImageSprite(obj,
                                            location=(loc_x, loc_y),
                                            name=name)
            self.drop_objects.add(obj_sprite)
            loc_x += 231

        self.draw_objects()

        pygame.display.update()
        self.detect_click()

    def draw_objects(self):
        if self.active_sprite:
            for sprite in self.drop_objects:
                if sprite.name != self.active_sprite.name:
                    sprite.paint(self.screen)

        else:
            self.drop_objects.draw(self.screen)

        self.used_objects.draw(self.screen)

    def detect_game_state(self):
        answers = self.current_question.get('respuesta')
        if len(self.drop_objects) == 0:
            #ver si gana..
            #comprobar el orden de las preguntas
            for i, area in enumerate(self.drop_areas):
                #scar el sprite que esta encima del area
                sprite = pygame.sprite.spritecollide(area, self.used_objects, False)[0]
                if sprite.name == answers[i]:
                    continue
                else:
                    return LOSS
            return WIN
        else:
            return INCOMPLETE

    def detect_click(self):
        while True:
            while Gtk.events_pending():
                Gtk.main_iteration()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    try:
                        pygame.quit()
                        sys.exit()
                        return
                    except Exception, e:
                        return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    touched_sprites = [s for s in self.drop_objects\
                                       if s.rect.collidepoint(pos)]
                    if touched_sprites:
                        self.active_sprite = touched_sprites[0]
                    else:
                        self.active_sprite = None
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if self.active_sprite:
                        touched_boxes = [s for s in self.drop_areas\
                                              if s.rect.collidepoint(pos)]
                        if touched_boxes:
                            box = touched_boxes[0]

                            if box.filled:
                                self.screen.blit(self.background, self.active_sprite.rect, self.active_sprite.rect)
                                self.active_sprite.move(self.screen, self.background, self.active_sprite.initial_pos)
                                self.draw_objects()
                                pygame.display.update()
                                self.active_sprite = None
                                continue

                            self.used_objects.add(self.active_sprite)
                            self.active_sprite.remove(self.drop_objects)
                            self.screen.blit(self.background, self.active_sprite.rect, self.active_sprite.rect)
                            sprite_pos = (box.rect.left + 20 , box.rect.top+130)
                            self.active_sprite.move(self.screen, self.background, sprite_pos)
                            box.filled = True
                            #comprobar ganador
                            game_state = self.detect_game_state()

                            if game_state == WIN:
                                self.show_message(WIN_MESSAGE)
                                self.active_sprite = False
                                box.filled = False
                                self.next_question()
                            elif game_state == LOSS:
                                self.show_message(LOSS_MESSAGE)
                                self.active_sprite = False
                                box.filled = False
                                self.next_question()

                            pygame.display.update()
                        else:
                            self.screen.blit(self.background, self.active_sprite.rect, self.active_sprite.rect)
                            self.active_sprite.move(self.screen, self.background, self.active_sprite.initial_pos)
                            pygame.display.update()

                        self.active_sprite = None
                elif event.type == pygame.MOUSEMOTION:
                    pos = pygame.mouse.get_pos()
                    if self.active_sprite:
                        self.screen.blit(self.background, self.active_sprite.rect, self.active_sprite.rect)
                        self.draw_question(self.current_question)
                        self.draw_objects()
                        self.active_sprite.move(self.screen, self.background, pos)
                        pygame.display.update()
                    else:
                        pass
                else:
                    continue


class MainClass(utils.BaseHelperClass):
    '''Main Class that starts the game'''

    def __init__(self, init_pygame=False):
        '''Start screen init'''
        #Hack para sugargame
        if init_pygame:
            pygame.init()
            self.screen = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption('Megamente')
            pygame.display.update()
        else:
            self.screen = None

    def run(self):
        '''Runs the main game'''
        start = DeduccionScreen(self.screen)
        start.run()

    def main(self):
        '''Runs main loop and stuff'''
        self.cursor = pygame.cursors.compile(CURSOR)

        #Hack para sugargame
        if not self.screen:
            self.screen = pygame.display.get_surface()

        pygame.mouse.set_cursor((32,32), (1,1), *self.cursor)
        self.start_screen()
        while True:
            while Gtk.events_pending():
                Gtk.main_iteration()

            for event in pygame.event.get():
                if event.type == QUIT:
                    try:
                        pygame.quit()
                    except:
                        pass
                    sys.exit()
                    break

if __name__ == "__main__":
    MainClass(True).run()
