"""The Ecowitt Weather Station Component."""
import asyncio
import logging
import time

from pyecowitt import (
    EcoWittListener,
    WINDCHILL_OLD,
    WINDCHILL_NEW,
    WINDCHILL_HYBRID,
)
import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.discovery import async_load_platform
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import (
    async_dispatcher_connect,
    async_dispatcher_send,
)
from homeassistant.helpers.entity import Entity

from homeassistant.const import (
    DEGREE,
    CONF_PORT,
    CONF_UNIT_SYSTEM_METRIC,
    CONF_UNIT_SYSTEM_IMPERIAL,
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    POWER_WATT,
    TEMP_CELSIUS,
    PERCENTAGE,
    PRESSURE_HPA,
    PRESSURE_INHG,
    LENGTH_INCHES,
    LENGTH_KILOMETERS,
    LENGTH_MILES,
    SPEED_KILOMETERS_PER_HOUR,
    SPEED_MILES_PER_HOUR,
    TIME_HOURS,
    TIME_DAYS,
    TIME_WEEKS,
    TIME_MONTHS,
    TIME_YEARS,
    UV_INDEX,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_ILLUMINANCE,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_PRESSURE,
    DEVICE_CLASS_TIMESTAMP,
)

from homeassistant.components.binary_sensor import (
    DEVICE_CLASS_MOISTURE,
)

_LOGGER = logging.getLogger(__name__)

TYPE_SENSOR = "sensor"
TYPE_BINARY_SENSOR = "binary_sensor"
DOMAIN = "ecowitt"
DATA_CONFIG = "config"
DATA_ECOWITT = "ecowitt_listener"
DATA_STATION = "station"
DATA_PASSKEY = "PASSKEY"
DATA_STATIONTYPE = "stationtype"
DATA_FREQ = "freq"
DATA_MODEL = "model"
DATA_READY = "ready"

CONF_UNIT_BARO = "barounit"
CONF_UNIT_WIND = "windunit"
CONF_UNIT_RAIN = "rainunit"
CONF_UNIT_WINDCHILL = "windchillunit"
CONF_UNIT_LIGHTNING = "lightningunit"

