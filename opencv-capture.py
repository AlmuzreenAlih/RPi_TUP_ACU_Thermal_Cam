import cv2

class OpenCvCapture:
    def __init__(self):
        for i in reversed(range(10)):
            cv2_cap = cv2.VideoCapture(i)
            if cv2_cap.isOpened():
                break

        if not cv2_cap.isOpened():
            print("Camera not found!")
            exit(1)

        self.cv2_cap = cv2_cap

    def show_video(self):
        cv2.namedWindow("lepton", cv2.WINDOW_NORMAL)
        print("Running, ESC or Ctrl-c to exit...")
        while True:
            ret, img = self.cv2_cap.read()

            if ret == False:
                print("Error reading image")
                break

            cv2.imshow("lepton", cv2.resize(img, (640, 480)))
            if cv2.waitKey(5) == 27:
                break

        cv2.destroyAllWindows()

if __name__ == '__main__':
    OpenCvCapture().show_video()
