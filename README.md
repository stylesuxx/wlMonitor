# Wiener Linien Monitor
Show the countdown for the next departure of given public transport line from a specific station in a specific direction.

## Features
 * Show the next 3 (if available) departure times for each line of your choosing
 * Alert indication. If there is a problem with a chosen line the station name is shown in red
 * Color coded departure times. The departure times are color coded based on the walking distance: 
    * __Red__: You will most possibly not get this one anymore _(less than walking distance)_
    * __Blue__: Pack your stuff, put on your shoes and find your keys _(walking distance  + 2 minutes)_
    * __Green__: If you leave now you most propably will catch it _(walking distance + 1 minute)_
                                                                                
 * Output to Framebuffer - no X required - works great on a Raspberry Pi + small screen attached via composite (or HDMI)

## Configuration
Adapt **query.json** to your needs.

Each point of interes in the config files has the following mandatory fields:

 * __name__: The name of the station from which to depart. This is a number. To find the matching number for the station name, check this CSV: http://data.wien.gv.at/csv/wienerlinien-ogd-haltestellen.csv
 * __line__: The name of the line you want to see the departure times for
 * __towards__: This is the direction you are interested for. This usually is the name of the last station of the line.
 * __walk__: This is the amount of time you need to walk to a given station. Color coding of departure times is done based on this value.

## Usage
    usage: wlMonitor.py [-h] INPUT

    Display the departures from a given JSON file

    positional arguments:
      INPUT       Path to the input JSON file to parse

    optional arguments:
      -h, --help  show this help message and exit