TYPE_BAROMABSHPA = "baromabshpa"
TYPE_BAROMRELHPA = "baromrelhpa"
TYPE_BAROMABSIN = "baromabsin"
TYPE_BAROMRELIN = "baromrelin"
TYPE_RAINRATEIN = "rainratein"
TYPE_EVENTRAININ = "eventrainin"
TYPE_HOURLYRAININ = "hourlyrainin"
TYPE_TOTALRAININ = "totalrainin"
TYPE_DAILYRAININ = "dailyrainin"
TYPE_WEEKLYRAININ = "weeklyrainin"
TYPE_MONTHLYRAININ = "monthlyrainin"
TYPE_YEARLYRAININ = "yearlyrainin"
TYPE_RAINRATEMM = "rainratemm"
TYPE_EVENTRAINMM = "eventrainmm"
TYPE_HOURLYRAINMM = "hourlyrainmm"
TYPE_TOTALRAINMM = "totalrainmm"
TYPE_DAILYRAINMM = "dailyrainmm"
TYPE_WEEKLYRAINMM = "weeklyrainmm"
TYPE_MONTHLYRAINMM = "monthlyrainmm"
TYPE_YEARLYRAINMM = "yearlyrainmm"
TYPE_HUMIDITY = "humidity"
TYPE_HUMIDITY1 = "humidity1"
TYPE_HUMIDITY2 = "humidity2"
TYPE_HUMIDITY3 = "humidity3"
TYPE_HUMIDITY4 = "humidity4"
TYPE_HUMIDITY5 = "humidity5"
TYPE_HUMIDITY6 = "humidity6"
TYPE_HUMIDITY7 = "humidity7"
TYPE_HUMIDITY8 = "humidity8"
TYPE_HUMIDITYIN = "humidityin"
TYPE_WINDDIR = "winddir"
TYPE_WINDDIR_A10 = "winddir_avg10m"
TYPE_WINDSPEEDKMH = "windspeedkmh"
TYPE_WINDSPEEDKMH_A10 = "windspdkmh_avg10m"
TYPE_WINDGUSTKMH = "windgustkmh"
TYPE_WINDSPEEDMPH = "windspeedmph"
TYPE_WINDSPEEDMPH_A10 = "windspdmph_avg10m"
TYPE_WINDGUSTMPH = "windgustmph"
TYPE_MAXDAILYGUST = "maxdailygust"
TYPE_MAXDAILYGUSTKMH = "maxdailygustkmh"
TYPE_TEMPC = "tempc"
TYPE_TEMPINC = "tempinc"
TYPE_TEMP1C = "temp1c"
TYPE_TEMP2C = "temp2c"
TYPE_TEMP3C = "temp3c"
TYPE_TEMP4C = "temp4c"
TYPE_TEMP5C = "temp5c"
TYPE_TEMP6C = "temp6c"
TYPE_TEMP7C = "temp7c"
TYPE_TEMP8C = "temp8c"
TYPE_DEWPOINTC = "dewpointc"
TYPE_DEWPOINTINC = "dewpointinc"
TYPE_DEWPOINT1C = "dewpoint1c"
TYPE_DEWPOINT2C = "dewpoint2c"
TYPE_DEWPOINT3C = "dewpoint3c"
TYPE_DEWPOINT4C = "dewpoint4c"
TYPE_DEWPOINT5C = "dewpoint5c"
TYPE_DEWPOINT6C = "dewpoint6c"
TYPE_DEWPOINT7C = "dewpoint7c"
TYPE_DEWPOINT8C = "dewpoint8c"
TYPE_WINDCHILLC = "windchillc"
TYPE_SOLARRADIATION = "solarradiation"
TYPE_UV = "uv"
TYPE_SOILMOISTURE1 = "soilmoisture1"
TYPE_SOILMOISTURE2 = "soilmoisture2"
TYPE_SOILMOISTURE3 = "soilmoisture3"
TYPE_SOILMOISTURE4 = "soilmoisture4"
TYPE_SOILMOISTURE5 = "soilmoisture5"
TYPE_SOILMOISTURE6 = "soilmoisture6"
TYPE_SOILMOISTURE7 = "soilmoisture7"
TYPE_SOILMOISTURE8 = "soilmoisture8"
TYPE_PM25_CH1 = "pm25_ch1"
TYPE_PM25_CH2 = "pm25_ch2"
TYPE_PM25_CH3 = "pm25_ch3"
TYPE_PM25_CH4 = "pm25_ch4"
TYPE_PM25_AVG_24H_CH1 = "pm25_avg_24h_ch1"
TYPE_PM25_AVG_24H_CH2 = "pm25_avg_24h_ch2"
TYPE_PM25_AVG_24H_CH3 = "pm25_avg_24h_ch3"
TYPE_PM25_AVG_24H_CH4 = "pm25_avg_24h_ch4"
TYPE_LIGHTNING_TIME = "lightning_time"
TYPE_LIGHTNING_NUM = "lightning_num"
TYPE_LIGHTNING_KM = "lightning"
TYPE_LIGHTNING_MI = "lightning_mi"
TYPE_LEAK_CH1 = "leak_ch1"
TYPE_LEAK_CH2 = "leak_ch2"
TYPE_LEAK_CH3 = "leak_ch3"
TYPE_LEAK_CH4 = "leak_ch4"
TYPE_WH25BATT = "wh25batt"
TYPE_WH26BATT = "wh26batt"
TYPE_WH40BATT = "wh40batt"
TYPE_WH57BATT = "wh57batt"
TYPE_WH68BATT = "wh68batt"
TYPE_WH65BATT = "wh65batt"
TYPE_WH80BATT = "wh80batt"
TYPE_SOILBATT1 = "soilbatt1"
TYPE_SOILBATT2 = "soilbatt2"
TYPE_SOILBATT3 = "soilbatt3"
TYPE_SOILBATT4 = "soilbatt4"
TYPE_SOILBATT5 = "soilbatt5"
TYPE_SOILBATT6 = "soilbatt6"
TYPE_SOILBATT7 = "soilbatt7"
TYPE_SOILBATT8 = "soilbatt8"
TYPE_BATTERY1 = "batt1"
TYPE_BATTERY2 = "batt2"
TYPE_BATTERY3 = "batt3"
TYPE_BATTERY4 = "batt4"
TYPE_BATTERY5 = "batt5"
TYPE_BATTERY6 = "batt6"
TYPE_BATTERY7 = "batt7"
TYPE_BATTERY8 = "batt8"
TYPE_PM25BATT1 = "pm25batt1"
TYPE_PM25BATT2 = "pm25batt2"
TYPE_PM25BATT3 = "pm25batt3"
TYPE_PM25BATT4 = "pm25batt4"
TYPE_PM25BATT5 = "pm25batt5"
TYPE_PM25BATT6 = "pm25batt6"
TYPE_PM25BATT7 = "pm25batt7"
TYPE_PM25BATT8 = "pm25batt8"
TYPE_LEAKBATT1 = "leakbatt1"
TYPE_LEAKBATT2 = "leakbatt2"
TYPE_LEAKBATT3 = "leakbatt3"
TYPE_LEAKBATT4 = "leakbatt4"
TYPE_LEAKBATT5 = "leakbatt5"
TYPE_LEAKBATT6 = "leakbatt6"
TYPE_LEAKBATT7 = "leakbatt7"
TYPE_LEAKBATT8 = "leakbatt8"

S_METRIC = 1
S_IMPERIAL = 2

W_TYPE_NEW = "new"
W_TYPE_OLD = "old"
W_TYPE_HYBRID = "hybrid"

LEAK_DETECTED = "Leak Detected"

