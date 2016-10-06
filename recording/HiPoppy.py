#!/usr/bin/python
# -*- coding: UTF-8 -*-  # this is to add arabic coding to python
import json
import time
import tkFileDialog
import tkMessageBox
from Tkinter import *
from timeit import default_timer

import finger
from pypot.robot import config
import pypot.robot


class REC():

    # SELECT OR DESELECT THE CHILD OF THE CHECKBUTTON CLICKED
    def selUsel(self, etat, list):
        for i in list:
            if etat == 1:
                self.chkb['Var_%02d' % i].select()
            else:
                self.chkb['Var_%02d' % i].deselect()
        i = 0
        for var, value in sorted(self.cb.items()):
            self.stat[i] = value.get()
            i += 1

    # CHECK THE CHECKBUTTON ON CLICK
    def check(self, index, stt):
        if index == 0:
            self.selUsel(stt, range(0, 21, 1))
        elif index == 1:
            self.selUsel(stt, [2, 3, 4])
        elif index == 5:
            self.selUsel(stt, [6, 7])
        elif index == 8:
            self.selUsel(stt, range(9, 21, 1))
        elif index == 9:
            self.selUsel(stt, range(10, 15, 1))
        elif index == 15:
            self.selUsel(stt, range(16, 21, 1))




    def child(self):
        self.stat
        i = 0
        chng = []
        for var, value in sorted(self.cb.items()):
            if self.stat[i] != value.get():
                chng = i
                stt = value.get()
            self.stat[i] = value.get()
            i += 1
        self.check(chng, stt)

        return self.stat

    def _motor_extractor(self, alias, name, space):
        l = []
        self.ndx += 1
        self.cb['Var_%02d' % self.ndx] = IntVar()
        self.chkb['Var_%02d' % self.ndx] = Checkbutton(self.master, text=space + name, variable=self.cb['Var_%02d' % self.ndx], command=self.child)
        self.chkb['Var_%02d' % self.ndx].pack(anchor=NW)
        space = '        ' + space
        if name not in alias:
            return [name]
        for key in alias[name]:
            if key in alias:
                l += self._motor_extractor(alias, key, space)
            else:
                l += [key]
                self.ndx += 1
                self.cb['Var_%02d' % self.ndx] = IntVar()
                self.chkb['Var_%02d' % self.ndx] = Checkbutton(self.master, text=space + key, variable=self.cb['Var_%02d' % self.ndx],
                                                     command=self.child)
                self.chkb['Var_%02d' % self.ndx].pack(anchor=NW)

        return l


    def cancelCall(self):

        self.master.destroy()


    def nextCall(self):
        selected = ''
        i = 0
        mtrs = []
        nonActive = []
        for var, value in sorted(self.cb.items()):
            if value.get():
                selected += self.list[i]
                if self.actors[i] != '':
                    mtrs.append(self.actors[i])
            else:
                if self.actors[i] != '':
                    nonActive.append(self.actors[i])
            i += 1
