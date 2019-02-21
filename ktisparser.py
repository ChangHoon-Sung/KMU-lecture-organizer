# -*- coding: utf-8 -*-

# Import Selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Import BeautifulSoup4
from bs4 import BeautifulSoup as bs


class KTISParser:

    def __init__(self, user_id, user_pw):
        self.LOGIN = {
            'id': user_id,
            'pw': user_pw,
            'status': False
        }
        self.name = ""
        self.driver = None

    @staticmethod
    def headless_mod():
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('--disable-gpu')

        # nProtect 우회를 위해 모바일로 접속한다
        options.add_argument(
            "user-agent=Mozilla/5.0 (Linux; Android 9; SM-G965N)"
            "AppleWebKit/537.36 (KHTML, like Gecko)"
            "Chrome/70.0.3538.110 Mobile Safari/537.36"
        )

        return options

    def login(self, options=None):
        self.driver = webdriver.Chrome('./driver/chromedriver.exe',
                                       chrome_options=options)
        # KTIS 메인 홈페이지
        self.driver.get('https://ktis.kookmin.ac.kr')

        # ID, PW 입력
        self.driver.find_element_by_id('txt_user_id').send_keys(
            self.LOGIN['id'])
        self.driver.find_element_by_name('txt_passwd').send_keys(
            self.LOGIN['pw'])
        self.driver.find_element_by_name('txt_passwd').send_keys(Keys.RETURN)

        # 로그인 실패 팝업 예외처리
        try:
            WebDriverWait(self.driver, 0.01).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            msg = str(alert.text)
            alert.accept()
            self.driver.close()
            self.LOGIN['status'] = False
            return msg

        # 로그인 성공
        except TimeoutException:
            self.driver.get(
                'https://ktis.kookmin.ac.kr/kmu/usa.Usa0209eFGet01.do')
            root = bs(self.driver.page_source, 'html.parser')
            self.name = root.find(string="성명").parent.parent.find_all('td')[
                3].string
            self.LOGIN['status'] = True
            return "Login Success"

    def get_lecture(self, year, period):

        # KTIS 수강신청내역출력 페이지
        self.driver.get('https://ktis.kookmin.ac.kr/kmu/usb.Usb0102rAGet01.do')

        # 년도 입력
        self.driver.find_element_by_name('txt_year').clear()
        self.driver.find_element_by_name('txt_year').send_keys(year)

        # 학기 선택
        semester = Select(self.driver.find_element_by_name('txt_smt'))
        semester.select_by_visible_text(period)

        self.driver.find_element_by_name("find").click()

        root = bs(self.driver.page_source, 'html.parser')
        root = root.find(string="교과목명").parent.parent.parent.find_all('tr')

        subjects = []
        for i in range(len(root)):
            lecture = [subject.string for subject in root[i].find_all('td')]
            subjects.append(lecture)

        return subjects


# TEST
if __name__ == "__main__":
    user = KTISParser('학번', '비번')
    login_msg = user.login(KTISParser.headless_mod())
    if user.LOGIN['status']:
        for l in user.get_lecture(2018, "2학기"):
            print(l)
    else:
        print(login_msg)
