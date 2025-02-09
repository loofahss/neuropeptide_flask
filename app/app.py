from flask import Flask, request, jsonify
from flask_cors import CORS
from db_utils import query_protein_info, query_peptides_by_protein, query_pdbdata

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/")
def index():
    return "Hello World!"

@app.route("/query/proteinsequence", methods=["POST"])
def query_by_protein():
    """根据 ProteinId 查询 ProteinSequence 和相关 Peptide"""
    data = request.json
    protein_id = data.get("protein_id")
    if not protein_id:
        return jsonify({"error": "Missing protein_id"}), 400
    
    protein_data = query_protein_info(protein_id)
    if "error" in protein_data:
        return jsonify(protein_data), 404

    peptides = query_peptides_by_protein(protein_id)
    
    return jsonify({
        "proteinsequence": protein_data["ProteinSequence"],
        "peptides": peptides
    })

@app.route("/query/pdbdata", methods=["POST"])
def query_pdbdata_route():
    """查询 Protein 和 Peptide 对应的 PDB 数据"""
    data = request.json
    protein_id = data.get("proteinid")
    peptide_id = data.get("peptideid")
    if not protein_id or not peptide_id:
        return jsonify({"error": "Missing proteinid or peptideid"}), 400

    result = query_pdbdata(protein_id, peptide_id)
    if result:
        return jsonify(result)
    return jsonify({"error": "No PDB data found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
