#Chromatics - Copyright (C) 2021 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

from chromatics import Chromatics
import base64
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO
import pygame as pg


chromatics = Chromatics()


class App(object):

    def __init__(self):
        chromatics.init()
        self.display_surf = None
        self.clock = None
        self.update_rects = []
        self.update_display = False
        self.quit = False

    def setup(self):
        pg.init()
        width = chromatics.get_width()
        height = chromatics.get_height()
        self.display_surf = pg.display.set_mode((width,height))
        pg.display.set_caption('Chromatics')
        icon = self.get_icon()
        pg.display.set_icon(icon)
        if hasattr(pg, 'WINDOWCLOSE'):
            self.windowclose = pg.WINDOWCLOSE
        else:
            self.windowclose = 0
        self.clock = pg.time.Clock()
        pg.event.set_blocked(pg.MOUSEMOTION)

    def get_icon(self):
        img = \
        """
        iVBORw0KGgoAAAANSUhEUgAAACAAAAAUCAIAAABj86gYAAAAVkl
        EQVQ4je3NsQ2DQBAEwIGYhAKcUMBfAP13QPA0gEQFllwAJIBogM
        S6TXdX0+woBMFI2HqVmUpl1Z2FoDCdxTX6fO+rYPB7vJfWy0kgg
        QQSSCCB/wAO2NESWvDa9xEAAAAASUVORK5CYII=
        """
        img = ''.join([s.lstrip() for s in img.split('\n')])
        try:
            image_dat = base64.b64decode(img)
        except AttributeError:
            image_dat = base64.decodestring(img)
        image_obj = BytesIO(image_dat)
        icon_img = pg.image.load(image_obj)
        icon = pg.Surface((32,32), pg.SRCALPHA)
        icon.blit(icon_img, (0,6))
        pg.draw.rect(icon, (10,10,10), (0,6,32,20), 1)
        return icon

    def display(self):
        self.chromatics_display = chromatics.display()
        rect = self.display_surf.blit(self.chromatics_display, (0,0))
        self.update_rects.append(rect)
        self.update_display = True

    def interact(self, pos):
        update = chromatics.interact(pos)
        if update:
            self.display()

    def refresh(self):
        chromatics.refresh()
        self.display()

    def input(self):
        for evt in pg.event.get():
            if evt.type == pg.MOUSEBUTTONDOWN:
                if evt.button == 1:
                    self.interact(evt.pos)
            elif evt.type == pg.ACTIVEEVENT:
                if evt.state == 2:
                    self.refresh()
            elif evt.type == pg.KEYDOWN:
                if evt.key == pg.K_ESCAPE:
                    self.quit = True
            elif evt.type in (pg.QUIT, self.windowclose):
                self.quit = True
            return self.quit

    def update(self):
        if self.update_display:
            pg.display.update(self.update_rects)
            self.update_rects[:] = []
            self.update_display = False

    def run(self):
        while True:
            if self.quit:
                break
            self.input()
            self.update()
            self.clock.tick(60)


def main():
    app = App()
    app.setup()
    app.display()
    app.run()


if __name__ == '__main__':
    main()

