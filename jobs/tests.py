from django.test import TestCase, Client
from django.urls import reverse
from datetime import time
from .models import Job, PlantItem, TeamMember, Vehicle


class JobModelTest(TestCase):

    def setUp(self):
        self.job = Job.objects.create(
            works_order_ref='WO-TEST-001',
            operative_name='Test Operative',
            arrived_time=time(8, 0),
            departed_time=time(12, 0),
            notes='Test job'
        )

    def test_job_created(self):
        self.assertEqual(self.job.works_order_ref, 'WO-TEST-001')

    def test_hours_on_site(self):
        self.assertEqual(self.job.hours_on_site(), 4.0)

    def test_labour_cost_one_person(self):
        self.assertEqual(self.job.labour_cost(), 112.0)

    def test_labour_cost_two_people(self):
        TeamMember.objects.create(job=self.job, name='Person One')
        TeamMember.objects.create(job=self.job, name='Person Two')
        self.assertEqual(self.job.labour_cost(), 224.0)

    def test_plant_cost(self):
        PlantItem.objects.create(job=self.job, item_key='cherry_picker_full')
        self.assertEqual(self.job.plant_cost(), 380.0)

    def test_total_cost(self):
        PlantItem.objects.create(job=self.job, item_key='cable_drum')
        self.assertEqual(self.job.total_cost(), 202.0)


class JobViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_operative_form_loads(self):
        response = self.client.get(reverse('operative_form'))
        self.assertEqual(response.status_code, 200)

    def test_qs_dashboard_loads(self):
        response = self.client.get(reverse('qs_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_submit_job(self):
        response = self.client.post(reverse('operative_form'), {
            'works_order_ref': 'WO-2024-999',
            'operative_name': 'Test Worker',
            'arrived_time': '09:00',
            'departed_time': '14:00',
            'notes': 'Test submission',
        })
        self.assertEqual(Job.objects.count(), 1)
