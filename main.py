# -*- coding: utf-8 -*-
"""
Created on Wed May 27 08:05:23 2020

@author: kanbei
"""

import world_gen as w
import tkinter as tk
from PIL import ImageTk, Image  


class wndw():
    def __init__(self):
        self.root = tk.Tk()  
        self.root.geometry("1280x800")
        self.f1 = tk.Frame(self.root,bg='#000000')
        self.f1.place(x=0,y=0,width = 1024, height = 1024)
        self.canvas = tk.Canvas(self.f1, width = 1024, height = 1024)  
        self.canvas.pack()
        self.img = ImageTk.PhotoImage(Image.open("test.png"))  
        self.imgArea = self.canvas.create_image(0, 0, anchor= 'nw', image=self.img) 

        self.f2 = tk.Frame(self.root,bg='#FFFFFF')
        self.f2.place(x=1024,y=0,width = 266, height = 1024)

        tk.Label(self.f2,text='Sea level 0-100').grid(row=0)
        self.e1 = tk.Entry(self.f2)
        self.e1.grid(row=0,column = 1)
        self.e1.insert(10,'1')
        
        tk.Label(self.f2,text='World Seed').grid(row=1)
        self.e2 = tk.Entry(self.f2)
        self.e2.grid(row=1,column = 1)
        self.e2.insert(10,'34')

        self.gen = tk.Button(self.f2, text="Generate", command=self.callback)
        self.gen.grid(row=2,column=1,pady=4)
        
        tk.Label(self.f2,text='Enter filename').grid(row=3)
        self.e3 = tk.Entry(self.f2)
        self.e3.grid(row=3,column = 1)
        
        self.sv = tk.Button(self.f2, text="Save", command=self.sv)
        self.sv.grid(row=3,column=2)
        
        self.qu = tk.Button(self.f2, text="Quit", command=self.qu)
        self.qu.grid(row=4,column=1,pady=4)

        self.root.mainloop() 
        
    def callback(self):
        if self.e1.get() == '':
            lvl = 1
        else:
            lvl = int(self.e1.get())/100
            
        if self.e2.get() == '':
            seed = 0
        else:
            seed = int(self.e2.get())
            
        self.world = w.world(z=lvl, b = seed)
        self.i = self.world.retBgMap()
        self.img = ImageTk.PhotoImage(self.i)
        self.canvas.itemconfig(self.imgArea, image=self.img) 
        
    def qu(self):
        self.root.destroy()
        
    def sv(self):
        strng = self.e3.get()
        if strng == '':
            strng = 'save_alt'
        elif strng == 'test':
            strng = 'test_alt'
        if hasattr(self ,'i'):
            self.i.save(strng + '.png')


app = wndw()
