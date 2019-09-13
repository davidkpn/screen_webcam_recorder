import mss
import numpy as np
import cv2
import time
from threading import Thread
import sys

def record():
    ###############################################################
    # Pick Region of interest
    ###############################################################
    sct = mss.mss()
    monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
    frame = np.array(sct.grab(monitor))
    cv2.namedWindow("frame")
    fromCenter = False
    x, y, dx, dy = cv2.selectROI("frame", frame, fromCenter)
    if x or y or dx or dy:
        monitor['top'] = y
        monitor['left'] = x
        monitor['width'] = dx
        monitor['height'] = dy



    ###############################################################
    # Cv2 text
    ###############################################################
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = .9
    color = (32, 32, 32)
    thickness = 1
    rectangle_bgr = (240, 240, 240)
    ###############################################################

    out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (monitor['width'],monitor['height']))
    video = False
    im_index = 1
    record = True
    webcam = False
    pause = False
    last_time = time.time()
    sct = mss.mss()
    cap = cv2.VideoCapture(0)
    while(record):
        if not pause:
            screen = np.array(sct.grab(monitor))
            fps = round(1/(time.time()-last_time))
            print('fps: {}'.format(fps))
            last_time = time.time()
            if webcam:
                _, cam_frame = cap.read()
                if cam_frame:
                    screen[0:cam_frame.shape[0], 0:cam_frame.shape[1]] = cam_frame
                else:
                    webcam = False
                    print("No webcam feed")
            if video:
                out.write(screen)
            else:
                cv2.imwrite(f"./images/{im_index}.jpg", screen);
                im_index+=1

            text = f'video mode:{ "on" if video else "off" }, webcam mode: { "on" if webcam else "off" }, fps:{fps}'
            (text_width, text_height) = cv2.getTextSize(text, font, font_scale, thickness=thickness)[0]
            text_offset_x = 10
            text_offset_y = screen.shape[0] - 25
            box_coords = ((text_offset_x+2, text_offset_y+2), (text_offset_x + text_width - 2, text_offset_y - text_height - 2))
            screen = cv2.rectangle(screen, box_coords[0], box_coords[1], rectangle_bgr, cv2.FILLED)
            screen = cv2.putText(screen, text, (text_offset_x, text_offset_y), font, font_scale, color, thickness, cv2.LINE_AA)
            cv2.imshow('frame',screen)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                record = False
            elif key == ord('p'):
                pause = not pause
            elif key == ord('w'):
                webcam = not webcam



if __name__ == "__main__":
    record()
    cv2.destroyAllWindows()
