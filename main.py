import fetch
total_prices = []
# количество страниц, которые надо спарсить(к сожалению из за защиты эльдорадо без капчи можно спарсить совсем немного)
total_pages = 5

for i in range(1, total_pages + 1):
    fetch.get_source_html(f"https://www.eldorado.ru/c/smartfony/b/APPLE?page={i}")
    total_prices = total_prices + fetch.parse("source-page.html")

avg_price = sum(total_prices) / len(total_prices)
min_price = min(total_prices)
max_price = max(total_prices)
print(f'Минимальная цена:{min_price}, Средняя цена:{avg_price:.3f}, Максимальная цена: {max_price}')