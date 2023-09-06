from tkinter import *
 
__author__ = {'name' : 'Hongten',
               'mail' : 'hongtenzone@foxmail.com',
               'blog' : 'http://www.cnblogs.com/',
               'QQ': '',
               'created' : '2013-09-10'}
 
def makeCascadeMenu():
     # make menu button
    Cascade_button = Menubutton(mBar, text='Cascading Menus', underline=0)
    Cascade_button.pack(side=LEFT, padx="2m")
 
     # the primary pulldown
    Cascade_button.menu = Menu(Cascade_button)
 
     # this is the menu that cascades from the primary pulldown....
    Cascade_button.menu.choices = Menu(Cascade_button.menu)
 
     # ...and this is a menu that cascades from that.
    Cascade_button.menu.choices.weirdones = Menu(Cascade_button.menu.choices)
 
     # then you define the menus from the deepest level on up.
    Cascade_button.menu.choices.weirdones.add_command(label='avacado', command=lambda:print('hello'))
    Cascade_button.menu.choices.weirdones.add_command(label='belgian endive')
    Cascade_button.menu.choices.weirdones.add_command(label='beefaroni')
 
     # definition of the menu one level up...
    Cascade_button.menu.choices.add_command(label='Chocolate')
    Cascade_button.menu.choices.add_command(label='Vanilla')
    Cascade_button.menu.choices.add_command(label='TuttiFruiti')
    Cascade_button.menu.choices.add_command(label='WopBopaLoopBapABopBamBoom')
    Cascade_button.menu.choices.add_command(label='Rocky Road')
    Cascade_button.menu.choices.add_command(label='BubbleGum')
    Cascade_button.menu.choices.add_cascade(
         label='Weird Flavors',
         menu=Cascade_button.menu.choices.weirdones)
 
     # and finally, the definition for the top level
    Cascade_button.menu.add_cascade(label='more choices',
                                     menu=Cascade_button.menu.choices)
 
    Cascade_button['menu'] = Cascade_button.menu
 
    return Cascade_button
 
 #################################################
 #### Main starts here ...
root = Tk()
root.geometry('600x300')
 
 # make a menu bar
mBar = Frame(root, relief=RAISED, borderwidth=2)
mBar.pack(fill=X)
 
Cascade_button = makeCascadeMenu()
 
mBar.tk_menuBar(Cascade_button)
 
root.title('menu demo')
root.iconname('menu demo')
 
root.mainloop()