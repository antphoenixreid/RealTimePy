import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import Tkinter as Tk

from audioSpec import *

status = True

if __name__ == "__main__":
  AV = Audio_Analysis()
  AV.continuousStart()

  root = Tk.Tk()
  fig = plt.Figure()
  fig.suptitle('Real Time Mic Frequency')

  canvas = FigureCanvasTkAgg(fig, master=root)
  canvas.show()
  canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

  toolbar = NavigationToolbar2TkAgg(canvas, root)
  toolbar.update()
  canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

  #label = Tk.Label(root, text="Real Time Frequency").grid(column=0, row=0)

  ax = fig.add_subplot(111)
  ax.axis([0, 2500, 40, 150])
  ax.set_xlabel('Frequency (Hz)')
  ax.set_ylabel('Amplitude (dB)')
  x, y = AV.realtimeFFT()
  #AV.counter += 1
  line, = ax.plot(x, y)

  def animate(i):
    x, y = AV.realtimeFFT()
    #AV.counter += 1
    line.set_xdata(x)
    line.set_ydata(y)

    return line,

  def _switchGraph():
    global status
    if status == True:
      status = False
    else:
      status = True

  button = Tk.Button(master=root, text='Switch Graph', command=_switchGraph)
  button.pack(side=Tk.BOTTOM)

  ani = animation.FuncAnimation(fig, animate, interval=10.0)
  Tk.mainloop()
  AV.close()
