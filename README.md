# homeassistant_ecowitt
Ecowitt driver for homeassistant

## Configuration:

    ecowitt:
      port: 4199
      barounit: metric
      windunit: imperial
      rainunit: imperial
      windchillunit: hybrid

Windchill can be one of "hybrid", "old", or "new".  Defaults for units are
as shown above.  The only mandatory "option" is "port".

## How to set up:

Use the WS View app for your Ecowitt device, and connect to it.  In the
configuration screens, where you set things like the wunderground connection,
move to the last screen, which is a custom connecition.

Pick the protocol Ecowitt, and put in the ip/hostname of your hass server.
Pick a port that is not in use on the server (netstat -lt).
Pick a reasonable value for updates, like 60 seconds.
Save configuration.  The Ecowitt should then start attempting to send data
to your server.

In homeassistant, cd ~/homeassistant/.homeassistant, mkdir custom_components,
git checkout this tree in there.

Add config to configuration.yaml.  Port is required.  Pick the same port you did
in the wsview app.

If you set a really long delay on updates, homeassistant could take awhile to
start.

If you get an error in the logs about an unhandled sensor, open an issue and
paste the log message so I can add the sensor.
