from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

price_sum = 0
price_count = 0

name_list = []


browser = webdriver.Chrome('chromedriver')
browser.get('http://www.globaldata.pt')
browser.maximize_window()
search_bar = browser.find_element_by_id('search')
search_bar.send_keys('Gráfica MSI RX5700', Keys.ENTER)

categorias=browser.find_element_by_xpath('//*[@id="instant-search-facets-container"]/div[3]/div/div')
componentes=categorias.find_elements_by_xpath("//a[contains(text(),'Componentes')]")
componentes[0].click()


#loop paginas
while True:

    products = browser.find_elements_by_class_name('product-item-link')
    for product in products:
        name = product.get_attribute('text').replace('\n', '').strip()
        link = product.get_attribute('href')

        #workaround for globaldata loop trap
        if name in name_list:
            break
        else:
            name_list.append(name)

        #open new browser to fetch some info
        new_browser = webdriver.Chrome('chromedriver')
        new_browser.get(link)
        new_browser.maximize_window()
        price = float(new_browser.find_element_by_class_name('price').text.replace('€', '').strip().replace(',', '.'))
        price_count = price_count + 1
        price_sum = price_sum + price
        print("%3.2f %s" % (price, name))

        new_browser.close()

    prox_pag = browser.find_elements_by_xpath("//a[contains(text(),'Próxima página')]")
    if not prox_pag:
        break
    prox_pag[0].click()

print('')
print('Average price for "Gráfica MSI RX5700 is %3.2f' % (price_sum/price_count))

browser.close()