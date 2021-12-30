import math
import cv2
import numpy
import numpy as np
import torch
import os
import time

cap = cv2.VideoCapture('zz.mp4')
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
count = 0

center_point_pre = []
tracking_objects = {}
speed_checks = {}
time_first = {}
time_ends = {}
#tracking_objects_pre1 = {}
#tracking_objects_pre2 = {}
track_id = 0
area = [(20,100),(20,102),(620,102),(620,100)]
zone = [(20,150),(20,152),(620,152),(620,150)]
try:
    while(True):
            _, frame1 = cap.read()
            frame1 = cv2.resize(frame1, (640, 620))
            frame = frame1[150:640, 0:620]
            detected = model(frame)
            results = detected.pandas().xyxy[0].to_dict(orient="records")
            center_point_cur = []
            count += 1
            cv2.polylines(frame,[np.array(area,np.int32)],True,(0,0,255),2)
            cv2.polylines(frame, [np.array(zone, np.int32)], True, (0, 255, 0), 2)
            for result in results:
                clas = result['class']
                confid = result['confidence']
                if confid > 0.3:
                    if clas == 2:

                        x1 = int(result['xmin'])
                        y1 = int(result['ymin'])
                        x2 = int(result['xmax'])
                        y2 = int(result['ymax'])
                        w = int(x1+(x2-x1)/2)
                        h = int(y1+(y2-y1)/2)
                        center_point_cur.append((w, h))
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 1)
                        #result = cv2.pointPolygonTest(np.array(area, np.int32), pt, False)
                        #cv2.circle(frame, pt, 2, (255, 0, 255), -1)

            if count <= 3:
                for pt in center_point_cur:
                    for pt2 in center_point_pre:
                        distance = math.hypot(pt2[0]-pt[0],pt2[1]-pt[1])
                        if distance < 35:
                            tracking_objects[track_id] = pt
                            track_id += 1
            else:
                tracking_objects_cop = tracking_objects.copy()
                center_point_cur_cop = center_point_cur.copy()

                for object_id, pt2 in tracking_objects_cop.items():
                    object_exits = False
                    for pt in center_point_cur_cop:
                        distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])

                        if distance < 35:
                            tracking_objects[object_id] = pt
                            object_exits = True
                            center_point_cur.remove(pt)
                            continue
                    if count % 2 == 0:
                        if not object_exits:
                            tracking_objects.pop(object_id)
                    else:
                        continue

                for pt in center_point_cur:
                    tracking_objects[track_id] = pt
                    track_id += 1
            for object_id, pt in tracking_objects.items():
                result1 = cv2.pointPolygonTest(np.array(area, np.int32), pt, False)
                if result1 >= 0:
                    cv2.circle(frame, pt, 2, (255, 0, 255), -1)
                    time_first[object_id] = time.time()

                result2 = cv2.pointPolygonTest(np.array(zone, np.int32), pt, False)
                if result2 >= 0:
                    cv2.circle(frame, pt, 2, (255, 0, 255), -1)
                    time_ends[object_id] = time.time()

                    speed_checks[object_id] = time_ends[object_id] - time_first[object_id]

            #print(time_first)
            #print("-----")
            #print(time_ends)
            #print(speed_checks)
            for object_id, pt in tracking_objects.items():
                for object_id1, pt1 in speed_checks.items():
                    if object_id == object_id1:
                        text = str(round(pt1*5,2)) +"km/h"
                        cv2.putText(frame,text, (pt[0], pt[1] +20), cv2.FONT_HERSHEY_DUPLEX,1, (100, 0, 255), 1)


            for object_id, pt in tracking_objects.items():
                text = str(object_id)
                cv2.circle(frame, pt, 2, (255, 0, 255), -1)
                cv2.putText(frame,text, (pt[0], pt[1] - 7), cv2.FONT_HERSHEY_DUPLEX,1, (0, 100, 255), 1)
            #print(tracking_objects)
            cv2.imshow('s', frame1)

            #print(count)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            #out = cv2.VideoWriter('end.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (640, 620))
except:
    print('end')
cap.release()
cv2.destroyAllWindows()