"""Constants used by ecowitt component."""

from homeassistant.const import (
    CONF_UNIT_SYSTEM_METRIC,
    CONF_UNIT_SYSTEM_IMPERIAL,
    DEGREE,
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    CONCENTRATION_PARTS_PER_MILLION,
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
    SPEED_METERS_PER_SECOND,
    TIME_HOURS,
    TIME_DAYS,
    TIME_WEEKS,
    TIME_MONTHS,
    TIME_YEARS,
    UV_INDEX,
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_ILLUMINANCE,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_PRESSURE,
    DEVICE_CLASS_TIMESTAMP,
    DEVICE_CLASS_VOLTAGE,
    ELECTRIC_POTENTIAL_VOLT,
)

from homeassistant.components.binary_sensor import (
    DEVICE_CLASS_MOISTURE,
)

from homeassistant.components.sensor import (
    STATE_CLASS_MEASUREMENT,
    STATE_CLASS_TOTAL_INCREASING,
)

ECOWITT_PLATFORMS = ["sensor", "binary_sensor"]

TYPE_SENSOR = "sensor"
TYPE_BINARY_SENSOR = "binary_sensor"
DOMAIN = "ecowitt"
DATA_CONFIG = "config"
DATA_OPTIONS = "options"
DATA_ECOWITT = "ecowitt_listener"
DATA_STATION = "station"
DATA_PASSKEY = "PASSKEY"
DATA_STATIONTYPE = "stationtype"
DATA_FREQ = "freq"
DATA_MODEL = "model"
DATA_READY = "ready"
REG_ENTITIES = "registered"

DEFAULT_PORT = 4199

SIGNAL_ADD_ENTITIES = "ecowitt_add_entities"
SIGNAL_REMOVE_ENTITIES = "ecowitt_remove_entities"

CONF_NAME = "component_name"
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
TYPE_WINDGUSTMS = "windgustms"
TYPE_WINDSPEEDMS = "windspeedms"
TYPE_WINDSPEEDMS_A10 = "windspdms_avg10m"
TYPE_MAXDAILYGUSTMS = "maxdailygustms"
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
TYPE_CO2_TEMP = "tf_co2"
TYPE_CO2_TEMPC = "tf_co2c"
TYPE_CO2_HUMIDITY = "humi_co2"
TYPE_CO2_PM25 = "pm25_co2"
TYPE_CO2_PM25_AVG_24H = "pm25_24h_co2"
TYPE_CO2_PM10 = "pm10_co2"
TYPE_CO2_PM10_AVG_24H = "pm10_24h_co2"
TYPE_CO2_CO2 = "co2"
TYPE_CO2_CO2_AVG_24H = "co2_24h"
TYPE_CO2_BATT = "co2_batt"
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
TYPE_WN34TEMP1C = "tf_ch1c"
TYPE_WN34TEMP2C = "tf_ch2c"
TYPE_WN34TEMP3C = "tf_ch3c"
TYPE_WN34TEMP4C = "tf_ch4c"
TYPE_WN34TEMP5C = "tf_ch5c"
TYPE_WN34TEMP6C = "tf_ch6c"
TYPE_WN34TEMP7C = "tf_ch7c"
TYPE_WN34TEMP8C = "tf_ch8c"
TYPE_WN34BATT1 = "tf_batt1"
TYPE_WN34BATT2 = "tf_batt2"
TYPE_WN34BATT3 = "tf_batt3"
TYPE_WN34BATT4 = "tf_batt4"
TYPE_WN34BATT5 = "tf_batt5"
TYPE_WN34BATT6 = "tf_batt6"
TYPE_WN34BATT7 = "tf_batt7"
TYPE_WN34BATT8 = "tf_batt8"

S_METRIC = 1
S_IMPERIAL = 2
S_METRIC_MS = 3

W_TYPE_NEW = "new"
W_TYPE_OLD = "old"
W_TYPE_HYBRID = "hybrid"
CONF_UNIT_SYSTEM_METRIC_MS = "metric_ms"

LEAK_DETECTED = "Leak Detected"

