import time
from guizero import App, Window, PushButton, Picture
from queue import Queue 
from threading import Thread 

millis = lambda: int(round(time.time() * 1000))


q = Queue() 
def consumer(in_q): 
    while True:
        data = in_q.get() 
        open_window()
        t2.start()

def counter():
    t = millis()
    while True:
        if millis()-t > 3000:
            close_window()
            break

t1 = Thread(target = consumer, args =(q, )) 
t2 = Thread(target = counter)
t1.start()

def open_window():
    window.show()

def close_window():
    window.hide()

app = App(title="Main window")

window = Window(app, title="Second window")
picture = Picture(window, image="images/Enroll.png")
window.hide()






