import subprocess
import sys
import time
import signal
import os
import shutil


PATH = lambda path: os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        path
    )
)


def handler(signal_num):
    print("\nYou Pressed Ctrl-C.")
    sys.exit(signal_num)


def execute_cmd(cmd):
    popen = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)

    while True:
        buff = popen.stdout.readline()
        sys.stdout.write(buff.decode())
        if buff.decode() == '':
            break
    print("dd")


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


def get_screen_capture(folder_path, count):

    current_file = os.path.join(folder_path, "screenshot_{}.png".format(str(count)))

    os_command = "adb shell /system/bin/screencap -p /sdcard/screenshot.png&adb pull /sdcard/screenshot.png " + current_file
    subprocess.run(os_command, shell=True, check=True, stdout=subprocess.PIPE)


if __name__ == '__main__':
    # cmd = "adb shell screenrecord --verbose /sdcard/demo1.mp4"
    # execute_cmd(cmd)

    folder_path = get_screen_folder_path_and_clear()
    count = 0
    while True:
        print("Try to capture the screen")
        count = count + 1
        start_time = time.time()
        get_screen_capture(folder_path, count)
        end_time = time.time()
        print("cost time is: {}".format(end_time - start_time))

