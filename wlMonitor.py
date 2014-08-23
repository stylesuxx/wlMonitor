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
      fontStation = pygame.font.Font(None, 50)
      fontTowards = pygame.font.Font(None, 30)

      bgColor = (0, 0, 0)
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

      lineSurface = pygame.Surface([120, 70])
      lineSurface.fill(bgColor)
      text = fontLine.render(station['line'], 1, fgColor)
      textpos = text.get_rect(centerx = 60, centery = 35)
      lineSurface.blit(text, textpos)
      background.blit(lineSurface, [25, 27 + (80 * counter)])

      stationName = fontStation.render(station['fullname'], 1, (255, 255, 255))
      stationPos = stationName.get_rect(left = 180, top = 30 + 80 * counter)
      background.blit(stationName, stationPos)
      
      towards = fontTowards.render(station['towards'], 1, (255, 255, 255))
      towardsPos = towards.get_rect(left = 180, top = 70 + 80 * counter)
      background.blit(towards, towardsPos)

      inner = 0
      marked = False
      for departure in station['departures']:
        if inner > 4:
          break
        timeColor = (255, 255, 255)
        diff = int(departure) - int(station['walk'])
        if diff == 0:
          timeColor = (0, 255, 0)
        if diff > 0 and diff < 2:
          timeColor = (0, 0, 255)
        if diff < 0:
          timeColor = (255, 0, 0)

        time = fontLine.render(departure, 1, timeColor)
        timePos = time.get_rect(left = 530 + (100 * inner), top = 27 + 80 * counter)
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
