import time
from guizero import App, Window, PushButton, Picture
from queue import Queue 
from threading import Thread 

millis = lambda: int(round(time.time() * 1000))
app = App(title="screens")

q = Queue() 
def consumer(in_q): 
    while True:
        data = in_q.get()
        print("recieved") 
        window = Window(app)
        picture = Picture(window, image="images/Enroll.png")
        window.show()
        t = millis()
        while True:
            print("contando")
            if millis()-t>3000:
                window.hide()
                window.destroy()
                break

t1 = Thread(target = consumer, args =(q, ))
t1.start()

# window = Window(app, title="Second window")
# picture = Picture(window, image="images/Enroll.png")
# window.hide()






