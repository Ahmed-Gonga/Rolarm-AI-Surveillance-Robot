# Wiring Guide

## Raspberry Pi GPIO BCM Pins

| Part | Module pin | Raspberry Pi BCM |
|---|---:|---:|
| L298N IN1 | IN1 | 17 |
| L298N IN2 | IN2 | 27 |
| L298N IN3 | IN3 | 22 |
| L298N IN4 | IN4 | 23 |
| L298N ENA | ENA | 18 |
| L298N ENB | ENB | 13 |
| Gas sensor DO | DO | 5 |
| Flame sensor DO | DO | 6 |
| PIR sensor OUT | OUT | 12 |
| Buzzer + | + | 24 |
| Alarm LED + | + | 25 |
| All grounds | GND | GND |

Use a separate motor battery for the L298N motor power. Connect battery negative to Raspberry Pi GND. Do not power motors from the Pi 5V pin.

Gas and flame modules differ: if the sensor works reversed, change `gas_active_level` or `fire_active_level` in `config.json` from `0` to `1`.
