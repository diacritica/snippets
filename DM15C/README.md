This little script takes serial output from a DM-15C calculator available here
http://www.rpn-calc.ch/ and translates it into float numbers.

A typical serial output from the calculator looks like this:

    ' --   __   __   __   __   __   __             __   __  --                      \r\n'
    '|    |__  |__  |__  |  | |  | |  |           |  |  __|   |                     \r\n'
    '|    |__|.|__|  __| |__| |__| |__|           |__| |__    |                     \r\n'
    '|                                                        |                     \r\n'
    '|__                                                    __|\r\n'

What the script basically does is read the first three lines and translate the ASCII segments into BCD coded numbers. It then correlates the BCD coded numbers into a float number asuming that the DM-15C is set to SCI numeric notation.

What the script assumes
-----------------------

* You have configured the serial connection as 38400,8n1 AND no software or hardware flow control. In Linux you can use minicom to achieve this.

* You have configured your DM-15C to SCI notation, which takes the form of 1.23456e78. If you stick with FIXED or ENGINEER notation, the script won't work. The problem is that points and commas are sent to the serial connection as points but using SCI notation you only get one point, the one separating integer and decimal parts.

* You have permission to read from the serial port (typically /dev/ttyUSB0 in Linux, check for other OSes' equivalents)

Error control
-------------

* As we said before, the script will only accept valid SCI notation. The problem is that the DM-15C will still send FIXED notaton while entering digits, so until ENTER is pressed or a result is obtained, the serial connection keeps sending useless data. The script will check for this useless data and assign a predetermined number. You should customised this number so you can trust its telling nature. You can modify the script so it outputs text but then remember to change the float conversion procedure at the end.

* If the DM-15C shows any kind of error on the LCD, the script will just think is useless data and default to the predefined number.

* If the DM-15C shows a blinking number (i.e. you exceeded the calculator memory size for a number), the script will cleanly exit showing an error message.

* If the DM-15C turns the LCD off for any reason (calculation time, battery saving), the script will just ignore this behaviour an wait for valid data.