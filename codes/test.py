import numpy as np
import cv2
from PIL import Image
from area import Area
from player import Player


def get_video():
    """
    ダメージを受けた(or回復した)時の体力ゲージの変化を動画で表示
    """ 
    cap = cv2.VideoCapture('../hp_gauge.mp4')
    cap1 = cv2.VideoCapture('../hp_gauge.mp4')
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, 20)
    cap1.set(cv2.CAP_PROP_POS_FRAMES, 40)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(906/8))
    cap1.set(cv2.CAP_PROP_FRAME_WIDTH, int(906/8))
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(386/8))
    cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, int(386/8))    

    end_frame = 80
    end_frame_min = 60

    for i in range(end_frame+1):
        frame_list = []
        frame_list_resize = []
        for s in range(2):
            ret, frame = cap.read()

            frame_list.append(frame)

        if i < end_frame_min:

            #for t in range(2):
                #frame_list_resize.append(cv2.resize(frame_list[t] , (int(906/4),int(386/4))))
                

            frame2 = cv2.hconcat([frame_list[0],frame_list[1]])

            cv2.imshow("Field",frame2)

            if cv2.waitKey(500) & 0xFF == ord('q'): 
                break
            
        elif end_frame_min <= i and i < end_frame:
            print('hello world')

            #if cv2.waitKey(500) & 0xFF == ord('q'): 
            #    break
        elif i == end_frame:
            if cv2.waitKey(0):
                break
    cap.release()

    cv2.destroyAllWindows()                                

get_video()
                   
