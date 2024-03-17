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
            # как показала практика - эльдорадо часто меняют классы на своем сайте,
            # так что к моменту проверки данной лабораторной работы парсер может тут поломаться :(
            show_more = driver.find_element(By.CLASS_NAME, "vy")
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

#  Функция, с помощью которой читаем полученный HTML документ и возвращаем данные с 1 страницы
def get_html_info(file_path):
    with open(file_path, encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "html.parser")

    blocks = soup.findAll('span', attrs={'data-pc': 'offer_price'})

    prices_arr = []
    for data in blocks:
        price = data.text.replace('руб.', '').replace(' ', '')
        prices_arr.append(int(price))

    return prices_arr

# Функция, которая загружает несколько страниц и выводит общие данные по всем страницам
def parse(n):
    total_prices = []
    for i in range(1, n + 1):
        get_source_html(f"https://www.eldorado.ru/c/smartfony/b/APPLE?page={i}")
        total_prices = total_prices + get_html_info("source-page.html")

    avg_price = sum(total_prices) / len(total_prices)
    min_price = min(total_prices)
    max_price = max(total_prices)
    print(f'Минимальная цена:{min_price}, Средняя цена:{avg_price:.3f}, Максимальная цена: {max_price}')