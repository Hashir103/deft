# type: ignore
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import asyncio

async def getTickets(url: str) -> list: 
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--disable-gpu")  # Disable GPU for headless mode
    chrome_options.add_argument('window-size=1920x1080');
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(options=chrome_options)

    # Seats Available
    seat_available = False

    # Navigate to the web page containing the iframe
    driver.get(url)

    # Switch to the iframe
    iframe = driver.find_element(By.ID, "product_detail_area")
    driver.switch_to.frame(iframe)

    # Locate the element with the "Select Date" dropdown
    play_date_dropdown = driver.find_element(By.ID, "play_date")

    # Click the dropdown to trigger the loading of options
    play_date_dropdown.click()

    # Wait for the date options to load (adjust the timeout as needed)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, "//select[@id='play_date']//option[2]")))

    # Now, you can select the 2nd option (index 1)
    play_date_select = Select(play_date_dropdown)
    play_date_select.select_by_index(1)

    # Locate the element with the "Select Time" dropdown
    play_time_dropdown = driver.find_element(By.ID, "play_time")

    # Click the dropdown to trigger the loading of options
    play_time_dropdown.click()

    # Wait for the time options to load (adjust the timeout as needed)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, "//select[@id='play_time']//option[2]")))

    # Now, you can select the 2nd option (index 1)
    play_time_select = Select(play_time_dropdown)
    play_time_select.select_by_index(1)
    
    # Wait for the "Available Seats" element to be populated
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table")))

    
    # Get and print the remaining seats table
    remaining_seats_element = driver.find_element(By.ID, "remain_seat")
    remaining_seats_html = remaining_seats_element.get_attribute('innerHTML')

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(remaining_seats_html, 'html.parser')

    # Extract tier information and seat counts into a dictionary
    tier_seat_dict = {}
    for strong_tag in soup.find_all('strong'):
        tier = strong_tag.text
        seat_info = strong_tag.next_sibling.strip()
        seat_count = int(seat_info.split(" ")[0])
        if seat_count > 0: 
            seat_available = True
        tier_seat_dict[tier] = seat_count
    
    # Switch back to the default content
    driver.switch_to.default_content()

    # Close the browser
    driver.quit()

    return [seat_available, tier_seat_dict]

async def printTicket(tier_seat_dict: dict):
    # Print the dictionary
    s = ""
    for tier, seat_count in tier_seat_dict.items():
        s+= f"{tier}: {seat_count}\n"

    return s