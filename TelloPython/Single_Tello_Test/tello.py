import socket
import threading
import time
from stats import Stats
import datetime
import cv2
import os
import h264decoder
import numpy as np

class Tello:
    def __init__(self):
        self.local_ip = ''
        self.local_port = 8889
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket for sending cmd
        self.socket.bind((self.local_ip, self.local_port))

        # thread for receiving cmd ack
        self.receive_thread = threading.Thread(target=self._receive_thread)
        self.receive_thread.daemon = True
        self.receive_thread.start()
        self.decoder = h264decoder.H264Decoder()

        self.tello_ip = '192.168.10.1'
        self.tello_port = 8889
        self.frame = None
        
        self.log = []
        self.socket_video = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket for receiving video stream
        self.tello_address = (self.tello_ip, self.tello_port)
        self.local_video_port = 11111 

        self.MAX_TIME_OUT = 15.0

        self.socket_video.bind((self.local_ip, self.local_video_port))

        # thread for receiving video
        self.receive_video_thread = threading.Thread(target=self._receive_video_thread)
        self.receive_video_thread.daemon = True

        self.receive_video_thread.start()

        # thread for reading qrcode
        self.foundFlag = False
        self.qrCodeValue = None
        self.readQRcodeThread = threading.Thread(target=self._readQRcode)
        self.readQRcodeThread.daemon = True

        self.readQRcodeThread.start()

    def send_command(self, command):

        """
        Send a command to the ip address. Will be blocked until
        the last command receives an 'OK'.
        If the command fails (either b/c time out or error),
        will try to resend the command
        :param command: (str) the command to send
        :param ip: (str) the ip of Tello
        :return: The latest command response
        """
        self.log.append(Stats(command, len(self.log)))

        self.socket.sendto(command.encode('utf-8'), self.tello_address)
        print('sending command: %s to %s' % (command, self.tello_ip))

        start = time.time()
        while not self.log[-1].got_response():
            now = time.time()
            diff = now - start
            if diff > self.MAX_TIME_OUT:
                print('Max timeout exceeded... command %s' % command)
                # TODO: is timeout considered failure or next command still get executed
                # now, next one got executed
                return
        print('Done!!! sent command: %s to %s' % (command, self.tello_ip))

    def _receive_thread(self):
        """Listen to responses from the Tello.

        Runs as a thread, sets self.response to whatever the Tello last returned.

        """
        while True:
            try:
                self.response, ip = self.socket.recvfrom(1024)
                print('from %s: %s' % (ip, self.response))

                self.log[-1].add_response(self.response)
            except socket.error as exc:
                print("Caught exception socket.error : %s" % exc)

    def _receive_video_thread(self):
        """
        Listens for video streaming (raw h264) from the Tello.

        Runs as a thread, sets self.frame to the most recent frame Tello captured.

        """
        packet_data = b''
        while True:
            try:
                res_string, ip = self.socket_video.recvfrom(2048)
                packet_data += res_string
                # end of frame
                # print(len(res_string))
                if len(res_string) != 1460:
                    for frame in self._h264_decode(packet_data):
                        # print(frame)
                        self.frame = frame
                    packet_data = b''

            except socket.error as exc:
                print ("Caught exception socket.error : %s" % exc)

    def _h264_decode(self, packet_data):
        """
        decode raw h264 format data from Tello
        
        :param packet_data: raw h264 data array
       
        :return: a list of decoded frame
        """
        res_frame_list = []
        frames = self.decoder.decode(packet_data)
        for framedata in frames:
            (frame, w, h, ls) = framedata
            if frame is not None:
                # print 'frame size %i bytes, w %i, h %i, linesize %i' % (len(frame), w, h, ls)

                frame = np.fromstring(frame, dtype=np.ubyte, count=len(frame), sep='')
                frame = (frame.reshape((int(h), int(ls / 3), 3)))
                frame = frame[:, :w, :]
                res_frame_list.append(frame)

        return res_frame_list

    def on_close(self):
        pass
        # for ip in self.tello_ip_list:
        #     self.socket.sendto('land'.encode('utf-8'), (ip, 8889))
        # self.socket.close()

    def get_log(self):
        return self.log

    def _readQRcode(self):
        # print(self.frame)
        while True:
            try:
                # ts = datetime.datetime.now()
                # filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))

                # p = os.path.sep.join(("./img/", filename))
                # print(self.frame)
                # save the file
                # frame = cv2.resize(self.frame, (480,480))
                # img = cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR)
                img = cv2.resize(self.frame, (500, 500))
                # print('Hallo')
                # img = cv2.imread(self.frame)
                # img = cv2.resize(img, (500,500))
                # ts = datetime.datetime.now()
                # filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
                # p = os.path.sep.join(("./img/", filename))
                # cv2.imwrite(p, img)
                detect = cv2.QRCodeDetector()
                self.qrCodeValue, points, straight_qrcode = detect.detectAndDecode(img)
                # print(value, points, straight_qrcode)
                if self.qrCodeValue == "D":
                    print('FOUND D')
                    self.foundFlag = True
            except:
                pass

    def takeSnapshot(self):
        """
        save the current frame of the video as a jpg file and put it into outputpath
        """

        # grab the current timestamp and use it to construct the filename
        ts = datetime.datetime.now()
        filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))

        p = os.path.sep.join(("./img/", filename))
        # print(self.frame)
        # save the file
        # frame = cv2.resize(self.frame, (480,480))
        cv2.imwrite(p, cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR))
        print("[INFO] saved {}".format(filename))