# Name, unit_of_measure, type, device_class, icon, metric=1
# name, uom, kind, device_class, icon, metric = SENSOR_TYPES[x]
SENSOR_TYPES = {
    TYPE_BAROMABSHPA: ("Absolute Pressure", PRESSURE_HPA,
                       TYPE_SENSOR, DEVICE_CLASS_PRESSURE,
                       "mdi:gauge", S_METRIC),
    TYPE_BAROMRELHPA: ("Relative Pressure", PRESSURE_HPA,
                       TYPE_SENSOR, DEVICE_CLASS_PRESSURE,
                       "mdi:gauge", S_METRIC),
    TYPE_BAROMABSIN: ("Absolute Pressure", PRESSURE_INHG,
                      TYPE_SENSOR, DEVICE_CLASS_PRESSURE,
                      "mdi:gauge", S_IMPERIAL),
    TYPE_BAROMRELIN: ("Relative Pressure", PRESSURE_INHG,
                      TYPE_SENSOR, DEVICE_CLASS_PRESSURE,
                      "mdi:gauge", S_IMPERIAL),
    TYPE_RAINRATEIN: ("Rain Rate", f"{LENGTH_INCHES}/{TIME_HOURS}",
                      TYPE_SENSOR, None, "mdi:water", S_IMPERIAL),
    TYPE_EVENTRAININ: ("Event Rain Rate", f"{LENGTH_INCHES}/{TIME_HOURS}",
                       TYPE_SENSOR, None, "mdi:water", S_IMPERIAL),
    TYPE_HOURLYRAININ: ("Hourly Rain Rate", f"{LENGTH_INCHES}/{TIME_HOURS}",
                        TYPE_SENSOR, None, "mdi:water", S_IMPERIAL),
    TYPE_TOTALRAININ: ("Total Rain Rate", f"{LENGTH_INCHES}",
                       TYPE_SENSOR, None, "mdi:water", S_IMPERIAL),
    TYPE_DAILYRAININ: ("Daily Rain Rate", f"{LENGTH_INCHES}/{TIME_DAYS}",
                       TYPE_SENSOR, None, "mdi:water", S_IMPERIAL),
    TYPE_WEEKLYRAININ: ("Weekly Rain Rate", f"{LENGTH_INCHES}/{TIME_WEEKS}",
                        TYPE_SENSOR, None, "mdi:water", S_IMPERIAL),
    TYPE_MONTHLYRAININ: ("Monthly Rain Rate", f"{LENGTH_INCHES}/{TIME_MONTHS}",
                         TYPE_SENSOR, None, "mdi:water", S_IMPERIAL),
    TYPE_YEARLYRAININ: ("Yearly Rain Rate", f"{LENGTH_INCHES}/{TIME_YEARS}",
                        TYPE_SENSOR, None, "mdi:water", S_IMPERIAL),
    TYPE_RAINRATEMM: ("Rain Rate", f"mm/{TIME_HOURS}",
                      TYPE_SENSOR, None, "mdi:water", S_METRIC),
    TYPE_EVENTRAINMM: ("Event Rain Rate", f"mm/{TIME_HOURS}",
                       TYPE_SENSOR, None, "mdi:water", S_METRIC),
    TYPE_HOURLYRAINMM: ("Hourly Rain Rate", f"mm/{TIME_HOURS}",
                        TYPE_SENSOR, None, "mdi:water", S_METRIC),
    TYPE_TOTALRAINMM: ("Total Rain Rate", f"mm",
                       TYPE_SENSOR, None, "mdi:water", S_METRIC),
    TYPE_DAILYRAINMM: ("Daily Rain Rate", f"mm/{TIME_DAYS}",
                       TYPE_SENSOR, None, "mdi:water", S_METRIC),
    TYPE_WEEKLYRAINMM: ("Weekly Rain Rate", f"mm/{TIME_WEEKS}",
                        TYPE_SENSOR, None, "mdi:water", S_METRIC),
    TYPE_MONTHLYRAINMM: ("Monthly Rain Rate", f"mm/{TIME_MONTHS}",
                         TYPE_SENSOR, None, "mdi:water", S_METRIC),
    TYPE_YEARLYRAINMM: ("Yearly Rain Rate", f"mm/{TIME_YEARS}",
                        TYPE_SENSOR, None, "mdi:water", S_METRIC),
    TYPE_HUMIDITY: ("Humidity", PERCENTAGE,
                    TYPE_SENSOR, DEVICE_CLASS_HUMIDITY,
                    "mdi:water-percent", 0),
    TYPE_HUMIDITYIN: ("Indoor Humidity", PERCENTAGE,
                      TYPE_SENSOR, DEVICE_CLASS_HUMIDITY,
                      "mdi:water-percent", 0),
    TYPE_HUMIDITY1: ("Humidity 1", PERCENTAGE,
                     TYPE_SENSOR, DEVICE_CLASS_HUMIDITY,
                     "mdi:water-percent", 0),
    TYPE_HUMIDITY2: ("Humidity 2", PERCENTAGE,
                     TYPE_SENSOR, DEVICE_CLASS_HUMIDITY,
                     "mdi:water-percent", 0),
    TYPE_HUMIDITY3: ("Humidity 3", PERCENTAGE,
                     TYPE_SENSOR, DEVICE_CLASS_HUMIDITY,
                     "mdi:water-percent", 0),
    TYPE_HUMIDITY4: ("Humidity 4", PERCENTAGE,
                     TYPE_SENSOR, DEVICE_CLASS_HUMIDITY,
                     "mdi:water-percent", 0),
    TYPE_HUMIDITY5: ("Humidity 5", PERCENTAGE,
                     TYPE_SENSOR, DEVICE_CLASS_HUMIDITY,
                     "mdi:water-percent", 0),
    TYPE_HUMIDITY6: ("Humidity 6", PERCENTAGE,
                     TYPE_SENSOR, DEVICE_CLASS_HUMIDITY,
                     "mdi:water-percent", 0),
    TYPE_HUMIDITY7: ("Humidity 7", PERCENTAGE,
                     TYPE_SENSOR, DEVICE_CLASS_HUMIDITY,
                     "mdi:water-percent", 0),
    TYPE_HUMIDITY8: ("Humidity 8", PERCENTAGE,
                     TYPE_SENSOR, DEVICE_CLASS_HUMIDITY,
                     "mdi:water-percent", 0),
    TYPE_WINDDIR: ("Wind Direction", DEGREE,
                   TYPE_SENSOR, None, "mdi:water-percent", 0),
    TYPE_WINDDIR_A10: ("Wind Direction 10m Avg", DEGREE,
                       TYPE_SENSOR, None, "mdi:water-percent", 0),
    TYPE_WINDSPEEDKMH: ("Wind Speed", SPEED_KILOMETERS_PER_HOUR,
                        TYPE_SENSOR, None, "mdi:weather-windy", S_METRIC),
    TYPE_WINDSPEEDKMH_A10: ("Wind Speed 10m Avg", SPEED_KILOMETERS_PER_HOUR,
                            TYPE_SENSOR, None, "mdi:weather-windy", S_METRIC),
    TYPE_WINDGUSTKMH: ("Wind Gust", SPEED_KILOMETERS_PER_HOUR,
                       TYPE_SENSOR, None, "mdi:weather-windy", S_METRIC),
    TYPE_WINDSPEEDMPH: ("Wind Speed", SPEED_MILES_PER_HOUR,
                        TYPE_SENSOR, None, "mdi:weather-windy", S_IMPERIAL),
    TYPE_WINDSPEEDMPH_A10: ("Wind Speed 10m Avg", SPEED_MILES_PER_HOUR,
                            TYPE_SENSOR, None, "mdi:weather-windy",
                            S_IMPERIAL),
    TYPE_WINDGUSTMPH: ("Wind Gust", SPEED_MILES_PER_HOUR,
                       TYPE_SENSOR, None, "mdi:weather-windy", S_IMPERIAL),
    TYPE_MAXDAILYGUST: ("Max Daily Wind Gust", SPEED_MILES_PER_HOUR,
                        TYPE_SENSOR, None, "mdi:weather-windy", S_IMPERIAL),
    TYPE_MAXDAILYGUSTKMH: ("Max Daily Wind Gust", SPEED_KILOMETERS_PER_HOUR,
                           TYPE_SENSOR, None, "mdi:weather-windy", S_METRIC),
    TYPE_TEMPC: ("Outdoor Temperature", TEMP_CELSIUS,
                 TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE, "mdi:thermometer", 0),
    TYPE_TEMP1C: ("Temperature 1", TEMP_CELSIUS,
                  TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE, "mdi:thermometer", 0),
    TYPE_TEMP2C: ("Temperature 2", TEMP_CELSIUS,
                  TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE, "mdi:thermometer", 0),
    TYPE_TEMP3C: ("Temperature 3", TEMP_CELSIUS,
                  TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE, "mdi:thermometer", 0),
    TYPE_TEMP4C: ("Temperature 4", TEMP_CELSIUS,
                  TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE, "mdi:thermometer", 0),
    TYPE_TEMP5C: ("Temperature 5", TEMP_CELSIUS,
                  TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE, "mdi:thermometer", 0),
    TYPE_TEMP6C: ("Temperature 6", TEMP_CELSIUS,
                  TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE, "mdi:thermometer", 0),
    TYPE_TEMP7C: ("Temperature 7", TEMP_CELSIUS,
                  TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE, "mdi:thermometer", 0),
    TYPE_TEMP8C: ("Temperature 8", TEMP_CELSIUS,
                  TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE, "mdi:thermometer", 0),
    TYPE_TEMPINC: ("Indoor Temperature", TEMP_CELSIUS,
                   TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE,
                   "mdi:thermometer", 0),
    TYPE_DEWPOINTC: ("Dewpoint", TEMP_CELSIUS,
                     TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE,
                     "mdi:thermometer", 0),
    TYPE_DEWPOINTINC: ("Indoor Dewpoint", TEMP_CELSIUS,
                       TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE,
                       "mdi:thermometer", 0),
    TYPE_DEWPOINT1C: ("Dewpoint 1", TEMP_CELSIUS,
                      TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE,
                      "mdi:thermometer", 0),
    TYPE_DEWPOINT2C: ("Dewpoint 2", TEMP_CELSIUS,
                      TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE,
                      "mdi:thermometer", 0),
    TYPE_DEWPOINT3C: ("Dewpoint 3", TEMP_CELSIUS,
                      TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE,
                      "mdi:thermometer", 0),
    TYPE_DEWPOINT4C: ("Dewpoint 4", TEMP_CELSIUS,
                      TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE,
                      "mdi:thermometer", 0),
    TYPE_DEWPOINT5C: ("Dewpoint 5", TEMP_CELSIUS,
                      TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE,
                      "mdi:thermometer", 0),
    TYPE_DEWPOINT6C: ("Dewpoint 6", TEMP_CELSIUS,
                      TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE,
                      "mdi:thermometer", 0),
    TYPE_DEWPOINT7C: ("Dewpoint 7", TEMP_CELSIUS,
                      TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE,
                      "mdi:thermometer", 0),
    TYPE_DEWPOINT8C: ("Dewpoint 8", TEMP_CELSIUS,
                      TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE,
                      "mdi:thermometer", 0),
    TYPE_WINDCHILLC: ("Windchill", TEMP_CELSIUS,
                      TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE,
                      "mdi:thermometer", 0),
    TYPE_SOLARRADIATION: ("Solar Radiation", f"{POWER_WATT}/m^2",
                          TYPE_SENSOR, DEVICE_CLASS_ILLUMINANCE,
                          "mdi:weather-sunny", 0),
    TYPE_UV: ("UV Index", UV_INDEX,
              TYPE_SENSOR, None, "mdi:sunglasses", 0),
    TYPE_SOILMOISTURE1: ("Soil Moisture 1", PERCENTAGE,
                         TYPE_SENSOR, DEVICE_CLASS_HUMIDITY,
                         "mdi:water-percent", 0),
    TYPE_SOILMOISTURE2: ("Soil Moisture 2", PERCENTAGE,
                         TYPE_SENSOR, DEVICE_CLASS_HUMIDITY,
                         "mdi:water-percent", 0),
    TYPE_SOILMOISTURE3: ("Soil Moisture 3", PERCENTAGE,
                         TYPE_SENSOR, DEVICE_CLASS_HUMIDITY,
                         "mdi:water-percent", 0),
    TYPE_SOILMOISTURE4: ("Soil Moisture 4", PERCENTAGE,
                         TYPE_SENSOR, DEVICE_CLASS_HUMIDITY,
                         "mdi:water-percent", 0),
    TYPE_SOILMOISTURE5: ("Soil Moisture 5", PERCENTAGE,
                         TYPE_SENSOR, DEVICE_CLASS_HUMIDITY,
                         "mdi:water-percent", 0),
    TYPE_SOILMOISTURE6: ("Soil Moisture 6", PERCENTAGE,
                         TYPE_SENSOR, DEVICE_CLASS_HUMIDITY,
                         "mdi:water-percent", 0),
    TYPE_SOILMOISTURE7: ("Soil Moisture 7", PERCENTAGE,
                         TYPE_SENSOR, DEVICE_CLASS_HUMIDITY,
                         "mdi:water-percent", 0),
    TYPE_SOILMOISTURE8: ("Soil Moisture 8", PERCENTAGE,
                         TYPE_SENSOR, DEVICE_CLASS_HUMIDITY,
                         "mdi:water-percent", 0),
    TYPE_PM25_CH1: ("PM2.5 1", CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                    TYPE_SENSOR, None, "mdi:eye", 0),
    TYPE_PM25_CH2: ("PM2.5 2", CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                    TYPE_SENSOR, None, "mdi:eye", 0),
    TYPE_PM25_CH3: ("PM2.5 3", CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                    TYPE_SENSOR, None, "mdi:eye", 0),
    TYPE_PM25_CH4: ("PM2.5 4", CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                    TYPE_SENSOR, None, "mdi:eye", 0),
    TYPE_PM25_AVG_24H_CH1: ("PM2.5 24h average 1",
                            CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                            TYPE_SENSOR, None, "mdi:eye", 0),
    TYPE_PM25_AVG_24H_CH2: ("PM2.5 24h average 2",
                            CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                            TYPE_SENSOR, None, "mdi:eye", 0),
    TYPE_PM25_AVG_24H_CH3: ("PM2.5 24h average 3",
                            CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                            TYPE_SENSOR, None, "mdi:eye", 0),
    TYPE_PM25_AVG_24H_CH4: ("PM2.5 24h average 4",
                            CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                            TYPE_SENSOR, None, "mdi:eye", 0),
    TYPE_LIGHTNING_TIME: ("Last Lightning strike", "",
                          TYPE_SENSOR, DEVICE_CLASS_TIMESTAMP, "mdi:clock", 0),
    TYPE_LIGHTNING_NUM: ("Lightning strikes", f"strikes/{TIME_DAYS}",
                         TYPE_SENSOR, None, "mdi:weather-lightning", 0),
    TYPE_LIGHTNING_KM: ("Lightning strike distance", LENGTH_KILOMETERS,
                        TYPE_SENSOR, None, "mdi:ruler", S_METRIC),
    TYPE_LIGHTNING_MI: ("Lightning strike distance", LENGTH_MILES,
                        TYPE_SENSOR, None, "mdi:ruler", S_IMPERIAL),
    TYPE_LEAK_CH1: ("Leak Detection 1", LEAK_DETECTED, TYPE_BINARY_SENSOR,
                    DEVICE_CLASS_MOISTURE, "mdi:leak", 0),
    TYPE_LEAK_CH2: ("Leak Detection 2", LEAK_DETECTED, TYPE_BINARY_SENSOR,
                    DEVICE_CLASS_MOISTURE, "mdi:leak", 0),
    TYPE_LEAK_CH3: ("Leak Detection 3", LEAK_DETECTED, TYPE_BINARY_SENSOR,
                    DEVICE_CLASS_MOISTURE, "mdi:leak", 0),
    TYPE_LEAK_CH4: ("Leak Detection 4", LEAK_DETECTED, TYPE_BINARY_SENSOR,
                    DEVICE_CLASS_MOISTURE, "mdi:leak", 0),
    TYPE_WH25BATT: ("WH25 Battery", "BATT", TYPE_SENSOR,
                    None, "mdi:battery", 0),
    TYPE_WH26BATT: ("WH26 Battery", "BATT", TYPE_SENSOR,
                    None, "mdi:battery", 0),
    TYPE_WH40BATT: ("WH40 Battery", "BATT", TYPE_SENSOR,
                    None, "mdi:battery", 0),
    TYPE_WH57BATT: ("WH57 Battery", "BATT", TYPE_SENSOR,
                    None, "mdi:battery", 0),
    TYPE_WH65BATT: ("WH65 Battery", "BATT", TYPE_SENSOR,
                    None, "mdi:battery", 0),
    TYPE_WH68BATT: ("WH68 Battery", "BATT", TYPE_SENSOR,
                    None, "mdi:battery", 0),
    TYPE_WH80BATT: ("WH80 Battery", "BATT", TYPE_SENSOR,
                    None, "mdi:battery", 0),
    TYPE_SOILBATT1: ("Soil Moisture 1 Battery", "BATT", TYPE_SENSOR,
                     None, "mdi:battery", 0),
    TYPE_SOILBATT2: ("Soil Moisture 2 Battery", "BATT", TYPE_SENSOR,
                     None, "mdi:battery", 0),
    TYPE_SOILBATT3: ("Soil Moisture 3 Battery", "BATT", TYPE_SENSOR,
                     None, "mdi:battery", 0),
    TYPE_SOILBATT4: ("Soil Moisture 4 Battery", "BATT", TYPE_SENSOR,
                     None, "mdi:battery", 0),
    TYPE_SOILBATT5: ("Soil Moisture 5 Battery", "BATT", TYPE_SENSOR,
                     None, "mdi:battery", 0),
    TYPE_SOILBATT6: ("Soil Moisture 6 Battery", "BATT", TYPE_SENSOR,
                     None, "mdi:battery", 0),
    TYPE_SOILBATT7: ("Soil Moisture 7 Battery", "BATT", TYPE_SENSOR,
                     None, "mdi:battery", 0),
    TYPE_SOILBATT8: ("Soil Moisture 8 Battery", "BATT", TYPE_SENSOR,
                     None, "mdi:battery", 0),
    TYPE_BATTERY1: ("Battery 1", "BATT", TYPE_SENSOR,
                    None, "mdi:battery", 0),
    TYPE_BATTERY2: ("Battery 2", "BATT", TYPE_SENSOR,
                    None, "mdi:battery", 0),
    TYPE_BATTERY3: ("Battery 3", "BATT", TYPE_SENSOR,
                    None, "mdi:battery", 0),
    TYPE_BATTERY4: ("Battery 4", "BATT", TYPE_SENSOR,
                    None, "mdi:battery", 0),
    TYPE_BATTERY5: ("Battery 5", "BATT", TYPE_SENSOR,
                    None, "mdi:battery", 0),
    TYPE_BATTERY6: ("Battery 6", "BATT", TYPE_SENSOR,
                    None, "mdi:battery", 0),
    TYPE_BATTERY7: ("Battery 7", "BATT", TYPE_SENSOR,
                    None, "mdi:battery", 0),
    TYPE_BATTERY8: ("Battery 8", "BATT", TYPE_SENSOR,
                    None, "mdi:battery", 0),
    TYPE_PM25BATT1: ("PM2.5 1 Battery", "BATT", TYPE_SENSOR,
                     None, "mdi:battery", 0),
    TYPE_PM25BATT2: ("PM2.5 2 Battery", "BATT", TYPE_SENSOR,
                     None, "mdi:battery", 0),
    TYPE_PM25BATT3: ("PM2.5 3 Battery", "BATT", TYPE_SENSOR,
                     None, "mdi:battery", 0),
    TYPE_PM25BATT4: ("PM2.5 4 Battery", "BATT", TYPE_SENSOR,
                     None, "mdi:battery", 0),
    TYPE_PM25BATT5: ("PM2.5 5 Battery", "BATT", TYPE_SENSOR,
                     None, "mdi:battery", 0),
    TYPE_PM25BATT6: ("PM2.5 6 Battery", "BATT", TYPE_SENSOR,
                     None, "mdi:battery", 0),
    TYPE_PM25BATT7: ("PM2.5 7 Battery", "BATT", TYPE_SENSOR,
                     None, "mdi:battery", 0),
    TYPE_PM25BATT8: ("PM2.5 8 Battery", "BATT", TYPE_SENSOR,
                     None, "mdi:battery", 0),
    TYPE_LEAKBATT1: ("Leak 1 Battery", "BATT", TYPE_SENSOR,
                     None, "mdi:battery", 0),
    TYPE_LEAKBATT2: ("Leak 2 Battery", "BATT", TYPE_SENSOR,
                     None, "mdi:battery", 0),
    TYPE_LEAKBATT3: ("Leak 3 Battery", "BATT", TYPE_SENSOR,
                     None, "mdi:battery", 0),
    TYPE_LEAKBATT4: ("Leak 4 Battery", "BATT", TYPE_SENSOR,
                     None, "mdi:battery", 0),
    TYPE_LEAKBATT5: ("Leak 5 Battery", "BATT", TYPE_SENSOR,
                     None, "mdi:battery", 0),
    TYPE_LEAKBATT6: ("Leak 6 Battery", "BATT", TYPE_SENSOR,
                     None, "mdi:battery", 0),
    TYPE_LEAKBATT7: ("Leak 7 Battery", "BATT", TYPE_SENSOR,
                     None, "mdi:battery", 0),
    TYPE_LEAKBATT8: ("Leak 8 Battery", "BATT", TYPE_SENSOR,
                     None, "mdi:battery", 0),
}

