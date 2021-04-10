from PIL import Image, ImageDraw
from turn import Left, Right
import random
import math
import os

class CircleSpiralDrawer:
  def __init__(self, step_size=None, step_pattern=None):
    self.step_size = step_size or random.randint(4,10)
    self.seed      = step_pattern or self.random_step_pattern()
    self.scale     = 100
    self.theta     = 360/self.step_size
    self.phi       = 0    # Initial angle
    self.position  = (0,0) # Initial position
    self.construct_walk()

  def random_step_pattern(self, step_count=None):
    steps = step_count or random.randint(8,32)
    def is_invalid(pattern):
      bits = [0,0]
      while pattern > 0:
        bits[pattern % 2] += 1
        pattern >>= 1
      return (bits[0] - bits[1]) % self.step_size == 0
    pattern = random.randint(2**(steps - 1), 2**steps - 1)
    while is_invalid(pattern):
      print(pattern, "was not valid!")
      pattern = random.randint(2**(steps - 1), 2**steps - 1)
    return pattern

  def construct_pattern(self):
    step_value = self.seed
    walk_pattern = []
    while step_value > 0:
      if step_value & 1 == 1:
        walk_pattern.insert(0, Left)
      else:
        walk_pattern.insert(0, Right)
      step_value >>= 1
    return walk_pattern

  def construct_walk(self):
    self.walk = []
    for s in self.construct_pattern() * self.step_size:
      t = s(self.scale, self.theta, self.position, self.phi)
      self.walk.append(t)
      self.position = t.new_point()
      self.phi = t.new_angle()
    return self.walk

  def trace_walk(self, image_center, line_thickness=0.2, color="blue"):
    for s in self.construct_walk():
      s.draw(self.ctx, image_center, line_thickness, color)

  def canvas_size(self):
    min_x = 0
    min_y = 0
    max_x = 0
    max_y = 0
    for (x, y) in map(lambda s: s.position, self.walk):
      min_x = min(x, min_x)
      min_y = min(y, min_y)
      max_x = max(x, max_x)
      max_y = max(y, max_y)
    return (min_x, min_y, max_x, max_y)

  def trace_walks(self, lower_corner, image_size):
    light_color = tuple([random.randint(150,200) for _ in range(3)])
    dark_color  = tuple([random.randint(50,100) for _ in range(3)])
    line_size = max(image_size)/10000
    self.trace_walk(lower_corner, line_thickness=3*line_size, color="black")
    self.trace_walk(lower_corner, line_thickness=2*line_size, color=light_color)
    self.trace_walk(lower_corner, line_thickness=1*line_size, color=dark_color)

  def draw_image(self):
    (x_min, y_min, x_max, y_max) = self.canvas_size()
    walk_height = math.ceil(y_max - y_min + 4*self.scale)
    walk_width  = math.ceil(x_max - x_min + 4*self.scale)
    image_size = (2*walk_height, walk_height)
    img = Image.new("RGBA", image_size, (255,255,255,0))  # create new Image
    self.ctx = ImageDraw.Draw(img)  # create drawing context
    lower_corner = (x_min - 2*self.scale - (walk_height - walk_width/2), y_min - 2*self.scale)
    self.trace_walks(lower_corner, image_size)
    del self.ctx
    if walk_height > 2048:
      print("height is ", walk_height)
      img = img.resize((4096,2048), resample=Image.LANCZOS).quantize()
    file_name = "/tmp/robot_walk.png"
    img.save(file_name)
