# -*- coding: utf-8 -*-
import os
import sys
import stat
import struct
import math
import copy
import RPi.GPIO as GPIO
import serial
from array import *
from ctypes import *
import threading
import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# from tkinter import *
from tkinter import *
#import tkinter
import tkinter as tk
from tkinter import font
from tkinter import messagebox
from tkinter import tix
from enum import Enum
from enum import IntEnum
from ctypes import *
from array import *
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import time
from numpy.ctypeslib import ndpointer
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os.path
import base64
from binascii import a2b_base64, b2a_base64
from typing import Text
import pyudev
from Crypto.Cipher import AES
from cryptography.fernet import Fernet
#from pywinauto import Application
from threading import Thread
from time import sleep
from random import randint

#python檢測U盤的插入，以及進行自動複製檔案並寫入檔案
from time import sleep
from shutil import copytree
from psutil import disk_partitions

class MeasurementType(IntEnum):
    Spectrum = 0
    Absorbance = 1
    Transmittance = 2
    Reflection = 3
    #Concentration = 4

#_location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + '/'

path = os.path.dirname(os.path.abspath(__file__)) + os.path.sep

#dll_name = "lib_linux_X64_1.0.15.so"
dll_name = "lib_linux_ARM_1.0.15.so"
#dll_name = "lib_ARM.so.1.2"
dllabspath = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + dll_name
dll = CDLL(dllabspath)
PID = 0
VID = 0

num = c_int(0)
frame_size = c_short()
hand = c_void_p(0)
phand = pointer(hand)
SN = (c_char * 16)()
MN = (c_char * 16)()

lambda_1_index = 0
lambda_2_index = 0
lambda_3_index = 0
lambda_4_index = 0
lambda_5_index = 0

#parameter
MeasureType = -1
#SerialNumber = (c_char * 16)()
# Display_name = []#= (c_char*len(1000))()
SerialNumber = ""
Usb_path = ""
passwd = ""
IntegrationTime = 0
Average=0
Serial_mode=-1
lambda_1 = 0
lambda_1_display=""
lambda_2 = 0
lambda_3 = 0
lambda_4 = 0
lambda_5 = 0

select_unit=0
Spectrum_unit=""
Absorbance_unit=""
Transmittance_unit=""
Reflection_unit=""
ppm_unit=""

Do_calibration=False
k=0
Lamp_reset = 0
Lamp_total_time = 0
Decimal_number = 0


checkLampFirst = False
checkLampSeccond = False

check_lambda = True

#AES
AesKey = "JaNdRgUkXp2s5u8x/A?D(G+KbPeShVmY" #密鑰
AesIv = "UkXp2s5v8y/B?E(G"  #密鑰向量

print("check num of devices...")
errorcode = dll.UAI_SpectrometerGetDeviceAmount(VID, PID, pointer(num))
if(num.value > 0):
    print("device number = ", num.value)
else:
    print("no device!!", errorcode, num.value)
    #exit()

#AES
def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)
    #return s+chr(16-len(s)%16)*(16-len(s)%16)

def encrypt(message, key, iv, key_size=256):
    #global encoder
    message = pad(message)
    #iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(message)

def decrypt(ciphertext, key, iv):
    #global encoder
    #iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b"\0")
    #return encoder.decode(plaintext)

def encrypt_file(file_name, key, iv):
    with open(file_name, 'rb') as fo:
        plaintext = fo.read()
    enc = encrypt(plaintext, key, iv)
    with open(file_name.replace(".ini", "") + "_Encrypt.ini", 'wb') as fo:
        fo.write(enc)

def decrypt_file(file_name, key, iv):
    with open(file_name, 'rb') as fo:
        ciphertext = fo.read()
    dec = decrypt(ciphertext, key ,iv)
    with open(file_name.replace(".ini", "") + "_Decrypt.ini", 'wb') as fo:
        fo.write(dec)
        
#decrypt_file('setup.ini', AesKey, AesIv)
decrypt_file(path+'config.ini', AesKey, AesIv)

n = int(num.value)
b = range(n)
pb = (c_int * n)(*b)
rerrorcode = dll.UAI_SpectrometerGetDeviceList(pointer(num), pb)

errorcode = dll.UAI_SpectrometerOpen(c_int(0),pointer(hand), c_int(0), c_int(0))
if(errorcode != 0):print("UAI_SpectrometerOpen errorcode = ", errorcode)

