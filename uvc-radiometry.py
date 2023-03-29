#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ImportantFunctions as IF
import datetime
import serial
from PIL import ImageTk
from PIL import Image
import PIL
import tkinter.font
import tkinter.messagebox
import tkinter.filedialog
import tkinter as tk
import imutils
import cv2 as cv2
import math

import keyboard
from uvctypes import *
import time
import cv2
import numpy as np
try:
    from queue import Queue
except ImportError:
    from Queue import Queue
import platform
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
BUF_SIZE = 2
q = Queue(BUF_SIZE)


def py_frame_callback(frame, userptr):

    array_pointer = cast(frame.contents.data, POINTER(
        c_uint16 * (frame.contents.width * frame.contents.height)))
    data = np.frombuffer(
        array_pointer.contents, dtype=np.dtype(np.uint16)
    ).reshape(
        frame.contents.height, frame.contents.width
    )  # no copy

    # data = np.fromiter(
    #   frame.contents.data, dtype=np.dtype(np.uint8), count=frame.contents.data_bytes
    # ).reshape(
    #   frame.contents.height, frame.contents.width, 2
    # ) # copy

    if frame.contents.data_bytes != (2 * frame.contents.width * frame.contents.height):
        return

    if not q.full():
        q.put(data)


PTR_PY_FRAME_CALLBACK = CFUNCTYPE(
    None, POINTER(uvc_frame), c_void_p)(py_frame_callback)


def ktof(val):
    return (1.8 * ktoc(val) + 32.0)


def ktoc(val):
    return (val - 27315) / 100.0


def raw_to_8bit(data):
    cv2.normalize(data, data, 0, 65535, cv2.NORM_MINMAX)
    np.right_shift(data, 8, data)
    return cv2.cvtColor(np.uint8(data), cv2.COLOR_GRAY2RGB)


def display_temperature(img, val_k, loc, color):
    val = ktof(val_k)
    cv2.putText(img, "{0:.1f} degF".format(val), loc,
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)
    x, y = loc
    cv2.line(img, (x - 2, y), (x + 2, y), color, 1)
    cv2.line(img, (x, y - 2), (x, y + 2), color, 1)


ctx = POINTER(uvc_context)()
dev = POINTER(uvc_device)()
devh = POINTER(uvc_device_handle)()
ctrl = uvc_stream_ctrl()

res = libuvc.uvc_init(byref(ctx), 0)
if res < 0:
    print("uvc_init error")
    exit(1)

try:
    res = libuvc.uvc_find_device(ctx, byref(dev), PT_USB_VID, PT_USB_PID, 0)
    print(PT_USB_VID, PT_USB_PID)
    if res < 0:
        print("uvc_find_device error")
        exit(1)
except:
    libuvc.uvc_exit(ctx)

try:
    res = libuvc.uvc_open(dev, byref(devh))
    if res < 0:
        print("uvc_open error")
        exit(1)

    print("device opened!")

    print_device_info(devh)
    print_device_formats(devh)

    frame_formats = uvc_get_frame_formats_by_guid(devh, VS_FMT_GUID_Y16)
    if len(frame_formats) == 0:
        print("device does not support Y16")
        exit(1)

    libuvc.uvc_get_stream_ctrl_format_size(devh, byref(ctrl), UVC_FRAME_FORMAT_Y16,
                                           frame_formats[0].wWidth, frame_formats[0].wHeight, int(
        1e7 / frame_formats[0].dwDefaultFrameInterval)
    )

    res = libuvc.uvc_start_streaming(
        devh, byref(ctrl), PTR_PY_FRAME_CALLBACK, None, 0)
    if res < 0:
        print("uvc_start_streaming failed: {0}".format(res))
        exit(1)
except:
    libuvc.uvc_unref_device(dev)


root = tk.Tk()  # Main Root
root.attributes('-fullscreen', True)
# root.state('normal')
root.configure(background='white')
subFont1 = tkinter.font.Font(family='Segoe UI', size=20, weight="bold")
subFont2 = tkinter.font.Font(family='Segoe UI', size=11, weight="bold")

