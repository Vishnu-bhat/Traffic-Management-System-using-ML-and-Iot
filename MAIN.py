import cv2
import pandas as pd
from ultralytics import YOLO
import cvzone
import numpy as np

import math

class Tracker:
    def __init__(self):
        # Store the center positions of the objects
        self.center_points = {}
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.id_count = 0


    def update(self, objects_rect):
        # Objects boxes and ids
        objects_bbs_ids = []

        # center point of object
        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # Find out if that object was detected already
            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])

                if dist < 35:
                    self.center_points[id] = (cx, cy)

                    objects_bbs_ids.append([x, y, w, h, id])
                    same_object_detected = True
                    break

            # New object is detected we assign the ID to that object
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1

        # Clean the dictionary by center points to remove IDS not used anymore
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        # Update dictionary with IDs not used removed
        self.center_points = new_center_points.copy()
        return objects_bbs_ids

import torch
torch.cuda.set_device(0)

model=YOLO('best.pt')


#def RGB(event, x, y, flags, param):
#    if event == cv2.EVENT_MOUSEMOVE :  
#      point = [x, y]
#      print(point) 
  

cv2.namedWindow('Yolo Project')
#cv2.setMouseCallback('Yolo Project', RGB)
            
 
cap=cv2.VideoCapture('id4.mp4')


my_file = open("coco1.txt", "r")
data = my_file.read()
class_list = data.split("\n") 

cy1=427
offset=6

count=0
tracker=Tracker()
tracker1=Tracker()
tracker2=Tracker()
tracker3=Tracker()
bus=[]
car=[]
auto_rikshaw=[]
motorcycle=[]
while True:    
    ret,frame = cap.read()
    if not ret:
       break
   

    count += 1
    if count % 3 != 0:
        continue
    frame=cv2.resize(frame,(1020,500))
    results=model.predict(frame)
    #print(results)
    a = results[0].boxes.data
    a_cpu = a.cpu().numpy()
    px = pd.DataFrame(a_cpu).astype("float")
    #print(px)
    
    list=[]
    list1=[]
    list2=[]
    list3=[]
    
    for index,row in px.iterrows():
 
        x1=int(row[0])
        y1=int(row[1])
        x2=int(row[2])
        y2=int(row[3])
        
        d=int(row[5])
        c=class_list[d]
       
        if 'bus' in c:
            list.append([x1,y1,x2,y2])
        elif 'car' in c:
             list1.append([x1,y1,x2,y2])
        elif 'auto-rikshaw' in c:
             list2.append([x1,y1,x2,y2])
        elif 'motor-cycle' in c:
             list3.append([x1,y1,x2,y2])
        
    bbox_idx=tracker.update(list)
    bbox1_idx=tracker1.update(list1)
    bbox2_idx=tracker2.update(list2)
    bbox3_idx=tracker3.update(list3)
    for bbox in bbox_idx:
        x3,y3,x4,y4,id=bbox
        cx=int(x3+x4)//2
        cy=int(y3+y4)//2
        if cy1<(cy+offset) and cy1>(cy-offset):
           cv2.rectangle(frame,(x3,y3),(x4,y4),(0,255,0),2)
           cvzone.putTextRect(frame,f'{id}',(x3,y3),1,1)
           if bus.count(id)==0:
              bus.append(id)
#CAR
    for bbox1 in bbox1_idx:
        x5,y5,x6,y6,id1=bbox1
        cx2=int(x5+x6)//2
        cy2=int(y5+y6)//2
        if cy1<(cy2+offset) and cy1>(cy2-offset):
           cv2.rectangle(frame,(x5,y5),(x6,y6),(0,255,0),2)
           cvzone.putTextRect(frame,f'{id1}',(x5,y5),1,1)
           if car.count(id1)==0:
              car.append(id1)
#auto-rikshaw
    for bbox2 in bbox2_idx:
        x7,y7,x8,y8,id2=bbox2
        cx3=int(x7+x8)//2
        cy3=int(y7+y8)//2
        if cy1<(cy3+offset) and cy1>(cy3-offset):
           cv2.rectangle(frame,(x7,y7),(x8,y8),(0,255,0),2)
           cvzone.putTextRect(frame,f'{id2}',(x7,y7),1,1)
           if auto_rikshaw.count(id2)==0:
              auto_rikshaw.append(id2)
#motorcycle
    for bbox3 in bbox3_idx:
        x9,y9,x10,y10,id3=bbox3
        cx4=int(x9+x10)//2
        cy4=int(y9+y10)//2
        if cy1<(cy4+offset) and cy1>(cy4-offset):
           cv2.rectangle(frame,(x9,y9),(x10,y10),(0,255,0),2)
           cvzone.putTextRect(frame,f'{id3}',(x9,y9),1,1)
           if motorcycle.count(id3)==0:
              motorcycle.append(id3)          
    countbus=(len(bus))
    countcar=(len(car))
    countauto_rikshaw=(len(auto_rikshaw))
    countmotorcycle=(len(motorcycle))
    cvzone.putTextRect(frame,f'Auto_Rikshaw :-{countauto_rikshaw}',(50,60),scale=2,thickness=2,colorR=(0,0,255))
    cvzone.putTextRect(frame,f'Bus :-{countbus}',(50,120),scale=2,thickness=2,colorR=(0,0,255))
    cvzone.putTextRect(frame,f'Car :-{countcar}',(50,180),scale=2,thickness=2,colorR=(0,0,255))
    cvzone.putTextRect(frame,f'MotorCycle :-{countmotorcycle}',(50,240),scale=2,thickness=2,colorR=(0,0,255))


    cv2.line(frame,(405,427),(580,427),(255,255,255),2)
    cv2.imshow("RGB", frame)
    if cv2.waitKey(1)&0xFF==27:
        break
cap.release()    
cv2.destroyAllWindows()




