#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(  bakeries,   200  )

# @app.route('/bakeries/<int:id>')
# def bakery_by_id(id):

#     bakery = Bakery.query.filter_by(id=id).first()
#     bakery_serialized = bakery.to_dict()
#     return make_response ( bakery_serialized, 200  )



@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.form
    name = data.get('name')
    price_string = data.get('price')
    bakery_id_string = data.get('bakery_id')


    baked_good = BakedGood()
    baked_good.name = name
    baked_good.price = price_string
    baked_good.bakery_id = bakery_id_string

    db.session.add(baked_good)
    db.session.commit()


    baked_good_jsonified = {
        'id': baked_good.id,
        'name': baked_good.name,
        'price': baked_good.price,
        'bakery_id': baked_good.bakery_id
    }

    return jsonify(baked_good_jsonified, 201)








@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    data = request.form
    new_name = data.get('name')
    bakery = db.session.get(Bakery, id)
    
    if bakery:
        bakery.name = new_name
        db.session.commit()

        bakery_jsonified = {
            'id': bakery.id,
            'name': bakery.name
        }
        return jsonify(bakery_jsonified), 200
    
    else:
        error_message_jsonified = {'message': 'Bakery not found'}        
        return jsonify(error_message_jsonified, 404)







@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):

    baked_good = db.session.get(BakedGood, id)
    
    if baked_good:
        db.session.delete(baked_good)
        db.session.commit()
        baked_good_jsonified = {'message': 'Baked good deleted successfully'}
        return jsonify(baked_good_jsonified), 200
    else:
        error_message_jsonified1 = {'message': 'Baked good not found'}
        return jsonify(error_message_jsonified1, 404)











@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    return make_response( baked_goods_by_price_serialized, 200  )
   

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()
    return make_response( most_expensive_serialized,   200  )

if __name__ == '__main__':
    app.run(port=5555, debug=True)