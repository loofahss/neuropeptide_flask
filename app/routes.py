from flask import Blueprint, request, jsonify
from app.db_utils import connect
from app.services import query_protein_info

bp = Blueprint('api', __name__)

@bp.route("/query/proteinsequence", methods=["POST"])
def query_byprotein():
    data = request.json
    protein_id = data.get("protein_id")
    db = connect()

    try:
        result = query_protein_info(db, protein_id)
    finally:
        db.close()

    return jsonify(result)

def init_routes(app):
    app.register_blueprint(bp)
