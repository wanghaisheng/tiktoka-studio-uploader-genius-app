from tkinter import *
import webbrowser

def callback(url):
    webbrowser.open_new(url)

words = ["Made with", "❤", "by"]
colors = ["white", "red", "white"]

root = Tk()
for index, word in enumerate(words):
    Label(root, text = word, bg="black", fg=colors[index]).grid(column=index, row=0)
link = Label(root, text = "LINK", font="TKDefaultFont 9 underline", fg = "white", bg = "black", cursor="hand2")
link.grid(column=len(words),row=0)
link.bind("<Button-1>", lambda e: callback("https://www.google.com"))

root.mainloop()