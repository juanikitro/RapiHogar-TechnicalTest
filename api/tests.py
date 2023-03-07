import json
from rapihogar.models import Scheme, Technician, User
from django.urls import reverse
from django.core.management import call_command

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rapihogar.models import Company, Pedido


class CompanyListCreateAPIViewTestCase(APITestCase):
    url = reverse("company-list")

    def setUp(self):
        self.username = "user_test"
        self.email = "test@rapihigar.com"
        self.password = "Rapi123"        
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_company(self):
        response = self.client.post(self.url, 
            {
                "name": "company delete!",
                "phone": "123456789",                
                "email": "test@rapihigar.com",
                "website": "http://www.rapitest.com"
            }
        )
        self.assertEqual(201, response.status_code)

    def test_list_company(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertTrue(len(json.loads(response.content)) == Company.objects.count())

class ComandTestCase(APITestCase):
    def setUp(self):
        Technician.objects.create(email='test@gmail.com', first_name='Test', last_name='tseT')
        User.objects.create_user('Test', 'test@mgail.com', 'Test123')

        return None

    def test_command(self):
        call_command("create_random_pedidos", '200', stdout=True)

        pedidos = Pedido.objects.all().count()
        self.assertEqual(pedidos, 0)

        call_command("create_random_pedidos", '10', stdout=True)

        pedidos = Pedido.objects.all().count()
        self.assertEqual(pedidos, 10)

class TechniciansListAPITestCase(APITestCase):
    url_technicians = '/api/technicians/'
    url_report = '/api/report/'

    def test_list_technicians(self):
        response = self.client.get(self.url_technicians)
        self.assertEqual(200, response.status_code)
        self.assertTrue(len(json.loads(response.content)) == Technician.objects.count())
        self.assertEqual(json.loads(response.content), [])

        Technician.objects.create(email='test@gmail.com', first_name='Test', last_name='tseT')
        response = self.client.get(self.url_technicians)
        self.assertEqual(200, response.status_code)
        self.assertTrue(len(json.loads(response.content)) == Technician.objects.count())
        self.assertEqual(json.loads(response.content), [{'full_name': 'Test tseT', 'hours_worked': 0, 'id': 1, 'orders_id': [], 'pay_by_hours': 0}])

        for i in range(10):
            Technician.objects.create(email=f'test{i}@gmail.com', first_name='Test', last_name=i)
        response = self.client.get(self.url_technicians)
        self.assertEqual(200, response.status_code)
        self.assertTrue(len(json.loads(response.content)) == Technician.objects.count())
        self.assertEqual(json.loads(response.content), [{"id": 1, "full_name": "Test tseT", "orders_id": [], "hours_worked": 0, "pay_by_hours": 0}, {"id": 2, "full_name": "Test 0", "orders_id": [], "hours_worked": 0, "pay_by_hours": 0}, {"id": 3, "full_name": "Test 1", "orders_id": [], "hours_worked": 0, "pay_by_hours": 0}, {"id": 4, "full_name": "Test 2", "orders_id": [], "hours_worked": 0, "pay_by_hours": 0}, {"id": 5, "full_name": "Test 3", "orders_id": [], "hours_worked": 0, "pay_by_hours": 0}, {"id": 6, "full_name": "Test 4", "orders_id": [], "hours_worked": 0, "pay_by_hours": 0}, {"id": 7, "full_name": "Test 5", "orders_id": [], "hours_worked": 0, "pay_by_hours": 0}, {"id": 8, "full_name": "Test 6", "orders_id": [], "hours_worked": 0, "pay_by_hours": 0}, {"id": 9, "full_name": "Test 7", "orders_id": [], "hours_worked": 0, "pay_by_hours": 0}, {"id": 10, "full_name": "Test 8", "orders_id": [], "hours_worked": 0, "pay_by_hours": 0}, {"id": 11, "full_name": "Test 9", "orders_id": [], "hours_worked": 0, "pay_by_hours": 0}])

        response = self.client.get(f'{self.url_technicians}?name=5')
        self.assertEqual(200, response.status_code)
        self.assertEqual(json.loads(response.content), [{'full_name': 'Test 5', 'hours_worked': 0, 'id': 7, 'orders_id': [], 'pay_by_hours': 0}])

    def test_report(self):
        response = self.client.get(self.url_report)
        self.assertEqual(200, response.status_code)
        self.assertEqual(json.loads(response.content), {
        "average_amount": 0,
        "below_average_technicians": {},
        "with_higher_amount": None,
        "with_lower_amount": None
        })

        Technician.objects.create(email='123@gmail.com', first_name='Lautaro', last_name='Martinez')
        Technician.objects.create(email='321@gmail.com', first_name='Juan', last_name='Portilla')
        Technician.objects.create(email='345345@gmail.com', first_name='Javier', last_name='Cuenca')
        User.objects.create_user('Test', 'test@mgail.com', 'Test123')
        Scheme.objects.create(name='Testscheme')
        call_command("create_random_pedidos", '50', stdout=True)

        response = json.loads(self.client.get(self.url_report).content)
        print(response)
        self.assertGreater(response["average_amount"], 0)
        self.assertLess(list(response["below_average_technicians"].values())[0], response["average_amount"])
