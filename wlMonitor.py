#!/usr/bin/python
import sys, argparse, json, time, os, pygame
import xml.etree.ElementTree as et
from quandoApi import Monitor

class DisplaywlMonitor:
  screen = None
  monitor = None
  
  def __init__(self, args):
    opts = vars(args)
    self.monitor = Monitor(opts['in'])

    "Ininitializes a new pygame screen using the framebuffer"
    disp_no = os.getenv("DISPLAY")

    # Check which frame buffer drivers are available
    # Start with fbcon since directfb hangs with composite output
    drivers = ['fbcon', 'directfb', 'svgalib']
    found = False
    for driver in drivers:
      # Make sure that SDL_VIDEODRIVER is set
      if not os.getenv('SDL_VIDEODRIVER'):
        os.putenv('SDL_VIDEODRIVER', driver)
      try:
        pygame.display.init()
      except pygame.error:
        print 'Driver: {0} failed.'.format(driver)
        continue
      found = True
      break
    
    if not found:
      raise Exception('No suitable video driver found!')

    pygame.init()
    size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    self.screen.fill((0, 0, 0))        
    pygame.font.init()
    pygame.display.update()

  def __del__(self):
    pass

  def update(self):
    background = pygame.Surface(self.screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    topOffset = 0;
    counter = 0

    stations = self.monitor.getDepartures()
    for station in stations:
      fontLine = pygame.font.Font(None, 70)
      fontTowards = pygame.font.Font(None, 30)

      bgColor = (255, 0, 0)
      fgColor = (255, 255, 255)
      if station['line'] == 'U1':
        bgColor = (226, 20, 22)
      if station['line'] == 'U2':
        bgColor = (118, 71, 133)
      if station['line'] == 'U3':
        bgColor = (247, 96, 19)
      if station['line'] == 'U4':
        bgColor = (0, 129, 49)
      if station['line'] == 'U6':
        bgColor = (136, 71, 31)

      pygame.draw.rect(background, bgColor, [20, 20 + 80 * counter, 120, 70])
      text = fontLine.render(station['line'], 1, fgColor)
      textpos = text.get_rect(left = 50, top = 27 + (80 * counter))
      background.blit(text, textpos)

      towards = fontTowards.render(station['towards'], 1, (255, 255, 255))
      towardsPos = towards.get_rect(left = 180, top = 40 + 80 * counter)
      background.blit(towards, towardsPos)

      inner = 0
      marked = False
      for departure in station['departures']:
        timeColor = (255, 255, 255)
        if int(departure) - int(station['walk']) >= 0 and not marked:
          timeColor = (0, 255, 0)
          marked = True
        if int(departure) - int(station['walk']) < 0:
          timeColor = (255, 0, 0)

        time = fontLine.render(departure, 1, timeColor)
        timePos = time.get_rect(left = 440 + (100 * inner), top = 27 + 80 * counter)
        background.blit(time, timePos)
        inner += 1

      counter += 1

    self.screen.blit(background, (0, 0))
    pygame.display.flip()

parser = argparse.ArgumentParser(description = 'Display the departures from a given JSON file')
parser.add_argument('in',
                    metavar = 'INPUT',
                    help = 'Path to the input JSON file to parse')

args = parser.parse_args()
display = DisplaywlMonitor(args)
counter = 0
done = False
while not done:
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      done = True
  
  if counter % 30 == 0:
    display.update()
    counter = 0
  
  counter += 1
  time.sleep(1)

pygame.quit()
