from tkinter import Frame
from authentication import authentication
from Frames import window
def main():
    
    # authUser = authentication.AuthUser()
    # authUser.mainloop()

    mainframe = window.Window("ramDB")
    mainframe.mainloop()

main()
