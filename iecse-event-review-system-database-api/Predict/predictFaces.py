import cv2
import dlib
import matplotlib.pyplot as plt
from imutils import face_utils


def detect(imgpath):
    frame = cv2.imread(imgpath)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    dnnFaceDetector = dlib.cnn_face_detection_model_v1("mmod_human_face_detector.dat")
    rects = dnnFaceDetector(gray, 1)
    for (i, rect) in enumerate(rects):
        x1 = rect.rect.left()
        y1 = rect.rect.top()
        x2 = rect.rect.right()
        y2 = rect.rect.bottom()

        # Rectangle around the face
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
    plt.imshow(frame)
    plt.show()


if __name__ == "__main__":
    detect('E:\Projects\iecse-event-review-system\Predict\Images\A1.jpg')