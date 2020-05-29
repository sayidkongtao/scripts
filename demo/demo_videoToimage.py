import numpy as np
import cv2 as cv
import os
import shutil
import time

PATH = lambda path: os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        path
    )
)


def frames_to_timecode(fps, frames):
    """
    视频 通过视频帧转换成时间
    :param fps: 视频帧率
    :param frames: 当前视频帧数
    :return:时间（00:00:01:01）
    """
    return '{0:02d}:{1:02d}:{2:02d}:{3:02d}'.format(int(frames / (3600 * fps)),
                                                    int(frames / (60 * fps) % 60),
                                                    int(frames / fps % 60),
                                                    int(frames % fps))


def get_screen_folder_path_and_clear():
    folder_name = "screenshot"

    folder_path = PATH(folder_name)

    if os.path.exists(folder_path):
        del_list = os.listdir(folder_path)
        for f in del_list:
            file_path = os.path.join(folder_path, f)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
    else:
        os.makedirs(folder_path)

    return folder_path


vc = cv.VideoCapture(r'C:\Users\Administrator\Desktop\work\test.mp4')

c = 0
folder_path = get_screen_folder_path_and_clear()

if vc.isOpened():
    rval, frame = vc.read()
else:
    rval = False

start_time = time.time()
while rval:
    rval, frame = vc.read()
    if not rval:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    c = c + 1
    cv.imwrite(os.path.join(folder_path, str(c) + '.jpg'), frame)


end_time = time.time()

print("cost time is: {}".format(end_time - start_time))
fps = vc.get(cv.CAP_PROP_FPS)
print("fps is: {}".format(fps))
print(frames_to_timecode(fps, c))
# while cap.isOpened():
#     ret, frame = cap.read()
#     # if frame is read correctly ret is True
#     if not ret:
#         print("Can't receive frame (stream end?). Exiting ...")
#         break
#     gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
#     cv.imshow('frame', gray)
#     if cv.waitKey(1) == ord('q'):
#         break
# cap.release()
# cv.destroyAllWindows()
