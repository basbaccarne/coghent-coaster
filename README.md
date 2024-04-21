# MugView
*MugView is an open source coffee coaster that keeps your coffee warm and presents a new image on each sip of the mug.*

Features:
- USB mug warmer
- Display with auto-updates on each sip
- Connects to APIs and includes metadata
- Current application: [Collections of Ghent](https://www.collections.gent/), a digital cultural heritage project 

# Hardware Components
- Circular display: [HyperPixel 2.1 Round](https://shop.pimoroni.com/products/hyperpixel-round?variant=39381081882707) (Pimoroni)
- Microprocessor: [Raspberry Pi Zero W 1.1](https://www.raspberrypi.com/products/raspberry-pi-zero-w/)
- GPIO Stacking Header
- USB extender module
- Heater module
- Case

# Installation
- Installation instructions on hold as long as the product is still in development.
- Instead the headers below describe the subchallenges and status

## Set-up circular display and Raspberry Pi OS *(ready)*
1. Solder a GPIO Stacking Header to the Raspberry Pi Zero (make sure to do this in the right direction. yes, I did it wrong the first time ;))
2. Mount the Raspberry Pi on the circular display
3. Set-up the Raspberry Pi to work with the display & PyGame ([like this](https://github.com/basbaccarne/HyperPixel2r_tests))

## Show API image on touch
- **Work in progress**
- Work with mouse first

## Show API image on mug lift
- **Work in progress**
- Which GPIO pin is still free
  
## Set-up USB heater module
- **Work in progress**
- Take power from USB out on Raspi
  
## Assembly
- **Work in progress**
- Also consider credential management
- Also cosider single python dependency download

## Old to To Dos
* increase speeed of the loading script
* add config.py for wifi credentials
* add requirements.txt (freeze)
