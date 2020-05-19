from performance_script import Performance
import optparse

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

    if not options.package:
        parser.error("please provide the corresponding parameters")

    performance = Performance()

    performance.get_app_uninstall_time(options.package)


if __name__ == "__main__":
    main()