# gripit-modbus-master

## General info:

In order to obtain better performance and better noise immunity gripit uses RS485 as the physical protocol under modbus. To create the differential lines necessary for RS485 a separate [SN65176BDR](http://www.ti.com/lit/gpn/SN65176B) is used together with Raspberry/Arduino boards.  

## Setup for using [SN65176BDR](http://www.ti.com/lit/gpn/SN65176B)

Raspberry:

- in order to use the SN65176B with the Raspberry, the DE pin needs to be driven by the Raspberry.
- the Raspberry can theoretically drive the SN65176B DE pin using the RTS pin (GPIO 17 on V2 rev 1.1).
- there are 2 ways to send data on the RTS pin
    - automatically - hardware flow control needs to be enabled for this. See [rpirtscts](https://github.com/Agilefreaks/rpirtscts)
    - manually - the RTS pin needs to be set high/low whenever writing/reading data. See [gist](https://gist.github.com/cristi-badila/463a9b0fac7402d32f04c8acab764d7b)

## Develop

- run tests via `python -m pytest`

Arduino:
- the modbus-arduino library supports RS-485 out of the box. The only difference between RS-232 and RS-485 is the addition of another argument indicating the pin used as the DE pin (5 in our case - D2)
