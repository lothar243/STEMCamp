echo "Setting up ciphor.py to be executed from anywhere"
sudo cp ciphor.py /usr/bin
echo "Setting up rsaHex.py to be executed from anywhere"
sudo chmod +x /usr/bin/ciphor.py
sudo cp rsaHex.py /usr/bin
sudo chmod +x /usr/bin/rsaHex.py
echo "Adding the STEM camp directory to PYTHONPATH, so that certain libraries can be imported from anywhere"
echo "export PYTHONPATH=\"${PYTHONPATH}:$(pwd)\"" >> ~/.bashrc

#echo "Enabling ssh"
sudo apt install -y openssh-server
sudo systemctl enable ssh --now


echo "Enabling SPI and I2C"
sudo sed -i "/dtparam=spi=on/s/^#//g" /boot/firmware/config.txt
sudo sed -i "/dtparam=i2c_arm=on/s/^#//g" /boot/firmware/config.txt
echo "Disabling WIFI
sudo echo dtoverlay=disable-wifi >> /boot/firmware/config.txt

sudo apt update
sudo apt install -y python3-libgpiod
#sudo apt install -y snapd
#sudo snap install core
#sudo snap install john-the-ripper

sudo apt install -y python3-pip
pip3 install --break-system-packages mfrc522
sudo pip3 install --break-system-packages rpi_ws281x adafruit-circuitpython-neopixel
pip3 install --break-system-packages freegames

# pip3 install smbus

# sudo python3 -m pip install --force-reinstall adafruit-blinka
