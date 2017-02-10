#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import collections
import serial
import time
import struct
#import msvcrt
from array import *
import binascii
import numpy as np
from math import *
import os
os.environ['PYTHON_EGG_CACHE'] = '/tmp'

import matplotlib
matplotlib.use('TKAgg')

from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
from collections import deque
#threading
import threading


#initilize the channle buffers
ch0_buf = deque(0 for _ in range(1000))
# for _ in range(1000):
#     ch0_buf = 0
ch1_buf = deque(0 for _ in range(1000))
avg = 0

def detect_peaks(x, mph=None, mpd=1, threshold=0, edge='rising',
                 kpsh=False, valley=False, show=False, ax=None):

    x = np.atleast_1d(x).astype('float64')
    if x.size < 3:
        return np.array([], dtype=int)
    if valley:
        x = -x
    # find indices of all peaks
    dx = x[1:] - x[:-1]
    # handle NaN's
    indnan = np.where(np.isnan(x))[0]
    if indnan.size:
        x[indnan] = np.inf
        dx[np.where(np.isnan(dx))[0]] = np.inf
    ine, ire, ife = np.array([[], [], []], dtype=int)
    if not edge:
        ine = np.where((np.hstack((dx, 0)) < 0) & (np.hstack((0, dx)) > 0))[0]
    else:
        if edge.lower() in ['rising', 'both']:
            ire = np.where((np.hstack((dx, 0)) <= 0) & (np.hstack((0, dx)) > 0))[0]
        if edge.lower() in ['falling', 'both']:
            ife = np.where((np.hstack((dx, 0)) < 0) & (np.hstack((0, dx)) >= 0))[0]
    ind = np.unique(np.hstack((ine, ire, ife)))
    # handle NaN's
    if ind.size and indnan.size:
        # NaN's and values close to NaN's cannot be peaks
        ind = ind[np.in1d(ind, np.unique(np.hstack((indnan, indnan-1, indnan+1))), invert=True)]
    # first and last values of x cannot be peaks
    if ind.size and ind[0] == 0:
        ind = ind[1:]
    if ind.size and ind[-1] == x.size-1:
        ind = ind[:-1]
    # remove peaks < minimum peak height
    if ind.size and mph is not None:
        ind = ind[x[ind] >= mph]
    # remove peaks - neighbors < threshold
    if ind.size and threshold > 0:
        dx = np.min(np.vstack([x[ind]-x[ind-1], x[ind]-x[ind+1]]), axis=0)
        ind = np.delete(ind, np.where(dx < threshold)[0])
    # detect small peaks closer than minimum peak distance
    if ind.size and mpd > 1:
        ind = ind[np.argsort(x[ind])][::-1]  # sort ind by peak height
        idel = np.zeros(ind.size, dtype=bool)
        for i in range(ind.size):
            if not idel[i]:
                # keep peaks with the same height if kpsh is True
                idel = idel | (ind >= ind[i] - mpd) & (ind <= ind[i] + mpd) \
                    & (x[ind[i]] > x[ind] if kpsh else True)
                idel[i] = 0  # Keep current peak
        # remove the small peaks and sort back the indices by their occurrence
        ind = np.sort(ind[~idel])

    if show:
        if indnan.size:
            x[indnan] = np.nan
        if valley:
            x = -x
        _plot(x, mph, mpd, threshold, edge, valley, ax, ind)

    return ind

peak_list = []
peak_x = []
peak_y = []
valley_x = []
valley_y = []
topanddown = 1

temp_peak = 0
temp_valley = 0

base_angle = 0
temp_angle = 0
total_angle = 0

firstTopOrBottom = True
goingup = True
reachingPeak = False

a_sensor_state = -1 #0-state, 1-state, 2-state, 3-state
state_cut_ratio = 0.005
state_cut_up = 0
state_cut_down = 0
b_sensor_dir = 1 #1-increase 2-decrease

#running and notrunning
running = False
prev_val = [] #10 frames
diff_prev_val = []
r_count = 0


def detectRunning(val_list):     
    return np.std(val_list)


# def detectRunning(val_list):
#     return np.std.(val_list)

def detectState(val, up, down):
    st = -1
    if up != 0 and down != 0:
        if val > up:
            st = 0
        elif val < down:
            st = 2
    return st


# def detectState(val, up, down)
#     st = -1
#     if up!= 0 and down != 0:

