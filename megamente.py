import pygame

import utils
import consts

class DeduccionScreen(utils.ScreenBaseClass):

    def __init__(self, screen):
        self.screen = screen
        self.background_src =  consts.DEDUCCION_ASSETS.get('background')
        self.drop_areas = pygame.sprite.Group()

    def run(self):
        self.set_background()

        #dibujamos el rectangulito para pregunta
        question_surface = utils.SurfaceSprite(consts.COLORS['white'],
                                               (1120, 150),
                                               location=self.translate_percent(3.5, 31.7),
                                               alpha=170
                                              )
        question_surface.paint(self.screen)
        question_area = utils.ImageSprite(
                                          consts.DEDUCCION_ASSETS.get('horizontal_panel'),
                                          location=self.translate_percent(4.5, 33)
                                         )
        question_area.paint(self.screen)

        #area de respuestas
        answer_surface = utils.SurfaceSprite(consts.COLORS['white'],
                                               (1120, 410),
                                               location=self.translate_percent(3.5, 52),
                                               alpha=170
                                              )
        answer_surface.paint(self.screen)

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
                arrow.paint(self.screen)
            self.drop_areas.add(answer_area)
            loc_x += 231

        self.drop_areas.draw(self.screen)

        #todo dibujar pregunta

        pygame.display.update()
        self.detect_click()


class MainClass(utils.BaseHelperClass):
    '''Main Class that starts the game'''

    def __init__(self, init_pygame=False):
        '''Start screen init'''
        #Hack para sugargame
        if init_pygame:
            pygame.init()
            self.screen = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption('Genios')
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
