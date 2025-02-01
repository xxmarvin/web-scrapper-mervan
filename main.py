from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, os

def kirmizi_metin(text):
    return f"\033[38;2;255;0;0m{text}\033[0m"  

def yesil_metin(text):
    return f"\033[38;2;0;190;0m{text}\033[0m" 

def sari_metin(text):
    return f"\033[38;2;255;255;0m{text}\033[0m"
os.system('cls' if os.name == 'nt' else 'clear')
opened_link = input(yesil_metin("Link Girin: "))
linnk = opened_link.replace("page=1", "page={page}")
desired_links = int(input(sari_metin("Kaç adet link çekmek istiyorsunuz: ")))

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--log-level=3")

driver = webdriver.Chrome(options=options)

collected_links = 0
page = 1  # Start from the first page

while collected_links < desired_links:
    driver.get(f"{linnk.format(page=page)}")
    wait = WebDriverWait(driver, 10)
    elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "jv-result-summary-title a")))

    for element in elements:
        link = element.get_attribute("href")
        if link is not None:
            with open("links.csv", "a", encoding="utf-8") as f:
                f.write(f"{link}\n")
            print(kirmizi_metin(link))
            collected_links += 1
            if collected_links >= desired_links:
                break

    if collected_links < desired_links:
        try:
            driver.execute_script('document.querySelector("#shared-pagination-next > a > span").click()')
            time.sleep(2)
            page += 1
            print(sari_metin(f"Sayfa: {page}"))
        except:
            print(kirmizi_metin("Tüm Sayfalar Çekildi!"))
            break
    else:
        break

driver.quit()
print(yesil_metin("Tüm linkler Çekildi! Veri Kazma Başlatılıyor!"))
os.system("python3 scrapper.py")
