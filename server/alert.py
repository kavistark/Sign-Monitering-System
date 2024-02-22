import time
import platform
if platform.system() == 'Windows':
    import winsound
else:
    import pygame

def aleram( trigger_text):
    print("This is a message")
    while True:
        user_input = 'Sad'
        if user_input == trigger_text:
            break
    if platform.system() == 'Windows':
        frequency = 855
        duration = 3000 
        winsound.Beep(frequency, duration)
    else:
        pygame.mixer.init()
        pygame.mixer.music.load("alarm.wav")
        pygame.mixer.music.play()
        time.sleep(1.5) 
        pygame.mixer.music.stop()

