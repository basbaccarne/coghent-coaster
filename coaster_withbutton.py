# This scripts shows a random image from unsplash
# It also checks if a button is pressed.
# If a transition from pressed to not pressed is detected (pick up your coffee mug), a new image is loaded

# tech set-up (pull-up button):
# wire from 3.3V to 10k resistor
# 10k resistor to BCM 14 pin (raspi1) & to button side 1
# button side 2 to ground

# import general modules
import RPi.GPIO as GPIO
import time
import tkinter as tk
from PIL import Image, ImageOps, ImageTk

# import local scripts
from fetch_unsplash import get_unsplash
from crop_image import fix_image

# define global variables
root = None
canvas = None
button_state = 0
previous_button_state = 0

# GPIO settings
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# define function to get an image & process it
def fetch():
    # get image
    get_unsplash("_dS_EqFCJvV75FSSBw8a6w2vnZJRYbEnwIb1OF81DY8")
    # crop image
    fix_image("image.jpg")


# download initial image on start-up
fetch()


# define callback function
def poll():
    # import global variables
    global root
    global canvas
    global button_state
    global previous_button_state

    # read button state (pull up buttons: high = button not pressed)
    button_state = not GPIO.input(14)

    # if sensor is switched from on to off (coffee leaves base)
    if button_state == 0 and previous_button_state == 1:

        # fetch a new image
        fetch()

        # replace the image in the interface
        img2 = ImageTk.PhotoImage(Image.open("image_cropped.jpg"))
        canvas.configure(image=img2)
        canvas.image = img2

    # in all other cases: print the value of the button
    else:
        print("we're all good, the button value is: " + str(button_state) + ". Press CTRL + C to exit.")

    # store the button value for future reference
    previous_button_state = button_state

    # schedule next cycle (in milliseconds)
    root.after(1000, poll)


# define the properties iof the user interface (root is the main window)
root = tk.Tk()
root.geometry("320x240")
root.overrideredirect(True)  # borderless
root.configure(bg="black")  # black background
root.eval("tk::PlaceWindow . center")  # place in center of screen

# define a frame in the center of the main window
frame = tk.Frame(root)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# lead and place the initial image in the frame
img1 = ImageTk.PhotoImage(Image.open("image_cropped.jpg"))
canvas = tk.Label(frame, image=img1, borderwidth=0, highlightthickness=0)
canvas.pack()

# schedule first cycle (in milliseconds)
root.after(1000, poll)

# run the interface
root.mainloop()
