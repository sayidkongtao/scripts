import subprocess
import re
import shutil
import os
from aip import AipOcr
import json
import time


PATH = lambda path: os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        path
    )
)


def swipe_function():
    res = subprocess.run("adb shell dumpsys window displays", shell=True, check=True, stdout=subprocess.PIPE)
    output = str(res.stdout, encoding="utf-8")
    search_obj = re.search(r'(?<=app=)\d+x\d+', output, re.M | re.I)

    if search_obj:
        pixel_str = search_obj.group()
        print("The phone pixel is: " + pixel_str)
    else:
        raise Exception("Cannot get the phone pixel")

    phone_width = int(pixel_str.split("x")[0])
    print("The phone width: " + str(phone_width))

    phone_height = int(pixel_str.split("x")[1])
    print("The phone height: " + str(phone_height))

    print("Complete")

    start_x = phone_width / 2
    start_y = phone_height * 3 / 4

    end_x = phone_width / 2
    end_y = phone_height * 1 / 5

    os_command = "adb shell input swipe {} {} {} {}".format(start_x, start_y, end_x, end_y)
    print("Command is: " + os_command)

    scroll_count = 0
    folder_path = get_screen_folder_path_and_clear()
    content = get_conf()

    strat_time = time.time()
    while scroll_count < content["Scroll_Count"]:
        # 向上滑动屏幕
        subprocess.run(os_command, shell=True, check=True, stdout=subprocess.PIPE)
        scroll_count = scroll_count + 1
        if scroll_count >= content["Start_Count"]:
            get_screen_capture(folder_path, scroll_count)

    to_find_target_screenshot(strat_time)


def parse_xml_contains_str(target_str):

    with open(PATH("window_dump.xml"), encoding="utf-8") as f:
        content = f.read()

    if content.find(target_str) > -1:
        return True
    else:
        return False


def pull_file_to_current_folder():
    subprocess.run("adb shell uiautomator dump --compressed /sdcard/window_dump.xml",
                   shell=True, check=True, stdout=subprocess.PIPE)
    current_file = PATH("window_dump.xml")
    subprocess.run("adb pull /sdcard/window_dump.xml " + current_file, shell=True, check=True, stdout=subprocess.PIPE)


def get_screen_folder_path_and_clear():
    floder_name = "screenshot"

    folder_path = PATH(floder_name)

    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

    os.makedirs(folder_path)

    return folder_path


def get_screen_folder_path():
    folder_name = "screenshot"

    folder_path = PATH(folder_name)

    return folder_path


def get_screen_capture(folder_path, count):

    current_file = os.path.join(folder_path, "screenshot_{}.png".format(str(count)))

    os_command = "adb shell /system/bin/screencap -p /sdcard/screenshot.png&adb pull /sdcard/screenshot.png " + current_file
    subprocess.run(os_command, shell=True, check=True, stdout=subprocess.PIPE)


def to_find_target_screenshot(start_time):
    print("Td find the target screen and please wait since it will take some time")
    content = get_conf()

    APP_ID = content["APP_ID"]
    API_KEY = content["API_KEY"]
    SECRET_KEY = content["SECRET_KEY"]
    Target_Str = content["Target_Str"]

    aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    folder_path = get_screen_folder_path()
    all_screenshot_name_list = os.listdir(folder_path)

    is_find = False;

    for one_file in all_screenshot_name_list:
        file_name = os.path.join(folder_path, one_file)
        screen_shot_content = get_file_content(file_name)
        result = aipOcr.basicGeneral(screen_shot_content)
        if str(result["words_result"]).find(Target_Str) > -1:
            time_dif = os.path.getctime(file_name) - start_time
            print("Success to find the screenshot, is: " + file_name)
            print("The start time is: " + time.ctime(start_time))
            print("The end time is: " + time.ctime(os.path.getctime(file_name)))
            print("The spend time is: " + str(time_dif))
            is_find = True
            break

    if not is_find:
        raise Exception("Failed to find target after " + str(content["Scroll_Count"]) + "scroll screen")


def get_conf():
    with open(PATH("baidu_api.json"), encoding="utf-8") as f:
        content = json.load(f)

    return content


def get_file_content(screen_shot_file):
    with open(screen_shot_file, 'rb') as fp:
        return fp.read()


if __name__ == '__main__':
    swipe_function()
