from dearpygui import dearpygui as dpg
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException,ElementClickInterceptedException,TimeoutException,NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.alert import Alert
from os import sys

#this script will serve as a test program for xperimenting with xpaths while writing automation code.

class Menus:
    def main_menu():
        if dpg.does_item_exist("main_menu"):
            dpg.show_item("main_menu")
        else:
            with dpg.window(label="Selector Path Testing",tag="main_menu",width=650,height=750):
                dpg.add_text("")
                #start new global driver instance for testing
                dpg.add_button(label="Start new driver instance",callback=start_driver)
                dpg.add_text("")

                #these fields do not do anything yet.
                with dpg.group(horizontal=True):
                    dpg.add_text("Implicit Wait? ")
                    dpg.add_checkbox(tag="driverImplicitWait",default_value=True)
                with dpg.group(horizontal=True):
                    dpg.add_text("Implicit Wait Time (seconds):")
                    dpg.add_input_int(tag="driverImplicitWaitTime",default_value=3,width=100,on_enter=True,callback=setImplicitWait)
                dpg.add_text("Once turned on, it cannot be turned off until new driver instance is made.")
                dpg.add_button(label="Update Implicit Wait Time",callback=setImplicitWait)

                dpg.add_text("")
                #field for telling the driver what URL to go to to start
                dpg.add_text("Target URL")
                with dpg.group(horizontal=True):
                    dpg.add_text("URL: ")
                    dpg.add_input_text(tag="DriverURL",default_value="http://",on_enter=True,callback=Testing.get_url)
                dpg.add_button(label="driver.get('url')",callback=Testing.get_url)
                dpg.add_text("")

                #field for selector type
                dpg.add_text("Selector Type")
                dpg.add_radio_button(['id','class','name','xpath','css'],tag='selectorType',default_value='xpath')
                dpg.add_text("")

                #field for selector action
                dpg.add_text("Selector Action")
                dpg.add_radio_button(['clear','click','type'],tag='selectorAction',default_value='click')
                dpg.add_text("")

                #additional field if selector action is type, then which something needs to be typed...
                dpg.add_text("If Selector Action is set to Type, please specify what is being typed.")
                with dpg.group(horizontal=True):
                    dpg.add_text("Typing Content: ")
                    dpg.add_input_text(tag='selectorText')
                dpg.add_text("")

                #field for selector Path
                with dpg.group(horizontal=True):
                    dpg.add_text("Selector Path: ")
                    dpg.add_input_text(tag="selectorPath")
                dpg.add_button(label="Perform Action",callback=Testing.selectorTest)
                dpg.add_text("---Result---")
                with dpg.group(horizontal=True):
                    dpg.add_text("Selector Action Test Result: ")
                    dpg.add_text(tag="selectorResult",default_value="None")


class Testing:
    #send driver instance to target url
    def get_url():
        try:
            driver.get(dpg.get_value("DriverURL"))
            Testing.Result(True)
        except:
            Testing.Result(False)
    
    #function for performing the selector action
    def selectorTest():
        selectorPath = dpg.get_value("selectorPath")
        selectorType = dpg.get_value("selectorType")
        selectorAction = dpg.get_value("selectorAction")
        selectorText = dpg.get_value("selectorText")

        #logic for determining what function within the sel class to call
        if selectorAction == 'clear':
            sel.clear(selectorType,selectorPath)
        elif selectorAction == 'click':
            sel.click(selectorType,selectorPath)
        elif selectorAction == 'type':
            sel.type(selectorType,selectorPath,selectorText)

    
    def Result(result):
        if result == True:
            resultText = "Successful"
        else:
            resultText = "Failed"
        dpg.set_value("selectorResult",resultText)

#creates driver instance globally
def start_driver():
    global driver
    driver = webdriver.Chrome(r'ChromeDriver/chromedriver.exe')
    setImplicitWait()
    return driver

