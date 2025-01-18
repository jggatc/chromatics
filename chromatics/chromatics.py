#Chromatics - Copyright (C) 2021 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

"""
Chromatics - Pygame Color Module
"""

import sys
import pygame as pg


class Chromatics(object):
    """
    Chromatics object.
    """

    def __init__(self):
        """
        Initiation of Chromatics object.
        """
        self._display = None
        self._size = None
        self._display_area = None
        self._width = None
        self._height = None
        self._spectrum = None
        self._spectrum_array = None
        self._spectrum_size = None
        self._spectrum_area = None
        self._colormap = None
        self._colormap_array = None
        self._colormap_size = None
        self._colormap_area = None
        self._colormap_resolution = {'x':0.0, 'y':0.0}
        self._colormap_hue = None
        self._colorselect = None
        self._colorselect_area = None
        self._selection = {'x':0, 'y':0}
        self._colorvalue = None
        self._colorstr = ['R','G','B']
        self._font = None
        self._clipboard = None
        self._clipboard_type = None
        self._clipboard_format = None
        self._update_rects = []
        self._update_display = False

    def init(self, display_size = (360, 360),
                   spectrum_size = (360, 40),
                   colormap_size = (300, 300),
                   spectrum_pos = (0,320),
                   colormap_pos = (10,10)):
        """
        Initiation of chromatics.

        Arguments:
            * display_size      default: (360, 360)
            * spectrum_size     default: (360, 40)
            * colormap_size     default: (300, 300)
            * spectrum_pos      default: (0, 320)
            * colormap_pos      default: (10, 10)
        """
        self.set_display(display_size)
        self.set_spectrum(spectrum_size, spectrum_pos)
        self.set_colormap(colormap_size, colormap_pos)
        self.set_colorselect()
        self.generate_spectrum()
        self.generate_colormap()
        self._selection['x'] = colormap_size[0] - 100
        self._selection['y'] = colormap_size[1] - 100

    def get_width(self):
        """
        Return chromatics display width.
        """
        return self._width

    def get_height(self):
        """
        Return chromatics display height.
        """
        return self._height

    def set_display(self, size=None, color=(150,150,150)):
        """
        Set chromatics display.

        Arguments include size and color of chromatics surface display.
        Called with chromatics.init().
        """
        self._size = size
        self._width = size[0]
        self._height = size[1]
        self._display_color = color
        self._display = pg.Surface((self._width, self._height))
        self._display_area = self._display.get_rect()
        self._display.fill(color)

    def set_spectrum(self, size, position):
        """
        Set chromatics spectrum.

        Arguments include spectrum size and position.
        Called with chromatics.init().
        """
        self._spectrum_size = size
        self._spectrum_area = pg.Rect(position, size)
        self._spectrum = pg.Surface(size)
        self._spectrum_array = pg.surfarray.array3d(self._spectrum)

    def set_colormap(self, size, position):
        """
        Set chromatics colormap.

        Arguments include colormap size and position.
        Called with chromatics.init().
        """
        self._colormap_size = size
        self._colormap_area = pg.Rect(position, size)
        self._colormap = pg.Surface(size)
        self._colormap_array = pg.surfarray.array3d(self._colormap)
        self._colormap_resolution['x'] = 1.0 / size[0]
        self._colormap_resolution['y'] = 1.0 / size[1]

    def set_colorselect(self):
        """
        Set chromatics colorselect.

        Called with chromatics.init().
        """
        self._colorselect = pg.Surface((30,30))
        self._colorselect_area = pg.Rect(self._width-40, 10, 30, 30)

    def set_colorvalue(self):
        """
        Initiate display of RGB value.
        """
        pg.font.init()
        self._font = pg.font.Font(None, 18)
        self._colorvalue = pg.Surface((40,60))
        try:
            self._clipboard = pg.scrap
            self._clipboard.init()
            if sys.platform in ('win32', 'linux'):
                self._clipboard_type = 'text/plain;charset=utf-8'
                self._clipboard_format = 'utf-8'
                if sys.platform == 'linux':
                    self._clipboard.set_mode(pg.SCRAP_CLIPBOARD)
            else:
                self._clipboard_type = pg.SCRAP_TEXT
                self._clipboard_format = 'ascii'
        except:
            self._clipboard = None

    def generate_spectrum(self):
        """
        Generate chromatics spectrum.

        Return spectrum surface.
        Called with chromatics.init().
        """
        array = self._spectrum_array
        for i in range(self._spectrum_size[0]):
            r, g, b = self.hsv_to_rgb(i/360.0, 1.0, 1.0)
            for j in range(self._spectrum_size[1]):
                array[i,j,0] = r
                array[i,j,1] = g
                array[i,j,2] = b
        pg.surfarray.blit_array(self._spectrum, self._spectrum_array)
        return self._spectrum

    def generate_colormap(self, color=(240,1.0,1.0)):
        """
        Generate chromatics colormap.

        Argument HSV color used for generation, default to (240, 1.0, 1.0).
        Return colormap surface.
        Called with chromatics.init().
        """
        width = self._colormap_size[0]
        height = self._colormap_size[1]
        h = color[0] / 360.0
        self._colormap_hue = h
        array = self._colormap_array
        for _i in range(width):
            for _j in range(height):
                s = _i * self._colormap_resolution['x']
                v = (height-_j) * self._colormap_resolution['y']
                i = int(h*6.0)
                f = (h*6.0) - i
                p = 255 * (v * (1.0 - s))
                q = 255 * (v * (1.0 - s * f))
                t = 255 * (v * (1.0 - s * (1.0-f)))
                u = v * 255
                i %= 6
                if i == 0:
                    array[_i,_j,0] = u
                    array[_i,_j,1] = t
                    array[_i,_j,2] = p
                    continue
                if i == 1:
                    array[_i,_j,0] = q
                    array[_i,_j,1] = u
                    array[_i,_j,2] = p
                    continue
                if i == 2:
                    array[_i,_j,0] = p
                    array[_i,_j,1] = u
                    array[_i,_j,2] = t
                    continue
                if i == 3:
                    array[_i,_j,0] = p
                    array[_i,_j,1] = q
                    array[_i,_j,2] = u
                    continue
                if i == 4:
                    array[_i,_j,0] = t
                    array[_i,_j,1] = p
                    array[_i,_j,2] = u
                    continue
                if i == 5:
                    array[_i,_j,0] = u
                    array[_i,_j,1] = p
                    array[_i,_j,2] = q
                    continue
        pg.surfarray.blit_array(self._colormap, self._colormap_array)
        return self._colormap

    def display(self):
        """
        Render chromatics images.

        Render spectrum, colormap, colorselect, and colorvalue onto chromatics display.
        Return chromatics display surface.
        """
        self.display_spectrum()
        self.display_colormap()
        self.display_colorselect()
        self.display_colorvalue()
        return self._display

    def display_spectrum(self):
        """
        Render chromatics spectrum on display surface.
        """
        spectrum_pos = (self._width-self._spectrum_size[0],
                        self._height-self._spectrum_size[1])
        rect = self._display.blit(self._spectrum, spectrum_pos)
        self._update_rects.append(rect)
        self._update_display = True

    def display_colormap(self):
        """
        Render chromatics colormap on display surface.
        """
        rect = self._display.blit(self._colormap, self._colormap_area)
        self._update_rects.append(rect)
        self._update_display = True

    def display_colorselect(self):
        """
        Render chromatics colorselect on display surface.
        """
        color = tuple(self._colormap_array[self._selection['x']]
                                          [self._selection['y']])
        self._colorselect.fill(color)
        pg.draw.rect(self._colorselect, (10,10,10),
                     (0, 0, self._colorselect_area[2], self._colorselect_area[3]), 1)
        rect = self._display.blit(self._colorselect, self._colorselect_area)
        self._update_rects.append(rect)
        self._update_display = True

    def display_colorvalue(self):
        """
        Render chromatics colorvalue on display surface.
        """
        if self._font is None:
            self.set_colorvalue()
        color = self.get_colorvalue()
        self._colorvalue.fill((150,150,150))
        self._colorstr[0] = 'R ' + str(color[0])
        self._colorstr[1] = 'G ' + str(color[1])
        self._colorstr[2] = 'B ' + str(color[2])
        for i, s in enumerate(self._colorstr):
            img = self._font.render(s, True, (0,0,0))
            self._colorvalue.blit(img, (5,15*i+5))
        self._display.blit(self._colorvalue, (self._width-45, 50))
        self._update_display = True

    def get_colorvalue(self):
        """
        Return selected colorvalue.
        """
        return tuple(self._colormap_array[self._selection['x']]
                                         [self._selection['y']])

    def get_spectrum(self):
        """
        Return chromatics spectrum surface.
        """
        return self._spectrum

    def get_colormap(self):
        """
        Return chromatics colormap surface.
        """
        return self._colormap

    def hsv_to_rgb(self, h, s, v):
        """
        Convert HSV to RGB.
        """
        i = int(h*6.0)
        f = (h*6.0) - i
        p = 255 * (v * (1.0 - s))
        q = 255 * (v * (1.0 - s * f))
        t = 255 * (v * (1.0 - (s * (1.0-f))))
        u = v * 255
        i %= 6
        if i == 0:
            return (u, t, p)
        if i == 1:
            return (q, u, p)
        if i == 2:
            return (p, u, t)
        if i == 3:
            return (p, q, u)
        if i == 4:
            return (t, p, u)
        if i == 5:
            return (u, p, q)

    def interact(self, position):
        """
        Check interaction with chromatics color objects.

        Interaction updates chromatics state.
        Return True on chromatics update.
        """
        if self._spectrum_area.collidepoint(position):
            return self.select_spectrum(position)
        elif self._colormap_area.collidepoint(position):
            return self.select_colormap(position)
        elif self._colorselect_area.collidepoint(position):
            self.select_colorselect()
        return False

    def select_spectrum(self, position):
        """
        Select hue from chromatics spectrum.

        Argument position to retrieve color hue.
        Interaction updates chromatics state.
        Return True on chromatics update.
        """
        self._colormap_hue = position[0]
        self._colormap = self.generate_colormap((self._colormap_hue, 1.0, 1.0))
        self._display.blit(self._colormap, self._colormap_area)
        self._update_rects.append(self._colormap_area)
        self._update_display = True
        return True

    def select_colormap(self, position):
        """
        Select color from chromatics colormap.

        Argument position to retrieve color.
        Interaction updates chromatics state.
        Return selected color.
        """
        self._selection['x'] = position[0] - self._colormap_area[0]
        self._selection['y'] = position[1] - self._colormap_area[1]
        self.display_colorselect()
        color = tuple(self._colormap_array[self._selection['x']]
                                          [self._selection['y']])
        return color

    def select_colorselect(self):
        """
        Color selected send to clipboard.
        """
        _color = str(self.get_colorvalue())
        if self._clipboard:
            self._clipboard.put(
                self._clipboard_type, _color.encode(self._clipboard_format))

    def refresh(self):
        """
        Set chromatics display refresh.
        """
        self._update_rects.append(self._display_area)
        self._update_display = True

    def update(self):
        """
        Render chromatics display if changed.
        """
        if self._update_display:
            pg.display.update(self._update_rects)
            self._update_rects[:] = []
            self._update_display = False

