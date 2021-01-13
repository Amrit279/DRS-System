import cv2 as cv # pip install opencv-python

def makeVideo():
    """
    Records video using installed webcam and saves it to a file
    """
    cap = cv.VideoCapture(0, cv.CAP_DSHOW) # Capturing Frames
    fourcc = cv.VideoWriter_fourcc(*'XVID') # Generating four code
    out = cv.VideoWriter('output.avi', fourcc, 20.0, (640, 480)) # Creating write object

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        out.write(frame)
        cv.imshow("Webcam", frame)

        if cv.waitKey(1) == ord('q'):
            break

    cap.release()
    out.release()
    cv.destroyAllWindows()