errorcode = dll.UAI_SpectrometerGetSerialNumber(hand, pointer(SN))
if(errorcode != 0):print("UAI_SpectrometerGetSerialNumber errorcode = ", errorcode)
#print("SN",str(SN.value.decode("utf-8")))
#print("SN",str(SN.value))
errorcode = dll.UAI_SpectrometerGetModelName(hand, pointer(MN))
if(errorcode != 0):print("UAI_SpectrometerGetModelName errorcode = ", errorcode)
dll.UAI_SpectromoduleGetFrameSize(hand, pointer(frame_size))
if(errorcode != 0):print("UAI_SpectromoduleGetFrameSize errorcode = ", errorcode)
if frame_size.value ==0:
     print("Framesize is invalid")
     exit()
SD_lambda_Raw = (c_float*frame_size.value)()
SD_lambda_resolution = (c_float*frame_size.value)()
dll.UAI_SpectrometerWavelengthAcquire(hand, pointer(SD_lambda_Raw))
buffer = (c_float*frame_size.value)()
#reference = (c_float*frame_size.value)()
buffer_resolution = (c_float*frame_size.value)()
if(errorcode != 0):print("UAI_SpectrometerWavelengthAcquire errorcode = ", errorcode)

#Init dark
dark = (c_float*frame_size.value)()
ref = (c_float*frame_size.value)()

def initial_parameter():
    #Read ini parameter
    #f_setup_ini = open(path+"setup.ini", mode='r')
    #f_SN_ini = open(path+"config_Decrypt.ini", mode='r')
    f_setup_ini = open(os.path.join(os.path.dirname(__file__), "setup.ini"), 'r')
    f_lamp_ini = open(os.path.join(os.path.dirname(__file__), "lamp.ini"), 'r')
    f_SN_ini = open(os.path.join(os.path.dirname(__file__), "config_Decrypt.ini"), 'r')
    #從第35位置開始讀取
    f_SN_ini.seek(35,0)
    setup_lines = f_setup_ini.readlines()
    lamp_lines = f_lamp_ini.readlines()
    SN_lines = f_SN_ini.readlines()

    global MeasureType
    global SerialNumber
    global Usb_path
    global passwd
    global k
    global IntegrationTime
    global Average
    global Serial_mode
    global lambda_1
    global lambda_1_display
    global lambda_2
    global lambda_3
    global lambda_4
    global lambda_5
    global select_unit
    global Spectrum_unit
    global Absorbance_unit
    global Transmittance_unit
    global Reflection_unit
    global ppm_unit
    #global Display_name
    global Do_calibration
    global Lamp_reset
    global Lamp_total_time
    global Decimal_number

    for line in setup_lines:       #把lines中的資料逐行讀取出來
        #if "\x8e\xd3\x97\x12\xe6N@\xfb\xcds\x1c\xf4*\x08X\xfa" not in line:

            #if '#' not in line and line != None and len(line) > 0:
            if "#" not in line and "=" in line:
                startIndex = line.index("=") + 1
                endIndex = len(line)
                # print("start",startIndex) 
                # print("end",endIndex)
                if "Measurement" in line:
                    #if int(line[startIndex:endIndex]) == int(MeasurementType.Absorbance):
                    MeasureType = int(line[startIndex:endIndex])
                    #print("read MeasureType = ",MeasureType)
                elif "Usb_path" in line:
                    Usb_path = line[startIndex:endIndex - 1]
                elif "k" in line:
                    k = float(line[startIndex:endIndex])
                elif "IntegrationTime" in line:
                    IntegrationTime = int(line[startIndex:endIndex])    
                elif "Average" in line:
                    Average = int(line[startIndex:endIndex])
                    #print("Average = ",Average)
                elif "Serial_mode" in line:
                    Serial_mode = int(line[startIndex:endIndex])
                elif "Lambda" in line:
                    if "Lambda_1" in line and int(line[startIndex:endIndex]) != 0:
                        lambda_1 = int(line[startIndex:endIndex])
                    if "Lambda_1_display" in line and (line[startIndex:endIndex]) != 0:
                        lambda_1_display = line[startIndex:endIndex].replace("\n","")
                        #print("Lambda_1_display = ",lambda_1_display)
                    elif "Lambda_2" in line and int(line[startIndex:endIndex]) != 0:
                        lambda_2 = int(line[startIndex:endIndex])
                    elif "Lambda_3" in line and int(line[startIndex:endIndex]) != 0:
                        lambda_3 = int(line[startIndex:endIndex])
                    elif "Lambda_4" in line and int(line[startIndex:endIndex]) != 0:
                        lambda_4 = int(line[startIndex:endIndex])
                    elif "Lambda_5" in line and int(line[startIndex:endIndex]) != 0:
                        lambda_5 = int(line[startIndex:endIndex])     
                elif "unit" in line:
                    if "select_unit" in line:
                        select_unit = int(line[startIndex:endIndex])
                    elif "Spectrum_unit" in line:
                        Spectrum_unit = line[startIndex:endIndex - 1]
                    elif "Absorbance_unit" in line:
                        Absorbance_unit = line[startIndex:endIndex - 1]
                    elif "Transmittance_unit" in line:
                        Transmittance_unit = line[startIndex:endIndex - 1]
                    elif "Reflection_unit" in line:
                        Reflection_unit = line[startIndex:endIndex - 1]
                    elif "ppm_unit" in line:
                        ppm_unit = line[startIndex:endIndex - 1]
                elif "Do_calibration" in line:
                    if line[startIndex:endIndex - 1] == "True":
                        Do_calibration = True
                    else :
                        Do_calibration = False    
                elif "Decimal_number" in line:
                    Decimal_number = int(line[startIndex:endIndex])
    for line in lamp_lines:       #Lamp
            if "#" not in line and "=" in line:
                startIndex = line.index("=") + 1
                endIndex = len(line)
                if "Lamp_reset" in line:
                        Lamp_reset = int(line[startIndex:endIndex])
                elif "Lamp_total_time" in line:
                    if Lamp_reset == 0:
                        Lamp_total_time = int(line[startIndex:endIndex])
                    else :    #reset
                        Lamp_total_time = 0
                    print(Lamp_total_time)    
    for line in SN_lines:       #SN
            if "#" not in line and "=" in line:
                startIndex = line.index("=") + 1
                endIndex = len(line)
                if "SN" in line:
                    SerialNumber = line[startIndex:endIndex - 1]
                    #print("SerialNumber",str(SerialNumber.value.decode("utf-8")))
                    #print("SerialNumber",SerialNumber)
                elif "passwd" in line:
                    passwd = line[startIndex:endIndex - 1]    
    try:
        #os.remove("setup.ini")
        os.remove(path+"config_Decrypt.ini")
        #os.remove("setup_Decrypt.ini")
    except OSError as e:
        print(e)
    # else:
    #     print("File is deleted successfully")

