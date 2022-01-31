import time
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
import adafruit_ssd1306
import adafruit_framebuf
from adafruit_pm25.uart import PM25_UART

reset_pin = None
# If you have a GPIO, its not a bad idea to connect it to the RESET pin
# reset_pin = DigitalInOut(board.G0)
# reset_pin.direction = Direction.OUTPUT
# reset_pin.value = False

# Init UART
uart = busio.UART(board.GP0, board.GP1, baudrate=9600)
# Init I2C
i2c = busio.I2C(board.GP5, board.GP4, frequency=100000)
# Init OLED
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
# Init PM2.5 sensor over UART
pm25 = PM25_UART(uart, reset_pin)

# Wait while sensor initializes. 30 seconds works
oled.fill(0)
oled.text('Found PM2.5 sensor,', 4,4,1)
oled.text('initializing.......', 4,14,1)
oled.show()
time.sleep(5)
oled.text('.', 4,24,1)
oled.show()
time.sleep(5)
oled.text('.', 10,24,1)
oled.show()
time.sleep(5)
oled.text('.', 16,24,1)
oled.show()
time.sleep(5)
oled.text('.', 22,24,1)
oled.show()
time.sleep(10)

while True:
    try:
        aqdata = pm25.read()
        # print(aqdata)
    except RuntimeError:
        oled.fill(0)
        oled.text('mistakes were made...', 4,4,1)
        oled.show()
        print("Unable to read from sensor, retrying...")
        continue

    oled.invert(False)
    oled.fill(0)
    oled.text('Air Quality Index', 4, 4, 1)
    oled.text('PM 1.0: %d' % (aqdata["pm10 env"]), 2, 14, 1)
    oled.text('PM 2.5: %d' % (aqdata["pm25 env"]), 2, 24, 1)
    oled.text('PM 10: %d' % (aqdata["pm100 env"]), 2, 34, 1)
    oled.show()
    time.sleep(6)
    oled.fill(0)
    oled.text('Particles Measured', 4, 4, 1) 
    oled.text('>0.3um/.1L air: %d' % (aqdata["particles 03um"]), 2, 14, 1)
    oled.text('>0.5um/.1L air: %d' % (aqdata["particles 05um"]), 2, 24, 1)
    oled.text('>2.5um/.1L air: %d' % (aqdata["particles 25um"]), 2, 34, 1)
    oled.text('>5.0um/.1L air: %d' % (aqdata["particles 50um"]), 2, 44, 1)
    oled.text('>10 um/.1L air: %d' % (aqdata["particles 100um"]), 2, 54, 1)
    oled.show()
    time.sleep(10)

