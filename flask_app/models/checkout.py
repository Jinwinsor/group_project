
from flask_app.config.mysqlconnection import connectToMySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash


class Checkout:
    db = "group_project"

    def __init__(self, data):
        self.id = data.get('id')
        self.user_id = data['user_id']
        # self.order_id = data['order_id']
        self.order_id = data.get('order_id')

    @classmethod
    def get_checkout_info(cls, order_id):
        query = """
            SELECT orders.id, orders.flavor, orders.price, orders.user_id, checkout.id AS checkout_id
            FROM orders
            LEFT JOIN checkout ON orders.id = checkout.order_id
            WHERE orders.id IN %(order_ids)s;
        """
        data = {'order_id': tuple(order_id)}
        results = connectToMySQL(cls.db).query_db(query, data)
        return [cls(result) for result in results]

    @classmethod
    def delete(cls, order_id):
        query = "DELETE FROM checkout WHERE order_id = %(order_id)s;"
        result = connectToMySQL(cls.db).query_db(query, {'order_id': order_id})
        return result

    @classmethod
    def count_checkout(cls, order_id):
        query = "SELECT COUNT(*) FROM checkout WHERE order_id = %(order_id)s"
        result = connectToMySQL(cls.db).query_db(query, {'order_id': order_id})
        return result[0]['COUNT(*)']

    @classmethod
    def every_checkout(cls, order_id):
        query = "SELECT * FROM checkout WHERE order_id = %(order_id)s;"
        result = connectToMySQL(cls.db).query_db(query, {'order_id': order_id})
        return result

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO checkout
        (user_id, order_id)
        VALUES
        (%(user_id)s, %(order_id)s);
        """
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    # @classmethod
    # def delete(cls, data):
    #     query = """
    #     DELETE FROM checkout
    #     WHERE user_id = %(user_id)s AND order_id = %(order_id)s;
    #     """
    #     result = connectToMySQL(cls.db).query_db(query, data)
    #     return result

    # @classmethod
    # def user_dont_like(cls, data):
    #     query = """
    #     SELECT * FROM checkout WHERE order.id
    #     NOT IN ( SELECT order_id FROM checkout
    #     WHERE user_id = %(id)s );
    #     """

    #     orders = []
    #     results = connectToMySQL(cls.db).query_db(query, data)
    #     if results:
    #         for row in results:
    #             orders.append(cls(row))
    #         return orders
    #     else:
    #         False
# ===================

    @classmethod
    def get_orders_by_checkout_id(cls, checkout_id):
        from flask_app.models.order import Order
        query = """
        SELECT * FROM orders
        JOIN checkout ON orders.id = checkout.order_id
        WHERE checkout.id = %(checkout_id)s;
        """
        results = connectToMySQL(cls.db).query_db(
            query, {'checkout_id': checkout_id})
        orders = []
        for row in results:
            orders.append(Order(row))
        return orders

    @classmethod
    def get_checkout_by_user_id(cls, user_id):
        query = "SELECT * FROM checkout WHERE user_id = %(user_id)s;"
        results = connectToMySQL(cls.db).query_db(query, {'user_id': user_id})
        checkouts = []
        for row in results:
            checkouts.append(Checkout(row))
        return checkouts

    @classmethod
    def get_by_id(cls, checkout_id):
        query = "SELECT * FROM checkout WHERE id = %(checkout_id)s;"
        result = connectToMySQL(cls.db).query_db(
            query, {'checkout_id': checkout_id})
        if len(result) != 1:
            return None
        return cls(result[0])

    # @classmethod
    # def get_checkout_by_user_id(cls, user_id):
    #     query = "SELECT * FROM checkout WHERE user_id = %(user_id)s;"
    #     result = connectToMySQL(cls.db).query_db(
    #     query, {'checkout_id': user_id})
    #     if len(result) != 1:
    #         return None
    #     return cls(result[0])
