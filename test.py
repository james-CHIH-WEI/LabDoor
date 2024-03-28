# -*- coding: utf-8 -*-
import cv2

cam = cv2.VideoCapture(0)

while True:
    ret, img = cam.read()
    # vis = img.copy()
    cv2.imshow("Camera", img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cam.release()
cv2.destroyAllWindows()
