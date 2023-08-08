from PIL import ImageGrab
import tensorflow as tf
from tkinter import *
import numpy as np
import win32gui

# Import Model to Use In File
model = tf.keras.models.load_model('./controller/model.h5')

# Predict Digit
def predict_digit(img):
    # Resize Image To 28*28 Pixels
    img = img.resize((28, 28))

    # Convert RGB To GrayScale
    img = img.convert('L')
    img = np.array(img)

    # Reshaping to Support our Model Input and Normalizing
    img = img.reshape(1, 28, 28, 1)
    img = img/255.0

    # predicting the class
    res = model.predict([img])[0]

    return np.argmax(res), max(res)

class Root:
    # Splash Window
    def begin(self):
        # Window
        self.splash_root = Tk()
        
        # Window Settings
        self.splash_root.title('Splash Screen')     
        self.splash_root.overrideredirect(True)
        self.splash_root.geometry("500x250+500+250")
        self.splash_root.config(background='#1d3557')
        
        # Splash Title 
        self.splashLabel = Label(
            self.splash_root,
            text = "Hand Writing Recognition",
            foreground = '#f1faee',
            background = '#1d3557',
            font = ("Helvetica", 30)
        )
        
        # Space Between Top and Label
        self.splashLabel.pack(pady = 100)

        # After 3s Navigate to MainWindow
        self.splash_root.after(3000, self.main_window)
        self.splash_root.mainloop()
    
    # App Window
    def main_window(self):
        # Delete Window SplashRoot
        self.splash_root.destroy()
        
        # Window
        self.root = Tk()
        
        # Window Settings
        self.root.state('zoomed')
        self.root.config(background='#1d3557')
        self.root.title('Hand Writing Recognition')
        
        # Get Screen's Height in pixels
        height = self.root.winfo_screenheight()
        
        # Get Screen's Width in pixels
        width = self.root.winfo_screenwidth()

        # Drawing Space For Digit
        self.canvas = Canvas(
            self.root,
            bd = 5,
            bg = "#1d3557",
            cursor = "dot",
            width = width * 0.5,
            height = height * 0.7
        )

        # Status of Line
        self.canvas.bind("<B1-Motion>", self.draw_lines)

        # Canvas Grid -> 0, 0
        self.canvas.grid(row = 0, column = 0, pady = height * 0.05, padx = height * 0.05)
        
        # Label Before PredictDigit 
        self.label = Label(
            self.root,
            foreground = 'White',
            background = '#1d3557',
            width = 20,
            text = "Draw Digit Now..",
            font = ("Helvetica", 30, 'bold')
        )

        # Label Grid -> 0, 1
        self.label.grid(row = 0, column = 1, pady = 50, padx = 50)

        # Clear Drawing
        self.btn_clear = Button(
            self.root,
            text = "Clear",
            bd = 0,
            height = 2,
            width = 20,
            bg = 'red',
            fg = '#f1faee',
            activebackground = 'red',
            activeforeground = '#f1faee',
            font = ("Helvetica", 14, 'bold'),        
            command = self.clear_all
        )

        # Clear Drawing Grid -> 1, 0
        self.btn_clear.grid(row = 1, column = 0, pady = 2)
        
        # Classify Driwing 
        self.btn_classify = Button(
            self.root,
            text = "Recognise",
            bd = 0,
            height = 2,
            width = 20,
            bg = 'green',
            fg = '#f1faee',
            activebackground = 'green',
            activeforeground = '#f1faee',
            font = ("Helvetica", 14, 'bold'),         
            command = self.classify_handwriting
        )

        # Classify Drawing Grid -> 1, 1
        self.btn_classify.grid(row = 1, column = 1, pady = 2, padx = 2)

        self.root.mainloop()

    # Clear Drawing Space
    def clear_all(self):
        self.x = 0.0
        self.y = 0.0
        self.canvas.delete("all")
        self.label.configure(text='Draw Digit Now..')
        

    # Drawing Digit
    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y

        # Size Of Point
        r = 30

        # Point
        self.canvas.create_oval(
            self.x - r,
            self.y - r,
            self.x + r,
            self.y + r,
            fill='white'
        )
        
    # Classify Digit
    def classify_handwriting(self):
        # If Draw Space Not Empty
        if self.x != 0 or self.y ==0 :
            # Get The Handle Of The Canvas
            HWND = self.canvas.winfo_id()

            # Get The Coordinate Of The Canvas
            rect = win32gui.GetWindowRect(HWND)
            im = ImageGrab.grab(rect)

            # Result Of Processing Digit
            digit, acc = predict_digit(im)

            # Display Result
            self.label.configure(text=str(digit)+', ' + str(int(acc*100))+'%',)