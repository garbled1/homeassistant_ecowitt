[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/hacs/integration)

# Ecowitt Weather Station integration for home-assistant
Ecowitt driver for homeassistant

![Bling](https://raw.githubusercontent.com/garbled1/homeassistant_ecowitt/master/md.images/overview.png)

## Configuration:

Configuration for the Ecowitt integration is now performed via a config flow
as opposed to yaml configuration file.

1. Go to HACS -> Integrations -> Click "+"
1. Search for "Ecowitt Weather Station" repository and add to HACS
1. Restart Home Assistant when it says to.
1. In Home Assistant, go to Configuration -> Integrations -> Click "+ Add Integration"
1. Search for "Ecowitt Weather Station" and follow the instructions to setup.

Ecowitt should now appear as a card under the HA Integrations page
with "Options" selection available at the bottom of the card.

You must select the port when enabling, see below section on "How to set up".

There are a few options available once the integration is setup, these are
available in the "options" dialog in the integrations box for the component.

* Barometer Unit (default metric)
* Wind Unit (default imperial)
* Rainfall Unit (default imperial)
* Lightning Unit (default imperial)
* Windchill Unit (default hybrid)

Windchill can be one of "hybrid", "old", or "new".
Defaults for units are as shown above.
Units can be one of "metric" or "imperial".

Note that if you change the units, it will create a new sensor for the
different unit.
For example, if you had wind set to imperial, "sensor.wind_speed" 
would have been your data entity, but switching to metric will create a
"sensor.wind_speed_2".
You will see in the entities page the original "sensor.wind_speed" will be
marked with a status of "Restored".
You can safely delete the old sensor once you validate you are seeing data
on the new one.
Be sure to update any automations/etc that reference the old sensor.


### Breaking changes

Version 0.5 converts this to a config flow from the previous yaml config method.
Once you restart hass, it will attempt to read your old config from yaml, and
port it over to the config flow.
Verify that it did so correctly, and double check the options match what you
expect for the units under "Options".

Additionally in 0.5, the battery sensors have been significantly changed.
Previously all batteries were simple floats with the raw value displayed.
There are 3 types of batteries that the ecowitt displays data for:

* Simple good/bad batteries.  These are now binary sensors.  This will leave
  A dead entry in your entities for the old battery sensor.  You may safely
  delete that entity.
* Voltage readings.  A few batteries display a voltage (soil, WH80).
  A soil battery is normally 1.5v, so a good alarm might be around 1.3?
  WH80 batteries seem to be about 2.38 - 2.4, so maybe in the 2.3 to 2.2 range
  for an alarm?
* Other batteries will now show as a percentage.
  The raw sensor gives a number from 0-5, this is simply multiplied by 20
  to give a percentage of 0-100.

If you were monitoring one of these, be sure to update any automations.

There was a bug in the wind gust sensors, where it was not being affected by
the windunit setting, once you load 0.5, you may find a dead entity for your
wind gust sensors that were setup for the wrong unit.
You may delete these.

Once your configuration has been moved, you should delete the old ecowitt
section from your configuration.yaml file and restart hass.


## How to set up:

Use the WS View app (on your phone) for your Ecowitt device, and connect to it.

1. Pick menu -> device list -> Pick your station.
1. Hit next repeatedly to move to the last screen titled "Customized"
1. Pick the protocol Ecowitt, and put in the ip/hostname of your hass server.
1. Path doesn't matter as long as it ends in /, leave the default, or change it to
	just /.
1. Pick a port that is not in use on the server (netstat -lt). 
   (4199 is probably a good default)
1. Pick a reasonable value for updates, like 60 seconds.
1. Save configuration.

The Ecowitt should then start attempting to send data to your server.

In home assistant, navigate to integrations, and search for the ecowitt component.
You will need to supply a port, and an optional name for the station (if you have
multiple stations this might be useful)
Pick the same port you did in the wsview app.

One note:  You may wish to setup the integration, and change the options for
the various units prior to setting up the physical device.
This will prevent creation of any entities for the wrong measurement unit from
being created if you decide to change one to a non-default.

## Errors in the logs

If you get an error in the logs about an unhandled sensor, open an issue and
paste the log message so I can add the sensor.

If you have a sensor that is barely in range, you will see a bunch of messages
in the logs about the sensor not being in the most recent update.
This can also be caused by a sensor that has a low battery.
If you know this sensor is just badly placed, you can ignore these, but if you
start seeing them for previously reliable sensors, check the batteries.


## Delay on startup

Older versions of this component would cause homeassistant to freeze on startup
waiting for the first sensor burst.
This is no longer the case.
Sensors will now show up as restored until the first data packet is recieved
from the ecowitt.
There should be no delay on startup at all.


## A note on leak sensors

Because leak sensors may be potentially important devices for automation,
they handle going out of range somewhat differently.
If a leak sensor is missing from the last data update from the ecowitt, it
will go into state Unknown.
If you rely upon a leak sensor for something vital, I suggest testing your
automation, by disconnecting the battery from the sensor, and validating
your code does something sane.


## I want a pretty card for my weather

I highly reccomend https://github.com/r-renato/ha-card-weather-conditions
It's fairly simple to setup as a custom card, and produces lovely results.
You can easily set it up to combine local data from your sensors, with
forcast data from external sources for sensors you don't have
(like pollen counts, for example).

This is a copy of my setup.
Sensors named with the sensor.cc_ are from the climacell external source,
other sensors are my local weatherstation.

```
air_quality:
  co: sensor.cc_co
  epa_aqi: sensor.cc_epa_aqi
  epa_health_concern: sensor.cc_epa_health_concern
  no2: sensor.cc_no2
  o3: sensor.cc_o3
  pm10: sensor.cc_pm10
  pm25: sensor.pm2_5_1
  so2: sensor.cc_so2
animation: true
name: WeatherStation
pollen:
  grass:
    entity: sensor.cc_pollen_grass
    high: 3
    low: 1
    max: 5
    min: 0
  tree:
    entity: sensor.cc_pollen_tree
    high: 3
    low: 1
    max: 5
    min: 0
  weed:
    entity: sensor.cc_pollen_weed
    high: 3
    low: 1
    max: 5
    min: 0
type: 'custom:ha-card-weather-conditions'
weather:
  current:
    current_conditions: sensor.cc_weather_condition
    feels_like: sensor.windchill
    forecast: true
    humidity: sensor.humidity
    precipitation: sensor.rain_rate
    pressure: sensor.absolute_pressure
    sun: sun.sun
    temperature: sensor.outdoor_temperature
    visibility: sensor.cc_visibility
    wind_bearing: sensor.wind_direction
    wind_speed: sensor.wind_speed
  forecast:
    icons:
      day_1: sensor.cc_weather_condition_0d
      day_2: sensor.cc_weather_condition_1d
      day_3: sensor.cc_weather_condition_2d
      day_4: sensor.cc_weather_condition_3d
      day_5: sensor.cc_weather_condition_4d
    precipitation_intensity:
      day_1: sensor.cc_max_precipitation_0d
      day_2: sensor.cc_max_precipitation_1d
      day_3: sensor.cc_max_precipitation_2d
      day_4: sensor.cc_max_precipitation_3d
      day_5: sensor.cc_max_precipitation_4d
    precipitation_probability:
      day_1: sensor.cc_precipitation_probability_0d
      day_2: sensor.cc_precipitation_probability_1d
      day_3: sensor.cc_precipitation_probability_2d
      day_4: sensor.cc_precipitation_probability_3d
      day_5: sensor.cc_precipitation_probability_4d
    temperature_high:
      day_1: sensor.cc_max_temperature_0d
      day_2: sensor.cc_max_temperature_1d
      day_3: sensor.cc_max_temperature_2d
      day_4: sensor.cc_max_temperature_3d
      day_5: sensor.cc_max_temperature_4d
    temperature_low:
      day_1: sensor.cc_min_temperature_0d
      day_2: sensor.cc_min_temperature_1d
      day_3: sensor.cc_min_temperature_2d
      day_4: sensor.cc_min_temperature_3d
      day_5: sensor.cc_min_temperature_4d
  icons_model: climacell
```
