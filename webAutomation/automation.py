from selenium import webdriver

driver = webdriver.Chrome()
driver.get('https://youtube.com')

searchinput = driver.find_element_by_xpath('//*[@id="search"]')
searchinput.send_keys("Chill Trap Music")

searchButton = driver.find_element_by_xpath('//*[@id="search-icon-legacy"]')
searchButton.click()

playSong = driver.find_element_by_xpath('//*[@id="thumbnail"]')
playSong.click()