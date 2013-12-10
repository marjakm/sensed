import logging
llog = logging.getLogger(__name__) # the name 'log' is taken in sdl2

from math import sin, cos, radians

from OpenGL.GL import *
from copenglconstants import * # import to silence opengl enum errors for pycharm. pycharm can't see pyopengl enums.

from sdl2 import *

import coordinate_system
import vector
import vbo


class Node:

    def __init__(self, pos, gltext):
        """pos is a vector.Vector()"""
        self.pos = pos.new()
        self.gltext = gltext
        # screen_pos is set from outside, usually before calling render_overlay. It's a book-keeping value for
        # the Node owner/renderer/editor.
        self.screen_pos = vector.Vector()
        self.mouse_hover = False
        self.selected = False

        self.node_id = "FACE"
        self.radius_pixels = 17.

        self._signal_strength_circles_vbo = self._build_signal_strength_circles_vbo()
        self._signal_strength_filled_circles_xz_vbo = self._build_filled_circle_xz_vbo(
            4., (0.5, 0.5, 0.9, 0.8), (0.5, 0.5, 0.9, 0.))

        self._icon_circle_outer_xy_vbo = self._build_filled_circle_xy_vbo(self.radius_pixels)
        self._icon_circle_inner_xy_vbo = self._build_filled_circle_xy_vbo(self.radius_pixels - 2.)

    def render(self):
        glLineWidth(1.)
        glPushMatrix()
        glTranslatef(*self.pos)
        self._signal_strength_filled_circles_xz_vbo.draw(GL_TRIANGLE_FAN)
        self._signal_strength_circles_vbo.draw(GL_LINES)
        glPopMatrix()

    def render_overlay(self):
        """Render the iconified representation at self.screen_pos screen-coordinates."""
        s = self.screen_pos
        glDisable(GL_TEXTURE_2D)

        glPushMatrix()
        glTranslatef(*s)

        if self.selected:
            outer_color = (1., .4, .4, 1.)
            inner_color = (0.9, 0.9, .9, 1.0)
        elif self.mouse_hover:
            outer_color = (1., 1., 1., 1.)
            inner_color = (0.9, 0.9, .9, 1.0)
        else:
            outer_color = (1., 1., 1., 1.)
            inner_color = (0.8, 0.8, 0.8, 1.0)

        glColor4f(*outer_color)
        self._icon_circle_outer_xy_vbo.draw(GL_TRIANGLE_FAN)
        glColor4f(*inner_color)
        self._icon_circle_inner_xy_vbo.draw(GL_TRIANGLE_FAN)
        glPopMatrix()

        glEnable(GL_TEXTURE_2D)
        self.gltext.drawmm(self.node_id, s[0], s[1], bgcolor=(1.0,1.0,1.0,0.), fgcolor=(0.,0.,0.,1.), z=s[2])

    def intersects(self, sx, sy):
        p = self.screen_pos
        return (sx - p[0])**2 + (sy - p[1])**2 < self.radius_pixels**2

    def _build_signal_strength_circles_vbo(self):
        """Build a vbo of some concnentric circles. meant to be rendered with GL_LINES."""
        v = []
        for i in range(4):  # 4 circles
            radius = i + 1
            prevpoint = []
            for a in range(0, 361, 5):
                point = [radius * sin(radians(a)), 0., radius * cos(radians(a)), 0.5, 0.5, 0.5, 0.9*(0.6**i)]
                if prevpoint:
                    v.extend(prevpoint)
                    v.extend(point)
                prevpoint = point
        return vbo.VBOColor(v)

    def _build_filled_circle_xz_vbo(self, radius, centercolor, edgecolor):
        """Build a vbo of a filled circle. meant to be rendered with GL_TRIANGLE_FAN."""
        r, g, b, a = edgecolor
        v = [0., 0., 0.] + list(centercolor)
        for angle in range(0, 361, 5):
            v.extend([radius * sin(radians(angle)), 0., radius * cos(radians(angle)), r, g, b, a])
        return vbo.VBOColor(v)

    def _build_filled_circle_xy_vbo(self, radius):
        """Build a vbo for the text background. Used with pixel projection. Meant to be rendered with GL_TRIANGLE_FAN."""
        v = [0., 0., 0.]
        for angle in range(0, 361, 5):
            v.extend([radius * sin(radians(angle)), radius * cos(radians(angle)), 0.])
        return vbo.VBO(v)


