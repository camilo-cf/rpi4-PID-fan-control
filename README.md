# Raspberry pi 4 - CPU Temperature control

- The circuit diagram is based on this https://howchoo.com/g/ote2mjkzzta/control-raspberry-pi-fan-temperature-python website.
- The PID controller is based on this https://apmonitor.com/pdc/index.php/Main/TCLabPIDControl
- The PID was manually tunned 
- The process starts automatically with a crontab job (on @reboot)

## Don't forget to install
```
  sudo apt install python3-rpi.gpio
  sudo apt install python3-numpy
```
In case of issues ubuntu 64 bits
https://github.com/gpiozero/gpiozero/issues/837#issuecomment-703743142
```
  cd /dev
  chmod og+rwx gpio*
```
