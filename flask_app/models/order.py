from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import checkout, user
from flask_app.models.user import User
from flask import flash
import json
from flask import jsonify


class Order:

    db = "group_project"

    def __init__(self, data):
        self.id = data['id']
        self.flavor = data['flavor']
        self.price = data['price']
        self.image = data['image']
        self.quantity = data["quantity"]
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.checkout = []
        self.owner = None

    def to_dict(self):
        order_dict = {
            "id": self.id,
            "flavor": self.flavor,
            "price": self.price,
            "image": self.image,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "quantity": self.quantity
        }
        if hasattr(self, 'user'):
            order_dict['user_id'] = self.user.id
        else:
            order_dict['user_id'] = None
        return order_dict

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO orders(flavor, price, quantity, image)
            VALUES(%(flavor)s,%(price)s, %(quantity)s, %(image)s);
            """
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    @classmethod
    def delete(cls, data):
        query = """
        DELETE FROM orders
        WHERE id = %(id)s
        """
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    @classmethod
    def get_all(cls):
        query = """
        SELECT * FROM orders LEFT JOIN users ON users.id = orders.user_id;
        """
        results = connectToMySQL(cls.db).query_db(query)
        print(" =================== ")
        print(results)
        print(" =================== ")

        if not results:
            return []

        all_orders = []

        for row in results:
            this_post = cls(row)
            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at'],
            }

            this_owner = user.User(user_data)
            this_post.owner = this_owner
            all_orders.append(this_post)

        return all_orders

    @classmethod
    def get_by_id(cls, id):

        query = """
        SELECT * FROM orders
        LEFT JOIN users ON orders.user_id = users.id
        LEFT JOIN checkout ON checkout.order_id = orders.id
        WHERE orders.id = %(id)s;
        """

        results = connectToMySQL(cls.db).query_db(query, {'id': id})
        if not results:
            return None
        print(" =================== \n")
        print(results)
        print(" =================== \n")

        row = results[0]
        this_order = cls(results[0])

        user_data = {
            'id': row['users.id'],     # posts.user_id = users.id
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'email': row['email'],
            'password': row['password'],
            'created_at': row['users.created_at'],
            'updated_at': row['users.updated_at'],
        }
        this_user = user.User(user_data)
        this_order.owner = this_user

        for rw in results:
            if not rw['checkout.id'] == None:
                this_liker = user.User({
                    'id': rw['users.id'],
                    'first_name': rw['first_name'],
                    'last_name': rw['last_name'],
                    'email': rw['email'],
                    'password': rw['password'],
                    'created_at': rw['users.created_at'],
                    'updated_at': rw['users.updated_at']
                })
                this_order.checkout.append(this_liker)
        return this_order
