import datetime
from tastypie.resources import ModelResource
from tastypie.test import ResourceTestCase
from django.contrib.auth.models import User
from okrs.models import Objective, KeyResult

class ObjectiveResourceTest(ResourceTestCase):
    def setUp(self):
        super(ObjectiveResourceTest, self).setUp()
        
        self.username = 'daniel'
        self.password = 'pass'
        self.user = User.objects.create_user(self.username, 'daniel@example.com', self.password)


        objective = Objective(
            name="Increase Revenue",
            description="Need more money",
            due_date=datetime.date(2014, 6, 1),
            created=datetime.datetime.now(),
            private=True,
            progress=0)
        objective.save()

        objective = Objective(
            name="Increase Revenue 2",
            description="Need more money",
            due_date=datetime.date(2014, 6, 1),
            created=datetime.datetime.now(),
            private=False,
            progress=0)
        objective.save()

    def get_credentials(self):
        return self.create_basic(username=self.username, password=self.password)

    def test_due_date_db_storage(self):
        objective = Objective.objects.get(name="Increase Revenue")
        self.assertTrue(objective.due_date == datetime.date(2014, 6, 1), True)

    def test_api_get_objective(self):
        resp = self.api_client.get('/api/v1/objectives/', format='json', authentication=self.get_credentials())
        response_length = len(self.deserialize(resp)['objects'])
        self.assertEqual(response_length, 2)

    def test_api_post_objective(self):
        new_objective = {
            'name': "Decrease Losses",
            'description': "Need more money!!",
            'due_date': datetime.date(2014, 6, 1),
            'created': datetime.datetime.now(),
            'private': False,
            'progress': 0,
        }
        self.assertHttpCreated(self.api_client.post('/api/v1/objectives/', format='json', data=new_objective, authentication=self.get_credentials()))
        objective = Objective.objects.get(name="Decrease Losses")
        self.assertEqual(objective.name == "Decrease Losses", True)

    def test_objective_private_dehydrate(self):
        objective_raw = Objective.objects.get(name="Increase Revenue")
        objective_raw_id = objective_raw.id

        resp = self.api_client.get('/api/v1/objectives/%d/' % objective_raw_id, format='json', authentication=self.get_credentials())
        objective_api = self.deserialize(resp)
        self.assertTrue(objective_raw.private)
        self.assertEqual(objective_api["private"], "private")

    def test_objective_public_dehydrate(self):
        objective_raw = Objective.objects.get(name="Increase Revenue 2")
        objective_raw_id = objective_raw.id

        resp = self.api_client.get('/api/v1/objectives/%d/' % objective_raw_id, format='json', authentication=self.get_credentials())
        objective_api = self.deserialize(resp)

        self.assertFalse(objective_raw.private)
        self.assertEqual(objective_api["private"], "public")
        
