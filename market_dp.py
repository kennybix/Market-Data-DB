# import necessary libraries

from dp_utils import *


# 1. Download the data
try:
    # Initialize the WebDriver
    driver = initialize_driver()
    
    download_data(driver, link_extension = 'd_us_txt', captcha=True)
    # Navigate back to the previous webpage driver.back()
    # driver.back()
    time.sleep(5)
    download_data(driver, link_extension = 'd_uk_txt', captcha=False)
    time.sleep(7)
    # driver.back()
    download_data(driver, link_extension = 'd_hk_txt', captcha=False)
    time.sleep(9)
    # driver.back()
    download_data(driver, link_extension = 'd_macro_txt', captcha=False)
    time.sleep(10)
    download_data(driver, link_extension = 'd_world_txt', captcha=False)
    time.sleep(600)

except Exception as e:
    print("An error occurred:", str(e))

finally:
    # driver.quit()
    driver = None

# also onboard the world dataset: currencies, crypto, indices etc

# 2. move all the files from downloads to the raw folder
move_market_data(filename='d_us_txt.zip')
move_market_data(filename='d_uk_txt.zip')
move_market_data(filename='d_hk_txt.zip')
move_market_data(filename='d_macro_txt.zip')


# # 3. Proceed with the extraction
move_us_market_data()
move_uk_market_data()
move_hk_market_data()
move_macro_data()


# 4. Delete raw -- only if previous steps are successful
delete_folder()