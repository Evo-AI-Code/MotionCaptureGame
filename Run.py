import tkinter as tk # Tkinter
from PIL import ImageTk, Image # Pillow
import cv2 as cv # OpenCV
import os
import random
import tensorflow as tf
from tensorflow import keras
import numpy as np
import pygame
classes = ['Running', 'RaiseTwo', 'BodyBuild','Dab','Greeting ','Salute','None']
RandomAction = random.choice(classes)
Command = "다음의 동작을 취하세요! : {}".format(RandomAction)
time_left = 0
ClassifiedAction = None
font_info = ("Helvetica", 30)
score = 0
start = False
model = tf.keras.models.load_model('keras_model.h5',compile=False)
asset = "C:\MCG\Sp.png"
tf.get_logger().setLevel('ERROR')
def refresh():#여기다가 동기화해야할 위젯들 넣고 위젯.config(안에는 대충 변화해야할 속성 넣으면 될듯)
    global score, RandomAction
    RandomAction = random.choice(classes)
    Command = "다음의 동작을 취하세요! : {}".format(trans(RandomAction))
    label_command.config(text=Command)
    score+=1
    label_point.config(text="점수 : {}".format(score))
    pygame.mixer.init()
    pygame.mixer.music.load('Effect.mp3')
    pygame.mixer.music.play()
    print("점수획득")

def trans(en):
    if en == classes[0]:
        kr = "달리기"
    elif en == classes[1]:
        kr = "손들기"
    elif en == classes[2]:
        kr = "보디빌딩"
    elif en == classes[3]:
        kr = "댑"
    elif en == classes[4]:
        kr = "배꼽인사"
    elif en == classes[5]:
        kr = "경례"
    elif en == classes[6]:
        kr = "서있기"
    return kr
    
def exit_program(status):
    win.destroy()
'''   
def condition():
    if start:
        if RandomAction == ClassifiedAction:
            refresh()
        win.after(500, condition)
'''
def video_play():
    global imgtk
    ret, frame = cap.read() # 프레임이 올바르게 읽히면 ret은 True
    if not ret:
        cap.release() # 작업 완료 후 해제
        return
    frame1 = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    img1 = Image.fromarray(frame1) # Image 객체로 변환
    imgtk = ImageTk.PhotoImage(image=img1) # ImageTk 객체로 변환
    frame2 = cv.resize(frame, (224, 224), interpolation=cv.INTER_AREA)
    frame2 = np.asarray(frame2, dtype=np.float32).reshape(1, 224, 224, 3)
    frame2 = (frame2 / 127.5) - 1
    prediction = model.predict(frame2)
    index = np.argmax(prediction)
    ClassifiedAction = classes[index]
    # OpenCV 동영상
    label_camera.imgtk = imgtk
    label_camera.configure(image=imgtk)
    label_camera.after(10, video_play)
    print("working", start)
    if start:
        print(ClassifiedAction, RandomAction)
        if ClassifiedAction == RandomAction:
            refresh()

def start_timer():
    global start, time_left, score
    if not start:
        start = True
        time_left = 60
        score = -1
        refresh()
    if time_left > 0:
        # 1초씩 감소
        time_left -= 1
        # label_time 업데이트
        label_time.config(text="남은시간: {}초".format(time_left))
        # 1초 후에 start_timer 함수 재호출
        win.after(1000, start_timer)
    else:
        label_time.config(text="타이머 종료")
        start = False
start = False
win=tk.Tk()
win.title("MotionCaptureGame")
win.geometry("1200x800+200+0")
win.resizable(False, False)
cap = cv.VideoCapture(0)

label_command=tk.Label(win, text=Command, font=font_info)
label_command.pack(side = "top", anchor = "n")


frm = tk.Frame(win, width=480, height=320) # 프레임 너비, 높이 설정
frm.pack(side = "top", anchor = "s")

label_camera = tk.Label(frm)
label_camera.pack()

label_time = tk.Label(win, text=time_left, font=font_info)
label_time.pack(side = "left", padx = 200)

label_point = tk.Label(win, text="점수 : {}".format(score), font=font_info)
label_point.pack(side = "right", padx = 180)

start_button = tk.Button(win, text="시작", command=start_timer)
start_button.pack(pady=10)

video_play()

win.bind('<q>', exit_program)

win.protocol("WM_DELETE_WINDOW", lambda:cap.release())
win.mainloop()