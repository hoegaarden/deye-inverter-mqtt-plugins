# stdout-publisher

This dumps the inverter metrics on stdout as JSON.
I use that in combination with [telegraf], but anything that can read JSON should be able to deal with the inverter readings.

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
