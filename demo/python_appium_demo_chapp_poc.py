from appium import webdriver
import time


desired_caps = {
  "platformName": "Android",
  "platformVersion": "10",
  "automationName": "UiAutomator2",
  "appActivity": ".MainActivity",
  "appPackage": "com.example.chapp_poc",
  "deviceName": "2NSDU20411004107",
  "newCommandTimeout": 7200,
  "noReset": True
}

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

time.sleep(2)

start_time = time.time()
btn = driver.find_element_by_xpath("//*[contains(@text, '纽崔莱')]")
end_time = time.time()

print("cost time is: {}".format(end_time - start_time))

start_time = time.time()
btn.click()
end_time = time.time()

print("cost time is: {}".format(end_time - start_time))

