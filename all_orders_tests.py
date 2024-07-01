import allure
import pytest
import requests

class TestOrderCreation:

    @pytest.fixture
    def base_order_data(self):
        return {
            "firstName": "Olya",
            "lastName": "Mishina",
            "address": "Zelenograd 1416",
            "metroStation": 4,
            "phone": "+7 985 381 68 44",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": ""
        }

    order_url = 'https://qa-scooter.praktikum-services.ru/api/v1/orders'

    @pytest.mark.parametrize("color", [
        (["BLACK"]),
        (["GREY"]),
        (["BLACK", "GREY"]),
        ([])
    ])
    @allure.title('Создание заказа с цветами')
    def test_create_order_with_colors(self, base_order_data, color):
        order_data = base_order_data.copy()
        if color:
            order_data['color'] = color
        response = requests.post(self.order_url, json=order_data)
        assert response.status_code == 201 and 'track' in response.json()

    @allure.title('Получение списка заказов')
    def test_get_orders_with_empty_data(self):
        response = requests.get(self.order_url)
        assert response.status_code == 200 and 'orders' in response.json()
        assert isinstance(response.json()['orders'], list)

