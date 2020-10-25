from tkinter import *

master = Tk(className='Weather')

from PIL import Image, ImageTk

root = Tk()
im = Image.open('combined.bmp',formats=['BMP'])
im.load()
img = ImageTk.PhotoImage(im)
panel = Canvas(master=root, width = 880, height = 528)
panel.create_image((0, 0), image = bmp, state='normal', anchor=NW)
panel.pack()

root.mainloop()

'''
window = tk.Tk(className='Weather')
import datetime
w = Canvas(master, width=200, height=100)
w.pack()

time = tk.Label(text = datetime.datetime.now())
time.place(x = 10, y = 450)

import socket
hostname = socket.gethostname()
ipAddress = socket.gethostbyname(hostname)

addr = tk.Label(text='{0:s}'.format(ipAddress))
addr.place(x = 700, y =450)

from model import NewsAPIReader

napir = NewsAPIReader.NewsAPIReader('ae277ae39eb84b0eb01efeae417fe724')
headlines = napir.getRandomHeadlines(5)
hlString = ''
for hl in headlines:
    hlString += '{0:s}\n'.format(hl)

lblHeadlines = tk.Label(text = hlString, anchor='w')
lblHeadlines.place(x = 10, y = 10)

print(hlString)

window.mainloop()
'''