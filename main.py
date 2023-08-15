import cv2
import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)


def captura():
    if not cap.isOpened():
        print("Cannot open camera")
        return
    while True:
        ret, frame = cap.read()
        frame = cv.resize(frame, (640, 480))

        bl = (640, 480)
        br = (640, 0)
        tl = (480, 300)
        tr = (480, 150)

        cv.circle(frame, tl, 5, (0, 255, 0), -1)
        cv.circle(frame, bl, 5, (0, 255, 0), -1)
        cv.circle(frame, tr, 5, (0, 255, 0), -1)
        cv.circle(frame, br, 5, (0, 255, 0), -1)

        pts1 = np.float32([tl, bl, tr, br])
        pts2 = np.float32([[0, 0], [0, 480], [640, 0], [640, 480]])

        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        transformed = cv2.warpPerspective(frame, matrix, (640, 480))

        cv.imshow('Frame', frame)
        cv.imshow('BEV Frame', transformed)

        if cv.waitKey(1) == ord('q'):
            break

captura()
"""
while True:
    # Capture frame-by-frame
    
    # if frame is read correctly ret is True
    # Our operations on the frame come here
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow('frame', gray)
    # Display the resulting frame
    if cv.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
"""