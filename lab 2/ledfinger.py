
import cv2
import mediapipe as mp
import time
import pyfirmata

time.sleep(2.0)
cap = cv2.VideoCapture(0)
Nfing = 5
mp_draw=mp.solutions.drawing_utils #use function drawing_utils to draw straight connect landmark point
mp_hand=mp.solutions.hands #use function hands to find hand on camera

tipIds=[4,8,12,16,20] # media-pipe position  of fingertips

def check_user_input(input):
    try:
        # Convert it into integer
        val = int(input)
        # print("Input is an integer number. Number = ", val)
        bv = True
    except ValueError:
        try:
            # Convert it into float
            val = float(input)
            # print("Input is a float  number. Number = ", val)
            bv = True
        except ValueError:
            # print("No.. input is not a number. It's a string")
            bv = False
    return bv

cport = input('Enter the camera port: ')
while not (check_user_input(cport)):
    print('Please enter a number not string')
    cport = input('Enter the camera port: ')

comport = input('Enter the arduino board COM port: ')
while not (check_user_input(comport)):
    print('Please enter a number not string')
    comport = input('Enter the arduino board COM port: ')


#Call hand pipe line module
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

board=pyfirmata.Arduino('COM'+comport)
led_1=board.get_pin('d:13:o') #Set pin to output
led_2=board.get_pin('d:12:o')
led_3=board.get_pin('d:11:o')
led_4=board.get_pin('d:10:o')
led_5=board.get_pin('d:9:o')

#### LED write function

## controller.py ##

def led(led_1,led_2,led_3,led_4,led_5,led1,led2,led3,led4,led5):#creat condition to controll digital out put
    led_1.write(led1)
    led_2.write(led2)
    led_3.write(led3)
    led_4.write(led4)
    led_5.write(led5)

while True:
    led1 = 0
    led2 = 0
    led3 = 0
    led4 = 0
    led5 = 0
    name = []
    Nfing = 5
    
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                if id == 4:
                    id4 = int(id)
                    cx4 = cx
                if id == 3:
                    id3 = int(id)
                    cx3 = cx
                if id == 8:
                    id8 = int(id)
                    cy8 = cy
                if id == 7:
                    id7 = int(id)
                    cy7 = cy
                if id == 16:
                    id6 = int(id)
                    cy16 = cy
                if id == 12:
                    id12 = int(id)
                    cy12 = cy
                if id == 15:
                    id15 = int(id)
                    cy15 = cy
                if id == 11:
                    id11 = int(id)
                    cy11 = cy
                if id == 19:
                    id19 = int(id)
                    cy19 = cy
                if id == 20:
                    id20 = int(id)
                    cy20 = cy
            
            if cy20 < cy19:
                name.append ("Little finger")
                led5 = 1

            if cy16 < cy15:
                 name.append("Ring finger")
                 led4 = 1
                 
            if cy12 < cy11:
                 name.append("Middle finger")
                 led3 = 1
            if cy8 < cy7:
                 name.append("Index finger")
                 led2 = 1
            if cx4 > cx3:
                 name.append("Thumb finger")
                 led1 = 1

    
    led(led_1,led_2,led_3,led_4,led_5,led1,led2,led3,led4,led5) #import function in module to control arduino output
    mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
   
    cv2.imshow("Image", img)
    cv2.waitKey(1)
    

 