IGNORED_SENSORS = [
    'tempinf',
    'tempf',
    'temp1f',
    'temp2f',
    'temp3f',
    'temp4f',
    'temp5f',
    'temp6f',
    'temp7f',
    'temp8f',
    'dateutc',
    'windgustms',
    'windspeedms',
    'windspdms_avg10m',
    'maxdailygustms',
    'windchillf',
    'dewpointf',
    'dewpointinf',
    'dewpoint1f',
    'dewpoint2f',
    'dewpoint3f',
    'dewpoint4f',
    'dewpoint5f',
    'dewpoint6f',
    'dewpoint7f',
    'dewpoint8f',
    DATA_PASSKEY,
    DATA_STATIONTYPE,
    DATA_FREQ,
    DATA_MODEL,
]

COMPONENT_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_PORT): cv.port,
        vol.Optional(CONF_UNIT_BARO,
                     default=CONF_UNIT_SYSTEM_METRIC): cv.string,
        vol.Optional(CONF_UNIT_WIND,
                     default=CONF_UNIT_SYSTEM_IMPERIAL): cv.string,
        vol.Optional(CONF_UNIT_RAIN,
                     default=CONF_UNIT_SYSTEM_IMPERIAL): cv.string,
        vol.Optional(CONF_UNIT_LIGHTNING,
                     default=CONF_UNIT_SYSTEM_IMPERIAL): cv.string,
        vol.Optional(CONF_UNIT_WINDCHILL,
                     default=W_TYPE_HYBRID): cv.string,
    }
)