def ReadFile(name):
    file = open(name, mode='r')
    #lines = file.readlines()

def WriteFile(name,SD_lambda_Raw,spectrum):
    T = time.strftime("%H%M%S") 
    D = time.strftime("_%Y%m%d")
    file = open(name + D + T, 'w')

    #print(Usb_path + '/' + name + D + T)
    #file = open(Usb_path+ '/' + name + D + T, 'w')
    I = range(frame_size.value)
    for i in I:
        file.write(str('%.3f'%SD_lambda_Raw[i])+','+str('%.8f'%spectrum[i]) + '\n')

    #content = ",".join([str(i) for i in spectrum])
    #file.write(content)
    file.close()

initial_parameter()

class CustomDialog(tk.Toplevel):
    def __init__(self, parent, prompt):
        tk.Toplevel.__init__(self, parent)
        #置頂
        self.wm_attributes('-topmost',1)
        self.wm_geometry("500x300")
        self.title(" ")
        self.var = tk.StringVar()
        self.font = 40
        self.label = tk.Label(self, text=prompt,font=('',self.font))
        self.entry = tk.Entry(self, textvariable=self.var,font=('',self.font))
        self.ok_button = tk.Button(self, text="OK", command=self.on_ok,font=('',self.font))

        self.label.pack(side="top", fill="x")
        self.entry.pack(side="top", fill="x")
        self.ok_button.pack(side="right")

        self.entry.bind("<Return>", self.on_ok)

    def on_ok(self, event=None):
        #print("terwerwe")
        self.popup_window_exist = False
        self.destroy()

    def show(self):
        self.wm_deiconify()
        self.entry.focus_force()
        self.wait_window()
        return self.var.get()

