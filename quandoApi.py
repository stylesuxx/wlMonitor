#!/usr/bin/python
import sys, json, urllib2
import xml.etree.ElementTree as et

class Monitor:
  api = 'http://webservice.qando.at/2.0/webservice.ft'
  stations = None

  def __init__(self, inputPath):
    jsonData = open(inputPath)
    self.stations = json.load(jsonData)
    jsonData.close()

  ''' Return a JSON representation of the Departures for all stations '''
  def getDepartures(self):
    for station in self.stations:
      req = self.buildRequest(station)
      res = self.postRequest(req)
      departures = self.getDepartureTimes(res, station['towards'])
      station['departures'] = departures

    return self.stations

  ''' Build a XML request for the API '''
  def buildRequest(self, station):
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

  ''' Sends an XML request to the API and returns a tree object of the XML response'''
  def postRequest(self, xml):
    req = urllib2.Request(self.api, data = xml)
    res = urllib2.urlopen(req)
    data = res.read()
    tree = et.fromstring(data)

    return tree

  ''' Extract the departure times for a given direction '''
  def getDepartureTimes(self, xml, towards):
    departures = []
    departureTimes = xml.findall("./response/monitor/lines/line/[@towards='" + towards + "']/departures/departure/departureTime")
    for departure in departureTimes:
      time = departure.get('countdown')
      departures.append(time)
  
    return departures
