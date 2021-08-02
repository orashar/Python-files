import cv2

face_cascade =  cv2.CascadeClassifier('./frontal_deault.xml')

video = cv2.VideoCapture(0)

while True:
    check, img = video.read()
    print(1)

    #img = cv2.imread('./download.jpeg')

    #cv2.imshow("image", img)

    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(grey, scaleFactor = 1.05, minNeighbors = 5)
    
    for x, y, w, h in faces:
        img = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)

    cv2.imshow("try", img)
    print(2)
    k = cv2.waitKey(1)
    
    if k ==27:
        break
cv2.destroyAllWindows()
    
