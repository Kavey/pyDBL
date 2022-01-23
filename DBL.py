from mss.darwin import MSS as mss
import mss.tools
import time
from multiprocessing import Process, Queue
import os
import keyboard
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import cv2

#Misc
start_time = time.time()
region = {"top": 225, "left": 1200, "width": 400, "height": 750}

#Controls
# Space = keyboard.press_and_release("space")
# Escape = keyboard.is_pressed("esc")
# RDash = keyboard.press_and_release("left")
# LDash = keyboard.press_and_release("right")
# ACARD = keyboard.press_and_release(12)
# ZCard = keyboard.press_and_release(13)
# ECard = keyboard.press_and_release(14)
# RCard = keyboard.press_and_release(15)
# Swap1 = keyboard.press_and_release(18)
# Swap2 = keyboard.press_and_release(19)
# Spell = keyboard.press_and_release(20)
# RRush = keyboard.press_and_release("f") //NOTOK

#Screens
screenshot = os.path.dirname(__file__) + "/images/screen.png"
alert = os.path.dirname(__file__) + "/images/alert.png"

#Workers
def grab(queue):
    with mss.mss() as sct:
        queue.put(sct.grab(region))

    queue.put(None)

def save(queue):
    img = queue.get()
    if img is None:
        return

    mss.tools.to_png(img.rgb, img.size, output=screenshot)

#Utils
def pressAndRelease(key):
    keyboard.press(key)
    keyboard.release(key)

def debug(counter, frame_counter, ShowFPS):
    # img_array = np.array(img)
    # imgImage = Image.fromarray(img_array)
    # cv2imShow = cv2.imshow('', img_array)
    end_time = time.time()
    fps = frame_counter / float(end_time - start_time)
    message = "Counter: %s" %(counter)

    ###Debug###
    ###Debug###

    if ShowFPS:
        message = print(message, " --- ", "FPS: ", fps)
    if not ShowFPS:
        message = print(message)
    return message

#Block manual inputs
def block_inputs():
    if keyboard.is_pressed("space"):
        keyboard.block_key("space")
    if keyboard.is_pressed("left"):
        keyboard.block_key("left")
    if keyboard.is_pressed("right"):
        keyboard.block_key("right")

#Rotation
def rotation(screen):
    block_inputs()
    pressAndRelease("right")

    # Screenshot = cv2.imread(screenshot)
    # dodgeAlert = cv2.imread(alert)
    # res = cv2.matchTemplate(Screenshot, dodgeAlert, cv2.TM_CCOEFF_NORMED)
    # threshold = .8
    # loc = np.where(res >= threshold)
    # for i in zip(*loc[::-1]):
    #     print('DODGING!')
    #     pressAndRelease("right")

#Main
def main(Multiprocessing, SaveToPng, ShowFPS, Debug, RunOnce):
    looperino = 1
    counter = 0
    frame_counter = 0
    with mss.mss() as sct:
        while looperino > 0:
            counter = counter + 1
            frame_counter += 1
            while not Multiprocessing:
                screen = sct.grab(region)
                if SaveToPng:
                    mss.tools.to_png(screen.rgb, screen.size, output=screenshot)
                break

            while Multiprocessing:
                if __name__ == "__main__":
                    queue = Queue()

                    Process(target=grab, args=(queue,)).start()
                    if SaveToPng:
                        Process(target=save, args=(queue,)).start()
                    time.sleep(1)
                break

            rotation(screen)

            if Debug:
                debug(counter, frame_counter, ShowFPS)
            if RunOnce:
                looperino -= 1
            if keyboard.is_pressed("esc"):
                print("You pressed Escape, stopping...")
                looperino -= 1

main(   Multiprocessing = False, SaveToPng = True,
        ShowFPS = False, Debug = False, RunOnce = False)
