import cv2  # defining face detector


class VideoCamera(object):
    def __init__(self, ip):
        #self.video = cv2.VideoCapture(0)
        self.video = cv2.VideoCapture(0)
    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret,image = self.video.read()
        ret,jpeg = cv2.imencode('.jpg',image)
        return jpeg.tobytes()