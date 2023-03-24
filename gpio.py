import wiringpi
import time
from wiringpi import GPIO
import subprocess

# wiringpi.wiringPiSetup()
# wiringpi.pinMode(8, GPIO.OUTPUT)

# wiringpi.digitalWrite(8, GPIO.HIGH)
# time.sleep(2)
# wiringpi.digitalWrite(8, GPIO.LOW)

def runCommand(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode().strip(), stderr.decode().strip()

def fillCommandString(first, chip, channel="", command=""):
    if channel=="":
        return f"echo {first} > /sys/class/pwm/{chip}/export"
    else:
        return f"echo {first} > /sys/class/pwm/{chip}/pwm{channel}/{command}"

# pwm_chip = "pwmchip1"
# channel = 0

stdout, stderr = runCommand(fillCommandString(0, 'pwmchip4'))
if stderr:
    print(f"Error: {stderr}")

# period_ns = 20000000  # 20ms period
# duty_cycle_ns = 1500000  # 1.5ms duty cycle (adjust as needed)


stdout, stderr = runCommand(fillCommandString(60, 'pwmchip4', 0, 'period'))
if stderr:
    print(f"Error: {stderr}")

stdout, stderr = runCommand(fillCommandString(20, 'pwmchip4', 0, 'duty_cycle'))
if stderr:
    print(f"Error: {stderr}")

stdout, stderr = runCommand(fillCommandString(1, 'pwmchip4', 0, 'enable'))
if stderr:
    print(f"Error: {stderr}")

time.sleep(2)

stdout, stderr = runCommand(fillCommandString(10, 'pwmchip4', 0, 'duty_cycle'))
if stderr:
    print(f"Error: {stderr}")

stdout, stderr = runCommand(fillCommandString(0, 'pwmchip4', 0, 'enable'))
if stderr:
    print(f"Error: {stderr}")