import sys, os
from selenium import webdriver
from pyvirtualdisplay import Display
from threading import Thread
from time import sleep
import datetime
from selenium.webdriver.common.keys import Keys

def print_exception(e):
    """This function takes e from "Exeption as e" and prints the details"""
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(f'{exc_type} {e} in {fname} at {exc_tb.tb_lineno}') # printing exception details

def validate_price(x):
    """This function return None if the len of passed argument is greater than specified number in the function"""
    if len(x)>=12:
        return None
    return x

def threads_by_chunks(target, c_list):
    """This function creates threads for each item, then executes them by chunks"""
    def chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    quanity = len(c_list)
    chunk_list = list(chunks(range(quanity), 3))
    threads = []
    for i in range(quanity):
        threads.append(Thread(target=target, args=(c_list[i],)))
    print('Threads are ready')
    chunk_n = 1
    chunk_all = len(chunk_list)
    for l in chunk_list:
        for sub_l in l:
            threads[sub_l].start()
            sleep(1)
        for sub_l in l:
            threads[sub_l].join()
        
        print(f'Executed Chunk {chunk_n}/{chunk_all}')
        chunk_n += 1

def remove_already_saved(l, c_list):
    """l is the list which contains links (urls) of already saved instances"""
    new_c_list = []
    for item in c_list:
        in_list = False
        for link in l:
            if link in item:
                in_list=True
        if not in_list:
            new_c_list.append(item)
    return new_c_list

def vps_selenium_setup():
    """This function creates virtual display and returns set up chrome driver.
    Execution time: ~ 1.2seconds"""
    display = Display(visible=0, size=(1000, 1000))
    display.start()
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument("--headless") 
    driver = webdriver.Chrome(options=options)
    return driver

def execute_js_scripts_max(driver):
    print('Executing JS scripts')
    driver.execute_script('$("#data_interval").val("Monthly");')
    driver.find_element_by_id('data_interval').value = "Monthly"
    driver.find_element_by_id('widgetFieldDateRange').click()
    driver.find_element_by_id('startDate').clear()
    driver.find_element_by_id('startDate').send_keys('01/01/1980', Keys.ENTER)
    print('Executed JS scripts, sleeping for 5 seconds')
    sleep(5)

def execute_js_scripts_5y(driver):
    startDate = datetime.datetime.now() - datetime.timedelta(days=5*365) # 5 Years ago today
    startDate = f'{startDate.month}/{startDate.day}/{startDate.year}'
    print('Executing JS scripts')
    driver.execute_script('$("#data_interval").val("Weekly");')
    driver.find_element_by_id('data_interval').value = "Weekly"
    driver.find_element_by_id('widgetFieldDateRange').click()
    driver.find_element_by_id('startDate').clear()
    driver.find_element_by_id('startDate').send_keys(startDate, Keys.ENTER)
    print('Executed JS scripts, sleeping for 5 seconds')
    sleep(5)