#        print mtrs
#        print nonActive
        if selected == '':
          #  tkMessageBox.ERROR
            tkMessageBox.showerror(title= 'Warning', message='You need to select at least ONE Actor!')
            return None
        if tkMessageBox.askyesno(title='Warning',
                              message='Warning: You selected folowing actors: ' + str(selected) + 'the rest of robot will be in mode "freeze" do you want to continue?'):


            rec_fram = Toplevel()
            rec_fram.grab_set()
            rec_fram.transient(self.master)
            # self.master.wait_window(RECD)
            myRec = RECORDING_1(rec_fram, mtrs)

    def method(self):
        if self.Var.get() == 1:
            for key, value in self.chkb.items():
                value.config(state = NORMAL)

            self.Next.config(state=NORMAL)
            self.loadFile.config(state=DISABLED)
        else:

            for key, value in self.chkb.items():
                value.config(state=DISABLED)

            self.Next.config(state=DISABLED)
            self.loadFile.config(state=NORMAL)

    def editSign(self):
        recFile = tkFileDialog.askopenfilename()
        if not recFile:
            return None
        print 'Openning the file: ' + recFile
        with open(recFile, "r") as sign:
            self.movement = json.load(sign)
        mtrs = self.movement['actors_NAME']
        #print mtrs
        edit_fram = Toplevel()
        edit_fram.grab_set()
        edit_fram.transient(self.master)
        handsSet = finger.__init__(edit_fram, self.movement)

    def __init__(self, master):
        self.master = master
        self.master.geometry('480x720')
        #self.master.title('RECORD SIGN')
        self.master.title('Hi Poppy ;)')
        self.label1 = Label(self.master, text='Hi Poppy', font="Helvetica 48 bold italic").pack(anchor=N)
        self.label2 = Label(self.master, justify=LEFT, text='To record new sing choose "Record new Sign" than select the actors, \n'
                                                            'or choose "Edit old Sign" and select the file to edit it.').pack(anchor=NW)

        self.Var = IntVar(master, value=1)
        self.option1 = Radiobutton(self.master, text="Record new Sign", variable = self.Var, value = 1, command=self.method)
        self.option1.pack(anchor=NW)
        self.option1.select()
        self.cb = dict()
        self.chkb = dict()
        with open('/home/odroid/catkin_ws/src/robot/recording/Poppy_torso.json', 'r') as f:
            config = json.load(f)
        alias = config['motorgroups']
        self.ndx = 0
        self.cb['Var_%02d' % self.ndx] = IntVar()
        self.chkb['Var_%02d' % self.ndx] = Checkbutton(master, text="_Poppy", variable=self.cb['Var_%02d' % self.ndx], command=self.child)
        self.chkb['Var_%02d' % self.ndx].pack(anchor=NW)
        space = "      |____ "
        self.list = ['', '', ' abs_z, ', 'bust_y, ', 'bust_x, ', '', 'head_z, ', 'head_y, ', '', '', 'l_shoulder_y, ', 'l_shoulder_x, ', 'l_arm_z, ', 'l_elbow_y, ', 'l_forearm_z, ',
                     '', 'r_shoulder_y, ', 'r_shoulder_x, ', 'r_arm_z, ', 'r_elbow_y. ', 'r_forearm_z']
        #self.actors = [0, 0, 33, 34, 35, 0, 36, 37, 0, 0, 41, 42, 43, 44, 45, 0, 51, 52, 53, 54]
        self.actors = ['', '', 'abs_z', 'bust_y', 'bust_x', '', 'head_z', 'head_y', '', '', 'l_shoulder_y', 'l_shoulder_x', 'l_arm_z', 'l_elbow_y', 'l_forearm_z',
                     '', 'r_shoulder_y', 'r_shoulder_x', 'r_arm_z', 'r_elbow_y', 'r_forearm_z']
        for c_name, c_params in config['controllers'].items():
            motor_names = sum([self._motor_extractor(alias, name, space)
                               for name in c_params['attached_motors']], [])
        self.stat = [0] * len(self.cb)



        self.Next = Button(master, text="Next", width=10, command=self.nextCall)
        self.Next.pack(anchor=N)

        self.option2 = Radiobutton(self.master, text="Edit old Sign", variable=self.Var, value = 2, command=self.method)
        self.option2.pack(anchor=NW)
        self.option2.deselect()

        self.loadFile = Button(self.master, text="Load File", width=10, command=self.editSign)
        self.loadFile.pack(anchor=N)
        self.loadFile.config(state=DISABLED)

        self.Cancel = Button(master, text="Cancel", width=10, command=self.cancelCall)
        self.Cancel.pack(anchor=W)




class RECORDING_1():
    def timeToStop(self):
        self.stopTime.config(state = NORMAL) if self.STP.get() == 1 else self.stopTime.config(state = DISABLED)

    def STARTREC(self):
        self.STOP = 0
        #if self.STP.get() == 1:
        self.sleeping = 1 / float(self.Frq.get())
        for m in self.robot.Active_motors:
            m.compliant = True
        IDs = [m.id for m in self.robot.motors]
        self.pos = {}
        i = 0
        for sec in range(int(self.StrTm.get())):
            self.info.config(text=str(sec))
            time.sleep(1)
        print 'Starting record'

        start = default_timer()
        while self.STOP == 0:
            #print default_timer()-start

            self.pos[str(i)] = {'Robot': [m.present_position for m in self.robot.Active_motors], 'Right_hand': [212, 165, 213, 264, 138, 288, 288, 280, 238], 'Left_hand': [178, 214, 283, 253, 123, 103, 99, 102, 136]}
            i+=1

            time.sleep(self.sleeping)
            if self.STP.get() == 1 & (default_timer()-start > float(self.StpTm.get())):
                self.STOP = 1
                print 'Stop Recording'
        self.frames = i

        self.movement = {'actors_ID':IDs,
                       'actors_NAME':self.motorsName,
                       'freq': self.Frq.get(),
                       'frame_number':self.frames,
                       'position':
                           self.pos
                       }
        self.save.config(state=NORMAL)
        self.play.config(state=NORMAL)
        self.handset.config(state=NORMAL)

        self.varInfo.set('Done Recording, now you can play the recorded movement\n'
                         'if it is OK you can save it or go to hand setting\n\n'
                         '<------ Click here to play the recording\n\n'
                         '<------ Click here to save the recording\n\n'
                         '<------ Click here to go to Hand Setting')
        self.info.config(justify=LEFT)
