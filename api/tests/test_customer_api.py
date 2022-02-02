import json
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from api.views import CustomerView
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status


class ApiUrlsTests(SimpleTestCase):
    
    def test_get_customers_is_resolved(self):
        url = reverse('customer')
        self.assertEquals(resolve(url).func.view_class, CustomerView)

class CustomerAPIViewTests(APITestCase):
    customers_urls = reverse('customer')

    def setUp(self):
        self.user = User.objects.create_user(username="admin",password="kgf789456@")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.token.key)

    def tearDown(self):
        pass

    def test_get_customers_authenticated(self):
        response = self.client.get(self.customers_urls)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_customers_un_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.customers_urls)
        self.assertEqual(response.status_code, 401)    

    def test_post_customer_authenticated(self):
        data={
            "title":"Mrs",
            "name":"avani",
            "last_name":"patel",
            "gender":"M",
            "status":"published"
        }    

        response = self.client.post(self.customers_urls, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'avani')


class CustomerDetailAPIViewTests(APITestCase): 
    customers_urls = reverse('customer')
    customer_url = reverse('customer_detail', args=[1])

    def setUp(self):
        self.user = User.objects.create_user(username="admin",password="kgf789456@")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.token.key)

        # Saving User
        data={
            "title":"Mrs",
            "name":"brijesh",
            "last_name":"patel",
            "gender":"M",
            "status":"published"
        }
        self.client.post(self.customers_urls, data, format='json')

    def test_get_customer_authenticated(self):
        response = self.client.get(self.customer_url)    
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'brijesh')

    def test_get_customer_un_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.customer_url)    
        self.assertEqual(response.status_code, 401)

    def test_put_customer_authenticated(self):
        data={
            "title":"Mrs",
            "name":"mitesh",
            "last_name":"patel",
            "gender":"M",
            "status":"published"
        }
        response = self.client.put(self.customer_url, data, format="json")    
        self.assertEqual(response.status_code, 200)    
        self.assertEqual(response.data['name'], 'mitesh')

    def test_delete_customer_authenticated(self):
        response = self.client.delete(self.customer_url)    
        self.assertEqual(response.status_code, 204)    