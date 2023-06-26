import time
import pyttsx3

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def handle_key_event(event):
    if event.name == 'z' and event.event_type == 'down':
        # Keydown event of 'z' detected
        print("Keydown event of 'z' detected")

import keyboard
# Register the key event handler
keyboard.on_press(handle_key_event)
engine = pyttsx3.init()
pause_length = 0.5
engine.setProperty('rate', 190)  # Adjust the speech rate if desired
engine.setProperty('pause', pause_length)

def handle_key_combinationA():
    print("Нажата комбинация клавиш")
def speak(text):
    engine.say(text)
    engine.runAndWait()


def go(cls,a=1,b=3):
    time.sleep(a)
    element = driver.find_element(By.CLASS_NAME, cls)
    element.click()
    print(cls)
    speak(str(i))
    time.sleep(b)
    driver.back()
#############################################################################
driver = webdriver.Chrome()
#url='https://andrei2.herokuapp.com/'
url='http://127.0.0.1:8001'

driver.get(url)

for i in range(1,17):
    s = f"hh{i}"
    go(s)

for i in range(1,23):
    s = f"mm{i}"
    go(s)

driver.quit()
'''
speak("вы находитесь на первой странице сайта Инструмент Ресурсного планирования ")




speak("Обратите внимание на то как устроена страница ")
speak("Вверху страницы - меню из четырех пунктов  ")
speak("Слева направо")
speak("   Домой  ")
speak( "  Проекты   ")
speak("  Ресурсы   ")
speak("  Балансы  ")
speak("Это меню висит на каждой странице сайта")
speak("Это позволяет нам вернуться сюда с любой страницы")
speak("Сейчас я перейду на другую страницу сайта")
speak("А вы попробуйте вернуться на первую страницу с помощью пункта Домой")


element_m1 = driver.find_element(By.CLASS_NAME, 'm1')
element_m1.click()


time.sleep(a)
element_m11 = driver.find_element(By.CLASS_NAME, 'm11')
element_m11.click()

wait = WebDriverWait(driver, 1000)
wait.until(EC.url_to_be(url))
speak("Отлично - вы справились")

speak("Теперь посмотрите на содержание")
speak("Некоторые его пункты помечены звездочкой")
speak("Это значит, что в текущей версии данную функцию может выполнить только администратор")

speak("Сечас мы сюда заходить не будем")
speak("Все остальные пункты содержания мы сейчас посмотрим")
speak("Портфель проектов")

element_m1 = driver.find_element(By.CLASS_NAME, 'm1')
element_m1.click()


time.sleep(a)
element_m11 = driver.find_element(By.CLASS_NAME, 'm11')
element_m11.click()
speak("В таблице представлены все проекты, которые сейчас идут в вашей организации")
speak("Справа - шкала времени, по месяцам")
speak("Слева - информация о проекте")
speak("Названия проектов можно кликать")
speak("Кликните одно из них")


speak("Теперь вы можете изменить данные проекта, например его сроки ")
speak("измените дату окончания и нажмите клавишу сохранить")
speak("у вас есть пять секунд чтобы изменить данные и сохранить их")
speak("проверьте что в портфеле проектов данные изменились")
time.sleep(5)

element_m11 = driver.find_element(By.CLASS_NAME, 'm0')
element_m11.click()

speak("Обратите внимание")
speak("на ту же страницу можно попасть используя верхнее меню - проекты - портфель проектов")


time.sleep(1)
element_m11 = driver.find_element(By.CLASS_NAME, 'm1')
element_m11.click()

time.sleep(1)
element_m11 = driver.find_element(By.CLASS_NAME, 'm11')
element_m11.click()

time.sleep(1)
element_m11 = driver.find_element(By.CLASS_NAME, 'm0')
element_m11.click()


speak("Итого")
speak("Для каждого пункта меню есть соотвествующий ему пункт содержания")
speak("Для каждого пункта содержания не помеченного звездочкой есть один пункт меню")
speak("Посмотрим другие пункты меню")

time.sleep(1)
element_m11 = driver.find_element(By.CLASS_NAME, 'm1')
element_m11.click()

time.sleep(1)
element_m11 = driver.find_element(By.CLASS_NAME, 'm12')
element_m11.click()

speak(" Эта таблица не только показывает руководителей проектов   но и дает им возможность действовать")




time.sleep(1)
element_m11 = driver.find_element(By.CLASS_NAME, 'm0')
element_m11.click()


speak(" Для продолжения осмотра нажмите клавишу Z")
keyboard.wait('z')

#######################################################################################################







time.sleep(b)


time.sleep(a)
element_m11 = driver.find_element(By.CLASS_NAME, 'm2')
element_m11.click()

time.sleep(a)
element_m11 = driver.find_element(By.CLASS_NAME, 'm21')
element_m11.click()

time.sleep(b)
element_m11 = driver.find_element(By.CLASS_NAME, 'm0')
element_m11.click()

time.sleep(a)
element_m11 = driver.find_element(By.CLASS_NAME, 'm2')
element_m11.click()

time.sleep(a)
element_m11 = driver.find_element(By.CLASS_NAME, 'm22')
element_m11.click()

time.sleep(b)
element_m11 = driver.find_element(By.CLASS_NAME, 'm0')
element_m11.click()

time.sleep(a)
element_m11 = driver.find_element(By.CLASS_NAME, 'm2')
element_m11.click()

time.sleep(a)
element_m11 = driver.find_element(By.CLASS_NAME, 'm23')
element_m11.click()

time.sleep(b)
element_m11 = driver.find_element(By.CLASS_NAME, 'm0')
element_m11.click()

time.sleep(a)
element_m11 = driver.find_element(By.CLASS_NAME, 'm3')
element_m11.click()

time.sleep(a)
element_m11 = driver.find_element(By.CLASS_NAME, 'm31')
element_m11.click()

time.sleep(b)
element_m11 = driver.find_element(By.CLASS_NAME, 'm0')
element_m11.click()


time.sleep(a)
element_m11 = driver.find_element(By.CLASS_NAME, 'm3')
element_m11.click()

time.sleep(a)
element_m11 = driver.find_element(By.CLASS_NAME, 'm32')
element_m11.click()

time.sleep(b)
element_m11 = driver.find_element(By.CLASS_NAME, 'm0')
element_m11.click()


time.sleep(a)
element_m11 = driver.find_element(By.CLASS_NAME, 'm3')
element_m11.click()

time.sleep(a)
element_m11 = driver.find_element(By.CLASS_NAME, 'm33')
element_m11.click()

time.sleep(b)
element_m11 = driver.find_element(By.CLASS_NAME, 'm0')
element_m11.click()


time.sleep(a)
element_m11 = driver.find_element(By.CLASS_NAME, 'm3')
element_m11.click()

time.sleep(a)
element_m11 = driver.find_element(By.CLASS_NAME, 'm34')
element_m11.click()



time.sleep(b)
element_m11 = driver.find_element(By.CLASS_NAME, 'm0')
element_m11.click()

time.sleep(a)
element_m11 = driver.find_element(By.CLASS_NAME, 'home2')
element_m11.click()

time.sleep(b)
element_m11 = driver.find_element(By.CLASS_NAME, 'm0')
element_m11.click()

time.sleep(a)
element_m11 = driver.find_element(By.CLASS_NAME, 'home3')
element_m11.click()

time.sleep(b)
element_m11 = driver.find_element(By.CLASS_NAME, 'm0')
element_m11.click()

time.sleep(a)
element_m11 = driver.find_element(By.CLASS_NAME, 'home4')
element_m11.click()

time.sleep(b)
element_m11 = driver.find_element(By.CLASS_NAME, 'm0')
element_m11.click()
time.sleep(c)

time.sleep(a)
element_m11 = driver.find_element(By.CLASS_NAME, 'home5')
element_m11.click()

time.sleep(b)
element_m11 = driver.find_element(By.CLASS_NAME, 'm0')
element_m11.click()

time.sleep(a)
element_m11 = driver.find_element(By.CLASS_NAME, 'home6')
element_m11.click()

time.sleep(b)
element_m11 = driver.find_element(By.CLASS_NAME, 'm0')
element_m11.click()


time.sleep(a)
element_m11 = driver.find_element(By.CLASS_NAME, 'home7')
element_m11.click()

time.sleep(b)
element_m11 = driver.find_element(By.CLASS_NAME, 'm0')
element_m11.click()

time.sleep(a)
element_m11 = driver.find_element(By.CLASS_NAME, 'home8')
element_m11.click()

time.sleep(b)
element_m11 = driver.find_element(By.CLASS_NAME, 'm0')
element_m11.click()

time.sleep(1)
element_m11 = driver.find_element(By.CLASS_NAME, 'home9')
element_m11.click()
print(334)
time.sleep(3)
elements = driver.find_elements(By.CLASS_NAME, 'brj')  # Returns a list of all elements with class 'm0'
desired_element = elements[3]  # Replace 'index' with the desired index
desired_element.click()  # Interact with the desired element

time.sleep(25)
element_m11 = driver.find_element(By.CLASS_NAME, 'm0')
element_m11.click()

time.sleep(1)
element_m11 = driver.find_element(By.CLASS_NAME, 'home9')
element_m11.click()

time.sleep(3)
print(333)
elements = driver.find_elements(By.CLASS_NAME, 'br')  # Returns a list of all elements with class 'm0'
desired_element = elements[3]  # Replace 'index' with the desired index
desired_element.click()  # Interact with the desired element

time.sleep(25)
element_m11 = driver.find_element(By.CLASS_NAME, 'm0')
element_m11.click()


time.sleep(1)
element_m11 = driver.find_element(By.CLASS_NAME, 'home9')
element_m11.click()

print(335)
time.sleep(3)
elements = driver.find_elements(By.CLASS_NAME, 'bj')  # Returns a list of all elements with class 'm0'
desired_element = elements[3]  # Replace 'index' with the desired index
desired_element.click()  # Interact with the desired element

time.sleep(25)
element_m11 = driver.find_element(By.CLASS_NAME, 'm0')
element_m11.click()
time.sleep(15)


# keyboard.add_hotkey('ctrl+b', handle_key_combinationB)
#
# def handle_key_combinationB():
#     # Ваш код для обработки события
#     print("Нажата комбинация клавиш")


# Создайте объект события, связанного с нажатием клавиши

'''