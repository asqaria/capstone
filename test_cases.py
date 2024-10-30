from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, People, Cars
import json
import unittest
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
JWT = os.environ.get("JWT")
hdr={"Authorization": 'Bearer {}'.format(JWT).strip()}

class TestCases(unittest.TestCase):
    hdr = None
    
    def setUp(self):
        
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.drop_all()
            self.db.create_all()

    def tearDown(self):
        pass

    def test_welcome(self):
        res = self.client().get('/')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    ## USERS
    def test_add_user_ok(self):
        res = self.client().post('/user', json={
            'name': "Aqtos",
            'email': "aqtos@gmail.com",
            'age': "22",
            'gender': "Male",
            'city': "Almaty",
        }, content_type='application/json', headers=hdr)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['result'])

    def test_add_user_fail(self):
        res = self.client().post('/user', json={
            'name': "Aqtos"
        }, content_type='application/json', headers=hdr)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_get_users_ok(self):
        res = self.client().get('/users', content_type='application/json', headers=hdr)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['result'])

    def test_get_users_error(self):
        res = self.client().get('/users')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_update_user_ok(self):
        res = self.client().patch('/user/2', json={
            'name': "Aitote"
        }, content_type='application/json', headers=hdr)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['result'])

    def test_update_user_error(self):
        res = self.client().patch('/user/10000', json={
            'name': "Aitote"
        }, content_type='application/json', headers=hdr)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_delete_user_ok(self):
        dummy_user = People(
            name='aaa',
            email='www',
            age='34',
            gender='male',
            city='ffsdfsdf',
        )
        dummy_user.insert()

        res = self.client().delete('/user/{}'.format(dummy_user.id), content_type='application/json', headers=hdr)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['result'])

    def test_delete_user_error(self):
        res = self.client().delete('/user/1000000', content_type='application/json', headers=hdr)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


    ## CARS
    def test_add_car_ok(self):
        res = self.client().post('/car', json={
            'make': "MB",
            'model': "E class",
            'price': "2200",
            'distance': "44",
            'people_id': 2,
        }, content_type='application/json', headers=hdr)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['result'])

    def test_add_car_fail(self):
        res = self.client().post('/car', json={
            'sdsd': "loko"
        }, content_type='application/json', headers=hdr)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_get_cars_ok(self):
        res = self.client().get('/cars', content_type='application/json', headers=hdr)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['result'])

    def test_get_car_error(self):
        res = self.client().get('/cars')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_delete_car_ok(self):
        dummy_car = Cars(
            make="BMW",
            model="M5",
            price="22100",
            distance=45,
            people_id=5
        )
        dummy_car.insert()

        res = self.client().delete('/car/{}'.format(dummy_car.id), content_type='application/json', headers=hdr)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['result'])

    def test_delete_car_error(self):
        res = self.client().delete('/car/1000000', content_type='application/json', headers=hdr)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_update_car_ok(self):
        res = self.client().patch('/car/2', json={
            'price': "9000"
        }, content_type='application/json', headers=hdr)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['result'])

    def test_update_car_error(self):
        res = self.client().patch('/car/10000', json={
            'price': "9000"
        }, content_type='application/json', headers=hdr)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    if __name__ == '__main__':
        unittest.main()
