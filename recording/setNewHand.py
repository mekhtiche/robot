import json
from Tkinter import *

from servo.Adafruit_PWM_Servo_Driver import PWM

DEBUG = 1
Lpwm = PWM(0x41, 4) # , debug = True  # for debuging the code and see what it send from the bus
Rpwm = PWM(0x40, 4) # 42
Lpwm.setPWMFreq(30)





def __init__(master):
    master.geometry('505x240')
    master.title('Setup the servo motors of the hands')

    with open('/home/odroid/catkin_ws/src/robot/recording/Poppy_torso.json', 'r') as f:
        config = json.load(f)

    Right_config = config['Right_Setting']
    Left_config = config['Left_Setting']



    def getValue(event):
        #print var1.get()
        if var1.get()==1:
            Rpwm.setPWM(var2.get(), 0, bar.get())
        elif var1.get()==2:
            Lpwm.setPWM(var2.get(), 0, bar.get())

    bar = Scale(master, label="Set the value", from_=0, to=400, orient=HORIZONTAL, length=400,
                         command=getValue)
    bar.set(110)
    bar.grid(row=1, column=0, columnspan=6)

    def setMin():
        if var1.get()==1:
            Right_config[str(var2.get())][0] = bar.get()
        elif var1.get()==2:
            Left_config[str(var2.get())][0] = bar.get()
        with open("/home/odroid/catkin_ws/src/robot/recording/Poppy_torso.json", "w") as h:
            json.dump(config, h)
        print "value setted"

    def setMax():
        if var1.get() == 1:
            Right_config[str(var2.get())][1] = bar.get()
        elif var1.get() == 2:
            Left_config[str(var2.get())][1] = bar.get()
        with open("/home/odroid/catkin_ws/src/robot/recording/Poppy_torso.json", "w") as h:
            json.dump(config, h)
        print "value setted"

    minBut = Button(master, text="Set MIN", command=setMin)
    minBut.grid(row=2, column=2)
    maxBut = Button(master, text="Set MAX", command=setMax)
    maxBut.grid(row=2, column=3)

    var1 = IntVar()
    right = Radiobutton(master, text="Right", variable=var1, value=1)
    right.grid(row=3, column=2)
    left = Radiobutton(master, text="Left", variable=var1, value=2)
    left.grid(row=3, column=3)

    var2 = IntVar()
    wrist_v = Radiobutton(master, text="Wrist_ver", variable=var2, value=1)
    wrist_v.grid(row=4, column=1)
    wrist_h = Radiobutton(master, text="Wrist_hor", variable=var2, value=2)
    wrist_h.grid(row=4, column=3)
    thump_j = Radiobutton(master, text="thump Joint", variable=var2, value=3)
    thump_j.grid(row=5, column=0)
    thump = Radiobutton(master, text="Thump", variable=var2, value=4)
    thump.grid(row=6, column=0)
    opn = Radiobutton(master, text="Open", variable=var2, value=5)
    opn.grid(row=7, column=2)
    index = Radiobutton(master, text="Index", variable=var2, value=6)
    index.grid(row=8, column=0)
    major = Radiobutton(master, text="Major", variable=var2, value=7)
    major.grid(row=8, column=1)
    ring = Radiobutton(master, text="Ring Finger", variable=var2, value=8)
    ring.grid(row=8, column=3)
    auri = Radiobutton(master, text="Auricular", variable=var2, value=9)
    auri.grid(row=8, column=4)


    def close():
        for servo in range(1, 10):
            print "releasing the servo N: " + str(servo)
            Rpwm.setPWM(servo, 0, 0)
            Lpwm.setPWM(servo, 0, 0)
        master.destroy()

    closeBut = Button(master, text="Close", command=close)
    closeBut.grid(row=10, column=6)



































