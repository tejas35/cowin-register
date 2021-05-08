from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os


class Register():

    def __init__(self, pincode, age="Age 18+", type=None):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome('./chromedriver', options=options)
        # self.driver = webdriver.Chrome('./chromedriver')
        self.driver.get("https://www.cowin.gov.in/home")
        self.pincode = pincode
        self.age = age
        self.type = type
        self.week = 0
        self.flag = False

    def notification(self):
        alarm = "alarm.wav"
        os.system(alarm)

    def filterbypin(self):
        pin = self.driver.find_element_by_id("mat-input-0")
        pin.clear()
        pin.send_keys(self.pincode)
        pin.send_keys(Keys.RETURN)
        time.sleep(5)

    def filtebyage(self):
        agefilter = self.driver.find_element_by_class_name("agefilterblock.filerandsearchblock")
        options = agefilter.find_elements_by_class_name("form-check.nomargright")
        arr = ["Age 18+", "Age 45+", "Covishield", "Covaxin", "Free", "Paid"]
        hashmap = {}
        for index, opts in enumerate(options):
            hashmap[arr[index]] = opts

        hashmap[self.age].click()
        if self.type != None:
            hashmap[self.type].click()
        # hashmap["Free"].click()

    def setkeys(self):
        self.rightbutt = self.driver.find_element_by_class_name("right.carousel-control.carousel-control-next")
        self.leftbutt = self.driver.find_element_by_class_name("left.carousel-control.carousel-control-prev")
        self.carousel_inner = self.driver.find_element_by_class_name("carousel-inner")

    def finddates(self):
        self.dates = self.carousel_inner.text.split("\n")
        print(self.dates)

    def setparams(self):
        self.filterbypin()
        self.filtebyage()
        self.setkeys()
        self.findslots()


    def findslots(self):
        self.finddates()
        matmain = self.driver.find_element_by_class_name("mat-main-field.center-main-field")
        rows = matmain.find_elements_by_class_name("row")
        for row in rows:
            if self.flag:
                break
            center_name = row.find_element_by_class_name("main-slider-wrap").text
            slots = row.find_element_by_class_name("slot-available-wrap")
            opts = slots.find_elements_by_class_name("slots-box")
            print(center_name)
            for date, opt in zip(self.dates, opts):
                if opt.text != "NA":
                    doses, type, age = opt.text.split("\n")
                    if doses != "Booked" and age == self.age:
                        print("date: "+ date + " doses: "+ doses + " type: " + type + " age: "+ age)
                        self.notification()
                        self.flag = True
                        break
        if self.flag == False:
            if self.week < 2:
                self.week += 1
                self.rightbutt.click()
                time.sleep(5)

            else:
                self.week = 0
                for _ in range(2):
                    self.leftbutt.click()
                    time.sleep(5)
            self.findslots()

if __name__ == '__main__':
    pincode = input("Please enter the pincode\n")
    age = input("please select from following => PS: select the number only[1 or 2] \n1. Age 18+\n2. Age 45+\n")
    age = "Age 18+" if age == "1" else "Age 45+"
    type = input("Which type would you prefer => PS: select the number only[1 or 2 or 3]\n1. Covisheild\n2. Covaxin\n3. Any\n")
    if type == "1":
        type = "Covishield"
    elif type == "2":
        type = "Covaxin"
    else:
        type = None

    citizen = Register(pincode, age, type)
    citizen.setparams()
