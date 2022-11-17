from tkinter import *
import tkinter as tk
from GUI import play_game


class Game(tk.Tk):
    depth = 5  # save user input
    algorithms = ['MiniMax without pruning', 'MiniMax with pruning']

    def __init__(self):  # create main page
        super().__init__()

        self.x = IntVar()
        self.config(background='#FEEBA0')  # main page background color
        self.geometry("440x500")  # size of the page
        self.resizable(False, False)  # set the page to fixed size
        self.title('Connect 4 game')  # page title

        self.frame = Frame(self)  # set a frame to hold input components
        self.entry = Entry(self.frame,  # make entry field to read input from user
                           font=('Arial', 25))
        self.enter_button = Button(self.frame,  # make Enter button to enter the input
                                   text="Enter",
                                   command=self.get_depth,
                                   font=("Arial", 20),
                                   bg='lightblue'
                                   )
        self.entry.pack(side=LEFT, expand=True)  # add the entry to the frame and fill the window
        self.enter_button.pack(side=RIGHT)  # put the button to the frame to the right of the entry
        self.frame.pack()  # add the frame to the window

        for index in range(len(self.algorithms)):  # create radio button for each algorithm to choose from them
            self.radio_button = Radiobutton(self,
                                            text=self.algorithms[index],
                                            variable=self.x,  # variable to hold the choose
                                            value=index,  # the value of each choose is its index
                                            padx=0,
                                            bg='#F5631A',
                                            width=50,
                                            indicatoron=0,
                                            font=('Arial', 25))
            self.radio_button.pack(anchor=W)  # add the radio buttons to window and set them to the west

        self.play = Button(self,  # add button to start playing the game
                           text='Play',
                           command=self.play,
                           font=("Comic Sans", 20),
                           )
        self.play.pack(pady=20)  # add the button to the window

    def get_depth(self):
        self.depth = int(self.entry.get())   # get the depth from the user

    def play(self):
        play_game(self.x.get(), self.depth)  # get the board and start the game


if __name__ == '__main__':

    game = Game()
    game.mainloop() # start the game
