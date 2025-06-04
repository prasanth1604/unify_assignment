import unittest
from django.test import Client, TestCase
from .models import FitnessClass
from django.urls import reverse
from datetime import datetime


class AllClassesViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.class1 = FitnessClass.objects.create(
            name="Yoga Class",
            time=datetime.now(),
            Instructor="John Doe",
            total_slots=5,
            registered_clients=[])
        self.class2 = FitnessClass.objects.create(
            name="Pilates Class",
            time=datetime.now(),
            Instructor="Jane Smith",
            total_slots=0,  # No slots available
            registered_clients=[])
        
        
    #GET method tests
    def test_get_all_classes(self):
        response = self.client.get(reverse('all_classes'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['name'], "Yoga Class")
      
    #POST method tests    
    def test_post_register_client(self):
        response = self.client.post(reverse('all_classes'), {
            'class_id': self.class1.id,
            'client_name': 'Alice',
            'client_email': 'alice@gmail.com'})
        self.assertEqual(response.status_code, 200)
        self.class1.refresh_from_db()
        self.assertIn('alice@gmail.com', self.class1.registered_clients)
        self.assertEqual(self.class1.total_slots, 4)
    def test_post_register_client_no_slots(self):
        response = self.client.post(reverse('all_classes'), {
            'class_id': self.class2.id,
            'client_name': 'Bob',
            'client_email': 'bob@yahoo.com'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['message'], "No slots available")
        
    def test_post_method_register(self):
        data = {'class_id': self.class1.id, 'client_name': 'John Doe', 'client_email': 'johndoe@example.com'}
        response = self.client.post(reverse('all_classes'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Client registered successfully')
        
    def test_post_method_no_slots(self):
        data = {'class_id': self.class2.id, 'client_name': 'John Doe', 'client_email': 'johndoe@example.com'}
        response = self.client.post(reverse('all_classes'), data)
        self.assertEqual(response.status_code, 400)

    def test_post_method_already_registered(self):
        data = {'class_id': self.class1.id, 'client_name': 'John Doe', 'client_email': 'johndoe@example.com'}
        self.client.post(reverse('all_classes'), data)
        response = self.client.post(reverse('all_classes'), data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], 'Client already registered')
        
    def test_post_method_class_not_found(self):
        data = {'class_id': 999, 'client_name': 'John Doe', 'client_email': 'johndoe@example.com'}
        response = self.client.post(reverse('all_classes'), data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['message'], 'Class not found')
        