#!/bin/bash

# DEFINE VARIABLES
wrkDir="/usr/local/bin/"
pivacPostTest="false"
usbModeSwitch=false

# DEFINE FUNCTIONS
enableLanUSBmodeService() {
    # ENABLE / START LAN USB MODE SWITCH ON STARTUP WATCHDOG
    echo "Enabling then starting watchdog service for RLT8152 LAN Mode Switch on startup..."
    sudo systemctl enable rtl8152_modeswitch.service
    sudo systemctl start rtl8152_modeswitch.service
}

enablePiVacService() {
    # ENABLE / START PIVAC ON STARTUP WATCHDOG
    echo "Enabling then starting watchdog service for PiVAC on startup..."
    sudo systemctl enable pivac.service
    sudo systemctl start pivac.service
    if [ "$usbModeSwitch" == "true" ]; then
      enableLanUSBmodeService
    fi
}

runTestScript() {
    # CHECK IF PYTHON AND DEPENDS ARE INSTALLED CORRECTLY BEFORE ENABLE SERVICE
    echo "Looking for PWM hat..."
    sudo i2cdetect -y 1
    echo "Running main script..."
    sudo python3 ./main.py
    enablePiVacService
}

sourceCodeSetup() {
    # DOWNLOAD GIT OF SOURCE CODE
    # cd /usr/local/bin
    echo "Downloading and unziping PiVAC source code from github https://github.com/FriendlyNGeeks/PiVAC/archive/refs/heads/main.zip..."
    sudo wget https://github.com/FriendlyNGeeks/PiVAC/archive/refs/heads/main.zip && echo "Source Code Zip has been downloaded" || error "Could not download Source Code zip"
    sudo unzip main.zip && echo "Zip directory has been unpacked" || error "Could not unpack the Zip directory"
    sudo rm main.zip && echo "Zip has been removed" || error "Could not remove the Zip"
    sudo mv PiVAC-main/ pivac && echo "Directory has been renamed" || error "Could not rename the directory"
    echo "Updating perms for execution of ALL FILES in pivac dir..."
    sudo chmod -R +x /usr/local/bin/pivac
    echo "Moving services to /etc/systemd/system"
    sudo mv /usr/local/bin/pivac/services/pivac.service /usr/local/bin/pivac/services/rtl8152_modeswitch.service /etc/systemd/system
    sudo systemctl daemon-reload
    # sudo pip install futures
    if [ "$pivacPostTest" == "true" ]; then
      runTestScript
    else
      enablePiVacService
    fi
}

enableSPI() {
    echo "\nChange option3 | enable SPI/i2c | confirm \nPress any key to continue..."
    read "kk"
    sudo raspi-config nonint do_i2c 0
    sudo raspi-config nonint do_spi 0
    <<<com
    option 3 | enable SPI | confirm
    option 3 | enable i2c | confirm
    com
    sourceCodeSetup
}

setupAutoMount() {
    # AUTO MOUNT REMOTE-CONFIG
    echo "Checking mount points [ect/fstab] for remote_config.json entry..."
    grep -q 'remote-config' /etc/fstab || 
    read -p "Enter server folder address (//192.168.X.XXX): " mountTarget < /dev/tty
    read -p "Enter mount point (default: /usr/local/share): " mountPoint < /dev/tty
    read -p "Enter mount user: " mountUser < /dev/tty
    read -p "Enter mount password: " mountPass < /dev/tty
    printf '# remote-config \n%s %s cifs user=%s,pass=%s 0 0\n' "$mountTarget" "$mountPoint" "$mountUser" "$mountPass" >> /etc/fstab
    sudo mount -a
    sudo systemctl daemon-reload
    enableSPI
}

