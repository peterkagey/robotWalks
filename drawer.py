from PIL import Image, ImageDraw
from turn import Left, Right
import random
import os

class CircleSpiralDrawer:
  def __init__(self, step_size):
    self.scale = 200
    self.step_size = step_size
    self.theta = 360/step_size
    self.phi = 90
    self.height = self.scale*50
    self.width = self.scale*50
    self.position = (self.width//2,self.height//2)

  def turn(self, direction):
    t = direction(self.scale, self.theta, self.position, self.phi)
    t.draw(self.ctx)
    self.position = t.new_point()
    self.phi = t.new_angle()

  def draw_random(self):
    walk = [Right]
    walk_name = 1
    for _ in range(20):
      s = random.choice([0, 1])
      if s == 1:
        walk.append(Right)
      else:
        walk.append(Left)
      walk_name *= 2
      walk_name += s
    for s in (walk * self.step_size):
      self.turn(s)
    return str(walk_name)

  def draw_image(self):
    img = Image.new("RGBA", (self.width, self.height), (255,255,255,0))  # create new Image
    self.ctx = ImageDraw.Draw(img)  # create drawing context
    self.name = self.draw_random()
    del self.ctx
    file_name = "tmp/robot_walk_" + str(self.step_size) + "_" + self.name + ".png"
    img.save(file_name)
    os.system("open " + file_name)

CircleSpiralDrawer(7).draw_image()
