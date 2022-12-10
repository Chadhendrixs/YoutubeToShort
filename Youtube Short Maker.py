#!/usr/bin/python3
from __future__ import unicode_literals
import tkinter as tk
import tkinter.ttk as ttk
import os
import subprocess
from youtube_dl import *

class PygubuApp:
    def __init__(self, master=None):
        # build ui
        labelframe1 = ttk.Labelframe(master)
        labelframe1.configure(
            height=200,
            text='Youtube Short Maker',
            width=200)
        label1 = ttk.Label(labelframe1)
        label1.configure(
            compound="top",
            font="TkTextFont",
            justify="left",
            text='Path or URL: ')
        label1.grid(column=0, row=0, sticky="w")
        self.path = ttk.Entry(labelframe1)
        self.path.configure(takefocus=False, validate="none")
        self.path.grid(column=1, padx=5, pady=2, row=0, sticky="e")
        label2 = ttk.Label(labelframe1)
        label2.configure(cursor="arrow", relief="flat", text='Start time: ')
        label2.grid(column=0, row=2, sticky="w")
        self.startTime = ttk.Entry(labelframe1)
        _text_ = '00:00:00'
        self.startTime.delete("0", "end")
        self.startTime.insert("0", _text_)
        self.startTime.grid(column=1, padx=5, pady=2, row=2, sticky="e")
        label3 = ttk.Label(labelframe1)
        label3.configure(text='End time: ')
        label3.grid(column=0, row=3, sticky="w")
        self.endTime = ttk.Entry(labelframe1)
        _text_ = '00:00:00'
        self.endTime.delete("0", "end")
        self.endTime.insert("0", _text_)
        self.endTime.grid(column=1, padx=5, pady=2, row=3, sticky="e")
        label4 = ttk.Label(labelframe1)
        label4.configure(justify="left", text='Scale Input to 16:9? ')
        label4.grid(column=0, columnspan=2, row=4, sticky="w")
        self.scaleFlag = ttk.Checkbutton(labelframe1)
        self.scaleFlag.configure(
            cursor="arrow",
            offvalue="False",
            onvalue="True")
        self.scaleFlag.grid(column=1, padx=5, pady=5, row=4)
        label5 = ttk.Label(labelframe1)
        label5.configure(
            cursor="arrow",
            justify="left",
            text='Justification: ')
        label5.grid(column=0, row=5)
        self.justification = tk.StringVar(value='center')
        __values = ['left', 'center', 'right']
        self.justificationMenu = tk.OptionMenu(
            labelframe1, self.justification, *__values, command=None)
        self.justificationMenu.grid(column=1, padx=5, row=5, sticky="e")
        self.generateId = ttk.Button(labelframe1)
        self.generateId.configure(
            compound="top",
            takefocus=True,
            text='Generate!')
        self.generateId.grid(column=1, padx=10, pady=10, row=8, sticky="e")
        self.generateId.configure(command=self.generate)
        labelframe1.pack(side="top")

        # Main widget
        self.mainwindow = labelframe1

    def run(self):
        self.mainwindow.mainloop()

    def generate(self):
        path = self.path.get()
        startTime = self.startTime.get()
        endTime = self.endTime.get()
        if str(self.scaleFlag.state()) == "('selected',)":
            scaleFlag = True
        else:
            scaleFlag = False
        justification = self.justification.get()
        inputs = [path, startTime, endTime, scaleFlag, justification]
        PygubuApp.main(inputs)

    def downloadVid(url):
        ydl_opts = {
            'format' : 'mp4'
        }

        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_id = info_dict.get('id', None)
            video_title = info_dict.get('title', None)

        return video_title + "-" + video_id + ".mp4"

    def create(path, startTime, endTime, scaleFlag, justification):
        cropPos = {
            'left' : ':0:0',
            'center' : '',
            'right' : ':(iw/2):0'
        }
        if not scaleFlag:
            scale = "ih:iw"

        else:
            scale = "3414:1920"
        ffmpegCommands = [
            '''ffmpeg -y -i "''' + path + '''" -ss ''' + startTime + ''' -to ''' + endTime + ''' -c:v libx264 -crf 30 cut.mp4''',
            '''ffmpeg -y -i cut.mp4 -vf scale=''' + scale + ''' -preset slow -crf 18 scale.mp4''',
            """ffmpeg -y -i scale.mp4 -filter:v "crop=(iw/3.25):ih""" + cropPos[justification.lower()] + """" -c:a copy output.mp4""",
        ]
        for command in ffmpegCommands:
            subprocess.call(command)
        os.remove("cut.mp4")
        os.remove("scale.mp4")

    def main(inputs):
        if "https" in inputs[0].split(':'):
            print("Downloading video...")
            path = PygubuApp.downloadVid(inputs[0].replace(" ", ""))
            print("Downloaded!")
        else:
            path = inputs[0]
        print("Working...")
        PygubuApp.create(path, inputs[1], inputs[2], inputs[3], inputs[4])
        


if __name__ == "__main__":
    root = tk.Tk()
    app = PygubuApp(root)
    app.run()