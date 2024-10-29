import cv2
import numpy as np
import mediapipe as mp
import time
import matplotlib.pyplot as plt
import pyautogui

cap=cv2.VideoCapture(0)

pose=mp.solutions.pose
pose_o=pose.Pose()
drawing=mp.solutions.drawing_utils
 
def inFrame(lst):
    if lst[24].visibility>0.7 and lst[23].visibility>0.7 and lst[16].visibility>0.7 and lst[15].visibility>0.7:
        return True
    return False

def find_sum(lst):
    return lst[24].y*640+lst[23].y*640+lst[16].y*640+lst[15].y*640

def shifting(new_sum):
    global sum_list

    for i in range(3,-1,-1):
        sum_list[i+1]=sum_list[i]

    sum_list[0]=abs(new_sum-prev_sum)

def isRunning():
    sm=0
    for i in sum_list:
        sm=sm+i
    if sm>40:
        return True
    return False

def isJump(lst):
    if (lst[0].y*480)<80:
        return True
    return False

def isShooting(lst):
    if abs(finalres[15].x*640 -finalres[16].x*640)<80:
        return True
    return False


sum_list=np.array([0.0]*5)
prev_sum=0
is_Init=False
temp_lst=[]

d_down=False
s_down=False
j_down=False

while True:
    _, frm=cap.read()

    res=pose_o.process(cv2.cvtColor(frm,cv2.COLOR_BGR2RGB))
    
    if res.pose_landmarks:
        finalres=res.pose_landmarks.landmark

    if res.pose_landmarks and inFrame(finalres):
        cv2.putText(frm,"Continue",(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        #logic for the jump
        if not (is_Init):
            is_Init=True
            prev_sum=find_sum(finalres)
        else:
            #run logic 
            new_sum=find_sum(finalres)
            shifting(new_sum)
           
           #Running check
            if isRunning():
                cv2.putText(frm,"Running",(50,100),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

                if not(s_down):
                    pyautogui.keyDown("s")
                    s_down=True
            else:
                cv2.putText(frm,"Not Running",(50,100),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

                if s_down:
                    pyautogui.keyUp("s")
                    s_down=False


            ##jump logic
            if isJump(finalres):
                cv2.putText(frm,"Jumping",(50,150),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

                if not(j_down):
                    pyautogui.keyDown("j")
                    j_down=True
            else:
                cv2.putText(frm,"Not Jumping",(50,150),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
                
                if j_down:
                    pyautogui.keyUp("j")
                    j_down=False
            ##shooting logic
            if isShooting(finalres):
                cv2.putText(frm,"Shooting",(50,200),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

                if not(d_down):
                    pyautogui.keyDown("d")
                    d_down=True
            else:
                cv2.putText(frm,"Not Shooting",(50,200),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
                
                if d_down:
                    pyautogui.keyUp("d")
                    d_down=False
            
            prev_sum=new_sum

    else:
         cv2.putText(frm,"Make sure full body in frame",(50,100),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

    cv2.imshow("window",frm)

    if cv2.waitKey(1) ==27:
        
        cap.release()
        cv2.destroyAllWindows()
        break 