#!/usr/bin/env python3

from flask import request, session, jsonify, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

import os
from config import create_app, db, api
from models import Book, BookSchema

env = os.getenv("FLASK_ENV", "dev")
app = create_app(env)

class Books(Resource):
    def get(self):
        # Read pagination controls from query params.
        # Defaults match the lab/test expectations when params are omitted.
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        # Fetch only the requested slice of rows instead of loading every book.
        # `error_out=False` keeps out-of-range pages safe by returning empty items.
        pagination = Book.query.order_by(Book.id).paginate(
            page=page,
            per_page=per_page,
            error_out=False,
        )

        # Return paginated data plus metadata so clients can render page controls.
        response = {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'total_pages': pagination.pages,
            'items': BookSchema(many=True).dump(pagination.items),
        }

        return response, 200


api.add_resource(Books, '/books', endpoint='books')


if __name__ == '__main__':
    app.run(port=5555, debug=True)