[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)

# Ecowitt Weather Station integration for home-assistant
Ecowitt driver for homeassistant

## Configuration:

    ecowitt:
      port: 4199
      barounit: metric
      windunit: imperial
      rainunit: imperial
      windchillunit: hybrid

Windchill can be one of "hybrid", "old", or "new".  Defaults for units are
as shown above.  The only mandatory "option" is "port".  Units can be one of
"metric" or "imperial".

## Warning

This device expects to be fed data from an ecowitt during hass startup.
Without this data, it doesn't know what devices to wire up.
Hopefully I can fix this in the future, but for now, do the setup on the
ecowitt device first, then add this to your configuration.yaml file.
If you do not, hass may hang on startup.

## How to set up:

Use the WS View app (on your phone) for your Ecowitt device, and connect to it.
Pick menu -> device list -> Pick your station.
Hit next repeatedly to move to the last screen titled "Customized"

Pick the protocol Ecowitt, and put in the ip/hostname of your hass server.
Path doesn't matter, pick the default.
Pick a port that is not in use on the server (netstat -lt). 
(4199 is probably a good default)
Pick a reasonable value for updates, like 60 seconds.
Save configuration.  The Ecowitt should then start attempting to send data
to your server.

Add config as shown above to configuration.yaml.  Port is required.
Pick the same port you did in the wsview app.

If you set a really long delay on updates, homeassistant could take awhile to
start.

If you get an error in the logs about an unhandled sensor, open an issue and
paste the log message so I can add the sensor.
