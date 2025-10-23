from flask import Flask, request, jsonify
import pymysql
from flask_cors import CORS
import random
#1.proteinid返回proteinsequence,peptideid,peptidesequence,pdbdata,string_len(peptidesequence)
#2.peptideid返回peptidesequence,proteinid,proteinsequence,pdbdata,string_len(proteinsequence)
# 显示pEI值,进行筛选
# 通过proteinid,peptideid查询pdbdata,显示pdbdata,pEI,peptidesequence
app = Flask(__name__)
# CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})
# 打开数据库连接
def connect():
    return pymysql.connect(host='localhost',
                        database='neuropenet',
                        user='root',
                        passwd='your_password')


@app.route("/")
def index():
    return "Hello World!"

@app.route("/query_protein/<string:protein_id>", methods=["GET"])
def query_protein(protein_id):
    db=connect()
    # 调用查询函数并返回结果
    result = query_protein_info(db, protein_id)
    return jsonify(result)
# post_form



@app.route("/query/proteinsequence", methods=["POST"])
def query_byprotein():
    data = request.json  # 使用 request.json 获取 JSON 数据
    protein_id = data.get("protein_id")
    db = connect()
    
    try:
        cursor = db.cursor()
        # 查询 proteinsequence
        proteinsequence_query = "SELECT proteinsequence FROM proteins WHERE proteinid = %s"
        cursor.execute(proteinsequence_query, (protein_id,))
        proteinsequence = cursor.fetchone()[0]

        # 查询 peptides
        peptides_query = """
            SELECT pp1.peptideid, p.peptideSequence, pp1.PEI ,pp1.pdbData
            FROM protein_peptide AS pp1
            JOIN peptides AS p ON pp1.peptideid = p.peptideid
            WHERE pp1.proteinid =%s
        """
        cursor.execute(peptides_query, (protein_id,))
        peptide_records = cursor.fetchall()
        
        peptides = []
        for peptide in peptide_records:
            peptides.append({
                'peptideid': peptide[0],
                'peptideSequence': peptide[1],
                'PEI': peptide[2],
                'pdb': peptide[3]
            })
        
        result = {
            'proteinsequence': proteinsequence,
            'peptides': peptides
        }
        print("peptidesequence:")
        print(peptides[2  ])
    except Exception as e:
        result = {'error': f"Error querying protein information: {str(e)}"}
    finally:
        cursor.close()
        db.close()
    
    return jsonify(result)

@app.route("/query/peptidesequence", methods=["POST"])
def query_bypeptide():
    data = request.json  # 使用 request.json 获取 JSON 数据
    protein_id = data.get("protein_id")
    db = connect()
    print("protein_id:")
    print(protein_id)
    try:
        cursor = db.cursor()
        # 查询 proteinsequence
        proteinsequence_query = "SELECT peptidesequence FROM peptides WHERE peptideid = %s"
        cursor.execute(proteinsequence_query, (protein_id,))
        proteinsequence = cursor.fetchone()[0]
        print(proteinsequence)
        # 查询 peptides
        peptides_query = """
            SELECT pp1.proteinid, p.ProteinSequence, pp1.PEI ,pp1.pdbData
            FROM protein_peptide AS pp1
            JOIN proteins AS p ON pp1.proteinid = p.proteinid
            WHERE pp1.peptideid =%s
        """
        cursor.execute(peptides_query, (protein_id,))
        peptide_records = cursor.fetchall()
        
        peptides = []
        for peptide in peptide_records:
            peptides.append({
                'peptideid': peptide[0],
                'peptideSequence': peptide[1],
                'PEI': peptide[2],
                'pdb': peptide[3]
            })
        
        result = {
            'proteinsequence': proteinsequence,
            'peptides': peptides
        }
        print("peptidesequence:")
        print(peptides[2  ])
    except Exception as e:
        result = {'error': f"Error querying protein information: {str(e)}"}
        print(result)
    finally:
        cursor.close()
        db.close()
    
    return jsonify(result)

@app.route("/query/pdbdata",methods=["POST"])
def query_pdbdata():
    db=connect()
    data = request.json  # 使用 request.json 获取 JSON 数据
    proteinid=data.get("proteinid")
    peptideid=data.get("peptideid")
    print('hii')
    result=query_pdbdata_info(db,proteinid,peptideid)
    # print(result)
    print(result['pdbData'])
    return {"pdbdata":result}

def query_pdbdata_info(connection,proteinid,peptideid):
    result = {}
    try:
        # 创建游标对象
        cursor = connection.cursor()
        sql = """
        SELECT pp.pdbdata,pp.PEI
        FROM Protein_Peptide pp
        JOIN Proteins p ON pp.proteinid = p.proteinid
        JOIN Peptides pt ON pp.peptideid = pt.peptideid
        WHERE p.proteinid = %s
            AND pt.peptideid = %s;
        """
        print(proteinid, peptideid)
        cursor.execute(sql, (proteinid, peptideid))
        result['pdbData'] = cursor.fetchone()

        
    except Exception as e:
        result['error'] = f"Error querying pdbdata information: {str(e)}"
    finally:
        cursor.close()
    
    return result

#蛋白质id 序列
def query_protein_info(connection, protein_id):
    result = {}
    try:
        # 创建游标对象
        cursor = connection.cursor()
        
        # 查询 Protein 表中的信息
        protein_query = "SELECT ProteinId, ProteinSequence FROM Proteins WHERE ProteinId = %s"
        cursor.execute(protein_query, (protein_id,))
        protein_info = cursor.fetchone()  # 只取一条记录
        
        if protein_info:
            result['ProteinId'] = protein_info[0]
            result['ProteinSequence'] = protein_info[1]
        else:
            result['error'] = f"No protein found with ID: {protein_id}"
        
    except Exception as e:
        result['error'] = f"Error querying protein information: {str(e)}"
    finally:
        cursor.close()
    
    return protein_info[1]

# @app.route("/query_protein/<string:protein_id>", methods=["GET"])
# def query_interface_info(connection, protein_id):
#     result = {}
#     try:
#         # 创建游标对象
#         cursor = connection.cursor()
        
#         # 查询 Protein 表中的信息
#         protein_query = "SELECT ProteinId, ProteinSequence FROM Proteins WHERE ProteinId = %s"
#         cursor.execute(protein_query, (protein_id,))
#         protein_info = cursor.fetchone()  # 只取一条记录
        
#         if protein_info:
#             result['ProteinId'] = protein_info[0]
#             result['ProteinSequence'] = protein_info[1]
#         else:
#             result['error'] = f"No protein found with ID: {protein_id}"
        
#         # 查询与该蛋白质相关的中间表信息
#         peptide_query = """
#         SELECT PeptideId, pdbData 
#         FROM Proteins 
#         WHERE ProteinId = %s
#         """
#         cursor.execute(peptide_query, (protein_id,))
#         peptide_records = cursor.fetchall()

#         if peptide_records:
#             result['Peptides'] = []
#             for peptide in peptide_records:
#                 result['Peptides'].append({
#                     'PeptideId': peptide[0],
#                     'pdbData': peptide[1]  # 可以选择在这里返回 pdbData
#                 })
#         else:
#             result['Peptides'] = "No peptide records found for Protein ID: {}".format(protein_id)
        
#     except Exception as e:
#         result['error'] = f"Error querying protein information: {str(e)}"
#     finally:
#         cursor.close()
    
#     return result


if __name__ == "__main__":
    app.run(debug=True)

