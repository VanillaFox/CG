from tkinter import messagebox
import tkinter as tk
from math import cos, sin
import numpy as np
 
def drawfunc():
   conva.delete("all")
   zoom = float(spinb.get())
   w = window.winfo_width()
   h = conva.winfo_height()
   a = scale.get()
   conva.create_line(w//2, 0, w//2, h, width=2, arrow="first")
   conva.create_line(0, h//2, w, h//2, width=2, arrow="last")
   count = 25
   for i in np.arange(w//2 + 25 * zoom, w, 25 * zoom):
       conva.create_line(i, (h//2)-3, i, (h//2)+3, width=2)
       conva.create_line(w-i, (h//2)-3, w-i, (h//2)+3, width=2)
       if count%10==0:
           conva.create_text(i, (h//2)+15, text=str(count), font=("Helvectica", "7"))
           conva.create_text(w-i, (h//2)+15, text=str(-count), font=("Helvectica", "7"))
       count += 25
 
   count = 25
   for i in np.arange(h//2 + 25 * zoom, h, 25 * zoom):
       conva.create_line((w//2)-3, i, (w//2)+3, i, width=2)
       conva.create_line((w//2)-3, h-i, (w//2)+3, h-i, width=2)
       if count%10==0:
           conva.create_text((w//2)+15, i, text=str(-count), font=("Helvectica", "7"))
           conva.create_text((w//2)+15, h-i, text=str(count), font=("Helvectica", "7"))
       count += 25
 
  
   ax = cos(0)*cos(0)*a*zoom + w//2
   ay = cos(0)*sin(0)*a*zoom+h//2
   for i in np.arange(0.0, 3.15, 0.01):
       bx = cos(7*i)*cos(i)*a*zoom+w//2
       by = cos(7*i)*sin(i)*a*zoom+h//2
       conva.create_line(ax, ay, bx, by, width=2)
       ax, ay = bx, by
 
def redraw(event):
   drawfunc()
 
def zooming(event):
   cur = float(spinb.get())+0.1
   spinb.delete(0, "end")
   spinb.insert(0, cur)
   drawfunc()
 
def decrease(event):
   cur = float(spinb.get())-0.1
   spinb.delete(0, "end")
   spinb.insert(0, cur)
   drawfunc()
 
def help():
   return tk.messagebox.showinfo('Helper', 'Press LCM to zoom\nPress RLM to decrease\nUse the slider to adjust the parameter \'a\'')
 
if __name__=="__main__":
   window = tk.Tk()
   window.geometry("+550+150")
   window.title("p=a*cos(7phi)")
   window.columnconfigure(0, weight=2, minsize=10)
   window.columnconfigure(1, weight=1, minsize=350)
   window.rowconfigure(0, weight=2, minsize=550)
   window.rowconfigure([1, 2, 3], weight=1, minsize=10)
 
   conva = tk.Canvas(window, bg="pink")
   conva.grid(row=0, column=0, sticky="nsew", columnspan=2)
 
   frame = tk.Frame(window, relief="sunken", borderwidth=3)
   frame.grid(row=1, column=0, sticky="nsew", pady=5, columnspan=2)
 
   scale = tk.Scale(master=frame, orient="horizontal", resolution=1, from_=1, to=200)
   scale.grid(row=1, column=1, sticky="ew")
   scale.set(100)
 
   labelscale = tk.Label(master=frame, text="Parametr \’a\’")
   labelscale.grid(row=1, column=0, sticky="ew")
  
   labelEnt = tk.Label(master=frame, text="Zoom")
   labelEnt.grid(row=2, column=0, sticky="ew")
 
   var = tk.DoubleVar(value=1)
   spinb = tk.Spinbox(master=frame, textvariable=var, width=100, from_=0.1, to=5, increment=0.1, command=drawfunc)
   spinb.grid(row=2, column=1, sticky="ew")
 
   button = tk.Button(frame, text="Help", command=help)
   button.grid(row=3, column=0, columnspan=2)
 
   window.update()
   window.minsize(window.winfo_width(), window.winfo_height())
   drawfunc()
  
   window.bind("<Configure>", redraw)
   scale.bind("<ButtonRelease-1>", redraw)
   conva.bind("<Button-1>", zooming)
   conva.bind("<Button-3>", decrease)
 
   window.mainloop()