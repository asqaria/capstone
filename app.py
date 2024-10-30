from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
from models import setup_db, Cars, People
from auth import AuthError, requires_auth

def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app, resource={r'/api/': {'origins': '*'}})
    setup_db(app)
    
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization, True')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST, DELETE, PATCH, OPTIONS')
        return response

    ### START API ###

    @app.route('/', methods=['GET'])
    def check_status():
        return jsonify({
            'success': True,
            'message': 'healthy'
        })

    ### CARS

    @app.route('/cars', methods=['GET'])
    @requires_auth('get:cars')
    def get_cars(jwt):
        cars = Cars.query.all()

        if not cars:
            abort(404)

        cars = [car.format() for car in cars]
        return return_json(True, cars)
    
    @app.route('/car/<int:car_id>', methods=['GET'])
    @requires_auth('get:car')
    def get_car(jwt, car_id):
        car = Cars.query.get(car_id)

        if not car:
            abort(404)

        car = car.format()
        return return_json(True, car)

    @app.route('/car', methods=['POST'])
    @requires_auth('add:car')
    def create_car(jwt):
        body = request.get_json()
        make = body.get('make')
        model = body.get('model')
        price = body.get('price')
        distance = body.get('distance')
        people_id = body.get('people_id')

        if not (make or model or price or distance or people_id):
            abort(422)
        
        try:
            car = Cars(
                make=make,
                model=model,
                price=price,
                distance=distance,
                people_id=people_id
            )

            car.insert()
            return return_json(True, car.format())
        except BaseException as e:
            print(e)
            abort(422)

    @app.route('/car/<int:car_id>', methods=['PATCH'])
    @requires_auth('update:car')
    def update_car(jwt, car_id):
        car = Cars.query.get(car_id)
        if car:
            try:
                body = request.get_json()
                price = body.get('price')
                distance = body.get('distance')

                if price:
                    car.price = price
                if distance:
                    car.distance = distance

                car.update()
                return return_json(True, car.format())
            except BaseException as e:
                print(e)
                abort(422)

        else:
            abort(404)

    @app.route('/car/<int:car_id>', methods=['DELETE'])
    @requires_auth('delete:car')
    def delete_car(jwt, car_id):
        car = Cars.query.get(car_id)

        if car:
            try:
                car.delete()
                return return_json(True, 'Deleted')
            except BaseException:
                abort(422)
        else:
            abort(404)


    ### PEOPLE

    @app.route('/users', methods=['GET'])
    @requires_auth('get:users')
    def get_users(jwt):
        users = People.query.all()

        if not users:
            abort(404)

        users = [user.format() for user in users]
        return return_json(True, users)

    @app.route('/user/int:<user_id>', methods=['GET'])
    @requires_auth('get:user')
    def get_user(jwt, user_id):
        user = People.query.get(user_id)

        if not user:
            abort(404)

        user = user.format()
        return return_json(True, user)

    @app.route('/user', methods=['POST'])
    @requires_auth('add:user')
    def create_user(jwt):
        body = request.get_json()
        name = body.get('name')
        email = body.get('email')
        age = body.get('age')
        gender = body.get('gender')
        city = body.get('city')

        if name is None or email is None or age is None or gender is None or city is None:
            abort(422)

        try:
            user = People(
                name = name,
                email = email,
                age = age,
                gender = gender,
                city = city
            )

            user.insert()
            return return_json(True, user.format())
        except BaseException as e:
            print(e)
            abort(422)

    @app.route('/user/<int:user_id>', methods=['PATCH'])
    @requires_auth('update:user')
    def update_user(jwt, user_id):
        user = People.query.get(user_id)
        if user:
            try:
                body = request.get_json()
                name = body.get('name')
                email = body.get('email')
                age = body.get('age')
                gender = body.get('gender')
                city = body.get('city')

                if name:
                    user.name = name
                if email:
                    user.email = email
                if age:
                    user.age = age
                if gender:
                    user.gender = gender
                if city:
                    user.city = city

                user.update()
                return return_json(True, user.format())
            except BaseException as e:
                print(e)
                abort(422)

        else:
            abort(422)

    @app.route('/user/<int:user_id>', methods=['DELETE'])
    @requires_auth('delete:user')
    def delete_user(jwt, user_id):
        user = People.query.get(user_id)

        if user:
            try:
                user.delete()
                return return_json(True, 'Deleted')
            except BaseException:
                abort(422)
        else:
            abort(404)

    ### END API ###

    def return_json(success, result):
        return jsonify({
            'success': success,
            'result': result
        })

    @app.errorhandler(404)
    def not_found(error):
        return return_error(404, 'Resource Not Found')

    @app.errorhandler(400)
    def bad_request(error):
        return return_error(400, 'Bad Request')

    @app.errorhandler(422)
    def unable_to_process(error):
        return return_error(422, 'Unable to process request')

    @app.errorhandler(500)
    def server_error(error):
        return return_error(500, 'Internal Server Error')

    @app.errorhandler(AuthError)
    def handle_auth_errors(error):
        return return_error(error.status_code, error.error)

    def return_error(error, msg):
        return jsonify({
            'success': False,
            'error': error,
            'message': msg
        }), error

    return app

app = create_app()

if __name__ == '__main__':
    app.run(port=8080, debug=True)