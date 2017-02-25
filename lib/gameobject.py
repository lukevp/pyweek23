import pygame
from lib import utils
import config
from platform import PlatformManager

class GameObject(object):
    def __init__(self, pos, screenwidth, screenheight, displacement):
        self.rotation_vector = 0
        self.rotation = 0
        self.speed = 0
        self.position = pos
        self.displacement = displacement
        self.resize(screenwidth, screenheight)
        self.screenwidth = screenwidth
        self.screenheight = screenheight
        self.is_dead = False

class StarObject(GameObject):
    def __init__(self, images, pos, screenwidth, screenheight, displacement):
        self.images = []
        for image in images:
            self.images.append(pygame.image.load(config.IMAGE_ROOT + image))
        self.image_offset = 0
        self.framems = 80
        self.imagems = 0
        self.width = self.images[0].get_size()[0]
        self.height = self.images[0].get_size()[1]
        super(StarObject, self).__init__(pos, screenwidth, screenheight, displacement)

    def isdead(self):
        return self.is_dead

    def move(self, newpos, dt):
        #animate by switching images
        x,y = newpos
        if x < self.width / 2:
            x = self.width / 2
        if x > config.GAME_WIDTH - (self.width / 2):
            x = config.GAME_WIDTH - (self.width / 2)
        if y <  self.displacement - self.height:
            self.is_dead = True
        # if we are moving left, then start rotating left.
        # if we are moving right, start rotating right.
        if (self.position[0] < x): # we are moving right
            self.rotation_vector -= 0.01 * dt
        elif (self.position[0] > x): # we're moving left
            self.rotation_vector += 0.01 * dt
        else:
            #move vector back toward 0.
            if self.rotation_vector > 0:
                self.rotation_vector = max(0, self.rotation_vector - 0.05 * dt)
            else:
                self.rotation_vector = min(0, self.rotation_vector + 0.05 * dt)
        self.position = (x, y)
        return self.position

    def update(self, surf, displacement, dt):
        self.rotation += (dt / 5.0 * self.rotation_vector)
        self.imagems += dt
        while self.imagems > self.framems:
            self.image_offset = (self.image_offset + 1) % len(self.images)
            self.imagems -= self.framems
            self.resize(surf.get_size()[0], surf.get_size()[1])

        self.displacement = displacement
        self.rotated_image = utils.rot_center(self.resized_image, self.rotation)
        drawpos = self.getpos(surf.get_size())
        #self.rotated.center = self.resized_image.get_rect().center
        surf.blit(self.rotated_image, drawpos)

    def get_bottomleft(self):
        return self.position[0] - self.width / 2, self.position[1]
    def get_bottomright(self):
        return self.position[0] + self.width / 2, self.position[1]

    def resize(self, screenwidth, screenheight):
        heightratio = float(screenwidth) / config.GAME_HEIGHT
        widthratio = float(screenheight) / config.GAME_WIDTH
        img = self.images[self.image_offset]
        self.resized_image = utils.aspect_scale(img, (img.get_size()[0] * widthratio, img.get_size()[1] * heightratio))
        self.resized_image.convert()

    def getpos(self, screensize):
        #bottom of image is y, center of bottom of image is x.
        drawpos = utils.get_screen_coords(self.position, screensize, self.displacement)
        drawpos = drawpos[0] - self.resized_image.get_size()[0]/2, drawpos[1] - self.resized_image.get_size()[1]
        return drawpos

    def getscreenrect(self, screensize):
        drawpos = self.getpos(screensize)
        return pygame.rect.Rect(drawpos[0], drawpos[1], self.resized_image.get_size()[0], self.resized_image.get_size()[1]).inflate(30, 30)


class PlatformObject(GameObject):
    def __init__(self, manager, is_dark, pos, unitwidth, screenwidth, screenheight, displacement):
        self.is_dark = is_dark
        #TODO: set width and height and load image
        self.platform_manager = manager
        self.image = self.platform_manager.getplatformimage(unitwidth, self.is_dark)
        self.width = self.image.get_size()[0]
        self.height = self.image.get_size()[1]
        self.unitwidth = unitwidth
        super(PlatformObject, self).__init__(pos, screenwidth, screenheight, displacement)

    def is_star_colliding(self, bottomleft, bottomright):
        #only collide with a light platform.
        if not self.is_dark:
            #TODO: make this collide better
            if self.position[1] - 30 < bottomleft[1] < self.position[1] + 30 and \
                bottomright[0] >= self.position[0] and \
                bottomleft[0] <= self.position[0] + self.width:
                return True
        return False

    #TODO: implement this
    def is_onscreen(self, displacement):
        return True

    def toggle_dark(self):
        self.is_dark = not self.is_dark
        self.image = self.platform_manager.getplatformimage(self.unitwidth, self.is_dark)
        self.resize(self.screenwidth, self.screenheight)

    def update(self, surf, displacement, dt):
        self.displacement = displacement
        drawpos = self.getpos(surf.get_size())
        surf.blit(self.resized_image, drawpos)

    def resize(self, screenwidth, screenheight):
        heightratio = float(screenwidth) / config.GAME_HEIGHT
        widthratio = float(screenheight) / config.GAME_WIDTH
        self.resized_image = utils.aspect_scale(self.image, (self.image.get_size()[0] * widthratio, self.image.get_size()[1] * heightratio))
        self.resized_image.convert_alpha()
        self.screenwidth = screenwidth
        self.screenheight = screenheight

    def get_top(self):
        return self.position[1]

    def getpos(self, screensize):
        drawpos = utils.get_screen_coords(self.position, screensize, self.displacement)
        return drawpos

    def getscreenrect(self, screensize):
        drawpos = self.getpos(screensize)
        return pygame.rect.Rect(drawpos[0], drawpos[1], self.resized_image.get_size()[0], self.resized_image.get_size()[1]).inflate(30, 30)
