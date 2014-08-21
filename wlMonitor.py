#!/usr/bin/python
import sys, argparse, json, urllib2, urllib
import xml.etree.ElementTree as et

def main(args):
  opts = vars(args)

  data = open(opts['in'])
  stations = json.load(data)
  data.close()

  for station in stations:
    data = buildXML(station)
    departures = getDepartures(data, station['towards'])
    station['departures'] = departures

  data = json.dumps(stations, indent = 2)
  file = open(opts['out'], 'w')
  print >> file, data
  file.close()

def buildXML(station):
  ft = et.Element('ft')
  request = et.SubElement(ft, 'request')
  request.set('clientId', 'wlMonitor')
  request.set('apiName', 'api_get_monitor')
  request.set('apiVersion', '2.0')
  requestType = et.SubElement(request, 'requestType')
  requestType.text = 'api_get_monitor' 
  monitor = et.SubElement(request, 'monitor')
  name = et.SubElement(monitor, 'name')
  name.text = station['name']
  line = et.SubElement(monitor, 'line')
  line.text = station['line']

  tree = et.ElementTree(ft)
  return et.tostring(ft)

def getDepartures(xml, towards):
  departures = []
  api = 'http://webservice.qando.at/2.0/webservice.ft'
  request = urllib2.Request(api, data = xml)
  response = urllib2.urlopen(request)
  data = response.read()
  tree = et.fromstring(data)
  departureTimes = tree.findall("./response/monitor/lines/line/[@towards='" + towards + "']/departures/departure/departureTime")
  for departure in departureTimes:
    time = departure.get('countdown')
    departures.append(time)
  
  return departures

parser = argparse.ArgumentParser(description='Save the next departure times of given public transportations to a json file.')
parser.add_argument('in',
                    metavar = 'INPUT',
                    help = 'Path to the input JSON file to parse')

parser.add_argument('out',
                    metavar = 'OUTPUT',
                    help = 'Path to the output JSON file')

args = parser.parse_args()
main(args)
