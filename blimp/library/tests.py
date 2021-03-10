from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

# Create your tests here.

class APITest(TestCase):
	def test_api_core(self):
		print("Testing Library API:")
#	register new accounts
		print("setting up accounts & login")
		url = reverse('signup_api')

		self.client.post(url, {'username':'test','email':'user@foo.com', 'password':'pass'}, format='json')

		self.client.post(url, {'username':'test2','email':'user@foo.com', 'password':'pass'}, format='json')


#	login and get tokens
		url = reverse('token_auth')

		resp = self.client.post(url, {'username':'test', 'password':'pass'}, format='json')
		self.assertTrue('access' in resp.data)
		token_user1 = resp.data['access']

		resp = self.client.post(url, {'username':'test2', 'password':'pass'}, format='json')
		self.assertTrue('access' in resp.data)
		token_user2 = resp.data['access']

#	add users as friends
		client = APIClient()

		url = reverse('friends_api')
		client.credentials(HTTP_AUTHORIZATION='Bearer ' + token_user1)

		resp = client.post(url, {'friend':'2'}, format='json')

		url = reverse('friends_pending_api')
		client.credentials(HTTP_AUTHORIZATION='Bearer ' + token_user2)

		resp = client.post(url, {'friend':'1'}, format='json')

#	test user upload video
#	test timeline
#	test viral
#	test user react