from appium import webdriver
import time
from appium_flutter_finder.flutter_finder import FlutterElement, FlutterFinder


desired_caps = {
  "platformName": "Android",
  "platformVersion": "10",
  "automationName": "flutter",
  "appActivity": ".MainActivity",
  "appPackage": "com.example.sayid_flutter_study_one",
  "deviceName": "2NSDU20411004107",
  "newCommandTimeout": 7200,
  "noReset": True
}

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

time.sleep(2)

finder = FlutterFinder()
text_finder = finder.by_text('You have pushed the button this many times:')


start_time = time.time()
element = FlutterElement(driver, text_finder)
end_time = time.time()

print("cost time is: {}".format(end_time - start_time))

start_time = time.time()
element.text
end_time = time.time()

print("cost time is: {}".format(end_time - start_time))

