import cv2 as cv


def findFace(imgPath):
    from mtcnn.mtcnn import MTCNN
    detector = MTCNN()
    face = cv.imread(imgPath, cv.IMREAD_COLOR)
    result_list = detector.detect_faces(face)
    
    # get the number of faces
    noOfFaces = len(result_list)

    capTime = imgPath.split("_")[-1]
    capTime = capTime.split('.')[0]

    return capTime, noOfFaces

if __name__ == "__main__":
    pass