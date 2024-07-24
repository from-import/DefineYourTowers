import pyglet
import math

class Bullet:
    def __init__(self, x, y, speed, damage, direction, window, faction):
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = damage
        self.direction = direction
        self.window = window
        self.faction = faction
        self.active = True

        # 加载子弹图像
        self.bullet_image = pyglet.resource.image('assets/Round/bullet.png')  # 请确保路径和文件名正确

    def update(self, dt):
        if self.active:
            rad = math.radians(self.direction)
            self.x += self.speed * dt * math.cos(rad)
            self.y += self.speed * dt * math.sin(rad)
            if (self.x < 0 or self.x > self.window.width or
                self.y < 0 or self.y > self.window.height):
                self.active = False

    def draw(self):
        if self.active:
            self.bullet_image.blit(self.x, self.y)

    def collides_with(self, target):
        return (self.x > target.x and self.x < target.x + target.width and
                self.y > target.y and self.y < target.y + target.height)
