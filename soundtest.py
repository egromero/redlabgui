from soundplayer import SoundPlayer
import time

soundpath = "/home/pi/redlabgui/sounds/"
song = "JohnCenaShort.mp3"
p = SoundPlayer(soundpath+song, 0)
p.playTone(400, 4, blocking=True, device=1)
time.sleep(0.01)
