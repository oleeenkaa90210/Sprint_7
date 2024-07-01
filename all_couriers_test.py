import allure
import unittest
import requests
from faker import Faker

fake = Faker('ru_RU')

def generate_random_courier_data():
    courier_data = {
        "login": fake.user_name(),
        "password": fake.password(),
        "firstName": fake.first_name(),
    }
    return courier_data

class TestCourierAPI(unittest.TestCase):

    login_url = 'https://qa-scooter.praktikum-services.ru/api/v1/courier/login'

    @classmethod
    def setUpClass(cls):
        cls.create_url = 'https://qa-scooter.praktikum-services.ru/api/v1/courier'
        cls.courier_data = generate_random_courier_data()
        cls.courier_id = None

    @allure.title('Создание курьера')
    def test_create_courier(self):
        valid_courier_data = generate_random_courier_data()
        response = requests.post(self.create_url, json=valid_courier_data)
        assert response.status_code == 201 and 'ok' in response.json()


    @allure.title('Создание уже имеющегося курьера')
    def test_create_duplicate_courier(self):
        valid_courier_data = generate_random_courier_data()
        response = requests.post(self.create_url, json=valid_courier_data)
        assert response.status_code == 201 and 'ok' in response.json()
        TestCourierAPI.courier_id = response.json().get('id')

        duplicate_response = requests.post(self.create_url, json=valid_courier_data)
        assert duplicate_response.status_code == 409
        assert duplicate_response.json().get('message') == "Этот логин уже используется. Попробуйте другой."

    @allure.title('Создание курьера без логина')
    def test_create_courier_without_login(self):
        valid_courier_data = generate_random_courier_data()
        courier_data_without_login = valid_courier_data.copy()
        courier_data_without_login.pop('login', None)

        response = requests.post(self.create_url, json=courier_data_without_login)

        assert response.status_code == 400 and response.json().get('message') == "Недостаточно данных для создания учетной записи"

    @allure.title('Создание курьера без пароля')
    def test_create_courier_without_password(self):
        valid_courier_data = generate_random_courier_data()
        courier_data_without_password = valid_courier_data.copy()
        courier_data_without_password.pop('password', None)

        response = requests.post(self.create_url, json=courier_data_without_password)

        assert response.status_code == 400 and response.json().get('message') == "Недостаточно данных для создания учетной записи"

    @allure.title('Создание курьера без фамилии')
    def test_create_courier_without_firstName(self):
        valid_courier_data = generate_random_courier_data()
        courier_data_without_firstName = valid_courier_data.copy()
        courier_data_without_firstName.pop('firstName', None)

        response = requests.post(self.create_url, json=courier_data_without_firstName)
        assert response.status_code == 201 and 'ok' in response.json()
        TestCourierAPI.courier_id = response.json().get('id')

    @allure.title('Авторизация курьера')
    def test_courier_can_login(self):
        valid_courier_data = generate_random_courier_data()
        response = requests.post(self.create_url, json=valid_courier_data)
        assert response.status_code == 201
        response = requests.post(self.login_url, json={
            "login": valid_courier_data['login'],
            "password": valid_courier_data['password']
        })
        assert response.status_code == 200 and 'id' in response.json()

    @allure.title('Авторизация курьера без логина')
    def test_login_without_login(self):
        response = requests.post(self.login_url, json={
            "login": '',
            "password": self.__class__.courier_data['password']
        })
        assert response.status_code == 400 and response.json().get('message') == "Недостаточно данных для входа"

    @allure.title('Авторизация курьера без пароля')
    def test_login_without_password(self):
        response = requests.post(self.login_url, json={
            "login": self.__class__.courier_data['password'],
            "password": ''
        })
        assert response.status_code == 400 and response.json().get('message') == "Недостаточно данных для входа"


    @allure.title('Авторизация курьера с несуществующим логином')
    def test_login_with_incorrect_login(self):
        valid_courier_data = generate_random_courier_data()
        create_response = requests.post(self.create_url, json=valid_courier_data)
        assert create_response.status_code == 201

        invalid_login_data = {
            "login": 'incorrect_login',
            "password": valid_courier_data['password']
        }
        login_response = requests.post(self.login_url, json=invalid_login_data)
        assert login_response.status_code == 404 and login_response.json().get('message') == "Учетная запись не найдена"


    @allure.title('Авторизация курьера с неверным паролем')
    def test_login_with_incorrect_password(self):
        valid_courier_data = generate_random_courier_data()
        create_response = requests.post(self.create_url, json=valid_courier_data)
        assert create_response.status_code == 201

        invalid_password_data = {
            "login": valid_courier_data['login'],
            "password": 'incorrect_password'
        }
        login_response = requests.post(self.login_url, json=invalid_password_data)
        assert login_response.status_code == 404 and login_response.json().get('message') == "Учетная запись не найдена"


    @allure.title('Авторизация несуществующего курьера')
    def test_login_not_exist_user(self):
        login_data = {
            "login": 'not_exist_user',
            "password": 'not_exist_password'
        }
        login_response = requests.post(self.login_url, json=login_data)
        assert login_response.status_code == 404 and login_response.json().get('message') == "Учетная запись не найдена"