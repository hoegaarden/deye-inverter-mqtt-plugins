# stdout-publisher

This dumps the inverter metrics on stdout as JSON.
I use that in combination with [telegraf], but anything that can read JSON should be able to deal with the inverter readings.

[telegraf]: https://github.com/influxdata/telegraf

## data structure

```json
{
  "serial": "123123123",
  "address": "192.128.0.1",
  "port": 8899,
  "data": [{
    "up": 1,
  }, {
    "energy": 0.2,
    "name": "Production today",
    "unit": "kWh",
    "groups": "string,micro",
    "sensor": "SingleRegisterSensor",
    "timestamp": 1686489718,
    "source": "day"
  }, {
    "energy": 10.600000000000001,
    "name": "Production Total",
    "unit": "kWh",
    "groups": "string,micro",
    "sensor": "DoubleRegisterSensor",
    "timestamp": 1686489718,
    "source": "total"
  }, {
    "voltage": 236.0,
    "name": "Phase1 Voltage",
    "unit": "V",
    "groups": "string,micro",
    "sensor": "SingleRegisterSensor",
    "timestamp": 1686489718,
    "source": "ac/l1"
  }, {
    ...
  }]
}
```

## Usage with `telegraf`

An example and minimal configuration for `telegraf` can be found [here](./telegraf.minimal.conf), which you can test with:
```terminal
env \
  DEYE_LOGGER_IP=10.0.10.23 \
  DEYE_LOGGER_SERIAL=123123123 \
  DEYE_IMAGE=ghcr.io/hoegaarden/deye-inverter-mqtt-plugins:7bb1392 \
  telegraf --config ./telegraf.minimal.conf --debug
```
