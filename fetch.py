from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

#  Функция, с помощью которой получаем полностью прогруженный HTML документ
def get_source_html(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    try:
        driver.get(url=url)
        #  Задержка чтобы страница успела прогрузится и можно было ввести капчу(если таковая вылезет)
        time.sleep(10)
        #  Переменная, которая отвечает за количество прокруток вниз по странице
        count_scroll = 0

        while True:
            show_more = driver.find_element(By.CLASS_NAME, "Yq")
            if count_scroll < 3:
                #  Листаем вниз с интервалом в 2 секунды
                actions = ActionChains(driver)
                actions.move_to_element(show_more).perform()
                time.sleep(2)
                count_scroll += 1
            else:
                # Когда долистали страницу, сохраняем полученный HTML в файл
                with open("source-page.html", "w", encoding="utf-8") as file:
                    file.write(driver.page_source)
                break

    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()

#  Функция, с помощью которой читаем полученный HTML документ и получаем/выводим данные о ценах
def parse(file_path):
    with open(file_path, encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "html.parser")

    blocks = soup.findAll('span', attrs={'data-pc': 'offer_price'})

    prices_arr = []
    for data in blocks:
        price = data.text.replace('руб.', '').replace(' ', '')
        prices_arr.append(int(price))

    avg_price = sum(prices_arr) / len(prices_arr)
    min_price = min(prices_arr)
    max_price = max(prices_arr)
    print(f'Минимальная цена:{min_price}, Средняя цена:{avg_price:.3f}, Максимальная цена: {max_price}')