CONFIG_SCHEMA = vol.Schema({DOMAIN: COMPONENT_SCHEMA}, extra=vol.ALLOW_EXTRA)


async def async_setup(hass: HomeAssistant, config):
    """Set up the Ecowitt component."""

    hass.data[DOMAIN] = {}
    sensor_sensors = []
    binary_sensors = []

    if DOMAIN not in config:
        return True

    conf = config[DOMAIN]

    # Store config
    hass.data[DOMAIN][DATA_CONFIG] = conf
    hass.data[DOMAIN][DATA_STATION] = {}
    hass.data[DOMAIN][DATA_READY] = False

    # preload some model info
    stationinfo = hass.data[DOMAIN][DATA_STATION]
    stationinfo[DATA_STATIONTYPE] = "Unknown"
    stationinfo[DATA_FREQ] = "Unknown"
    stationinfo[DATA_MODEL] = "Unknown"

    # setup the base connection
    ws = EcoWittListener(port=conf[CONF_PORT])
    hass.data[DOMAIN][DATA_ECOWITT] = ws

    if conf[CONF_UNIT_WINDCHILL] == W_TYPE_OLD:
        ws.set_windchill(WINDCHILL_OLD)
    if conf[CONF_UNIT_WINDCHILL] == W_TYPE_NEW:
        ws.set_windchill(WINDCHILL_NEW)
    if conf[CONF_UNIT_WINDCHILL] == W_TYPE_HYBRID:
        ws.set_windchill(WINDCHILL_HYBRID)

    hass.loop.create_task(ws.listen())

    async def close_server(*args):
        """ Close the ecowitt server."""
        await ws.stop()

    # hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, close_server)

    # # go to sleep until we get the first report
    # await ws.wait_for_valid_data()

    def check_imp_metric_sensor(sensor):
        """Check if this is the wrong sensor for our config (imp/metric)."""
        # Is this a metric or imperial sensor, lookup and skip
        name, uom, kind, device_class, icon, metric = SENSOR_TYPES[sensor]
        if "baro" in sensor:
            if (conf[CONF_UNIT_BARO] == CONF_UNIT_SYSTEM_IMPERIAL
                    and metric == S_METRIC):
                return False
            if (conf[CONF_UNIT_BARO] == CONF_UNIT_SYSTEM_METRIC
                    and metric == S_IMPERIAL):
                return False
        if "rain" in sensor:
            if (conf[CONF_UNIT_RAIN] == CONF_UNIT_SYSTEM_IMPERIAL
                    and metric == S_METRIC):
                return False
            if (conf[CONF_UNIT_RAIN] == CONF_UNIT_SYSTEM_METRIC
                    and metric == S_IMPERIAL):
                return False
        if "wind" in sensor:
            if (conf[CONF_UNIT_WIND] == CONF_UNIT_SYSTEM_IMPERIAL
                    and metric == S_METRIC):
                return False
            if (conf[CONF_UNIT_WIND] == CONF_UNIT_SYSTEM_METRIC
                    and metric == S_IMPERIAL):
                return False
        if (sensor == 'lightning'
                and conf[CONF_UNIT_LIGHTNING] == CONF_UNIT_SYSTEM_IMPERIAL):
            return False
        if (sensor == 'lightning_mi'
                and conf[CONF_UNIT_LIGHTNING] == CONF_UNIT_SYSTEM_METRIC):
            return False
        return True

    def check_and_append_sensor(sensor):
        """Check the sensor for validity, and append to appropriate list."""
        if sensor not in SENSOR_TYPES:
            if sensor not in IGNORED_SENSORS:
                _LOGGER.warning("Unhandled sensor type %s", sensor)
            return None

        # Is this a metric or imperial sensor, lookup and skip
        if not check_imp_metric_sensor(sensor):
            return None

        name, uom, kind, device_class, icon, metric = SENSOR_TYPES[sensor]
        if kind == TYPE_SENSOR:
            sensor_sensors.append(sensor)
        if kind == TYPE_BINARY_SENSOR:
            binary_sensors.append(sensor)
        return(kind)

    async def _first_data_rec(weather_data):
        _LOGGER.info("First ecowitt data recd, setting up sensors.")
        # check if we have model info, etc.
        if DATA_PASSKEY in ws.last_values:
            stationinfo[DATA_PASSKEY] = ws.last_values[DATA_PASSKEY]
            ws.last_values.pop(DATA_PASSKEY, None)
        else:
            _LOGGER.error("No passkey, cannot set unique id.")
            return False
        if DATA_STATIONTYPE in ws.last_values:
            stationinfo[DATA_STATIONTYPE] = ws.last_values[DATA_STATIONTYPE]
            ws.last_values.pop(DATA_STATIONTYPE, None)
        if DATA_FREQ in ws.last_values:
            stationinfo[DATA_FREQ] = ws.last_values[DATA_FREQ]
            ws.last_values.pop(DATA_FREQ, None)
        if DATA_MODEL in ws.last_values:
            stationinfo[DATA_MODEL] = ws.last_values[DATA_MODEL]
            ws.last_values.pop(DATA_MODEL, None)

        # load the sensors we have
        for sensor in ws.last_values.keys():
            check_and_append_sensor(sensor)

        if not sensor_sensors and not binary_sensors:
            _LOGGER.error("No sensors found to monitor, check device config.")
            return False

        if sensor_sensors:
            hass.async_create_task(
                async_load_platform(hass, "sensor", DOMAIN, sensor_sensors,
                                    config)
            )
        if binary_sensors:
            hass.async_create_task(
                async_load_platform(hass, "binary_sensor", DOMAIN, binary_sensors,
                                    config)
            )
        hass.data[DOMAIN][DATA_READY] = True

    async def _async_ecowitt_update_cb(weather_data):
        """Primary update callback called from pyecowitt."""
        _LOGGER.debug("Primary update callback triggered.")
        if not hass.data[DOMAIN][DATA_READY]:
            await _first_data_rec(weather_data)
            return
        for sensor in weather_data.keys():
            if sensor not in SENSOR_TYPES:
                if sensor not in IGNORED_SENSORS:
                    _LOGGER.warning("Unhandled sensor type %s value %s, "
                                    + "file a PR.", sensor, weather_data[sensor])
            elif (sensor not in sensor_sensors
                  and sensor not in binary_sensors
                  and sensor not in IGNORED_SENSORS
                  and check_imp_metric_sensor(sensor)):
                _LOGGER.warning("Unregistered sensor type %s value %s received.",
                                sensor, weather_data[sensor])
                # try to register the sensor
                new_sensor = []
                new_sensor.append(sensor)
                kind = check_and_append_sensor(sensor)
                if kind == TYPE_SENSOR:
                    hass.async_create_task(
                        async_load_platform(hass, "sensor", DOMAIN,
                                            new_sensor, config)
                    )
                if kind == TYPE_BINARY_SENSOR:
                    hass.async_create_task(
                        async_load_platform(hass, "binary_sensor", DOMAIN,
                                            new_sensor, config)
                    )

        async_dispatcher_send(hass, DOMAIN)

    ws.register_listener(_async_ecowitt_update_cb)

    return True