def AddValue(val):
    global avg
    global topanddown

    global base_angle
    global temp_angle
    global firstTopOrBottom
    global temp_peak
    global temp_valley
    global total_angle
    global goingup
    global reachingPeak
    global state_cut_up
    global state_cut_down
    global a_sensor_state
    global prev_val
    global diff_prev_val
    global running

    global r_count

    ch0_buf.append(val)  #array in and array out
    ch0_buf.popleft()  # queue uses popleft()

    # ch0_buf.append(val)
    # ch0_buf.popleft()
    
    # 
    avg = avg + 0.1*(val-avg)    # low-pass filter
    ch1_buf.append(avg)
    ch1_buf.popleft()

    peak_list.append(val)

    if len(peak_list) > 1000:
        peak_list.pop(0)

    prev_val.append(val)
    if len(prev_val) > 10:
        prev_val.pop(0)

        std_value = detectRunning(prev_val)



    # peak_list.append(val)
    # if len(peak_list) > 1000:
    #     peak_list.pop(0)

    # prev_val.append(val)

    # if len(prev_val) > 10:
    #     prev_val.pop(0)

    #     std_value = detectRunning(prev_val)






        #print(std_value)
        
        if std_value > 0.5:  # predict as running
            #print("running")
            if running == False:  # see the change of state from stop to run at that moment
                running = True

                if a_sensor_state == 0:
                    a_sensor_state = 1

                elif a_sensor_state == 1:
                    a_sensor_state = 1

                elif a_sensor_state == 2:
                    a_sensor_state = 3

                elif a_sensor_state == 3:
                    a_sensor_state = 3


        # if std_value > 0.5:

        #     if running == True:
        #         running = False

        #         if a_sensor_state == 0:
        #             a_sensor_state = 1

        #         elif a_sensor_state == 1:
        #             a_sensor_state = 1

        #         elif a_sensor_state == 2:
        #             a_sensor_state = 2

        #         elif a_sensor_state == 3:
        #             a_sensor_state = 3


        else:
            #r_count = r_count + 1
            #print(r_count)  #predict as not running
            if running == True:
                running = False

                temp_st = detectState(val, state_cut_up, state_cut_down)  # use state 0 / 2 to judge whether it comes to 1/3;  -1 state doesn't change
                if temp_st != -1:
                    a_sensor_state = temp_st



        # else:

        #     if running == True:
        #         running = False

        #         temp_st = detectState(val, state_cut_up, state_cut_down)

        #         if temp_st !=-1:
        #             a_sensor_state = temp_st
        
       
        
    #running or not



    if topanddown == 1:  # To find peak
        filter_peaks = detect_peaks(peak_list, mph=920, mpd=20, threshold=0, edge='rising',  # return the newest location of the peak, threshold: 两个数差值大于0，才找到peak
                 kpsh=False, valley=False, show=False, ax=None)
    
        if len(filter_peaks)>0:  #found a peak 
            peak_x.append(1000)  # return its position  for visualization
            peak_y.append(peak_list[filter_peaks[-1]])  
            temp_peak = peak_list[filter_peaks[-1]]   # get the peak
            goingup = False   
            del peak_list[:]  # delete for the 
            topanddown = -1  # To find valley

            #angle cal
            if firstTopOrBottom:   # before the first frame
                base_angle = 0
                temp_angle = 0
                firstTopOrBottom = False
            else:
                base_angle += 20
                temp_angle = 0
                reachingPeak = True
                state_cut_up = temp_peak - (temp_peak - temp_valley) * state_cut_ratio

            a_sensor_state = 1  # set a state to 1


    if topanddown == 1:
        filter_peaks = detect_peaks(peak_list, mph=940, mpd=20, threshold=0, edge='rising',  # return the newest location of the peak, threshold: 两个数差值大于0，才找到peak
                 kpsh=False, valley=False, show=False, ax=None)

        temp_peak = peak_list[filter_peaks[-1]]
        










    else:
        filter_valleys = detect_peaks(peak_list, mph=-50, mpd=20, threshold=0, edge='rising',
                 kpsh=False, valley=True, show=False, ax=None)

        if len(filter_valleys)>0:  #found a valley
            valley_x.append(1000)
            valley_y.append(peak_list[filter_valleys[-1]])
            temp_valley = peak_list[filter_valleys[-1]]
            goingup = True
            del peak_list[:]
            topanddown = 1

            if firstTopOrBottom:
                base_angle = 0
                temp_angle = 0
                firstTopOrBottom = False
            else:
                base_angle += 20
                temp_angle = 0
                reachingPeak = True
                state_cut_down = temp_valley + (temp_peak - temp_valley) * state_cut_ratio

            a_sensor_state = 3


    
    if reachingPeak ==  False:
        if temp_peak*temp_valley != 0:
            if goingup:
                temp_angle = abs(val - temp_valley) * 20 / abs(temp_peak - temp_valley)
            else:
                temp_angle = abs(val - temp_peak) * 20 / abs(temp_peak - temp_valley)
    else:
        reachingPeak = False

    

    total_angle = base_angle + temp_angle

    if total_angle >= 360:
        base_angle = 0
        temp_angle = 0

    #print(total_angle)

    # For visualization

    if len(peak_x)>0:
        for itrx in range(len(peak_x)):
            peak_x[itrx] = peak_x[itrx] - 1

            #print(peak_x[itrx])

    if len(valley_x) > 0:
        for itrx in range(len(valley_x)):
            valley_x[itrx] = valley_x[itrx] - 1

    #print(peak_x)

    print(a_sensor_state)


    


    

