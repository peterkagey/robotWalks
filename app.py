from secrets import *
from drawer import CircleSpiralDrawer
import tweepy

class TwitterPoster:
  def __init__(self):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    self.api = tweepy.API(auth)

api = TwitterPoster().api

def pattern_word(seed):
  step_value = seed
  walk_pattern = []
  while step_value > 0:
    if step_value & 1 == 1:
      walk_pattern.insert(0, "R")
    else:
      walk_pattern.insert(0, "L")
    step_value >>= 1
  return "".join(walk_pattern)

def handler(event, context):
  if "step_size" in event and "step_pattern" in event:
    step_size = event['step_size']
    step_pattern = event['step_pattern']
    drawer = CircleSpiralDrawer(step_size, step_pattern)
  else:
    drawer = CircleSpiralDrawer()
    step_size = drawer.step_size
    step_pattern = drawer.seed

  drawer.draw_image()
  file_with_path = "/tmp/robot_walk.png"
  tweet_copy = "Step size: 1/" + str(step_size) + ".\nStep pattern: " + pattern_word(step_pattern) + "."
  api.update_with_media(filename=file_with_path, status=tweet_copy)
  return "Posted Tweet with message: '" + tweet_copy + "'"