#        with open("sign2.json", "w") as record:
#            json.dump({'actors_ID':IDs,
#                       'actors_NAME':self.motorsName,
#                       'freq': 10,
#                       'frame_number':self.frames,
#                       'position':
#                           self.pos
#                       }, record)

    def STOPREC(self):
        self.STOP = 1

    def PLAY(self):
        #print('Starting the Robot')
        #self.robot = pypot.robot.from_config(pypot.robot.config.robot_config, True, True, False, activemotors=self.motorsName)
        #print('Robot started')
        for m in self.robot.motors:
            m.compliant = False
        #for m in self.robot.Dead_motors:
        #    m.goal_position = 0
        print 'Playing'
        for frame in range(self.frames):
            id=0
            for m in self.robot.Active_motors:
                m.goal_position = self.movement['position'][str(frame)]['Robot'][id]
                id += 1
            time.sleep(self.sleeping)
        #print 'Closing the robot'
        for m in self.robot.Active_motors:
            m.compliant = True
        #self.robot.close()
        print 'Done'

    def SAVE(self):
        print 'saving movement without hand motion '
        saveFile = tkFileDialog.asksaveasfilename()
        if not saveFile:
            return None
        with open(saveFile, "w") as record:
            json.dump(self.movement, record)
        print 'saved'

    def CLOSE(self):
#        self.robot.close()
        print 'closing the robot'
        for m in self.robot.motors:
            m.compliant = True
        self.robot.close()
        print 'Robot Closed'
        self.master.destroy()

    def Handset(self):
        #print self.movement
        #for m in self.robot.motors:
         #   m.compliant = True
        #self.robot.close()
        edit_fram = Toplevel()
        edit_fram.grab_set()
        edit_fram.transient(self.master)
        handsSet = finger.__init__(edit_fram, self.movement, self.robot)
        #lefthand = finger.__init__(self.movement)



    def __init__(self, master, motors):
        self.motorsName = motors
        #print self.motorsName
        self.master = master
        self.master.geometry('540x220')
        self.master.title('AUTO RECORDING')
        self.freqLb = Label(master, text = "freq").grid(row=0, column=0)
        self.Frq = StringVar(self.master, value='50')
        self.freq = Entry(master, width = 10, textvariable = self.Frq).grid(row=0, column=1)
        self.strTm = Label(master, text="Time to start").grid(row=1, column=1)
        self.StrTm = StringVar(self.master, value='2')
        self.startTime = Entry(master, width=10, textvariable=self.StrTm).grid(row=1, column=2, sticky=W)
        self.stpTm = Label(master, text="Time to stop").grid(row=2, column=1)
        self.STP = IntVar(self.master, value=1)
        self.stop = Checkbutton(master, variable = self.STP, command = self.timeToStop).grid(row=2, column=0)
        self.StpTm = StringVar(self.master, value='10')
        self.stopTime = Entry(self.master, width=10, textvariable=self.StpTm)
        self.stopTime.grid(row=2, column=2, sticky=W)
        #self.stopTime.config(state=DISABLED)
        self.startRec = Button(self.master, text = 'Start Recording', width = 10, command = self.STARTREC)
        self.startRec.grid(row=5, column=1, sticky=NW)
        #self.stopRec = Button(self.master, text='Stop Recording', width=10, command=self.STOPREC)
        #self.stopRec.grid(row=5, column=2)
        #self.stopRec.config(state=DISABLED)
        self.play = Button(self.master, text='Play', width=10, command=self.PLAY)
        self.play.grid(row=6, column=1, sticky=NW)
        self.play.config(state=DISABLED)
        self.save = Button(self.master, text='Save', width=10, command=self.SAVE)
        self.save.grid(row=7, column=1, sticky=NW)
        self.save.config(state=DISABLED)
#        self.edit = Button(self.master, text='Edit', width=6, command=self.EDIT)
#        self.edit.grid(row=5, column=5)
        self.varInfo = StringVar(self.master, value="<------ Click here to start recording \n\n\n\n"
                                                    "First you need to set the friquance of recording, \n"
                                                    "time to start and the recording time \n"
                                                    "than click on Start Recording Button to start the recording.")
        self.info = Label(self.master, justify=LEFT, width=50, height=8, textvariable = self.varInfo)
        self.info.grid(row=5, column=2, rowspan=4, sticky=W)
        self.close = Button(self.master, text='Close', width=6, command=self.CLOSE)
        self.close.grid(row=9, column=2, sticky=E)

        self.handset = Button(self.master, text='Hand set', width=10, command=self.Handset)
        self.handset.grid(row=8, column=1)
        self.handset.config(state=DISABLED)
        self.STOP = 0

        print('starting the ROBOT')
#        self.robot = config(config.robot_config, True, True, False,
#                                 activemotors=self.motorsName)


        self.robot = pypot.robot.from_config(pypot.robot.config.robot_config, True, True, False,
                                             activemotors=self.motorsName)

        IDs = [m.id for m in self.robot.motors]
        self.pos = {}
        i = 0

        for m in self.robot.Dead_motors:
            m.compliant = False
        for m in self.robot.Dead_motors:
            m.goal_position = 0
        print('Robot started')





def main():
    root = Tk()
    hi_poppy = REC(root)
    root.mainloop()



if __name__ == '__main__':
    main()
