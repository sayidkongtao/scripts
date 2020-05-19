import subprocess
import platform
import time
import re
import optparse
import csv


class Performance:
    def __init__(self):
        self.__find_str = self.__get_find_str()
        self.user_id = ""
        self.app_install_time = 0
        self.app_launch_time = 0
        # {"package_name":[(current_time, cpu, mem)]}
        self.app_cpu_mem = {}
        # [(current_time, receive_bytes, transmit_bytes)]
        self.app_network_traffic = []

    def get_app_install_time(self, app_file, package_name):
        command_uninstall = "adb uninstall " + package_name
        self.__run_cmd(command_uninstall, check=False)

        command_install = "adb install " + app_file
        app_install_start = time.time()

        self.__run_cmd(command_install)
        app_install_end = time.time()
        self.app_install_time = app_install_end - app_install_start
        print(self.app_install_time)

    def get_app_uninstall_time(self, package_name):
        command_uninstall = "adb uninstall " + package_name

        app_uninstall_start = time.time()

        self.__run_cmd(command_uninstall)
        app_uninstall_end = time.time()
        app_uninstall_time = app_uninstall_end - app_uninstall_start
        print(app_uninstall_time)

    def get_app_launch_time(self, app_package_name, app_main_activity):
        # Stop the app first
        command_stop = "adb shell am force-stop " + app_package_name
        self.__run_cmd(command_stop, check=False)

        command_launch = "adb shell am start -W -n {}/.{}".format(app_package_name, app_main_activity)
        ret = self.__run_cmd(command_launch)
        self.app_launch_time = re.search(r'(?<=ThisTime: )\d+', ret.stdout).group()

    def get_app_cpu_mem(self, app_package_name):
        command = "adb shell top -b -n 1 | {} {}".format(self.__find_str, app_package_name)

        while True:
            ret = self.__run_cmd(command)

            current_time = self.get_current_time()
            if len(ret) != 0:
                split_list = ret.split("\n")
                for one_node in split_list:
                    one_node_list = list(filter(lambda x: x != "", one_node.split(" ")))
                    one_package_name = one_node_list[11]
                    one_mem = one_node_list[9]
                    one_cpu = one_node_list[8]
                    if one_package_name in self.app_cpu_mem.keys():
                        self.app_cpu_mem[one_package_name].append((current_time, one_cpu, one_mem))
                    else:
                        self.app_cpu_mem[one_package_name] = [(current_time, one_cpu, one_mem)]
            else:
                for one_key in self.app_cpu_mem.keys():
                    self.app_cpu_mem[one_key] = [(current_time, 0, 0)]

    def get_app_network_traffic(self):
        command = "adb shell cat /proc/net/xt_qtaguid/stats | {} {}".format(self.__find_str, self.user_id)

        while True:
            if len(self.app_network_traffic) == 0:
                pre_total_rec = 0
                pre_total_tr = 0
            else:
                pre_total_rec = self.app_network_traffic[len(self.app_network_traffic) - 1][1]
                pre_total_tr = self.app_network_traffic[len(self.app_network_traffic) - 1][2]

            ret = self.__run_cmd(command)
            current_time = self.get_current_time()

            current_total_rec = 0
            current_total_tr = 0
            split_list = ret.split("\n")

            for one_node in split_list:
                one_node_list = one_node.split(" ")
                current_total_rec = current_total_rec + one_node_list[5]
                current_total_tr = current_total_tr + one_node_list[7]

            self.app_network_traffic.append(
                (current_time, current_total_rec - pre_total_rec, current_total_tr - pre_total_tr))

    def get_user_id(self, package_name):
        command = "adb shell dumpsys package {} | {} userId".format(package_name, self.__find_str)
        ret = self.__run_cmd(command)
        user_id = re.search(r'(?<=userId=)\d+', ret.stdout).group()
        return user_id;

    def get_current_time(self):
        currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return currentTime

    def __run_cmd(self, command, check=True):
        ret = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        if check:
            if ret.returncode == 0:
                print("Success to execute command: " + command, ret.stdout)
                return ret.stdout.strip()
            else:
                print("Failed to execute command: " + command, ret.stderr)

    def __get_platform(self):
        platform_type = platform.system()
        print("platform_type is: " + platform_type)
        return platform_type

    def __get_find_str(self):
        platform_type = self.__get_platform()
        if platform_type == "Windows":
            return "findstr"
        return "grep"


def main():
    usage = "python %prog -p <package name> -a <main activity> -f <app file> -i <interval>"
    parser = optparse.OptionParser(usage)
    parser.add_option('-p', dest='package', type='string', help='package name')
    parser.add_option('-a', dest='activity', type='string', help='main  activity')
    parser.add_option('-f', dest='file', type='string', help='app file')
    parser.add_option('-i', dest='interval', type='int', help='interval', default=3)

    (options, args) = parser.parse_args()
    print(options.package)
    print(options.activity)
    print(options.file)
    print(options.interval)

    # not options.package or not options.activity or

    if not options.file:
        parser.error("please provide the corresponding parameters")

    performance = Performance()

    performance.get_app_install_time(options.file, options.package)


def test():
    a = [("a","b","c"), (1,1,1), (2,2,2)]
    with open("csv_test.txt", "w", newline='') as write_csvfile:
        writer = csv.writer(write_csvfile)
        writer.writerows(a)


if __name__ == "__main__":
    main()



