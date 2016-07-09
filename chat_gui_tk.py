#!/usr/bin/env python3
import tkinter as tk
import time
from multiprocessing import Pipe



class Chat_list(tk.Frame):
    message_list = []
    # def __init__(self, parent, pipe):
    #     tk.Frame.__init__(self, parent)
    #     self.pipe = pipe
    #     self.scrollbar = tk.Scrollbar(parent)
    #     self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    #     self.lb = tk.Listbox(self, yscrollcommand=self.scrollbar.set)
    #     self.lb.pack(fill="both", expand=True)
    #
    #     #self.lb.insert("end", "item 1","the current time", "item 3")
    #     self.after(1000, self._update_list)
    def __init__(self, root, pipe):

        tk.Frame.__init__(self, root)
        self.canvas = tk.Canvas(root, borderwidth=0, background="#ffffff")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.img = {}
        self.img[':GG:'] = tk.PhotoImage(file="./img/goodgame.png",width=32, height=32)
        self.img[':TWITCH:'] = tk.PhotoImage(file="./img/twitch.png", width=32, height=32)



        self.row = 0
        self.pipe = pipe

        self.after(1000, self._check_msg)


    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def parse_msg(self, msg):
        print (msg)
        msg = msg.split()
        chat = msg[0].strip()
        sender = msg[1].strip()
        msg = ' '.join(msg[2:])
        return (chat, sender, msg)


    def _update_chat(self):
        i = 0
        while i < len(self.message_list):

            chat, sender, msg = self.parse_msg(self.message_list[i])
            tk.Label(self.frame, image=self.img[chat], width=32, height=32, borderwidth="1", relief="solid").grid(row=self.row, column=0)
            sender_text = tk.Text(self.frame,  height=1, width = len(sender))
            sender_text.insert(1.0, sender)
            sender_text.config(state=tk.DISABLED)
            sender_text.grid(row=self.row, column=1)
            tk.Label(self.frame, text= msg).grid(row=self.row, column=2,sticky=tk.W)
            i = i + 1
            self.row = self.row + 1

        self.canvas.yview_scroll(1, 'units')
        self.after(1000, self._check_msg)

    # def _update_listbox(self):
    #
    #     #self.lb.delete(0, tk.END)
    #     i = 0
    #     while  i < len(self.message_list):
    #         self.lb.insert(tk.END, self.message_list[i])
    #         i = i+1
    #     self.lb.pack(fill="both", expand=True)
    #     self.after(1000, self._update_list)

    def _check_msg(self):
        self.message_list.clear()
        if self.pipe is not None:
            is_data = self.pipe.poll()
            if is_data:
                msg = self.pipe.recv()
                self.message_list.append(msg)
        else:
            self.message_list.append(':GG: '+ 'SENDER :' + str(time.time()))
        self.after(10, self._update_chat)


if __name__ == "__main__":
    root = tk.Tk()
    Chat_list(root,None).pack(fill="both", expand=True)
    root.mainloop()