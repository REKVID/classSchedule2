

# ПО ЧЕЛЕВЕЧЕСКИ НАДО РАСКИДАТЬ ВЕСЬ КОД ПО ФАЙЛАМ КЛАССОВ НО ПОХУЙ

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

class Lesson:
    def __init__(self, time_slot, auditory, subject, teacher, date):
        self.time_slot = time_slot
        self.auditory = auditory
        self.subject = subject
        self.teacher = teacher
        self.date = date

    def __str__(self):
        return (f"  Время: {self.time_slot}, Аудитория: {self.auditory}, "
                f"Предмет: {self.subject}, Преподаватель: {self.teacher}, Дата: {self.date}")


class DaySchedule:
    def __init__(self, title):
        self.title = title
        self.lessons = []

    def add_lesson(self, lesson):
        self.lessons.append(lesson)

    def __str__(self):
        result = f"{self.title}:\n"
        for lesson in self.lessons:
            result += str(lesson) + "\n"
        return result


class WebDriverConfig:
    def __init__(self, driver_path):
        self.driver_path = driver_path

    def create_driver(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        service = Service(self.driver_path)
        return webdriver.Chrome(service=service, options=options)


class ScheduleFetcher:
    def __init__(self, driver):
        self.driver = driver

    def open_site(self, url):
        self.driver.get(url)
        time.sleep(2)  # читай ниже

    def enter_group_number(self, group_number):
        group_input = self.driver.find_element(By.CLASS_NAME, "groups")
        group_input.send_keys(group_number)
        time.sleep(1)

    def click_group(self, group_number):
        group_element = self.driver.find_element(By.ID, group_number)
        group_element.click()

    def wait_for_schedule(self):
        time.sleep(1)  # !!!! ЕСТЬ НАМНОГО БОЛЕЕ ПРАВИЛЬНЫЙ СПОСОБ НЕ ОБОСРАТЬСЯ НА
                                # НЕПРОГРУЖЕННОЙ СТРАНИЦЕ НО ОН ИНОГДА БАГАЕТСЯ ХЗ ПОЧЕМУ
                                # ЕСЛИ ХОЧЕШЬ ИСПРАВИТЬ ЧЕКНИ webdriverWait

    def fetch_schedule(self):
        schedule_days = self.driver.find_elements(By.CLASS_NAME, "schedule-day")
        if not schedule_days:
            print("Хуй тебе а не расписание..")
            return

        week_schedule = []
        for day in schedule_days:
            title = day.find_element(By.CLASS_NAME, "schedule-day__title").text
            day_schedule = DaySchedule(title)
            pairs = day.find_elements(By.CLASS_NAME, "pair")
            for pair in pairs:
                time_slot = pair.find_element(By.CLASS_NAME, "time").text
                lessons = pair.find_elements(By.CLASS_NAME, "schedule-lesson")
                for lesson in lessons:
                    auditory = lesson.find_element(By.CLASS_NAME, "schedule-auditory").text
                    subject = lesson.find_element(By.CLASS_NAME, "bold").text
                    teacher = lesson.find_element(By.CLASS_NAME, "teacher").text
                    date = lesson.find_element(By.CLASS_NAME, "schedule-dates").text
                    lesson_obj = Lesson(time_slot, auditory, subject, teacher, date)
                    day_schedule.add_lesson(lesson_obj)
            week_schedule.append(day_schedule)

        self.print_week_schedule(week_schedule)

    def print_week_schedule(self, week_schedule):
        for day in week_schedule:
            print(day)
        print()


def main():
    driver_path = '/opt/homebrew/bin/chromedriver'  # !!!!!!! СВОЙ ПУТЬ УКАЖИ !!!!!!!!!
    url = "https://rasp.dmami.ru/"
    group_number = "241-361"   # КОНТОРА ПИДОРАСОВ

    web_driver_config = WebDriverConfig(driver_path)
    driver = web_driver_config.create_driver()

    try:
        schedule_fetcher = ScheduleFetcher(driver)
        schedule_fetcher.open_site(url)
        schedule_fetcher.enter_group_number(group_number)
        schedule_fetcher.click_group(group_number)
        schedule_fetcher.wait_for_schedule()
        schedule_fetcher.fetch_schedule()
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
