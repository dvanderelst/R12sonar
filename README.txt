# NOTE BEFORE ARCHIVING

June 24, 2024 
This seems to be older code that is *NOT* the code running on the R12 sonarhead (ie the head with the two maxbotix sensors).
The code running on the sonarhead is the PyboardD repository. To avoia confusion, I am archiving this repo.

# END NOTE

This is a MicroPython board

You can get started right away by writing your Python code in 'main.py'.

For a serial prompt:
 - Windows: you need to go to 'Device manager', right click on the unknown device,
   then update the driver software, using the 'pybcdc.inf' file found on this drive.
   Then use a terminal program like Hyperterminal or putty.
 - Mac OS X: use the command: screen /dev/tty.usbmodem*
 - Linux: use the command: screen /dev/ttyACM0

Please visit http://micropython.org/help/ for further help.
