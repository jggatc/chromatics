#Chromatics - Copyright (C) 2021 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

#version 0.1

import pygame as pg


class Chromatics(object):

    def __init__(self):
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
        self._update_rects = []
        self._update_display = False

    def init(self, display_size = (360, 360),
                   spectrum_size = (360, 40),
                   colormap_size = (300, 300),
                   spectrum_pos = (0,320),
                   colormap_pos = (10,10)):
        """
        Initiation of chromatics.
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
        return self._width

    def get_height(self):
        return self._height

    def set_display(self, size=None, display=None):
        if display is None:
            self._size = size
            self._width = size[0]
            self._height = size[1]
            self._display = pg.Surface((self._width, self._height))
            self._display_area = self._display.get_rect()
            self._display.fill((150,150,150))
        else:
            self._display = display
            self._size = self._display.get_size()
            self._width = self._size[0]
            self._height = self._size[1]
            self._display_area = self._display.get_rect()

    def set_spectrum(self, size, position):
        self._spectrum_size = size
        self._spectrum_area = pg.Rect(position, size)
        self._spectrum = pg.Surface(size)
        self._spectrum_array = pg.surfarray.array3d(self._spectrum)

    def set_colormap(self, size, position):
        self._colormap_size = size
        self._colormap_area = pg.Rect(position, size)
        self._colormap = pg.Surface(size)
        self._colormap_array = pg.surfarray.array3d(self._colormap)
        self._colormap_resolution['x'] = 1.0 / size[0]
        self._colormap_resolution['y'] = 1.0 / size[1]

    def set_colorselect(self):
        self._colorselect = pg.Surface((30,30))
        self._colorselect_area = pg.Rect(self._width-40, 10, 30, 30)

    def set_colorvalue(self):
        pg.init()
        self._font = pg.font.Font(None, 18)
        self._colorvalue = pg.Surface((40,60))
        pg.scrap.init()
        self._clipboard = pg.scrap
        self._clipboard_type = pg.SCRAP_TEXT

    def generate_spectrum(self):
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
                if i == 0:
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
        self.display_spectrum()
        self.display_colormap()
        self.display_colorselect()
        self.display_colorvalue()
        return self._display

    def display_spectrum(self):
        spectrum_pos = (self._width-self._spectrum_size[0],
                        self._height-self._spectrum_size[1])
        rect = self._display.blit(self._spectrum, spectrum_pos)
        self._update_rects.append(rect)
        self._update_display = True

    def display_colormap(self):
        rect = self._display.blit(self._colormap, self._colormap_area)
        self._update_rects.append(rect)
        self._update_display = True

    def display_colorselect(self):
        color = tuple(self._colormap_array[self._selection['x']]
                                          [self._selection['y']])
        self._colorselect.fill(color)
        pg.draw.rect(self._colorselect, (10,10,10),
                     (0, 0, self._colorselect_area[2], self._colorselect_area[3]), 1)
        rect = self._display.blit(self._colorselect, self._colorselect_area)
        self._update_rects.append(rect)
        self._update_display = True

    def display_colorvalue(self):
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
        return tuple(self._colormap_array[self._selection['x']]
                                         [self._selection['y']])

    def get_spectrum(self):
        return self._spectrum

    def get_colormap(self):
        return self._colormap

    def hsv_to_rgb(self, h, s, v):
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
        if self._spectrum_area.collidepoint(position):
            return self.select_spectrum(position)
        elif self._colormap_area.collidepoint(position):
            return self.select_colormap(position)
        elif self._colorselect_area.collidepoint(position):
            self.select_colorselect()
        return False

    def select_spectrum(self, position):
        self._colormap_hue = position[0]
        self._colormap = self.generate_colormap((self._colormap_hue, 1.0, 1.0))
        self._display.blit(self._colormap, self._colormap_area)
        self._update_rects.append(self._colormap_area)
        self._update_display = True
        return True

    def select_colormap(self, position):
        self._selection['x'] = position[0] - self._colormap_area[0]
        self._selection['y'] = position[1] - self._colormap_area[1]
        self.display_colorselect()
        color = tuple(self._colormap_array[self._selection['x']]
                                          [self._selection['y']])
        return color

    def select_colorselect(self):
        _color = str(self.get_colorvalue())
        _type = self._clipboard_type
        try:
            self._clipboard.put(_type, _color)
        except:
            pass

    def refresh(self):
        self._update_rects.append(self._display_area)
        self._update_display = True

    def update(self):
        if self._update_display:
            pg.display.update(self._update_rects)
            self._update_rects[:] = []
            self._update_display = False

