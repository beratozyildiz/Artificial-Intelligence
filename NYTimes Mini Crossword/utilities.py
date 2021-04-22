from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

def create_driver():
    if flag:
        print("\nInitializing the web driver...\n")
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    # driver.maximize_window()
    return driver


def get_to_the_page(driver):
    if flag:
        print('\nGoing to the "https://www.nytimes.com/crosswords/game/mini"...')
        driver.get("https://www.nytimes.com/crosswords/game/mini")
        ok = driver.find_element_by_css_selector('#root > div > div > div.app-mainContainer--3CJGG > div > main > div.layout > div > div.Veil-veil--3oKaF.Veil-stretch--1wgp0 > div.Veil-veilBody--2x-ZE.Veil-autocheckMessageBody--31wj3 > div > article > div.buttons-modalButtonContainer--35RTh > button')
        print('Arrived to the page trying to get ok button...')
        time.sleep(4)
        ok.click()
        print('Clicked to the ok button...')
    else:
        driver.get("https://www.nytimes.com/crosswords/game/mini")
        ok = driver.find_element_by_css_selector('#root > div > div > div.app-mainContainer--3CJGG > div > main > div.layout > div > div.Veil-veil--3oKaF.Veil-stretch--1wgp0 > div.Veil-veilBody--2x-ZE.Veil-autocheckMessageBody--31wj3 > div > article > div.buttons-modalButtonContainer--35RTh > button')
        time.sleep(3)
        ok.click()

def get_clues(driver):
    if flag:
        print("Downloading the clues...")
    clue_elements = driver.find_elements_by_class_name('Clue-text--3lZl7')
    across_clues = [element.text for element in clue_elements[:5]]
    down_clues = [element.text for element in clue_elements[5:]]
    if flag:
        print("Clues are downloaded...")
    return across_clues , down_clues

def reveal(driver):
    if flag:
        print("Revealing the answers before downloading puzzle grid...")
    reveal1 = driver.find_element_by_css_selector('#root > div > div > div.app-mainContainer--3CJGG > div > main > div.layout > div > div.Toolbar-wrapper--1S7nZ > ul > div.Toolbar-expandedMenu--2s4M4 > li:nth-child(2)')
    ac1 = ActionChains(driver)
    ac1.move_to_element(reveal1).move_by_offset(0, 0).click().perform()
    time.sleep(2)

    ac2 = ActionChains(driver)
    puzzle = driver.find_element_by_xpath( '//*[@id="root"]/div/div/div[4]/div/main/div[2]/div/div/ul/div[2]/li[2]/ul/li[3]/a')
    ac2.move_to_element(puzzle).move_by_offset(0, 0).click().perform()
    time.sleep(2)

    ac3 = ActionChains(driver)
    reveal2 = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/article/div[2]/button[2]/div/span')
    ac3.move_to_element(reveal2).move_by_offset(0, 0).click().perform()
    close_button = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/span')
    close_button.click()

def get_answers(driver):
    if flag:
        print("Downloading the puzzle grid with answers...")
    cells = []

    for i in range(0,25):
        css_link = "".join(['#xwd-board > g:nth-child(5) > g:nth-child(', str(i + 1), ')'])
        if not driver.find_elements_by_css_selector(css_link):
            cells.append('')
        else:
            cells.append(driver.find_elements_by_css_selector(css_link)[0].text.split("\n"))

    cells_matrix = []
    for j in range(5):
        cells_matrix.append(cells[j*5:(j+1)*5])



    return cells_matrix



def conversion(cells_matrix,across,down):
    if flag:
        print("Converting the info to the form our system uses...")
    # Across Keys
    result = {}


    across_clues = {}
    across_values = {}
    across_keys = []

    for i in range(len(cells_matrix)):
        for j in range(len(cells_matrix[0])):
            if len(cells_matrix[i][j]) == 2:
                across_key_number = cells_matrix[i][j][0]
                across_index = 5*i + j
                across_key = across_key_number + 'A'
                across_keys.append(across_key)
                value = []
                value.append(across_index)
                answer = ''
                for k in range(j,5):
                    if len(cells_matrix[i][k]) == 2:
                        answer += cells_matrix[i][k][1]
                    elif len(cells_matrix[i][k]) == 1:
                        if cells_matrix[i][k][0] != '':
                            answer += cells_matrix[i][k][0]
                        else:
                            break
                value.append(answer)
                across_values[across_key] = value
                break


    across_keys.sort()
    for i in range(len(across_keys)):
        across_clues[across_keys[i]] = across[i]
    for i in range(len(across_values.keys())):
        x = across_values[across_keys[i]]
        x.append(across_clues[across_keys[i]])
        result[across_keys[i]] = x




    # Down Keys
    down_clues = {}
    down_values = {}
    down_keys = []

    for i in range(len(cells_matrix)):
        for j in range(len(cells_matrix[0])):
            if len(cells_matrix[j][i]) == 2:
                down_key_number = cells_matrix[j][i][0]
                down_index = 5*j + i
                down_key = down_key_number + 'D'
                down_keys.append(down_key)
                value = []
                value.append(down_index)
                answer = ''
                for k in range(j, 5):
                    if len(cells_matrix[k][i]) == 2:
                        answer += cells_matrix[k][i][1]
                    elif len(cells_matrix[k][i]) == 1:
                        if cells_matrix[k][i][0] != '':
                            answer += cells_matrix[k][i][0]
                        else:
                            break
                value.append(answer)
                down_values[down_key] = value
                break


    down_keys.sort()
    for i in range(len(down_keys)):
        down_clues[down_keys[i]] = down[i]
    for i in range(len(down_values.keys())):
        x = down_values[down_keys[i]]
        x.append(down_clues[down_keys[i]])
        result[down_keys[i]] = x
    return result

def download_puzzle(single_stepping = False):
    global flag
    flag = single_stepping
    driver = create_driver()
    get_to_the_page(driver)
    
    across, down = get_clues(driver)
    
    reveal(driver)
    
    cells_matrix = get_answers(driver)
    time.sleep(2)
    driver.close()
    result = conversion(cells_matrix,across,down)
    if flag:
        print("Input of the system is ready...")
    return result