class NodeEditor:
    def __init__(self, mouse, gltext, conf):
        self.conf = conf
        self.mouse = mouse  # TODO: use a special mouse object instead of the editor_main object directly.
        self.gltext = gltext
        self.nodes = []

        self.mouse_hover = False
        self.mouse_dragging = False
        self.selected = None
        self.selected_pos_ofs = vector.Vector()

        h = 0.  # 10 cm from the ground. nnope. for now, h has to be 0.
        n = Node( vector.Vector((0., h, 0.)), gltext )
        self.nodes.append(n)
        n = Node( vector.Vector((4., h, 0.)), gltext )
        self.nodes.append(n)
        n = Node( vector.Vector((6., h, -1.)), gltext )
        self.nodes.append(n)
        n = Node( vector.Vector((-2., h, 2.)), gltext )
        self.nodes.append(n)
        n = Node( vector.Vector((-3., h, -2.)), gltext )
        self.nodes.append(n)
        n = Node( vector.Vector((-11., h, 1.)), gltext )
        self.nodes.append(n)

    def tick(self, dt, keys):
        pass

    def render(self):
        for node in self.nodes:
            node.render()

    def render_overlay(self):
        for node in self.nodes:
            node.render_overlay()

    def recalculate_screen_pos(self, camera, camera_ocs, projection_mode, w_pixels, h_pixels):
        for node in self.nodes:
            # 1. proj obj to camera_ocs
            # 2. proj coord to screenspace
            v = camera_ocs.projv_in(node.pos)
            node.screen_pos.set(camera.screenspace(projection_mode, v, w_pixels, h_pixels))

    def intersects(self, sx, sy):
        for node in self.nodes:
            if node.intersects(float(sx), float(sy)):
                return node
        return None

    def event(self, event):
        if event.type == SDL_MOUSEMOTION:
            for node in self.nodes:
                node.mouse_hover = False
            node = self.intersects(event.motion.x, event.motion.y)
            if node:
                self.mouse_hover = True
                node.mouse_hover = True
            else:
                self.mouse_hover = False

            if self.selected and self.mouse.mouse_lbdown_floor_coord:
                self.selected.pos.set(self.mouse.mouse_floor_coord + self.selected_pos_ofs)

        elif event.type == SDL_MOUSEBUTTONDOWN:
            if event.button.button == SDL_BUTTON_LEFT:
                node = self.intersects(event.button.x, event.button.y)
                for n in self.nodes:
                    n.selected = False
                self.selected = node
                if node:
                    node.selected = True
                    self.selected_pos_ofs.set(node.pos - self.mouse.mouse_lbdown_floor_coord)
                    self.mouse_dragging = True

                ## find object under cursor. if no object, drag the world
                #self.mouse_dragging = True
                #self.object_under_cursor = None
                #self.mouse_floor_coord = self.get_pixel_floor_coord(event.button.x, event.button.y)
                #if self.mouse_floor_coord:
                #    self.mouse_lbdown_floor_coord = self.mouse_floor_coord.new()
                #    self.mouse_lbdown_camera_coord = self.camera_ocs.pos.new()
                #    self.mouse_lbdown_window_coord = (float(event.button.x), float(event.button.y))

        elif event.type == SDL_MOUSEBUTTONUP:
            if event.button.button == SDL_BUTTON_LEFT:
                self.mouse_dragging = False
                #self.mouse_dragging = False
                #self.mouse_lbdown_floor_coord = None
                #self.mouse_lbdown_camera_coord = None
                #self.mouse_lbdown_window_coord = None