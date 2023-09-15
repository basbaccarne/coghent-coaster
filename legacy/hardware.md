# components
* Raspberry Pi 4 + stacking
* Screen: PiTFT Mini 320x240 2.4 inch (HAT)
* Sensor: FSR- Interlink 402 Force Sensing Resistor 1/2"
* Case: Lasercutted Bamboo

# hardware installation
* mount PiTFT Mini 320x240 2.4 inch (solder if needed)

# configugation
* fresh install raspberry pi OS

## init screen mirror
* `sudo apt-get install -y git python3-pip`
* `pip3 install adafruit-python-shell`
* `git clone https://github.com/adafruit/Raspberry-Pi-Installer-Scripts.git`
* `cd Raspberry-Pi-Installer-Scripts`
* `sudo python3 adafruit-pitft.py`
* (settings: 2.4 inch, 90°, no console)
  
## init image display (& test)
* `sudo apt-get install fbi`
* `wget http://adafruit-download.s3.amazonaws.com/adapiluv320x240.jpg`
* `sudo fbi -T 2 -d /dev/fb1 -noverbose -a adapiluv320x240.jpg`
