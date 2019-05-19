# -*- coding: UTF-8 -*-

import re
from abc import ABCMeta
import cv2
import time
import numpy as np
import os
import datetime

import logging
logger = logging.getLogger(__name__)
class WebCamFactory(object):
    @classmethod
    def new_webcam(cls, **kwargs):
        if kwargs:
            return WebCam(**kwargs)
        else:
            return NullWebCam()


class BaseWebCam(object):
    __metaclass__ = ABCMeta

    def capture_image(self, *args, **kwargs):
        pass

    def capture_video(self, *args, **kwargs):
        pass


class NullWebCam(BaseWebCam):
    """
    See <Null Object> design pattern for detail: http://www.oodesign.com/null-object-pattern.html
    """


class OpenCVWebCam(BaseWebCam):
    def __init__(self, devnum):
        print(devnum)
        self.__devnum = int(devnum)

    def capture_image(self,name,scale=False):
        cap = cv2.VideoCapture(self.__devnum)
        try:
            ret, frame = cap.read()
            # Display the resulting frame+
            # cv2.imshow('frame', frame)
            cv2.imwrite(name, frame)

        finally:
            cap.release()
            if scale:
                pic = cv2.imread(name)
                res=cv2.resize(pic, (160, 90))
                cv2.imwrite(name,res)
            time.sleep(3)
    def capture_one_image(self,cycle_time):
        cap = cv2.VideoCapture(self.__devnum)
        start_time = end_time = time.time()
        temp_path = os.path.dirname(__file__)

        while end_time - start_time < cycle_time:
            ret, frame = cap.read()
            time.sleep(60)
            cv2.imwrite(os.path.join(temp_path + str(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f'))) + ".png", frame)
            end_time = time.time()
            print(end_time)

        cap.release()

    """
    can record 21 pictures per 1s.
    """
    def capture_continued_image(self,cycle_time=1,image_dir=r"E:\husky_new\lib\simg\equipment\temp_image\\"):
        cap = cv2.VideoCapture(self.__devnum)
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # mjpg can support 50 pics /s 'xvid'only support 30 pics/s
        print(fourcc)
        cap.set(3,640.0)
        cap.set(4,480.0)
        cap.set(5,120.101)
        cap.set(6,1196444237.0)# should add set fourcc to MJPG which can supports
        time.sleep(1)
        start_time = time.time()
        count=0
        while time.time() - start_time < cycle_time:
            ret, frame = cap.read()
            count+=1
            cv2.imwrite(os.path.join(image_dir,str(time.time()))+".jpeg",frame)

        print(count)
        cap.release()


    def get_pixel_values(self,name):
        image = cv2.imread(name)
        (b, g, r) = image[100, 100]
        logger.info("blue is %s green is %s red is %s" % (b, g, r))
        return r, g, b

    def capture_video(self, duration_time=60,interval=60,path=None):

        mins  = int(duration_time /int(interval)) # capture image per 10 mins
        for i in range(0,mins):
            cap = cv2.VideoCapture(self.__devnum)
            print('output_%s_%s.avi'%(i,self.__devnum))
            # Define the codec and create VideoWriter object
            # fourcc = cv2.VideoWriter_fourcc(*'DIVX')
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            # fourcc = cv2.CV_FOURCC("D", "I", "B", " ")
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            if path:
                image_name = os.path.join(path,timestamp)
                print(image_name)
                out = cv2.VideoWriter(image_name+".avi", fourcc, 20.0, (640, 480))
            else:
                out = cv2.VideoWriter('output_%s_%s_%s.avi'%(i,self.__devnum,timestamp), fourcc, 20.0, (640, 480))
            start_time = end_time = time.time()
            font = cv2.FONT_HERSHEY_SIMPLEX
            while (cap.isOpened()):
                ret, frame = cap.read()
                if ret == True:
                    frame = cv2.resize(frame, (640, 480)) # this for 2 webcamers
                    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                    cv2.putText(frame, str(timestamp), (400, 460), \
                                font, 0.5, (0, 0, 255), 1)
                    # write the flipped frame
                    out.write(frame)

                    end_time = time.time()
                    if end_time - start_time >= int(interval):
                        break
                else:
                    break

            # Release everything if job is finished
            cap.release()
            out.release()

            cap.release()
        return 1

    def get_images_from_video(self,video_files,image_dir=r"E:\husky_new\lib\simg\equipment\temp_image\\"):
        cap = cv2.VideoCapture(video_files)
        flash_rate = 0

        while True:
            ret, frame = cap.read()
            if ret:
                cv2.imwrite(os.path.join(image_dir, str(time.time())) + ".png", frame)
            else:
                break

        print(flash_rate)


    def __str__(self):
        return "web_num_%s" % self.__devnum


WebCam = OpenCVWebCam


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)-15s [%(levelname)-8s] - %(message)s'
    )
    import threading
    import argparse
    import sys

    # parser = argparse.ArgumentParser(description="please input web num")
    # parser.add_argument('--web1', help="please input the web num 1",type=str)
    # parser.add_argument('--duration', help="please input durationt time",type=int)
    # parser.add_argument('--interval', help="please input durationt time", type=int)
    # #
    # args = parser.parse_args()
    # #
    # web_1 = WebCam(args.web1)
    # print("Start to record the video")
    # try:
    #     web_1.capture_video(args.duration,args.interval)
    # except KeyboardInterrupt:
    #     sys.exit()
    web_2 = WebCam("0")
    # web_2.capture_continued_image(1)
    web_2.capture_video(path=r"C:\video_clips")
    # a = threading.Thread(target=web_1.capture_video, args=(args.duration,))
    # print(a)
    # b = threading.Thread(target=web_2.capture_one_image, args=(args.duration,))
    # print(b)
    # a.start()
    # b.start()
    # a.join()
    # b.join()

    # # web_1.capture_continued_iamge()
    # web_1.capture_image(name_test)
    # web_1.capture_one__image()
    # web_1.capture_image(name_golden)

