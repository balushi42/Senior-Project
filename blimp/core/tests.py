from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

# Create your tests here.

class APITest(TestCase):
	def test_api_core(self):
		print("Testing Core API:")
#	test register
		print("Testing signup & login")
		url = reverse('signup_api')

		resp = self.client.post(url, {'email':'user@foo.com', 'password':'pass'}, format='json')
		self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

		resp = self.client.post(url, {'username':'test','email':'user@foo.com', 'password':'pass'}, format='json')
		self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

		resp = self.client.post(url, {'username':'test2','email':'user@foo.com', 'password':'pass'}, format='json')
		self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

#	already taken username
		resp = self.client.post(url, {'username':'test2','email':'user@foo.com', 'password':'pass'}, format='json')
		self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

#	test login
		url = reverse('token_auth')

		resp = self.client.post(url, {'username':'test', 'password':'pass21'}, format='json')
		self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

		resp = self.client.post(url, {'username':'test', 'password':'pass'}, format='json')
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		self.assertTrue('access' in resp.data)
		token_user1 = resp.data['access']

		resp = self.client.post(url, {'username':'test2', 'password':'pass'}, format='json')
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		self.assertTrue('access' in resp.data)
		token_user2 = resp.data['access']


#	test profile
		print("Testing profile")
		client = APIClient()
		client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'abc')
		url = reverse('profile_api')

		resp = client.get(url, format='json')
		self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

		client.credentials(HTTP_AUTHORIZATION='Bearer ' + token_user1)

		resp = client.get(url, format='json')
		self.assertEqual(resp.status_code, status.HTTP_200_OK)

		print("Testing Friendship add and accept with outliers")
#	test add friend
		url = reverse('friends_api')
		client.credentials(HTTP_AUTHORIZATION='Bearer ' + token_user1)

		resp = client.post(url, {'friend':'2'}, format='json')
		self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

#	add already pending friend
		resp = client.post(url, {'friend':'2'}, format='json')
		self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

#	add self as friend
		resp = client.post(url, {'friend':'1'}, format='json')
		self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


		client.credentials(HTTP_AUTHORIZATION='Bearer ' + token_user2)

#	add already pending friend
		resp = client.post(url, {'friend':'1'}, format='json')
		self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

		url = reverse('friends_pending_api')

		resp = client.post(url, {'friend':'1'}, format='json')
		self.assertEqual(resp.status_code, status.HTTP_202_ACCEPTED)

		url = reverse('friends_api')

#	add friend that is already accepted
		resp = client.post(url, {'friend':'1'}, format='json')
		self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

		print("Done")