threshold_value = 90
area_required = 270
box_size = 30
box_size2 = 40
def MainLoop():
    global threshold_value
    global area_required
    global box_size
    global box_size2
    
    data = q.get(True, 500)    
    print(len(data),len(data[0]))
    data = cv2.resize(data[:, :], (240, 180))
    temperature = data / 100 - 273.15
    min_temp = 33
    max_temp = 37.5
    temp_norm = math.e ** ((temperature - min_temp) / (max_temp - min_temp))
    temp_norm = temp_norm * 255 / math.e
    temp_norm = np.clip(temp_norm, 0, 255)
    temp_norm = temp_norm.astype(np.uint8)
    
    min_temp2 = 28
    max_temp2 = 35
    temp_norm2 = math.e ** ((temperature - min_temp2) / (max_temp2 - min_temp2))
    temp_norm2 = temp_norm2 * 255 / math.e
    temp_norm2 = np.clip(temp_norm2, 0, 255)
    temp_norm2 = temp_norm2.astype(np.uint8)
    
    min_temp_fnd = round(np.amin(temperature), 2)
    max_temp_fnd = round(np.amax(temperature), 2)
    
    threshold_value = threshold_value_Entry.get()
    if threshold_value:
        try:
            threshold_value = int(threshold_value)
        except:
            threshold_value = 0
    else:
        threshold_value = 0
        
    try:
        threshold_value_temp = threshold_value*math.e/255
        threshold_value_temp = math.log(threshold_value_temp)/math.log(math.e)
        threshold_value_temp = threshold_value_temp*(max_temp - min_temp)
        threshold_value_temp = round(threshold_value_temp + min_temp,2)
    except:
        threshold_value_temp = 0
        
    area_required = area_required_Entry.get()
    if area_required:
        try:
            area_required = int(area_required)
        except:
            area_required = 0
    else:
        area_required = 0
        
    # print(threshold_value_temp)
    threshold_value_label.configure(text="Threshold Value: (Approx: " +str(threshold_value_temp)+ ")")
    _, temp_thresh = cv2.threshold(temp_norm, threshold_value, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5, 5), np.uint8)

    cv2.imwrite("Video1.png", temp_thresh)

    new_img = cv2.imread("Video1.png")
    height, width = new_img.shape[:2]
    
    rows = new_img.shape[0]
    cols = new_img.shape[1]

    box_size = box1_Entry.get()
    if box_size:
        try:
            box_size = int(box_size)
        except:
            box_size = 1
    else:
        box_size = 1
        
    box_size2 = box2_Entry.get()
    if box_size2:
        try:
            box_size2 = int(box_size2)
        except:
            box_size2 = 1
    else:
        box_size2 = 1
    
    for i in range(0, width, box_size2):
        cv2.line(new_img, (i, 0), (i, height), (0, 0, 255), 1)

    for i in range(0, height, box_size):
        cv2.line(new_img, (0, i), (width, i), (0, 0, 255), 1)
    
    Count = 0
    logics = []
    for i in range(0, rows, box_size):
        for j in range(0, cols, box_size2):
            grid = temp_thresh[i:i+box_size, j:j+box_size2]
            grid2 = temp_norm[i:i+box_size, j:j+box_size2]
            ave = round(np.average(grid2))/255
            ave = ave*math.e
            ave = math.log(ave) / math.log(math.e)
            ave = ave * (max_temp - min_temp)
            ave = ave + min_temp
            ave = round(ave, 2)
            white_pixels = np.sum(grid == 255)
            if white_pixels > area_required:
                cv2.rectangle(new_img, (j, i), (j+box_size2, i+box_size), (0, 255, 0), 1)
                Count = Count + 1
                font = cv2.FONT_HERSHEY_SIMPLEX
                # cv2.putText(new_img, str(Count), (j, i+7), font, 0.35, (0, 255, 0), 1, cv2.LINE_AA)
                logics.append(True)
            else:
                logics.append(False)
    
    color_map = cv2.COLORMAP_JET
    temp_normed = cv2.normalize(temperature, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    temp_colored = cv2.applyColorMap(temp_norm2, color_map)
    
    while True:
        try:
            RGB_CamImg = cv2.imread("downloaded.png")
            RGB_CamImg = cv2.resize(RGB_CamImg,(240,180))
            a=RGB_CamImg #Pang save lang, para safe

            gray = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            print(faces)
            Centers = []
            for (x, y, w, h) in faces:
                # cv2.rectangle(a, (x, y), (x+w, y+h), (0, 255, 0), 2)
                Centers.append((x+int(w/2),y+int(h/2)))
            print(Centers)
            break
        except:
            pass
    Count2 = 0
    itera = 0
    for i in range(0, rows, box_size):
        for j in range(0, cols, box_size2):
            cv2.rectangle(RGB_CamImg, (j, i), (j+box_size2, i+box_size), (0, 0, 255), 1)
            if FindCenterOn(j, i, box_size2, box_size, Centers) and logics[itera] == True:
                cv2.rectangle(RGB_CamImg, (j, i), (j+box_size2, i+box_size), (0, 255, 0), 1)
                cv2.circle(RGB_CamImg,FindCenter(j, i, box_size2, box_size, Centers),5,(0,255,0),-1,cv2.LINE_AA)
                Count2 = Count2 + 1
                cv2.putText(RGB_CamImg, str(Count2), (j, i+7), font, 0.35, (0, 255, 0), 1, cv2.LINE_AA)
                
            elif FindCenterOn(j, i, box_size2, box_size, Centers):
                cv2.rectangle(RGB_CamImg, (j, i), (j+box_size2, i+box_size), (255, 0, 0), 1)
                cv2.circle(RGB_CamImg,FindCenter(j, i, box_size2, box_size, Centers),5,(0,255,0),-1,cv2.LINE_AA)
                Count2 = Count2 + 1
                cv2.putText(RGB_CamImg, str(Count2), (j, i+7), font, 0.35, (0, 255, 0), 1, cv2.LINE_AA)
            elif logics[itera] == True:
                cv2.rectangle(RGB_CamImg, (j, i), (j+box_size2, i+box_size), (255, 0, 0), 1)
                Count2 = Count2 + 1
                cv2.putText(RGB_CamImg, str(Count2), (j, i+7), font, 0.35, (0, 255, 0), 1, cv2.LINE_AA)
            itera = itera + 1
            
            # if white_pixels > area_required:
            #     cv2.rectangle(new_img, (j, i), (j+box_size2, i+box_size), (0, 255, 0), 1)
            #     Count2 = Count2 + 1
            #     font = cv2.FONT_HERSHEY_SIMPLEX
            #     cv2.putText(new_img, str(Count), (j, i+7), font, 0.35, (0, 255, 0), 1, cv2.LINE_AA)
    
    pips_value_label.configure(text="People (approx.): " + str(Count2))
    min_value_label.configure(text="Min Temp: " + str(min_temp_fnd) + " C")
    max_value_label.configure(text="Max Temp: " + str(max_temp_fnd) + " C")
    
    cv2.imwrite("Video1A.png", new_img)
    cv2.imwrite("Video2A.png", temp_colored)
    try:
        cv2.imwrite("Video3A.png", RGB_CamImg)
    except:
        pass
    IF.tkShow(Video1, "Video1A.png", 1)
    IF.tkShow(Video2, "Video2A.png", 1)
    IF.tkShow(Video3, "Video3A.png", 1)
    root.after(5, MainLoop)

def FindCenterOn(j, i, box_size_2, box_size, centers):
    for center in centers:
        if (j <= center[0] <= j+box_size_2) and (i <= center[1] <= i+box_size):
            return True
    return False

def FindCenter(j, i, box_size_2, box_size, centers):
    for center in centers:
        if (j <= center[0] <= j+box_size_2) and (i <= center[1] <= i+box_size):
            return center
    return False


GUI1 = tk.Frame(root)
GUI1.pack()

IF.Create_White_Screen("bg1.png", root.winfo_screenwidth(),
                       root.winfo_screenheight())
Background = tk.Label(GUI1, text='', font=subFont1, bg='white', bd=0)
Background.pack()
IF.tkShow(Background, "bg1.png", 1)

Video1 = tk.Label(GUI1, font=subFont1, bg='white')
Video1.place(x=10, y=10)

Video2 = tk.Label(GUI1, font=subFont1, bg='white')
Video2.place(x=300, y=10)

Video3 = tk.Label(GUI1, font=subFont1, bg='white')
Video3.place(x=300, y=270)

max_value_label = tk.Label(GUI1, font=subFont2, bg='white', height=1, text="Max Temp: ")
max_value_label.place(x=10, y=220)

min_value_label = tk.Label(GUI1, font=subFont2, bg='white', height=1, text="Min Temp: ")
min_value_label.place(x=10, y=240)

pips_value_label = tk.Label(GUI1, font=subFont2, bg='white', height=1, text="People: ")
pips_value_label.place(x=10, y=260)

threshold_value_label = tk.Label(GUI1, font=subFont2, bg='white', height=1, text="Threshold Value")
threshold_value_label.place(x=10, y=300)

threshold_value_Entry = tk.Entry(GUI1, font=subFont2, bg='white',width=5)
threshold_value_Entry.place(x=10, y=320)
threshold_value_Entry.insert(0, threshold_value)

area_required_label = tk.Label(GUI1, font=subFont2, bg='white', height=1, text="Required Area: (max is 30x30=900)")
area_required_label.place(x=10, y=340)

area_required_Entry = tk.Entry(GUI1, font=subFont2, bg='white',width=5)
area_required_Entry.place(x=10, y=360)
area_required_Entry.insert(0, area_required)

box1_label = tk.Label(GUI1, font=subFont2, bg='white', height=1, text="y: ")
box1_label.place(x=10, y=400)

box1_Entry = tk.Entry(GUI1, font=subFont2, bg='white',width=5)
box1_Entry.place(x=40, y=400)
box1_Entry.insert(0, box_size)

box2_label = tk.Label(GUI1, font=subFont2, bg='white', height=1, text="x: ")
box2_label.place(x=10, y=380)

box2_Entry = tk.Entry(GUI1, font=subFont2, bg='white',width=5)
box2_Entry.place(x=40, y=380)
box2_Entry.insert(0, box_size2)




root.after(5, MainLoop)
root.mainloop()

libuvc.uvc_stop_streaming(devh)
libuvc.uvc_unref_device(dev)
libuvc.uvc_exit(ctx)
