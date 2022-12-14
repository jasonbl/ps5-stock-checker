import os

from dotenv import load_dotenv
from random_user_agent.params import SoftwareName, OperatingSystem
from random_user_agent.user_agent import UserAgent
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from PlaystationSeller import PlaystationSeller
from textSender import sendInStockText

software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value, OperatingSystem.MAC_OS_X.value]
user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)

def build_web_driver():
    load_dotenv()

    user_agent = user_agent_rotator.get_random_user_agent()
    print(user_agent)

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(f"user-agent={user_agent}")

    return webdriver.Remote(
        command_executor=os.getenv('REMOTE_DRIVER_URL'),
        # executable_path='./chromedriver',
        options=options,
    )

def check_amazon(driver: WebDriver):
    print("Checking Amazon...")
    driver.get(PlaystationSeller.AMAZON.url)

    wait = WebDriverWait(driver, timeout=3)
    wait.until(lambda d: d.find_elements_by_id("outOfStock") or d.find_elements_by_id("add-to-cart-button"))
    try:
        driver.find_element_by_id("add-to-cart-button")
        sendText(PlaystationSeller.AMAZON)
    except NoSuchElementException:
        print("Unavailable")

def check_game_stop(driver: WebDriver):
    print("Checking GameStop...")
    driver.get(PlaystationSeller.GAME_STOP.url)

    wait = WebDriverWait(driver, timeout=3)
    add_to_cart_button = wait.until(lambda d: d.find_elements_by_class_name("add-to-cart"))[0]
    if add_to_cart_button.text.lower() == "add to cart":
        sendText(PlaystationSeller.GAME_STOP)
    else:
        print("Unavailable")

def check_best_buy(driver: WebDriver):
    print("Checking Best Buy...")
    driver.get(PlaystationSeller.BEST_BUY.url)

    wait = WebDriverWait(driver, timeout=5)
    add_to_cart_button = wait.until(lambda d: d.find_elements_by_class_name("add-to-cart-button"))[0]
    if add_to_cart_button.text.lower() == "add to cart":
        sendText(PlaystationSeller.BEST_BUY)
    else:
        print("Unavailable")

def check_target(driver: WebDriver):
    print("Checking Target...")
    driver.get(PlaystationSeller.TARGET.url)

    wait = WebDriverWait(driver, timeout=3)

    # Purposely looking for the sold out block first because Target sometimes loads the purchase button
    # before it realizes stock isn't available
    try:
        wait.until(lambda d: d.find_elements_by_css_selector("div[data-test=soldOutBlock]"))
        print("Unavailable")
        return
    except TimeoutException:
        pass

    wait.until(lambda d: d.find_elements_by_css_selector("button[data-test=shipItButton]"))
    sendText(PlaystationSeller.TARGET)

def sendText(source: PlaystationSeller):
    print("PS5 in stock at " + source.seller_name + ". Sending text...")
    sendInStockText(source.seller_name, source.url)
    print("Text successfully sent")

def check_stock(event, context):
    seller = event["seller"]
    with build_web_driver() as driver:
        if seller == "AMAZON":
            check_amazon(driver)
        elif seller == "GAME_STOP":
            check_game_stop(driver)
        elif seller == "BEST_BUY":
            # Best Buy appears to block web traffic coming from AWS, so this won't work remotely
            check_best_buy(driver)
        elif seller == "TARGET":
            check_target(driver)
        # Walmart not included because it blocks all headless browser requests
        else:
            raise ValueError("Invalid seller: " + seller)

if __name__ == "__main__":
    event = {
        "seller": "TARGET"
    }
    check_stock(event, None)