def serial_read():
    t = threading.currentThread()

    serial_port = serial.Serial(port='/dev/tty.usbmodem1421', baudrate=9600)
    
    sx = 0
    try:
        while getattr(t, "do_run", True):   
            read_val = serial_port.readline()
            #print("read:%s"%(read_val))
            AddValue(int(read_val))          

            #time.sleep(0.1)  # ~200Hz
    except ValueError:
        pass

    print('existing...')
    """
    while serial_port.inWaiting():
        read_val = serial_port.read(serial_port.inWaiting())
        print("Read:%s" % (binascii.hexlify(read_val)))
    """
    serial_port.close()
    exit()


# def serial_read():
#     t = threading.currentThread()
#     serial_read = serial.Serial(port='/dev/tty.usbmodem1421', baudrate=9600)
#     sx = 0

#     try:
#         while getattr(t,"do_run",True)
#         read_val = serial_port.readline()
#         AddValue(read_val)

#     except ValueError:
#         pass

#     print("existing")

#     serial_port.close()

#     exit()





#############################################################################################

def main():
    t = threading.Thread(target=serial_read)
    t.start()

    def handle_close(evt):
        t.do_run = False
        t.join()

    def reScale():
        range_max_temp = 0
        range_min_temp = 8800000000
        for itrd in ch0_buf:
            if range_max_temp < itrd:
                range_max_temp = itrd
            if range_min_temp > itrd:
                range_min_temp = itrd
        print("max: %s, min: %s" % (range_max_temp,range_min_temp))
        return [range_max_temp, range_min_temp] 

    def press(event):
        print('press', event.key)
        sys.stdout.flush()
        if event.key == 'r':  #rescale
            r_max, r_min = reScale()
            p1.set_ylim(r_min, r_max)
            p2.set_ylim(r_min, r_max)
            fig.canvas.draw()

        if event.key == 'i':  #zoom in
            r_min, r_max = p1.get_ylim()
            r_range = r_max - r_min
            r_adaption = r_range * 0.1
            p1.set_ylim(r_min+r_adaption, r_max-r_adaption)
            p2.set_ylim(r_min+r_adaption, r_max-r_adaption)
            fig.canvas.draw()

        if event.key == 'o':  #zoom out
            r_min, r_max = p1.get_ylim()
            r_range = r_max - r_min
            r_adaption = r_range * 0.1
            p1.set_ylim(r_min-r_adaption, r_max+r_adaption)
            p2.set_ylim(r_min-r_adaption, r_max+r_adaption)
            fig.canvas.draw()

        if event.key == 'w':   #shift up
            r_min, r_max = p1.get_ylim()
            r_range = r_max - r_min
            r_adaption = r_range * 0.1
            p1.set_ylim(r_min+r_adaption, r_max+r_adaption)
            p2.set_ylim(r_min+r_adaption, r_max+r_adaption)
            fig.canvas.draw()

        if event.key == 'x':   #shift down
            r_min, r_max = p1.get_ylim()
            r_range = r_max - r_min
            r_adaption = r_range * 0.1
            p1.set_ylim(r_min-r_adaption, r_max-r_adaption)
            p2.set_ylim(r_min-r_adaption, r_max-r_adaption)
            fig.canvas.draw()

    fig, (p1, p2) = plt.subplots(2, 1)
    fig.canvas.mpl_connect('close_event', handle_close)
    fig.canvas.mpl_connect('key_press_event', press)

    range_max = 1100
    range_min = -10

    plot_data, = p1.plot(ch0_buf, animated=True)

    #plot_processed, = p2.plot(ch1_buf, animated=True)
    
    wedge = mpatches.Wedge((0.5, 0.5), 0.2, 0, 0)
    p2.add_patch(wedge)
    #p2.axis('equal')
    #p2.axis("off")
    
    plot_peak, = p1.plot(peak_x, peak_y, 'ro')
    plot_valley, = p1.plot(valley_x, valley_y, 'ro')


    p1.set_ylim(range_min, range_max)
    #p2.set_ylim(range_min, range_max)
    
    def animate(i):
        plot_data.set_ydata(ch0_buf)
        plot_data.set_xdata(range(len(ch0_buf)))
        
        #plot_processed.set_ydata(ch1_buf)
        #plot_processed.set_xdata(range(len(ch1_buf)))
        #wedge.theta1 += 0.1
        #wedge._recompute_path()
        wedge.theta2 = total_angle
        wedge._recompute_path()

        plot_peak.set_ydata(peak_y)
        plot_peak.set_xdata(peak_x)

        plot_valley.set_ydata(valley_y)
        plot_valley.set_xdata(valley_x)

        return [plot_data, wedge, plot_peak, plot_valley]
    
    ani = animation.FuncAnimation(fig, animate, range(1000), 
                                  interval=20, blit=True)  #20 delay, frames refresh 50 times per sec
    plt.show()

if __name__ == "__main__":
    main()
