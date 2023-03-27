import wiringpi
import time
from wiringpi import GPIO
import subprocess

ena = 2
enb = 5
in1 = 7
in2 = 8
in3 = 11
in4 = 12

wiringpi.wiringPiSetup()
wiringpi.pinMode(in1, GPIO.OUTPUT)
wiringpi.pinMode(in2, GPIO.OUTPUT)
wiringpi.pinMode(in3, GPIO.OUTPUT)
wiringpi.pinMode(in4, GPIO.OUTPUT)

def runCommand(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode().strip(), stderr.decode().strip()

def fillCommandString(first, chip, command, channel=""):
    if channel=="":
        return f"echo {first} > /sys/class/pwm/{chip}/{command}"
    else:
        return f"echo {first} > /sys/class/pwm/{chip}/pwm{channel}/{command}"

def initializePWM():
    stdout, stderr = runCommand(fillCommandString(0, 'pwmchip4', 'export'))
    if stderr:
        print(f"Error: {stderr}")

    stdout, stderr = runCommand(fillCommandString(60, 'pwmchip4', 'period', 0))
    if stderr:
        print(f"Error: {stderr}")

    stdout, stderr = runCommand(fillCommandString(0, 'pwmchip5', 'export'))
    if stderr:
        print(f"Error: {stderr}")

    stdout, stderr = runCommand(fillCommandString(60, 'pwmchip5', 'period', 0))
    if stderr:
        print(f"Error: {stderr}")

def pulseWidth(chip, duty):
    if chip == 2:
        chip = 'pwmchip5'
    if chip == 5:
        chip = 'pwmchip4'
    stdout, stderr = runCommand(fillCommandString(duty, chip, 'duty_cycle', 0))
    if stderr:
        print(f"Error: {stderr}")

    if duty != 60:
        stdout, stderr = runCommand(fillCommandString(1, chip, 'enable', 0))
        if stderr:
            print(f"Error: {stderr}")
    else:
        stdout, stderr = runCommand(fillCommandString(0, chip, 'enable', 0))
        if stderr:
            print(f"Error: {stderr}")

def closePWM():
    stdout, stderr = runCommand(fillCommandString(0, 'pwmchip4', 'enable', 0))
    if stderr:
        print(f"Error: {stderr}")
    stdout, stderr = runCommand(fillCommandString(0, 'pwmchip4', 'unexport'))
    if stderr:
        print(f"Error: {stderr}")
    stdout, stderr = runCommand(fillCommandString(0, 'pwmchip5', 'enable', 0))
    if stderr:
        print(f"Error: {stderr}")
    stdout, stderr = runCommand(fillCommandString(0, 'pwmchip5', 'unexport'))
    if stderr:
        print(f"Error: {stderr}")

def stop():
    wiringpi.digitalWrite(in1, GPIO.LOW)
    wiringpi.digitalWrite(in2, GPIO.LOW)
    wiringpi.digitalWrite(in3, GPIO.LOW)
    wiringpi.digitalWrite(in4, GPIO.LOW)
    pulseWidth(ena, 60)
    pulseWidth(enb, 60)

def turnLeft():
    wiringpi.digitalWrite(in1, GPIO.HIGH)
    wiringpi.digitalWrite(in2, GPIO.LOW)
    wiringpi.digitalWrite(in3, GPIO.LOW)
    wiringpi.digitalWrite(in4, GPIO.HIGH)
    pulseWidth(ena, 20)
    pulseWidth(enb, 20)

def turnRight():
    wiringpi.digitalWrite(in1, GPIO.LOW)
    wiringpi.digitalWrite(in2, GPIO.HIGH)
    wiringpi.digitalWrite(in3, GPIO.HIGH)
    wiringpi.digitalWrite(in4, GPIO.LOW)
    pulseWidth(ena, 20)   
    pulseWidth(enb, 20)

def forward():
    wiringpi.digitalWrite(in1, GPIO.HIGH)
    wiringpi.digitalWrite(in2, GPIO.LOW)
    wiringpi.digitalWrite(in3, GPIO.HIGH)
    wiringpi.digitalWrite(in4, GPIO.LOW)
    pulseWidth(ena, 20)    
    pulseWidth(enb, 20)

initializePWM()
turnLeft()
time.sleep(1)
turnRight()
time.sleep(1)
stop()

closePWM()