installDepends() {
    # WORKAROUND GPIO 'busy' kernel since BOOKWORM CE0 SOURCE | https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/spi-sensors-devices
    sudo pip3 install --upgrade adafruit-python-shell click
    wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/main/raspi-spi-reassign.py
    sudo -E env PATH=$PATH python3 /usr/local/bin/raspi-spi-reassign.py --ce0=5 --ce1=6
    # PRE-REQ
    echo "Installing prerequisites [pip,setuptools,adafruit-python-shell,adafruit-circuitpython-rgb-display,spidev,fonts-dejavu,python3-pil,python3-numpy,adafruit-circuitpython-pca9685]..."
    sudo apt-get install python3-pip -y
    sudo apt-get install python-smbus -y
    sudo apt-get install i2c-tools -y
    sudo pip3 install --upgrade setuptools
    sudo pip3 install --upgrade adafruit-python-shell
    sudo pip3 install adafruit-circuitpython-rgb-display
    sudo pip3 install --upgrade --force-reinstall spidev
    sudo apt-get install fonts-dejavu -y
    sudo apt-get install python3-pil -y
    sudo apt-get install python3-numpy -y
    sudo pip3 install adafruit-circuitpython-pca9685
    setupAutoMount
}

checkUpdateUpgrade() {
    # ALWAYS RUN FIRST ON NEW BUILD
    echo "\nYou may be prompted for Sudo user password \nPress any key to continue..."
    read "kk"
    echo "Preforming system update and upgrade checks..."
    sudo apt-get update -y
    sudo apt-get upgrade -y
    installDepends
}

checkForWrkDir() {
  if ! [ "$PWD" == "$wrkDir" ]; then
    echo"Entering work directory: <$wrkDir>"
    cd $wrkDir
  fi;
  checkUpdateUpgrade
}

checkInternet() {
  printf "Checking if you are online..."
  wget -q --spider http://github.com
  if [ $? -eq 0 ]; then
    echo "Online. Continuing."
  else
    error "Offline. Go connect to the internet then run the script again."
  fi
}

# BEGIN PROGRAM
clear
echo "Clearing Terminal Screen"
echo "Timestamp: $(date +"%m-%d-%y @ %T")"

checkInternet

# TEST PYTHON SCRIPT FOR MISSING DEPENDS BEFORE RUNNING SERVICE
# sudo python3 /usr/local/bin/pivac/main.py



check_for_flowtype () {

echo "********************* Welcome to PiVAC Build BASH *********************"
while true; do
    echo "Y/y) Enable"
    echo "N/n) Disable"
    read -p "Would you like to enable the log file? " yn < /dev/tty
    case $yn in
        [Y/y]* ) pivacPostTest=true; break;;
        [N/n]* ) pivacPostTest=false; break;;
        * ) echo "Unknown response, enter a number Y/y-N/n.";;
    esac
done

while true; do
    echo "Y/y) Enable"
    echo "N/n) Disable"
    echo -e "\033[31;47mWARNING\033[0m Only enable if LAN connection is active (ssh relog) \033[31;47mWARNING\033[0m"
    read -p "Would you like to mode switch Realtek 8152B for LAN connection? [RECOMMENDED] " yn < /dev/tty
    case $yn in
        [Y/y]* ) usbModeSwitch=true; break;;
        [N/n]* ) usbModeSwitch=false; break;;
        * ) echo "Unknown response, enter a number Y/y-N/n.";;
    esac
done

if [ "$usbModeSwitch" == "true" ]; then
  echo "Disabling wlan0 to allow mode switch..."
  sh -c "usb_modeswitch -v 0bda -p 8151 -M 555342430860d9a9c0000000800006e0000000000000000000000000000000"
  sh -c "ip link set wlan0 down"
fi

while true; do
    echo "1) Full Upgrade/Install"
    echo "2) Install Prerequisites"
    echo "3) Automount Remote Config"
    echo "4) Enable SPI/i2c[raspi-config]"
    echo "5) Source Code Setup"
    echo "6) Enable PiVAC Service"
    echo "0) Exit"
    read -p "Please select a number above: " x < /dev/tty
    case $x in
        [1]* ) checkForWrkDir; break;;
        [2]* ) installDepends; break;;
        [3]* ) setupAutoMount; break;;
        [4]* ) enableSPI/i2c; break;;
        [5]* ) sourceCodeSetup; break;;
        [6]* ) enablePiVacService; break;;
        [0]* ) exit;;
        * ) echo "Unknown response, enter a number 1-5 or 0 to quit.";;
    esac
done
}
check_for_flowtype

echo "END OF SCRIPT"