class EcowittEntity(Entity):
    """Base class for Ecowitt Weather Station."""

    def __init__(self, hass, key, name):
        """Construct the entity."""
        self.hass = hass
        self._key = key
        self._name = name
        self._stationinfo = hass.data[DOMAIN][DATA_STATION]
        self._ws = hass.data[DOMAIN][DATA_ECOWITT]

    @property
    def should_poll(self):
        """Ecowitt is a push."""
        return False

    @property
    def unique_id(self):
        """Return a unique ID for this sensor."""
        return f"{self._stationinfo[DATA_PASSKEY]}-{self._key}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def device_info(self):
        """Return device information for this sensor."""
        return {
            "station": self._stationinfo[DATA_STATIONTYPE],
            "model": self._stationinfo[DATA_MODEL],
            "frequency": self._stationinfo[DATA_FREQ],
        }

    async def async_added_to_hass(self):
        """Setup a listener for the entity."""
        async_dispatcher_connect(self.hass, DOMAIN, self._update_callback)

    @callback
    def _update_callback(self) -> None:
        """Call from dispatcher when state changes."""
        _LOGGER.debug("Updating state with new data. %s", self._name)
        self.async_schedule_update_ha_state(force_refresh=True)

    @property
    def assumed_state(self) -> bool:
        """Return whether the state is based on actual reading from device."""
        if (self._ws.lastupd + 5 * 60) < time.time():
            return True
        return False
