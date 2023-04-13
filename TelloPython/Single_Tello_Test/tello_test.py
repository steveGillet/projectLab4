from tello import Tello
import sys
from datetime import datetime
import time

def flyDrone(tello):
    start_time = str(datetime.now())

    file_name = sys.argv[1]

    f = open(file_name, "r")
    commands = f.readlines()

    # tello = Tello()

    # tello.send_command('command')
    # tello.send_command('streamon')
    # tello.send_command('takeoff')
    # tello.send_command('speed 100')

    # time.sleep(1)


    # print(commands)
    for command in commands:
        if tello.foundFlag == True:
            break
        if command != '' and command != '\n':
            command = command.rstrip()

            tello.send_command(command)
        time.sleep(1)

        
    # while(tello.foundFlag == False):
    #     tello.send_command('forward 20')
    #     time.sleep(1)
    #     tello.send_command('cw 90')
    #     time.sleep(1)

    print('found')
    # tello.send_command('land')

    # log = tello.get_log()

    # out = open('log/' + start_time + '.txt', 'w')
    # for stat in log:
    #     stat.print_stats()
    #     str = stat.return_stats()
    #     out.write(str)
