
import cv2
import numpy as np

cascade1 = cv2.CascadeClassifier('haarcascade_fullbody.xml')
cascade2 = cv2.CascadeClassifier('haarcascade_upperbody.xml')
cascade3 = cv2.CascadeClassifier('haarcascade_lowerbody.xml')

cap = cv2.VideoCapture('Street Walking.mp4')
#cap = cv2.VideoCapture(0)
frame_width = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height =int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.mp4',fourcc, 20.0, (640,480))

ret, frame1 = cap.read()
ret, frame2 = cap.read()
print(frame1.shape)
while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        (x, y, w, h) = (x - 100, y - 100, w + 100, h + 100)

        if cv2.contourArea(contour) < 10000:
            continue

        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 255), 2)

        roi_gray = gray[y:y + h, x:x + w]
        body1 = cascade1.detectMultiScale(roi_gray, 1.3, 5)
        body2 = cascade2.detectMultiScale(roi_gray, 1.3, 5)
        body3 = cascade3.detectMultiScale(roi_gray, 1.3, 5)

        for (x, y, w, h) in body1:
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (255, 0, 0), 2)

        for (x, y, w, h) in body2:
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 0, 255), 2)

        for (x, y, w, h) in body3:
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 3)
    #cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)

    image = cv2.resize(frame1, (640,480))
    out.write(image)
    cv2.imshow("feed", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(40) == 27:
        break

cap.release()
out.release()
cv2.destroyAllWindows()