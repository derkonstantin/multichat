#!/usr/bin/env python3

import twich_irc_async_io
import config_parser
import goodgame
from multiprocessing import Pipe
import tkinter as tk
import chat_gui_tk


def main():
    parent_conn, child_conn = Pipe()
    config = config_parser.get_config('./multi_chat.config')

    twitch = twich_irc_async_io.IRC_twicth(config,child_conn)
    twitch.start()

    GG = goodgame.GoodGame_websock(config, child_conn)
    GG.start()

    root = tk.Tk()
    chat_gui_tk.Chat_list(root,parent_conn).pack(fill="both", expand=True)
    root.mainloop()
    # while True:
    #     message = parent_conn.recv()
    #     print(message)





if __name__ == '__main__':
    main()
    #test_tk()