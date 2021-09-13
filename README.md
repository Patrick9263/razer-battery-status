# razer-battery-status

This python program creates a system tray indicator to show the battery percentage of a Razer Viper Ultimate (Wireless)

## How to run

1. Ensure python3 is installed by running the following in terminal:
```shell
python3 --version

# Python 3.x.x
```

2. Run command manually:
```shell
python3 ./razerBattery.py
```

3. Add to startup Cron Job (if on Linux, thanks [Stackoverflow!](https://stackoverflow.com/questions/24518522/run-python-script-at-startup-in-ubuntu))
```shell

    # Copy the python file to /bin:
    sudo cp -i ./razerBattery.py /bin

    #Add A New Cron Job:
    sudo crontab -e

    #Scroll to the bottom and add the following line (after all the #'s):
    @reboot python /bin/razerBattery.py &

    # The “&” at the end of the line means the command is run in the background and it won’t stop the system booting up.

    # Test it:
    sudo reboot

```

## Demo
![Demo Image](https://github.com/Patrick9263/razer-battery-status/blob/main/images/razerDemo.gif)

