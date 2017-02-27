#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import sys
import collections
import serial
import time
import struct
from array import *
import binascii
import numpy as np
from math import *
from random import randint
from collections import deque

import os
os.environ['PYTHON_EGG_CACHE'] = '/tmp'

import matplotlib
matplotlib.use('TKAgg')
matplotlib.rcParams['toolbar'] = 'None'

from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection


from playsound import playsound

trial_distraction_correct = 0
trial_isWaitingForAnswer = 0  #0-tesitng, 1-wait for profile, 2-wait for color, 3-check color answer
trial_answer_color = 0
color_correct_trial = 0
color_accuracy = 0
idx = 0
idx_p = 0
idxc = 0
idxc_p = 0
pause = True
current_trial = 0

def main():
    
    global trial_distraction_correct
    global trial_isWaitingForAnswer
    global trial_answer_color
    global color_correct_trial
    global color_accuracy

    def close_event():
        exit()

    def handle_close(event):
        close_event()

    def press(event):
        global trial_answer_color
        global color_correct_trial
        global color_accuracy
        global pause
        global trial_isWaitingForAnswer
        global current_trial
        global trial_distraction_correct

        #mMotor.write_serial(event.key)
        if event.key == ' ':
            if trial_isWaitingForAnswer == 1:
                print("expecting answers")

            else:
                pause^=True
                if not pause:
                    trial_isWaitingForAnswer = 0
                    current_trial+=1
                    trial_distraction_correct = 0

                if pause:
                    print("color: %s"%trial_distraction_correct)
                    trial_isWaitingForAnswer = 1

        elif event.key == 'q':
            #close
            plt.close(fig)

        else:   
            if trial_isWaitingForAnswer == 1:
                try:
                    trial_answer_color = int(event.key)
                    if trial_answer_color == trial_distraction_correct:
                        color_correct_trial+=1

                    color_accuracy = (color_correct_trial / current_trial) * 100.0
                    trial_isWaitingForAnswer = 2
                except ValueError:
                    trial_isWaitingForAnswer = 1
                    print("not a valid number")
            

    fig, p1 = plt.subplots()
    p1.axis("off")
    fig.canvas.set_window_title('Study Train Distractor')

    fig.canvas.mpl_connect('close_event', handle_close)
    fig.canvas.mpl_connect('key_press_event', press)


    color_pool = ['b', 'g', 'r', 'y', 'k'] #5
    text_pool = ['BLUE', 'GREEN', 'RED', 'YELLOW', 'BLACK'] #5
   
    show_text = p1.text(0.5, 0.3, '', color='g', fontsize=30, horizontalalignment='center', verticalalignment='center', transform=p1.transAxes, animated=True)
    show_color_accuracy = p1.text(0.8, 0.55, '', color='b', fontsize=16, horizontalalignment='center', verticalalignment='center', transform=p1.transAxes, animated=True)
    
    def animate(i):
        global idx
        global idx_p
        global idxc
        global idxc_p
        global trial_distraction_correct

        if not pause:
            
            idx = randint(0, 4)
            while idx == idx_p:
                idx = randint(0, 4)

            show_text.set_text(text_pool[idx])
            idxc = randint(0, 4)
            while idxc == idxc_p:
                idxc = randint(0, 4)
            show_text.set_color(color_pool[idxc])

            idx_p = idx
            idxc_p = idxc

            if idx == idxc:
                trial_distraction_correct+=1
            
        else:
            if trial_isWaitingForAnswer == 1:
                show_text.set_text("how many text-color matches?")
                show_text.set_color('b')
            elif trial_isWaitingForAnswer == 2:
                if int(trial_answer_color) == trial_distraction_correct:
                    show_text.set_text("text-color matches correct")
                    show_text.set_color('b')
                else:
                    show_text.set_text("text-color matches not correct")
                    show_text.set_color('r')


        show_color_accuracy.set_text("color test accuracy: %1.1f"%color_accuracy)
        if color_accuracy > 80:
            show_color_accuracy.set_color('b')
        else:
            show_color_accuracy.set_color('r')


        return [show_text, show_color_accuracy]

    ani = animation.FuncAnimation(fig, animate, 100, 
                                  interval=2000, blit=True)  #20 delay, frames refresh 50 times per sec

    plt.show()

if __name__ == "__main__":
    main()
