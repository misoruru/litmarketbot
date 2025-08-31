from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
from multiprocessing import Process
import time

fake = Faker()

firefox_path = r"/path/to/firefox"
geckodriver_path = r"/path/to/geckodriver"

def create_tor_driver():
    profile = webdriver.FirefoxProfile()
    profile.set_preference("network.proxy.type", 1)
    profile.set_preference("network.proxy.socks", "127.0.0.1")
    profile.set_preference("network.proxy.socks_port", 9050)
    profile.set_preference("network.proxy.socks_remote_dns", True)
    profile.set_preference("permissions.default.image", 2)
    profile.set_preference("permissions.default.stylesheet", 2)
    profile.set_preference("gfx.downloadable_fonts.enabled", False)
    profile.set_preference("webgl.disabled", True)
    profile.update_preferences()

    options = Options()
    options.profile = profile
    options.binary_location = firefox_path
    options.page_load_strategy = "eager"

    service = Service(executable_path=geckodriver_path)
    driver = webdriver.Firefox(service=service, options=options)
    return driver


def run_bot(instance_id, target_url):
    driver = create_tor_driver()
    wait = WebDriverWait(driver, 20)

    try:
        driver.get(target_url)

        if instance_id % 400 == 0:
            time.sleep(2)
            try:
                btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "lmButton")))
                btn.click()
            except:
                pass

            time.sleep(2)
            email = fake.user_name() + "@gmail.com"
            password = fake.password()
            wait.until(EC.presence_of_element_located((By.ID, "email"))).send_keys(email)
            time.sleep(1)
            driver.find_element(By.ID, "password").send_keys(password)
            driver.find_element(By.XPATH, '//input[@value="Регистрация"]').click()
            time.sleep(3)

        try:
            read_button = driver.find_element(By.XPATH, '//span[text()="Читать онлайн"]/..')
            driver.execute_script("arguments[0].click();", read_button)
        except:
            pass

    except Exception:
        pass
    finally:
        driver.quit()


if __name__ == "__main__":
    target_url = "https://example.com"  # универсальный URL, можно менять
    processes = []
    for i in range(10):  # для примера запускаем 10 процессов
        p = Process(target=run_bot, args=(i+1, target_url))
        p.start()
        processes.append(p)
        time.sleep(1)

    for p in processes:
        p.join()
