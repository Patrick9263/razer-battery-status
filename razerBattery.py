#!/bin/env python
import os
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk as gtk, AppIndicator3 as appindicator
from openrazer.client import DeviceManager
import asyncio
import threading
from plyer import notification

class TrackStatus:
    def __init__(self):
        self.isRunning = True
        self.isWarned = False

    def getIsRunning(self):
        return self.isRunning

    def setNotRunning(self):
        self.isRunning = False

    def setIsWarned(self, isWarned):
        self.isWarned = isWarned

    def getIsWarned(self):
        return self.isWarned


status = TrackStatus()

def getBatteryStats(test=None):
    device_manager = DeviceManager()
    viper = None
    for device in device_manager.devices:
        if "Razer Viper Ultimate (Wireless)" == device.name:
            viper = device

    isCharging = False
    if viper == None:
        print("n/a")
        return (False, 0)
    else:
        if viper.is_charging:
            isCharging = True
        if viper.is_charging and viper.battery_level > 26:
            status.setIsWarned(False)

        return (isCharging, viper.battery_level)


def note(_):
    os.system("gedit $HOME/Documents/notes.txt")


def sendNotification(isCharging, percentage):
    if not isCharging and percentage > 0 and percentage < 25 and not status.getIsWarned():
        try:
            notification.notify(
                #title of the notification,
                title = "Razer Mouse Low Battery",
                #the body of the notification
                message = "{}%".format(percentage),
                #creating icon for the notification
                #we need to download a icon of ico file format
                app_icon = r"/home/patrick/Pictures/razer-logo.png",
                # the notification stays for 10sec
                timeout  = 10
            )
            status.setIsWarned(True)
        except:
            print('Error while sending Low Battery Notification!')

async def refreshBatteryStatus(razer_command):
    while status.getIsRunning():
        (isCharging, percentage) = getBatteryStats()
        chargeText = "Charging" if isCharging else "Not Charging"
        new_label = "Razer Mouse: {} {}%".format(chargeText, str(percentage))
        # print(new_label)
        razer_command.set_label(new_label)
        sendNotification(isCharging, percentage)
        await asyncio.sleep(5)

def quit(_):
    status.setNotRunning()
    print('Quitting...')
    gtk.main_quit()

def menu():
    menu = gtk.Menu()

    # command_one = gtk.MenuItem()
    # command_one.set_label('My Notes')
    # command_one.connect('activate', note)
    # menu.append(command_one)

    razer_command = gtk.MenuItem()
    razer_command.set_label(str(getBatteryStats()[1]))
    menu.append(razer_command)

    exittray = gtk.MenuItem()
    exittray.set_label('Exit Tray')
    exittray.connect('activate', quit)
    menu.append(exittray)

    menu.show_all()
    return (menu, razer_command)

def runGtk():
    gtk.main()

async def main():
    print('Running Razer Tray...')

    try:
        indicator = appindicator.Indicator.new(
            "myrazertray",
            r"/home/patrick/Pictures/razer-logo.png",
            appindicator.IndicatorCategory.APPLICATION_STATUS
        )
        indicator.set_status(appindicator.IndicatorStatus.ACTIVE)

        (myMenu, razer_command) = menu()
        indicator.set_menu(myMenu)

        x = threading.Thread(target=runGtk)
        x.start()
        await refreshBatteryStatus(razer_command)

        print('Closing Razer Tray...')

    except Exception as e:
        print("Error while running Razer Tray:")
        print(e)


if __name__ == '__main__':
    asyncio.run(main())