class MainWindow(tk.Frame):
    def __init__(self,master):    
        tk.Frame.__init__(self, master)
        self.master = master
        self.FileName = "lamp.ini"
        #print(self.FileName)
        self.master.title(" ")
        self.Lambda = tix.StringVar()
        self.Intensity = tix.StringVar()
        #self.Info = tix.StringVar()
        self.Lamp_time = tix.StringVar()
        self.popup_window_exist = False
        self.FirstGetReference = True
        self.GetReference = False
        self.checkLampStatus = True
        self.font = 20
        self.font_lambda = 50
        self.font_value = 75

        helv36 = font.Font(family='Helvetica', size=28)
        font.families()
        self.unit = ""

        self.show_Calibration = False
        self.show_Update = False
        self.show_lampTime = False
        self.show_lamptitle = False

        self.starttime = datetime.datetime.now()

        self.fm1 = Frame(self.master)
        self.fm1.pack(side=TOP, fill=BOTH, expand=YES)
        self.label = tk.Label(self.fm1,textvariable = self.Lambda,height = 1,width=10,font=('',self.font_lambda)).pack(side='top', anchor='sw', expand='yes',pady=5)

        self.fm2 = Frame(self.master)
        self.fm2.pack(side=TOP, fill=BOTH, expand=YES)
        self.master.wm_title("tk")
        self.master.grab_set()

        self.fm3 = Frame(self.master)
        self.fm3.pack(side=TOP, fill=BOTH, expand=YES)

        if Serial_mode == 0 : #RS232
            self.RS232_initial()
        elif Serial_mode == 1 : #RS485
            self.RS485_initial()

        #右鍵  
        self.Label_right = tk.Label(self.fm2,textvariable = self.Intensity,height = 1,font=('',self.font_value))
        self.Label_right.pack(side="top", fill="both", expand=FALSE, pady=5)
        self.menu = Menu(self, tearoff = 0)
        self.menu.add_command(label ="Input",command = self.Input_passwd,font=('',self.font))
        self.menu.add_command(label ="Hide",command = self.hide_button,font=('',self.font))
        self.Label_right.bind("<Button-3>", self.do_popup)

        #parameters
        self.runG = 1
        self.auto = 1
        self.ABSornot = False
        self.Dark = False

        self.getDark()
        self.set_unit()
        self.action()

    def hide_button(self):
        # if self.show_Calibration :
        #     self.button_calibration.pack_forget()
        #     self.show_Calibration = False
        if self.show_Update :
            self.button_update.pack_forget()
            self.show_Update = False
        if self.label_lampTime :
            self.label_lampTime.pack_forget()
            self.show_lampTime = False    
        if self.label_title :
            self.label_title.pack_forget()
            self.show_lamptitle = False    
        self.popup_window_exist = False    

    def Input_passwd(self):
        if self.popup_window_exist == False:
            self.popup_window_exist = TRUE
            string = CustomDialog(self, "Enter password:").show()
            Replace_string = passwd.replace("\"","")
            #input passwd
            if str(string) == str(Replace_string) and self.show_Calibration == False and self.show_Update == False and self.show_lampTime == False:
                self.label_title = tk.Label(self.fm3,text = "燈泡時間", width=4,font=('',self.font))
                self.label_title.pack(side="left", fill="both", expand=True)
                self.label_lampTime = tk.Label(self.fm3 ,textvariable=self.Lamp_time, width=7,font=('',self.font))
                self.label_lampTime.pack(side="left", fill="both", expand=True,padx=11, pady=11)
                # self.button_calibration = tk.Button(self.fm3, text="校正", command=self.check_do_calibration,font=('',self.font))
                # self.button_calibration.pack(side="left", fill="both", expand=True,padx=11, pady=11)
                self.button_update = tk.Button(self.fm3, text="更新", command=self.update_program,font=('',self.font))
                self.button_update.pack(side="left", fill="both", expand=True,padx=11, pady=11)
                self.show_Calibration = True
                self.show_Update = True
                self.show_lampTime = True
                self.show_lamptitle = True    
            elif str(string) != str(Replace_string) :
                self.popup_window_exist = False
                messagebox.showerror("Password error!","please contact the application vendor")

    #RS485 Initial
    def RS485_initial(self):
        #if use half-auto, EN_485 = LOW is Receiver, EN_485 = HIGH is Send
        MODE = 0 #mode = 0 is full-guto, mode = 1 is half-auto
        if MODE == 1:
            EN_485 =  4
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(EN_485,GPIO.OUT)
            GPIO.output(EN_485,GPIO.HIGH)
        self.ser = serial.Serial("/dev/ttyS0",115200,timeout=1)     

    #RS232 Initial
    def RS232_initial(self):
        self.ser = serial.Serial("/dev/ttyS0", 9600, timeout=1) #port, baudrate

    def update_program(self):
        print("")
        quit()

    def do_popup(self,event):
        try:
            self.menu.tk_popup(event.x_root, event.y_root,0)
        finally:
            self.menu.grab_release()

    def set_unit(self):
        if select_unit == 0 :
            self.unit = Spectrum_unit
        if select_unit == 1 :
            self.unit = Absorbance_unit
        if select_unit == 2 :
            self.unit = Transmittance_unit
        if select_unit == 3 :
            self.unit = Reflection_unit
        if select_unit == 4 :
            self.unit = ppm_unit                

    def Getdata (self):
        
        buffer = (c_float*frame_size.value)()
        
        errorcode = dll.UAI_SpectrometerDataAcquire(hand, IntegrationTime*1000, pointer(buffer), 1)
        #print("DataOneshot errorcode = ", errorcode)#errorcode = dll.UAI_SpectrometerDataOneshot(hand, temp_IT*1000, pointer(buffer), self.avg.get())
        
        if(errorcode != 0):print("DataAcquire errorcode = ", errorcode)

        self.buffer = buffer
        del buffer

        self.Measurement()

    def Measurement(self):
        #Get color
        global SD_lambda_resolution
        global buffer_resolution
        global checkDoReference
        global reference
        global Lamp_reset
        global Lamp_total_time
        global Do_calibration
        global count
        global ser
        #count = 0
        
        buffer = (c_float*frame_size.value)()
        for x in range(frame_size.value):
            buffer[x] = self.buffer[x] 

        errorcode = 0
        if(MeasureType == MeasurementType.Spectrum):
            errorcode = dll.UAI_BackgroundRemoveWithAVG(hand,IntegrationTime*1000, pointer(buffer))
            if(errorcode != 0):print("Background errorcode = ", errorcode)
        else:
            for x in range(frame_size.value):
                buffer[x] = buffer[x] - dark[x]
        
        errorcode = dll.UAI_LinearityCorrection(hand, frame_size, pointer(buffer))
        if(errorcode != 0):print( "Linearity errorcode = ", errorcode)

        # for x in range(frame_size.value):
        #         print(x,SD_lambda_Raw[x],buffer[x])
        # print("---------")      
        self.wavelength_resolution(buffer)
        length_size = len(buffer_resolution)
        

        #print(max(buffer))
        #Check do Reference
        if max(buffer)>5000 :
            if self.FirstGetReference :
                if(self.FirstGetReference) :
                    self.getRef()
                    # for x in range(length_size):
                    #     self.reference[x] = buffer_resolution[x]
                    #     #print(reference[x],buffer_resolution[x])
                    # #print("------------------------------------------------------")          
                    self.FirstGetReference = False
                    self.GetReference = True
                    self.Excute_startTime = datetime.datetime.now()
            
                # for x in range(frame_size.value):
                #     print(reference[x])

            if self.GetReference:
                self.starttime = datetime.datetime.now()

                loan_plot = (c_float*length_size)()
                for x in range(length_size):
                    if MeasureType == MeasurementType.Spectrum:
                        loan_plot[x] = buffer_resolution[x] * k
                    else:
                        loan_plot[x] = buffer_resolution[x] 
                
                if MeasureType == MeasurementType.Spectrum:
                    self.print(SD_lambda_resolution,loan_plot,lambda_1_index,lambda_1_display,self.unit)
                    # for x in range(frame_size.value):
                    #     print(SD_lambda_resolution[x],loan_plot[x])
                if MeasureType == MeasurementType.Transmittance or MeasureType == MeasurementType.Reflection:
                    
                    for x in range(length_size):
                        if (loan_plot[x] <= 0 or self.reference[x] <= 0):
                            loan_plot[x] = 0
                        else:
                            loan_plot[x] = 100 * k * buffer_resolution[x] / self.reference[x]
                    
                    if MeasureType == MeasurementType.Transmittance :
                        self.print(SD_lambda_resolution,loan_plot,lambda_1_index,lambda_1_display,self.unit)
                    elif MeasureType == MeasurementType.Reflection :
                        self.print(SD_lambda_resolution,loan_plot,lambda_1_index,lambda_1_display,self.unit)

                #elif MeasureType == MeasurementType.Absorbance or MeasureType == MeasurementType.Concentration:
                elif MeasureType == MeasurementType.Absorbance:

                    for x in range(length_size):
                        if (loan_plot[x] <= 0 or self.reference[x] <= 0):
                            loan_plot[x] = 0
                        else:
                            loan_plot[x] = buffer_resolution[x] / self.reference[x]
                            #elif MeasureType == MeasurementType.Concentration:
                            if Do_calibration :    
                                loan_plot[x] = -1 * (math.log10(loan_plot[x])) * k
                            #if MeasureType == MeasurementType.Absorbance:
                            else:
                                loan_plot[x] = -1 * (math.log10(loan_plot[x])) * k
  
                    # for x in range(frame_size.value):
                    #     print(SD_lambda_resolution[x],loan_plot[x])

                    #if MeasureType == MeasurementType.Absorbance :
                    if Do_calibration :
                        self.print(SD_lambda_resolution,loan_plot,lambda_1_index,lambda_1_display,self.unit)
                    else :    
                        self.print(SD_lambda_resolution,loan_plot,lambda_1_index,lambda_1_display,self.unit)
                    #elif MeasureType == MeasurementType.Concentration :

                #self.checkLampAlive(buffer)
                self.Excute_endTime = datetime.datetime.now()
                self.temp =(self.Excute_endTime - self.Excute_startTime).seconds
                if(self.temp > 86400):
                    self.diff_time =(self.Excute_endTime - self.Excute_startTime).min
                else:    
                    self.diff_time =(self.Excute_endTime - self.Excute_startTime).seconds
                
                self.Display_Lamp_time(Lamp_total_time + self.diff_time)
                if Lamp_total_time + self.diff_time > 0:
                    Lamp_reset = 0
                else :
                    Lamp_reset = 1    
                self.save()
                #time.sleep(0.05)
            
                del buffer
                del loan_plot
                del errorcode
                
        self.endtime = datetime.datetime.now()

        #print((self.endtime - self.starttime).seconds)
        if (self.endtime - self.starttime).seconds > 60:
            if self.checkLampStatus:
                self.Lamp_error_msg()
                self.checkLampStatus = False
            #print("Lamp error")

    def Lamp_error_msg(self):
        global Do_calibration
        MsgBox = messagebox.showerror ('Error','Please change a new lamp',icon = 'warning')

    def search_lambda_index(self):     
        global lambda_1_index
        global lambda_2_index
        global lambda_3_index
        global lambda_4_index
        global lambda_5_index
        global lambda_1
        global lambda_2
        global lambda_3
        global lambda_4
        global lambda_5

        for x in range(len(SD_lambda_resolution)):
            if SD_lambda_resolution[x] == lambda_1:
                lambda_1_index = x
            if SD_lambda_resolution[x] == lambda_2:
                lambda_2_index = x
            if SD_lambda_resolution[x] == lambda_3:
                lambda_3_index = x		
            if SD_lambda_resolution[x] == lambda_4:
                lambda_4_index = x
            if SD_lambda_resolution[x] == lambda_5:
                lambda_5_index = x						

    #內插成整數波長    
    def wavelength_resolution(self,buffer):
        global SD_lambda_resolution
        global buffer_resolution
        global check_lambda

        last = 0 
        thread = 0.0
        list_wavelength = []
        list_intensity = []

        #range(起始值, 結束值, 遞增值)
        for i in range(0,int(SD_lambda_Raw[frame_size.value -1]+1),1):
            for j in range(last,frame_size.value - 1):
                thread = i
                if SD_lambda_Raw[j] <= thread and SD_lambda_Raw[j+1] > thread:
                    list_wavelength.append(i)
                    #list_intensity.append((self.buffer[j] + (self.buffer[j + 1] - self.buffer[j]) * (i - SD_lambda_Raw[j]) / (SD_lambda_Raw[j + 1] - SD_lambda_Raw[j])))
                    list_intensity.append((buffer[j] + (buffer[j + 1] - buffer[j]) * (i - SD_lambda_Raw[j]) / (SD_lambda_Raw[j + 1] - SD_lambda_Raw[j])))
                    last = j

        SD_lambda_resolution = (c_int*len(list_wavelength))()
        buffer_resolution = (c_float*len(list_intensity))()
        for x in range(len(list_wavelength)):
            SD_lambda_resolution[x] = list_wavelength[x]
            buffer_resolution[x] = list_intensity[x]
            #print(x,SD_lambda_resolution[x],buffer_resolution[x])
                              
        if check_lambda:
            self.search_lambda_index()
            check_lambda = False

    def getDark(self):
        #dark
        #f_dark = open(path+"dark", mode='r')
        f_dark = open(os.path.join(os.path.dirname(__file__), 'dark'), 'r')
        #print(len(f_dark.readlines()))
        #print("--------------------")
        lines = f_dark.readlines()
        dark=[0]*(len(lines))
        #print(len(lines))
        i=0
        for line in lines:
            startIndex = line.index(",") + 1
            endIndex = len(line)
            dark[i] = float(line[startIndex:endIndex])
            #print(dark[i])
            i+=1

    def getRef(self):
        f_ref = open(os.path.join(os.path.dirname(__file__), 'ref'), 'r')
        lines = f_ref.readlines()
        ref=[0]*(len(lines))
        #print("len ref = ",len(lines))
        i=0
        for line in lines:
            startIndex = line.index(",") + 1
            endIndex = len(line)
            ref[i] = float(line[startIndex:endIndex])
            #print(dark[i])
            i+=1        

        last = 0 
        thread = 0.0
        list_wavelength = []
        list_intensity = []
        #print("len SD_lambda_Raw = ",len(SD_lambda_Raw))
        #print("frame_size.value = ",frame_size.value)
        for i in range(0,int(SD_lambda_Raw[frame_size.value -1]+1),1):
            #print(SD_lambda_Raw[i])
            for j in range(last,frame_size.value - 1):
                thread = i
                if SD_lambda_Raw[j] <= thread and SD_lambda_Raw[j+1] > thread:
                    list_wavelength.append(i)
                    #print("j = ", j)
                    list_intensity.append((ref[j] + (ref[j + 1] - ref[j]) * (i - SD_lambda_Raw[j]) / (SD_lambda_Raw[j + 1] - SD_lambda_Raw[j])))
                    last = j

        self.reference = (c_float*len(list_intensity))()
        for x in range(len(list_wavelength)):
            self.reference[x] = list_intensity[x]
            #print("ref  ", list_wavelength[x] , self.reference[x])
                              
        self.GetReference = True    

    def action(self):
        self.thread = Thread(target=self.runData,args=())
        self.thread.setDaemon(True)
        self.thread.start()

    def rs485(self,strInput):
        while 1:
            #strInput = input('enter some words:')  
            self.ser.write(strInput)
        self.ser.flush()

    def calibration(self):
        #self.thread.stop()
        self.button_start.configure(bg = 'gainsboro')
        self.button_autoI.configure(bg = 'gainsboro')
        self.runG = 1

    def runData(self):
        while 1:     
            self.Getdata()
        #RS485    
        self.ser.flush()   
    
    # button callback
    def check_do_calibration(self):
        global Do_calibration
        MsgBox = messagebox.askquestion ('Do Calibration','Are you sure you want to do the calibration?',icon = 'warning')
        if MsgBox == 'yes':
            Do_calibration = True
            self.button_calibration.pack_forget()
            self.show_Calibration = False
            #self.window.destroy()
            return()
        else:
            messagebox.showinfo('Return','You will now return to the application screen')

    def print(self,LambdaArray,IntensityArray,index,display_lambda,unit):
        global Decimal_number

        if Decimal_number == 2 :
            #self.Lambda.set(str('{:}'.format(LambdaArray[index])) + " nm")
            self.Lambda.set(str('{:}'.format(display_lambda)) + " nm")
            self.Intensity.set(str('{:.2f}'.format(IntensityArray[index])) + " "  + unit)
            buffer_string = "Lambda = ".encode()+ str('{:}'.format(LambdaArray[index])).encode() + unit.encode() + " = ".encode() + str('{:.2f}'.format(IntensityArray[index])).encode() + "\t".encode()
            #self.ser.write(buffer_string)
        elif Decimal_number == 3 :
            #self.Lambda.set(str('{:}'.format(LambdaArray[index])) + " nm")
            self.Lambda.set(str('{:}'.format(display_lambda) + " nm"))
            self.Intensity.set(str('{:.3f}'.format(IntensityArray[index])) + " " + unit)
            #print("lambda_1 = ",lambda_1)
            # print(index)
            # for x in range(frame_size.value):
            #         print(str('{:}'.format(LambdaArray[x])),IntensityArray[x])
            #print(str('{:}'.format(LambdaArray[index])) ,str('{:.4f}'.format(IntensityArray[index])))
            buffer_string = "Lambda = ".encode()+ str('{:}'.format(LambdaArray[index])).encode() + unit.encode() + " = ".encode() + str('{:.3f}'.format(IntensityArray[index])).encode() + "\t".encode()
            #self.ser.write("Lambda = ".encode()+ str('{:}'.format(LambdaArray[index])).encode() + unit.encode() + " = ".encode() + str('{:.3f}'.format(IntensityArray[index])).encode() + "\t")
        elif Decimal_number == 4 :
            #self.Lambda.set(str('{:}'.format(LambdaArray[index])) + " nm")
            self.Lambda.set(str('{:}'.format(display_lambda)) + " nm")
            self.Intensity.set(str('{:.4f}'.format(IntensityArray[index])) + " "  + unit)
            buffer_string = "Lambda = ".encode()+ str('{:}'.format(LambdaArray[index])).encode() + unit.encode() + " = ".encode() + str('{:.4f}'.format(IntensityArray[index])).encode() + "\t".encode()
            #self.ser.write("Lambda = ".encode()+ str('{:}'.format(LambdaArray[index])).encode() + unit.encode() + " = ".encode() + str('{:.4f}'.format(IntensityArray[index])).encode() + "\t")
        else :
            #self.Lambda.set(str('{:}'.format(LambdaArray[index])) + " nm")
            self.Lambda.set(str('{:}'.format(display_lambda)) + " nm")
            self.Intensity.set(str('{:.2f}'.format(IntensityArray[index])) + " "  + unit)
            buffer_string = "Lambda = ".encode()+ str('{:}'.format(LambdaArray[index])).encode() + unit.encode() + " = ".encode() + str('{:.2f}'.format(IntensityArray[index])).encode() + "\t".encode()
            #self.ser.write("Lambda = ".encode()+ str('{:}'.format(LambdaArray[index])).encode() + unit.encode() + " = ".encode() + str('{:.2f}'.format(IntensityArray[index])).encode() + "\t")
        self.ser.write(buffer_string)

    def Display_Lamp_time(self,lampTime):
        #print(type(lampTime),lampTime)
        #lampTime = 4000
        if lampTime < 60 :
            self.Lamp_time.set(str('{:}'.format(lampTime) + " s"))
        elif lampTime >= 60 and lampTime < 3600:
            self.Lamp_time.set(str('{:d}'.format(int(lampTime/60)) + " min  " + '{:}'.format(lampTime%60) + " s"))
        elif lampTime >= 3600:
            hr = int(lampTime/3600)
            min = int((lampTime%3600)/60)
            sec = (lampTime%3600)%60
            #self.Lamp_time.set(str('{:d}'.format(int(lampTime/3600)) + " hr  " + str('{:d}'.format(int((lampTime%3600)/60))) + " min  " + '{:}'.format((lampTime%3600)/60)%60 + " s"))
            self.Lamp_time.set(str('{:d}'.format(hr) + " hr  " + str('{:d}'.format(min) + " min  " + '{:}'.format(sec) + " s")))
    
    def save_setup_ini(self):
        global AesKey #密鑰
        global AesIv #密鑰向量
        self.encrypt_file(self.FileName)

    def save(self):
        global MeasureType
        global SerialNumber
        global Usb_path
        global passwd
        global k
        global IntegrationTime
        global Average
        global Serial_mode
        global lambda_1
        global lambda_1_display
        global lambda_2
        global lambda_3
        global lambda_4
        global lambda_5
        global select_unit
        global Spectrum_unit
        global Absorbance_unit
        global Transmittance_unit
        global Reflection_unit
        global ppm_unit
        global Do_calibration
        global Lamp_reset
        global Lamp_total_time
        global Decimal_number

        i = 0
        with open(os.path.join(os.path.dirname(__file__), self.FileName), 'w') as f:  
            f.write('########################################\n')
            f.write('##########       setup        ##########\n')
            f.write('########################################\n')
            f.write('\n')
            f.write('#Lamp reset,0:Don\'t reset,1:Do reset\n')
            f.write('Lamp_reset=' + str(Lamp_reset))
            f.write('\n')
            f.write('Lamp_total_time=' + str(Lamp_total_time + self.diff_time))
            f.write('\n')
            f.close()
        os.chmod(os.path.join(os.path.dirname(__file__), self.FileName), 0o777)
        #os.close(f)
        #self.save_setup_ini()

    def run(self):
        self.window.mainloop()
   
    def reset(self):
        global hand
        global frame_size
        global SD_lambda_Raw
        global SN, MN
        errorcode = dll.DLI_SpectrometerGetDeviceAmount(VID, PID, pointer(num))
        if(num.value == 0 or errorcode != 0):
            messagebox.showinfo("Device not found", "Please plug in the USB and wait for 5 s")
            return()

        errorcode = dll.UAI_SpectrometerOpen(c_int(0),pointer(hand), c_int(0), c_int(0))
        if(num.value == 0 or errorcode != 0):
            messagebox.showinfo("Device not found", "Please plug in the USB and wait for 5 s")
            return()
        SN = (c_char * 16)()
        MN = (c_char * 16)()
        errorcode = dll.UAI_SpectrometerGetSerialNumber(hand, pointer(SN))
        if(SN[1] == '/xff'):
            messagebox.showinfo("Conneted time out", "Please reconnect again!")
            return()
        errorcode = dll.UAI_SpectrometerGetModelName(hand, pointer(MN))
        frame_size = (c_short)()
        errorcode = dll.UAI_SpectromoduleGetFrameSize(hand, pointer(frame_size))
        if(frame_size.value == 0):
            messagebox.showinfo("Conneted time out", "Please reconnect again!")
            return()
        SD_lambda_Raw = (c_float*frame_size.value)()
        errorcode = dll.UAI_SpectrometerWavelengthAcquire(hand, pointer(SD_lambda_Raw))
        

if __name__ == "__main__":
    root = tk.Tk()
    root.wm_geometry("800x400")
    #root.overrideredirect(1)    #toolbar 隱藏
    #tkinter窗口的全屏屬性 
    root.attributes('-fullscreen', True)
    # screen = os.popen("xrandr | grep current")
    # cur = screen.read().split(',')[1].split(' ')
    # root.geometry(cur[2]+cur[3]+cur[4])
    MainWindow(root).pack(fill="both", expand=True)
    root.mainloop()