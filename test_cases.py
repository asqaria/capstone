from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, People, Cars
import json
import unittest

JWT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJHNGlUcGQ5eFEzc0dXcmF1dThuRiJ9.eyJpc3MiOiJodHRwczovL2Rldi1zeXZvZGpjdHpoeXk2M2VpLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwODA4NTg5MDI5MzY1NjU5NDc4OSIsImF1ZCI6ImNvZmZlZXNob3AiLCJpYXQiOjE3MzAyNzAwODMsImV4cCI6MTczMDI3NzI4Mywic2NvcGUiOiIiLCJhenAiOiJEMmd2NWJHc1hHOG4zandiQW9PeFFka1FId2dCeHlPUyIsInBlcm1pc3Npb25zIjpbImFkZDpjYXIiLCJhZGQ6dXNlciIsImRlbGV0ZTpjYXIiLCJkZWxldGU6dXNlciIsImdldDpjYXIiLCJnZXQ6Y2FycyIsImdldDp1c2VyIiwiZ2V0OnVzZXJzIiwidXBkYXRlOmNhciIsInVwZGF0ZTp1c2VyIl19.CJY2x5tzGrc2Z_Cb6ndWNMaWIdHnsL-2v-DkLH7rEbyQBTg9S3Y2qizvUYpeOkQ6ce8kykGvoPU3t7MWxhtQuhQESDutoLOIeHF2L4LfHcbNM7VYiwg-T_x0TZ097BjTQQhVBX3VPDotE5ACN3zFqnqN-jLHjt1JkPS8zUs6FGm1LNa6O_dVaVfjFqJ8GFNaYoT-4N2gg_4fgWTGh69CRUG6Kg3ZS-sdBPI8uCpDgFJql5ex-dZDeQWnMGMSDxLNcib0yh5oAnUORsWC25y5ehl4u3bLyUeoFBtcvyH3Oo1LD0eSNbo0_u9RpJeWHQCe-6neTp8yIQ2QUlWR6KoQ0A'
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
