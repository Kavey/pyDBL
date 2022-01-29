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
import sys

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

#Utils
def pressAndRelease(key):
    keyboard.press(key)
    keyboard.release(key)

def getPixel(screen, key, xaxis, yaxis, r, g, b):
    width, height = screen.size

    for xaxis in range(0, width, 5):
        for yaxis in range(0, height, 5):

            r, g, b = screen.getpixel((xaxis, yaxis))

            if r == r and g == g and b == b:
                detected = 1
                pressAndRelease(key)
                print("same color")
                break

        if detected == 1:
            break

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
    # pressAndRelease("right")

    # Screenshot = cv2.imread(screen)
    # dodgeAlert = cv2.imread(alert)
    # res = cv2.matchTemplate(Screenshot, dodgeAlert, cv2.TM_CCOEFF_NORMED)
    # threshold = .8
    # loc = np.where(res >= threshold)
    # for i in zip(*loc[::-1]):
    #     print('DODGING!')
    #     pressAndRelease("right")
    block_inputs()

#Main Pixel
def mainPixel(Multiprocessing, SaveToPng, ShowFPS, Debug, RunOnce):
    counter = 0
    frame_counter = 0
    looperino = 1
    while looperino > 0:
        with mss.mss() as sct:
            counter = counter + 1
            frame_counter += 1
            screen = sct.grab(region)

            # print(np.array(screen))
            while not Multiprocessing:
                if SaveToPng:
                    mss.tools.to_png(screen.rgb, screen.size, output=screenshot)
                break

            # rotation()

            if Debug:
                debug(counter, frame_counter, ShowFPS)
            if RunOnce:
                looperino -= 1
            if keyboard.is_pressed("esc"):
                print("You pressed Escape, stopping...")
                looperino -= 1

#Main Memory
def mainMemory():
    looperino = 1
    while looperino > 0:
        print("Memory stuff...")
        looperino -= 1

#Runner
def main(isPixel, isMemory):
    if isPixel:
        mainPixel(  Multiprocessing = False, SaveToPng = True,
            ShowFPS = True, Debug = True, RunOnce = False)

    if isMemory:
        mainMemory()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Usage: sudo python %s -pixel OR -memory" % sys.argv[0])
        exit()

    for argument in sys.argv:
        if argument == "-pixel":
            main(True, False)

        if argument == "-memory":
            main(False, True)
