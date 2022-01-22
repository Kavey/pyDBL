from mss.darwin import MSS as mss
import mss.tools
import time
import numpy as np
from pynput import keyboard
import keyboard
from PIL import Image
import cv2
import multiprocessing
from multiprocessing import Process, Queue
import os

start_time = time.time()
region = {"top": 225, "left": 1200, "width": 400, "height": 750}
output = os.path.dirname(__file__) + "/screens/sample.png"

#Workers
def grab(queue):
    with mss.mss() as sct:
        queue.put(sct.grab(region))

    queue.put(None)

def save(queue):
    img = queue.get()
    if img is None:
        return

    mss.tools.to_png(img.rgb, img.size, output=output)

#Utils
def debug(counter, frame_counter, ShowFPS):
    end_time = time.time()
    fps = frame_counter / float(end_time - start_time)
    message = "Counter: %s" %(counter)
    if ShowFPS:
        message = print("FPS: ", fps, " --- ", message)
    if not ShowFPS:
        message = print(message)
    return message

#Main
def main(ToPng, Multiprocessing, ShowFPS, Debug, RunOnce):
    looperino = 1
    counter = 0
    frame_counter = 0
    with mss.mss() as sct:
        while looperino > 0:
            counter = counter + 1
            frame_counter += 1
            while not Multiprocessing:
                img = sct.grab(region)
                if ToPng:
                    mss.tools.to_png(img.rgb, img.size, output=output)
                break

            while Multiprocessing:
                if __name__ == "__main__":
                    queue = Queue()

                    Process(target=grab, args=(queue,)).start()
                    if ToPng:
                        Process(target=save, args=(queue,)).start()
                    time.sleep(1)
                break

            if Debug:
                img_array = np.array(img)
                imgImage = Image.fromarray(img_array)
                cv2imShow = cv2.imshow('', img_array)
                debug(counter, frame_counter, ShowFPS)

            if RunOnce:
                looperino -= 1
# def print_pressed_keys():
# 	line = ', '.join(str(code) for code in keyboard._pressed_events)
# 	print('\r' + line + ' ' * 40, end='')

main(ToPng = True, Multiprocessing = False, Debug = False, ShowFPS = False, RunOnce = False)
# keyboard.hook(print_pressed_keys)
# keyboard.wait()
