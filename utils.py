import sys
import pygame
from pygame.locals import QUIT
from gi.repository import Gtk
import consts

OLPC_SCREEN_SIZE = (1200, 900)

import logging
_logger = logging.getLogger('genio-activity')

class ImageSprite(pygame.sprite.Sprite):
    '''Class to create a background image'''

    def __init__(self, image_file, location=(0, 0), name=None, scale=None):
        '''
            image_file: filepath for the image
            location: tuple of x y coordinates
            name: name for the sprite
            scale: tuple of the new size of the image
        '''
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file).convert_alpha()
        if scale:
            self.image = pygame.transform.scale(self.image, scale)

        self.name = name
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

    def move(self, display, background, position):
        #TODO: clean dirty rects
        self.rect.left, self.rect.top = position
        display.blit(self.image, self.rect)


class BaseHelperClass(object):
    '''
    Helper class to locate objects on the screen based on percentage
    need to improve the name of this
    '''
    width, height = OLPC_SCREEN_SIZE

    def translate_percent(self, width, height):
        '''translates percentages to screen positions'''
        x = (width / 100.0) * self.width
        y = (height / 100.0) * self.height
        return x, y

    def translate_percent_centered(self, width, height, rect):
        '''
        translates percentages to screen positions
        using the sprite center as point instead of top corner
        '''
        x, y = self.translate_percent(width, height)
        x = x - (rect.width/2.0)
        y = y - (rect.height/2.0)
        return x, y

class ScreenBaseClass(BaseHelperClass):
    '''
    Base class to draw screens it contains
    helper methods for screen and click detection
    '''
    def __init__(self, screen):
        self.screen = screen

    def set_background(self):
        '''Sets the background on the screen'''
        background = ImageSprite(self.background_src, scale=OLPC_SCREEN_SIZE)
        self.screen.blit(background.image, background.rect)
        surface = pygame.Surface(OLPC_SCREEN_SIZE)
        surface.blit(background.image, background.rect)
        self.background = surface
        return background

    def run(self):
        '''This method is executed to start drawing stuff on screen'''
        raise NotImplementedError

    def click_callback(self):
        '''This method is executed when detecting a click on items'''
        raise NotImplementedError

    def detect_click(self):
        '''Event loop to detect clicks'''
        while True:
            #hack para sugargame
            while Gtk.events_pending():
                Gtk.main_iteration()

            for event in pygame.event.get():
                if event.type == QUIT:
                    try:
                        pygame.quit()
                        sys.exit()
                        return
                    except Exception, e:
                        return
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    clicked_sprites = [s for s in self.menu_items \
                                       if s.rect.collidepoint(pos)]
                    for s in clicked_sprites:
                        self.click_callback(s)
                        break
                else:
                    continue