UNIT_OPTS = [CONF_UNIT_SYSTEM_METRIC, CONF_UNIT_SYSTEM_IMPERIAL]
WIND_OPTS = [
    CONF_UNIT_SYSTEM_METRIC,
    CONF_UNIT_SYSTEM_IMPERIAL,
    CONF_UNIT_SYSTEM_METRIC_MS
]
WINDCHILL_OPTS = [W_TYPE_HYBRID, W_TYPE_NEW, W_TYPE_OLD]



# Name, unit_of_measure, type, device_class, icon, metric=1
# name, uom, kind, device_class, icon, metric = SENSOR_TYPES[x]
SENSOR_TYPES = {
    TYPE_BAROMABSHPA: ("Ecowitt Absolute Pressure", PRESSURE_HPA,
                       TYPE_SENSOR, DEVICE_CLASS_PRESSURE,
                       "mdi:gauge", S_METRIC),
    TYPE_BAROMRELHPA: ("Ecowitt Relative Pressure", PRESSURE_HPA,
                       TYPE_SENSOR, DEVICE_CLASS_PRESSURE,
                       "mdi:gauge", S_METRIC),
    TYPE_BAROMABSIN: ("Ecowitt Absolute Pressure", PRESSURE_INHG,
                      TYPE_SENSOR, DEVICE_CLASS_PRESSURE,
                      "mdi:gauge", S_IMPERIAL),
    TYPE_BAROMRELIN: ("Ecowitt Relative Pressure", PRESSURE_INHG,
                      TYPE_SENSOR, DEVICE_CLASS_PRESSURE,
                      "mdi:gauge", S_IMPERIAL),
    TYPE_RAINRATEIN: ("Ecowitt Rain Rate", f"{LENGTH_INCHES}/{TIME_HOURS}",
                      TYPE_SENSOR, None, "mdi:water", S_IMPERIAL),
    TYPE_EVENTRAININ: ("Ecowitt Event Rain Rate", f"{LENGTH_INCHES}/{TIME_HOURS}",
                       TYPE_SENSOR, None, "mdi:water", S_IMPERIAL),
    TYPE_HOURLYRAININ: ("Ecowitt Hourly Rain Rate", f"{LENGTH_INCHES}/{TIME_HOURS}",
                        TYPE_SENSOR, None, "mdi:water", S_IMPERIAL),
    TYPE_TOTALRAININ: ("Ecowitt Total Rain Rate", f"{LENGTH_INCHES}",
                       TYPE_SENSOR, None, "mdi:water", S_IMPERIAL),
    TYPE_DAILYRAININ: ("Ecowitt Daily Rain Rate", f"{LENGTH_INCHES}/{TIME_DAYS}",
                       TYPE_SENSOR, None, "mdi:water", S_IMPERIAL),
    TYPE_WEEKLYRAININ: ("Ecowitt Weekly Rain Rate", f"{LENGTH_INCHES}/{TIME_WEEKS}",
                        TYPE_SENSOR, None, "mdi:water", S_IMPERIAL),
    TYPE_MONTHLYRAININ: ("Ecowitt Monthly Rain Rate", f"{LENGTH_INCHES}/{TIME_MONTHS}",
                         TYPE_SENSOR, None, "mdi:water", S_IMPERIAL),
    TYPE_YEARLYRAININ: ("Ecowitt Yearly Rain Rate", f"{LENGTH_INCHES}/{TIME_YEARS}",
                        TYPE_SENSOR, None, "mdi:water", S_IMPERIAL),
    TYPE_RAINRATEMM: ("Ecowitt Rain Rate", f"mm/{TIME_HOURS}",
                      TYPE_SENSOR, None, "mdi:water", S_METRIC),
    TYPE_EVENTRAINMM: ("Ecowitt Event Rain Rate", f"mm/{TIME_HOURS}",
                       TYPE_SENSOR, None, "mdi:water", S_METRIC),
    TYPE_HOURLYRAINMM: ("Ecowitt Hourly Rain Rate", f"mm/{TIME_HOURS}",
                        TYPE_SENSOR, None, "mdi:water", S_METRIC),
    TYPE_TOTALRAINMM: ("Ecowitt Total Rain Rate", f"mm",
                       TYPE_SENSOR, None, "mdi:water", S_METRIC),
    TYPE_DAILYRAINMM: ("Ecowitt Daily Rain Rate", f"mm/{TIME_DAYS}",
                       TYPE_SENSOR, None, "mdi:water", S_METRIC),
    TYPE_WEEKLYRAINMM: ("Ecowitt Weekly Rain Rate", f"mm/{TIME_WEEKS}",
                        TYPE_SENSOR, None, "mdi:water", S_METRIC),
    TYPE_MONTHLYRAINMM: ("Ecowitt Monthly Rain Rate", f"mm/{TIME_MONTHS}",
                         TYPE_SENSOR, None, "mdi:water", S_METRIC),
    TYPE_YEARLYRAINMM: ("Ecowitt Yearly Rain Rate", f"mm/{TIME_YEARS}",
                        TYPE_SENSOR, None, "mdi:water", S_METRIC),
    TYPE_HUMIDITY: ("Ecowitt Humidity", PERCENTAGE,
                    TYPE_SENSOR, DEVICE_CLASS_HUMIDITY,
                    "mdi:water-percent", 0),
    TYPE_HUMIDITYIN: ("Ecowitt Indoor Humidity", PERCENTAGE,
                      TYPE_SENSOR, DEVICE_CLASS_HUMIDITY,
                      "mdi:water-percent", 0),
    TYPE_HUMIDITY1: ("Ecowitt Humidity 1", PERCENTAGE,
                     TYPE_SENSOR, DEVICE_CLASS_HUMIDITY,
                     "mdi:water-percent", 0),
    TYPE_HUMIDITY2: ("Ecowitt Humidity 2", PERCENTAGE,
                     TYPE_SENSOR, DEVICE_CLASS_HUMIDITY,
                     "mdi:water-percent", 0),
    TYPE_HUMIDITY3: ("Ecowitt Humidity 3", PERCENTAGE,
                     TYPE_SENSOR, DEVICE_CLASS_HUMIDITY,
                     "mdi:water-percent", 0),
    TYPE_HUMIDITY4: ("Ecowitt Humidity 4", PERCENTAGE,
                     TYPE_SENSOR, DEVICE_CLASS_HUMIDITY,
                     "mdi:water-percent", 0),
    TYPE_HUMIDITY5: ("Ecowitt Humidity 5", PERCENTAGE,
                     TYPE_SENSOR, DEVICE_CLASS_HUMIDITY,
                     "mdi:water-percent", 0),
    TYPE_HUMIDITY6: ("Ecowitt Humidity 6", PERCENTAGE,
                     TYPE_SENSOR, DEVICE_CLASS_HUMIDITY,
                     "mdi:water-percent", 0),
    TYPE_HUMIDITY7: ("Ecowitt Humidity 7", PERCENTAGE,
                     TYPE_SENSOR, DEVICE_CLASS_HUMIDITY,
                     "mdi:water-percent", 0),
    TYPE_HUMIDITY8: ("Ecowitt Humidity 8", PERCENTAGE,
                     TYPE_SENSOR, DEVICE_CLASS_HUMIDITY,
                     "mdi:water-percent", 0),
    TYPE_WINDDIR: ("Ecowitt Wind Direction", DEGREE,
                   TYPE_SENSOR, None, "mdi:compass", 0),
    TYPE_WINDDIR_A10: ("Ecowitt Wind Direction 10m Avg", DEGREE,
                       TYPE_SENSOR, None, "mdi:compass", 0),
    TYPE_WINDSPEEDKMH: ("Ecowitt Wind Speed", SPEED_KILOMETERS_PER_HOUR,
                        TYPE_SENSOR, None, "mdi:weather-windy", S_METRIC),
    TYPE_WINDSPEEDKMH_A10: ("Ecowitt Wind Speed 10m Avg", SPEED_KILOMETERS_PER_HOUR,
                            TYPE_SENSOR, None, "mdi:weather-windy", S_METRIC),
    TYPE_WINDGUSTKMH: ("Ecowitt Wind Gust", SPEED_KILOMETERS_PER_HOUR,
                       TYPE_SENSOR, None, "mdi:weather-windy", S_METRIC),
    TYPE_WINDSPEEDMPH: ("Ecowitt Wind Speed", SPEED_MILES_PER_HOUR,
                        TYPE_SENSOR, None, "mdi:weather-windy", S_IMPERIAL),
    TYPE_WINDSPEEDMPH_A10: ("Ecowitt Wind Speed 10m Avg", SPEED_MILES_PER_HOUR,
                            TYPE_SENSOR, None, "mdi:weather-windy",
                            S_IMPERIAL),
    TYPE_WINDGUSTMPH: ("Ecowitt Wind Gust", SPEED_MILES_PER_HOUR,
                       TYPE_SENSOR, None, "mdi:weather-windy", S_IMPERIAL),
    TYPE_MAXDAILYGUST: ("Ecowitt Max Daily Wind Gust", SPEED_MILES_PER_HOUR,
                        TYPE_SENSOR, None, "mdi:weather-windy", S_IMPERIAL),
    TYPE_MAXDAILYGUSTKMH: ("Ecowitt Max Daily Wind Gust", SPEED_KILOMETERS_PER_HOUR,
                           TYPE_SENSOR, None, "mdi:weather-windy", S_METRIC),
    TYPE_WINDGUSTMS: ("Ecowitt Wind Gust", SPEED_METERS_PER_SECOND,
                      TYPE_SENSOR, None, "mdi:weather-windy", S_METRIC_MS),
    TYPE_WINDSPEEDMS: ("Ecowitt Wind Speed", SPEED_METERS_PER_SECOND,
                       TYPE_SENSOR, None, "mdi:weather-windy", S_METRIC_MS),
    TYPE_WINDSPEEDMS_A10: ("Ecowitt Wind Speed", SPEED_METERS_PER_SECOND,
                           TYPE_SENSOR, None, "mdi:weather-windy", S_METRIC_MS),
    TYPE_MAXDAILYGUSTMS: ("Ecowitt Max Daily Wind Gust", SPEED_METERS_PER_SECOND,
                          TYPE_SENSOR, None, "mdi:weather-windy", S_METRIC_MS),
    TYPE_TEMPC: ("Ecowitt Outdoor Temperature", TEMP_CELSIUS,
                 TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE, "mdi:thermometer", 0),
    TYPE_TEMP1C: ("Ecowitt Temperature 1", TEMP_CELSIUS,
                  TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE, "mdi:thermometer", 0),
    TYPE_TEMP2C: ("Ecowitt Temperature 2", TEMP_CELSIUS,
                  TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE, "mdi:thermometer", 0),
    TYPE_TEMP3C: ("Ecowitt Temperature 3", TEMP_CELSIUS,
                  TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE, "mdi:thermometer", 0),
    TYPE_TEMP4C: ("Ecowitt Temperature 4", TEMP_CELSIUS,
                  TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE, "mdi:thermometer", 0),
    TYPE_TEMP5C: ("Ecowitt Temperature 5", TEMP_CELSIUS,
                  TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE, "mdi:thermometer", 0),
    TYPE_TEMP6C: ("Ecowitt Temperature 6", TEMP_CELSIUS,
                  TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE, "mdi:thermometer", 0),
    TYPE_TEMP7C: ("Ecowitt Temperature 7", TEMP_CELSIUS,
                  TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE, "mdi:thermometer", 0),
    TYPE_TEMP8C: ("Ecowitt Temperature 8", TEMP_CELSIUS,
                  TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE, "mdi:thermometer", 0),
    TYPE_TEMPINC: ("Ecowitt Indoor Temperature", TEMP_CELSIUS,
                   TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE,
                   "mdi:thermometer", 0),
    TYPE_DEWPOINTC: ("Ecowitt Dewpoint", TEMP_CELSIUS,
                     TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE,
                     "mdi:thermometer", 0),
    TYPE_DEWPOINTINC: ("Ecowitt Indoor Dewpoint", TEMP_CELSIUS,
                       TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE,
                       "mdi:thermometer", 0),
    TYPE_DEWPOINT1C: ("Ecowitt Dewpoint 1", TEMP_CELSIUS,
                      TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE,
                      "mdi:thermometer", 0),
    TYPE_DEWPOINT2C: ("Ecowitt Dewpoint 2", TEMP_CELSIUS,
                      TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE,
                      "mdi:thermometer", 0),
    TYPE_DEWPOINT3C: ("Ecowitt Dewpoint 3", TEMP_CELSIUS,
                      TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE,
                      "mdi:thermometer", 0),
    TYPE_DEWPOINT4C: ("Ecowitt Dewpoint 4", TEMP_CELSIUS,
                      TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE,
                      "mdi:thermometer", 0),
    TYPE_DEWPOINT5C: ("Ecowitt Dewpoint 5", TEMP_CELSIUS,
                      TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE,
                      "mdi:thermometer", 0),
    TYPE_DEWPOINT6C: ("Ecowitt Dewpoint 6", TEMP_CELSIUS,
                      TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE,
                      "mdi:thermometer", 0),
    TYPE_DEWPOINT7C: ("Ecowitt Dewpoint 7", TEMP_CELSIUS,
                      TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE,
                      "mdi:thermometer", 0),
    TYPE_DEWPOINT8C: ("Ecowitt Dewpoint 8", TEMP_CELSIUS,
                      TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE,
                      "mdi:thermometer", 0),
    TYPE_WINDCHILLC: ("Ecowitt Windchill", TEMP_CELSIUS,
                      TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE,
                      "mdi:thermometer", 0),
    TYPE_SOLARRADIATION: ("Ecowitt Solar Radiation", f"{POWER_WATT}/m^2",
                          TYPE_SENSOR, DEVICE_CLASS_ILLUMINANCE,
                          "mdi:weather-sunny", 0),
    TYPE_UV: ("Ecowitt UV Index", UV_INDEX,
              TYPE_SENSOR, None, "mdi:sunglasses", 0),
    TYPE_SOILMOISTURE1: ("Ecowitt Soil Moisture 1", PERCENTAGE,
                         TYPE_SENSOR, DEVICE_CLASS_HUMIDITY,
                         "mdi:water-percent", 0),
    TYPE_SOILMOISTURE2: ("Ecowitt Soil Moisture 2", PERCENTAGE,
                         TYPE_SENSOR, DEVICE_CLASS_HUMIDITY,
                         "mdi:water-percent", 0),
    TYPE_SOILMOISTURE3: ("Ecowitt Soil Moisture 3", PERCENTAGE,
                         TYPE_SENSOR, DEVICE_CLASS_HUMIDITY,
                         "mdi:water-percent", 0),
    TYPE_SOILMOISTURE4: ("Ecowitt Soil Moisture 4", PERCENTAGE,
                         TYPE_SENSOR, DEVICE_CLASS_HUMIDITY,
                         "mdi:water-percent", 0),
    TYPE_SOILMOISTURE5: ("Ecowitt Soil Moisture 5", PERCENTAGE,
                         TYPE_SENSOR, DEVICE_CLASS_HUMIDITY,
                         "mdi:water-percent", 0),
    TYPE_SOILMOISTURE6: ("Ecowitt Soil Moisture 6", PERCENTAGE,
                         TYPE_SENSOR, DEVICE_CLASS_HUMIDITY,
                         "mdi:water-percent", 0),
    TYPE_SOILMOISTURE7: ("Ecowitt Soil Moisture 7", PERCENTAGE,
                         TYPE_SENSOR, DEVICE_CLASS_HUMIDITY,
                         "mdi:water-percent", 0),
    TYPE_SOILMOISTURE8: ("Ecowitt Soil Moisture 8", PERCENTAGE,
                         TYPE_SENSOR, DEVICE_CLASS_HUMIDITY,
                         "mdi:water-percent", 0),
    TYPE_PM25_CH1: ("Ecowitt PM2.5 1", CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                    TYPE_SENSOR, None, "mdi:eye", 0),
    TYPE_PM25_CH2: ("Ecowitt PM2.5 2", CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                    TYPE_SENSOR, None, "mdi:eye", 0),
    TYPE_PM25_CH3: ("Ecowitt PM2.5 3", CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                    TYPE_SENSOR, None, "mdi:eye", 0),
    TYPE_PM25_CH4: ("Ecowitt PM2.5 4", CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                    TYPE_SENSOR, None, "mdi:eye", 0),
    TYPE_PM25_AVG_24H_CH1: ("Ecowitt PM2.5 24h average 1",
                            CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                            TYPE_SENSOR, None, "mdi:eye", 0),
    TYPE_PM25_AVG_24H_CH2: ("Ecowitt PM2.5 24h average 2",
                            CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                            TYPE_SENSOR, None, "mdi:eye", 0),
    TYPE_PM25_AVG_24H_CH3: ("Ecowitt PM2.5 24h average 3",
                            CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                            TYPE_SENSOR, None, "mdi:eye", 0),
    TYPE_PM25_AVG_24H_CH4: ("Ecowitt PM2.5 24h average 4",
                            CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                            TYPE_SENSOR, None, "mdi:eye", 0),
    TYPE_LIGHTNING_TIME: ("Ecowitt Last Lightning strike", "",
                          TYPE_SENSOR, DEVICE_CLASS_TIMESTAMP, "mdi:clock", 0),
    TYPE_LIGHTNING_NUM: ("Ecowitt Lightning strikes", f"strikes/{TIME_DAYS}",
                         TYPE_SENSOR, None, "mdi:weather-lightning", 0),
    TYPE_LIGHTNING_KM: ("Ecowitt Lightning strike distance", LENGTH_KILOMETERS,
                        TYPE_SENSOR, None, "mdi:ruler", S_METRIC),
    TYPE_LIGHTNING_MI: ("Ecowitt Lightning strike distance", LENGTH_MILES,
                        TYPE_SENSOR, None, "mdi:ruler", S_IMPERIAL),
    TYPE_LEAK_CH1: ("Ecowitt Leak Detection 1", LEAK_DETECTED, TYPE_BINARY_SENSOR,
                    DEVICE_CLASS_MOISTURE, "mdi:leak", 0),
    TYPE_LEAK_CH2: ("Ecowitt Leak Detection 2", LEAK_DETECTED, TYPE_BINARY_SENSOR,
                    DEVICE_CLASS_MOISTURE, "mdi:leak", 0),
    TYPE_LEAK_CH3: ("Ecowitt Leak Detection 3", LEAK_DETECTED, TYPE_BINARY_SENSOR,
                    DEVICE_CLASS_MOISTURE, "mdi:leak", 0),
    TYPE_LEAK_CH4: ("Ecowitt Leak Detection 4", LEAK_DETECTED, TYPE_BINARY_SENSOR,
                    DEVICE_CLASS_MOISTURE, "mdi:leak", 0),
    TYPE_CO2_PM25: ("Ecowitt WH45 PM2.5", CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                    TYPE_SENSOR, None, "mdi:eye", 0),
    TYPE_CO2_PM25_AVG_24H: ("Ecowitt WH45 PM2.5 24h average",
                            CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                            TYPE_SENSOR, None, "mdi:eye", 0),
    TYPE_CO2_PM10: ("Ecowitt WH45 PM10", CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                    TYPE_SENSOR, None, "mdi:eye", 0),
    TYPE_CO2_PM10_AVG_24H: ("Ecowitt WH45 PM10 24h average",
                            CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                            TYPE_SENSOR, None, "mdi:eye", 0),
    TYPE_CO2_HUMIDITY: ("Ecowitt WH45 Humidity", PERCENTAGE,
                        TYPE_SENSOR, DEVICE_CLASS_HUMIDITY,
                        "mdi:water-percent", 0),
    TYPE_CO2_TEMPC: ("Ecowitt WH45 Temperature", TEMP_CELSIUS,
                     TYPE_SENSOR, DEVICE_CLASS_TEMPERATURE, "mdi:thermometer", 0),
    TYPE_CO2_CO2: ("Ecowitt WH45 CO2", CONCENTRATION_PARTS_PER_MILLION,
                   TYPE_SENSOR, None, "mdi:molecule-co2", 0),
    TYPE_CO2_CO2_AVG_24H: ("Ecowitt WH45 CO2 24h average", CONCENTRATION_PARTS_PER_MILLION,
                           TYPE_SENSOR, None, "mdi:molecule-co2", 0),
    TYPE_CO2_BATT: ("Ecowitt WH45 Battery", PERCENTAGE, TYPE_SENSOR,
                    DEVICE_CLASS_BATTERY, "mdi:battery", 0),
    TYPE_WH25BATT: ("Ecowitt WH25 Battery", "BATT", TYPE_BINARY_SENSOR,
                    DEVICE_CLASS_BATTERY, "mdi:battery", 0),
    TYPE_WH26BATT: ("Ecowitt WH26 Battery", "BATT", TYPE_BINARY_SENSOR,
                    DEVICE_CLASS_BATTERY, "mdi:battery", 0),
    TYPE_WH40BATT: ("Ecowitt WH40 Battery", ELECTRIC_POTENTIAL_VOLT, TYPE_SENSOR,
                    DEVICE_CLASS_VOLTAGE, "mdi:battery", 0),
    TYPE_WH57BATT: ("Ecowitt WH57 Battery", PERCENTAGE, TYPE_SENSOR,
                    DEVICE_CLASS_BATTERY, "mdi:battery", 0),
    TYPE_WH65BATT: ("Ecowitt WH65 Battery", "BATT", TYPE_BINARY_SENSOR,
                    DEVICE_CLASS_BATTERY, "mdi:battery", 0),
    TYPE_WH68BATT: ("Ecowitt WH68 Battery", ELECTRIC_POTENTIAL_VOLT, TYPE_SENSOR,
                    DEVICE_CLASS_BATTERY, "mdi:battery", 0),
    TYPE_WH80BATT: ("Ecowitt WH80 Battery", ELECTRIC_POTENTIAL_VOLT, TYPE_SENSOR,
                    DEVICE_CLASS_BATTERY, "mdi:battery", 0),
    TYPE_SOILBATT1: ("Ecowitt Soil Moisture 1 Battery", ELECTRIC_POTENTIAL_VOLT, TYPE_SENSOR,
                     DEVICE_CLASS_VOLTAGE, "mdi:battery", 0),
    TYPE_SOILBATT2: ("Ecowitt Soil Moisture 2 Battery", ELECTRIC_POTENTIAL_VOLT, TYPE_SENSOR,
                     DEVICE_CLASS_VOLTAGE, "mdi:battery", 0),
    TYPE_SOILBATT3: ("Ecowitt Soil Moisture 3 Battery", ELECTRIC_POTENTIAL_VOLT, TYPE_SENSOR,
                     DEVICE_CLASS_VOLTAGE, "mdi:battery", 0),
    TYPE_SOILBATT4: ("Ecowitt Soil Moisture 4 Battery", ELECTRIC_POTENTIAL_VOLT, TYPE_SENSOR,
                     DEVICE_CLASS_VOLTAGE, "mdi:battery", 0),
    TYPE_SOILBATT5: ("Ecowitt Soil Moisture 5 Battery", ELECTRIC_POTENTIAL_VOLT, TYPE_SENSOR,
                     DEVICE_CLASS_VOLTAGE, "mdi:battery", 0),
    TYPE_SOILBATT6: ("Ecowitt Soil Moisture 6 Battery", ELECTRIC_POTENTIAL_VOLT, TYPE_SENSOR,
                     DEVICE_CLASS_VOLTAGE, "mdi:battery", 0),
    TYPE_SOILBATT7: ("Ecowitt Soil Moisture 7 Battery", ELECTRIC_POTENTIAL_VOLT, TYPE_SENSOR,
                     DEVICE_CLASS_VOLTAGE, "mdi:battery", 0),
    TYPE_SOILBATT8: ("Ecowitt Soil Moisture 8 Battery", ELECTRIC_POTENTIAL_VOLT, TYPE_SENSOR,
                     DEVICE_CLASS_VOLTAGE, "mdi:battery", 0),
    TYPE_BATTERY1: ("Ecowitt Battery 1", "BATT", TYPE_BINARY_SENSOR,
                    DEVICE_CLASS_BATTERY, "mdi:battery", 0),
    TYPE_BATTERY2: ("Ecowitt Battery 2", "BATT", TYPE_BINARY_SENSOR,
                    DEVICE_CLASS_BATTERY, "mdi:battery", 0),
    TYPE_BATTERY3: ("Ecowitt Battery 3", "BATT", TYPE_BINARY_SENSOR,
                    DEVICE_CLASS_BATTERY, "mdi:battery", 0),
    TYPE_BATTERY4: ("Ecowitt Battery 4", "BATT", TYPE_BINARY_SENSOR,
                    DEVICE_CLASS_BATTERY, "mdi:battery", 0),
    TYPE_BATTERY5: ("Ecowitt Battery 5", "BATT", TYPE_BINARY_SENSOR,
                    DEVICE_CLASS_BATTERY, "mdi:battery", 0),
    TYPE_BATTERY6: ("Ecowitt Battery 6", "BATT", TYPE_BINARY_SENSOR,
                    DEVICE_CLASS_BATTERY, "mdi:battery", 0),
    TYPE_BATTERY7: ("Ecowitt Battery 7", "BATT", TYPE_BINARY_SENSOR,
                    DEVICE_CLASS_BATTERY, "mdi:battery", 0),
    TYPE_BATTERY8: ("Ecowitt Battery 8", "BATT", TYPE_BINARY_SENSOR,
                    DEVICE_CLASS_BATTERY, "mdi:battery", 0),
    TYPE_PM25BATT1: ("Ecowitt PM2.5 1 Battery", PERCENTAGE, TYPE_SENSOR,
                     DEVICE_CLASS_BATTERY, "mdi:battery", 0),
    TYPE_PM25BATT2: ("Ecowitt PM2.5 2 Battery", PERCENTAGE, TYPE_SENSOR,
                     DEVICE_CLASS_BATTERY, "mdi:battery", 0),
    TYPE_PM25BATT3: ("Ecowitt PM2.5 3 Battery", PERCENTAGE, TYPE_SENSOR,
                     DEVICE_CLASS_BATTERY, "mdi:battery", 0),
    TYPE_PM25BATT4: ("Ecowitt PM2.5 4 Battery", PERCENTAGE, TYPE_SENSOR,
                     DEVICE_CLASS_BATTERY, "mdi:battery", 0),
    TYPE_PM25BATT5: ("Ecowitt PM2.5 5 Battery", PERCENTAGE, TYPE_SENSOR,
                     DEVICE_CLASS_BATTERY, "mdi:battery", 0),
    TYPE_PM25BATT6: ("Ecowitt PM2.5 6 Battery", PERCENTAGE, TYPE_SENSOR,
                     DEVICE_CLASS_BATTERY, "mdi:battery", 0),
    TYPE_PM25BATT7: ("Ecowitt PM2.5 7 Battery", PERCENTAGE, TYPE_SENSOR,
                     DEVICE_CLASS_BATTERY, "mdi:battery", 0),
    TYPE_PM25BATT8: ("Ecowitt PM2.5 8 Battery", PERCENTAGE, TYPE_SENSOR,
                     DEVICE_CLASS_BATTERY, "mdi:battery", 0),
    TYPE_LEAKBATT1: ("Ecowitt Leak 1 Battery", PERCENTAGE, TYPE_SENSOR,
                     DEVICE_CLASS_BATTERY, "mdi:battery", 0),
    TYPE_LEAKBATT2: ("Ecowitt Leak 2 Battery", PERCENTAGE, TYPE_SENSOR,
                     DEVICE_CLASS_BATTERY, "mdi:battery", 0),
    TYPE_LEAKBATT3: ("Ecowitt Leak 3 Battery", PERCENTAGE, TYPE_SENSOR,
                     DEVICE_CLASS_BATTERY, "mdi:battery", 0),
    TYPE_LEAKBATT4: ("Ecowitt Leak 4 Battery", PERCENTAGE, TYPE_SENSOR,
                     DEVICE_CLASS_BATTERY, "mdi:battery", 0),
    TYPE_LEAKBATT5: ("Ecowitt Leak 5 Battery", PERCENTAGE, TYPE_SENSOR,
                     DEVICE_CLASS_BATTERY, "mdi:battery", 0),
    TYPE_LEAKBATT6: ("Ecowitt Leak 6 Battery", PERCENTAGE, TYPE_SENSOR,
                     DEVICE_CLASS_BATTERY, "mdi:battery", 0),
    TYPE_LEAKBATT7: ("Ecowitt Leak 7 Battery", PERCENTAGE, TYPE_SENSOR,
                     DEVICE_CLASS_BATTERY, "mdi:battery", 0),
    TYPE_LEAKBATT8: ("Ecowitt Leak 8 Battery", PERCENTAGE, TYPE_SENSOR,
                     DEVICE_CLASS_BATTERY, "mdi:battery", 0),
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
    'tf_co2',
    'tf_ch1',
    'tf_ch2',
    'tf_ch3',
    'tf_ch4',
    'tf_ch5',
    'tf_ch6',
    'tf_ch7',
    'tf_ch8',
    'dateutc',
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
    'mac',
    'fields',
    DATA_PASSKEY,
    DATA_STATIONTYPE,
    DATA_FREQ,
    DATA_MODEL,
]