def setImplicitWait():
    global driver
    if dpg.get_value("driverImplicitWait") == False:
        return
    implicitWaitTime = dpg.get_value("driverImplicitWaitTime")
    if implicitWaitTime < 0:
        print("invalid input for implicit wait time, skipping function.")
        return
    else:
        driver.implicitly_wait(implicitWaitTime)
        print("driver set to have implicit wait of " + str(implicitWaitTime) + " seconds.")
        return driver

"""modified sel class for selector path testing. The main changes will be that sys.press_enter() will be removed and will be returning true or false for a result variable
based on if an exception was raised."""

class sel:
    def value(element_type,element):
        if element_type in ['class_name']:
            try:
                element_value = driver.find_element_by_class_name(element).text()
                
                return element_value
            except:
                print("error")
        if element_type in ['xpath']:
            try:
                element_value = driver.find_element_by_xpath(element)
                print(element_value)
                element_value = element_value.text()
                

                return element_value
            except:
                print("error")

    def click(element_type,element):
        if element_type in ['id']:
            try:
                driver.find_element_by_id(element).click()
                Testing.Result(True)
            except:
                Testing.Result(False)

        if element_type in ['class']:
            try:
                driver.find_element_by_class_name(element).click()
                Testing.Result(True)
            except:
                Testing.Result(False)

        if element_type in ['name']:
            try:
                driver.find_element_by_name(element).click()
                Testing.Result(True)
            except:
                Testing.Result(False)

        if element_type in ['xpath']:
            try:
                driver.find_element_by_xpath(element).click()
                Testing.Result(True)
            except:
                Testing.Result(False)

        if element_type in ['css']:
            try:
                driver.find_element_by_css_selector(element).click()
                Testing.Result(True)
            except:
                Testing.Result(False)

    def type(element_type,element,data):
        if element_type in ['id']:
            try:
                driver.find_element_by_id(element).send_keys(data)
                Testing.Result(True)
            except:
                Testing.Result(False)

        if element_type in ['class']:
            try:
                driver.find_element_by_class_name(element).send_keys(data)
                Testing.Result(True)
            except:
                Testing.Result(False)

        if element_type in ['name']:
            try:
                driver.find_element_by_name(element).send_keys(data)
                Testing.Result(True)
            except:
                Testing.Result(False)

        if element_type in ['xpath']:
            try:
                driver.find_element_by_xpath(element).send_keys(data)
                Testing.Result(True)
            except:
                Testing.Result(False)

        if element_type in ['css']:
            try:
                driver.find_element_by_css_selector(element).send_keys(data)
                Testing.Result(True)
            except:
                Testing.Result(False)

    def clear(element_type,element):
        if element_type in ['id']:
            try:
                driver.find_element_by_id(element).clear()
                Testing.Result(True)
            except:
                Testing.Result(False)

        if element_type in ['name']:
            try:
                driver.find_element_by_name(element).clear()
                Testing.Result(True)
            except:
                Testing.Result(False)

        if element_type in ['xpath']:
            try:
                driver.find_element_by_xpath(element).clear()
                Testing.Result(True)
            except:
                Testing.Result(False)

        if element_type in ['css']:
            try:
                driver.find_element_by_css_selector(element).clear()
                Testing.Result(True)
            except:
                Testing.Result(False)

    def find(element_type,element):
        if element_type in ['id']:
            try:
                driver.find_element_by_id(element)
                Testing.Result(True)
            except:
                Testing.Result(False)
        
        if element_type in ['class']:
            try:
                driver.find_element_by_class_name(element)
                Testing.Result(True)
            except:
                Testing.Result(False)

        if element_type in ['name']:
            try:
                driver.find_element_by_name(element)
                Testing.Result(True)
            except:
                Testing.Result(False)

        if element_type in ['xpath']:
            try:
                driver.find_element_by_xpath(element)
                Testing.Result(True)
            except:
                Testing.Result(False)
        
        if element_type in ['css']:
            try:
                driver.find_element_by_css_selector(element)
                Testing.Result(True)
            except:
                Testing.Result(False)

if __name__ == '__main__':
    dpg.create_context()
    dpg.create_viewport(title="Selector Path Tester")
    dpg.setup_dearpygui()


    Menus.main_menu()

    #this goes at the very end of the script
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()