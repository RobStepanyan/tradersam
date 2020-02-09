import sys, os
from selenium import webdriver
from pyvirtualdisplay import Display
from threading import Thread
from time import sleep
import datetime
from dateutil.relativedelta import relativedelta
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

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def dct_chunks(dct, n):
    """Return tuples with n-sized chunks from a dictinary(dct)."""
    lst = []
    for key, value in dct.items():
        lst.append((key, value))
    return list(chunks(lst, n))

def threads_by_chunks(target, c_list, n):
    """This function creates threads for each item, then executes them by n-sized chunks"""

    quanity = len(c_list)
    chunk_list = list(chunks(range(quanity), 3))
    threads = []
    for i in range(quanity):
        threads.append(Thread(target=target, args=(c_list[i],)))
    print('Threads are ready!')
    chunk_n = 1
    chunk_all = len(chunk_list)
    for l in chunk_list:
        for item in l:
            threads[item].start()
        for item in l:
            threads[item].join()
        
        print(f'Executed Chunk {chunk_n}/{chunk_all}')
        chunk_n += 1

# def live_threads_by_chunks(driver, target, dct, n):
#     """Takes a dictionary runs threads by n-sized chunks"""
#     lst_of_items = [(key, value) for key, value in dct.items()]
#     quanity = len(dct)
#     chunk_list = list(chunks(range(quanity), n))
#     threads = []
#     for i in range(quanity):
#         threads.append(Thread(target=target, args=(driver, lst_of_items[i][0], lst_of_items[i][1])))
#     print('Threads are ready!')
#     chunk_n = 1
#     chunk_all = len(chunk_list)
#     for l in chunk_list:
#         for item in l:
#             threads[item].start()
#         for item in l:
#             threads[item].join()
        
#         print(f'Executed Chunk {chunk_n}/{chunk_all}')
#         chunk_n += 1

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
    # display = Display(visible=0, size=(1000, 1000))
    # display.start()
    options = webdriver.ChromeOptions()
    prefs = {
        "profile.managed_default_content_settings.images":2,
        "profile.default_content_setting_values.notifications":2,
        "profile.managed_default_content_settings.stylesheets":2,
        "profile.managed_default_content_settings.plugins":1,
        "profile.managed_default_content_settings.popups":2,
        "profile.managed_default_content_settings.geolocation":2,
        "profile.managed_default_content_settings.media_stream":2,
    }
    options.add_experimental_option("prefs", prefs)
    options.add_argument('--no-sandbox')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
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

def execute_js_scripts_1y1m(driver, data_age):
    today = datetime.date.today()
    if data_age == '1y':
        start_date = today - relativedelta(years=+1)
        start_date = f'{start_date.month}/{start_date.day}/{start_date.year}'
    else:
        months = data_age[0] # '1m' -> 1
        start_date = today - relativedelta(months=+months)
        start_date = f'{start_date.month}/{start_date.day}/{start_date.year}'
    print('Executing JS scripts')
    driver.execute_script('$("#data_interval").val("Daily");')
    driver.find_element_by_id('data_interval').value = "Daily"
    driver.find_element_by_id('widgetFieldDateRange').click()
    driver.find_element_by_id('startDate').clear()
    driver.find_element_by_id('startDate').send_keys(start_date, Keys.ENTER)
    print('Executed JS scripts')
