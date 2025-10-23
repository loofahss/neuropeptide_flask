from flask import Blueprint, request, jsonify

# 创建一个名为 "api" 的蓝图
api = Blueprint('api', __name__)

from flask import Flask, request, jsonify
import pymysql
from flask_cors import CORS
import random
#1.proteinid返回proteinsequence,peptideid,peptidesequence,pdbdata,string_len(peptidesequence)
#2.peptideid返回peptidesequence,proteinid,proteinsequence,pdbdata,string_len(proteinsequence)
# 显示pEI值,进行筛选
# 通过proteinid,peptideid查询pdbdata,显示pdbdata,pEI,peptidesequence
# app = Flask(__name__)
# CORS(app)
CORS(api, resources={r"/*": {"origins": "*"}})
# 打开数据库连接
def connect():
    return pymysql.connect(host='localhost',
                        database='neuropep_ina',
                        user='root',
                        passwd='Isyslab408',
			unix_socket='/var/lib/mysql/mysql.sock')
# def connect():
#     return pymysql.connect(host='localhost',
#                         database='neuropenet',
#                         user='root',
#                         passwd='your_password')
@api.route("/")
def index():
    return "Hello World!"


# post_form


# #get proteinsequence
# @app.route("/query/proteinsequence", methods=["POST"])
# def query_byprotein():
#     data = request.json  # 使用 request.json 获取 JSON 数据
#     protein_id = data.get("protein_id")
#     db=connect()
#     result = query_interface_info(db, protein_id)
#     proteinsequence=query_protein_info(db,protein_id)
#     print(proteinsequence)
#     # print(protein_id)
#     # print(result)
#     return {"proteinsequence":proteinsequence}


@api.route("/proteinsequence", methods=["POST"])
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


@api.route("/peptidesequence", methods=["POST"])
def query_bypeptide():
    data = request.json  # 使用 request.json 获取 JSON 数据
    protein_id = data.get("protein_id")
    db = connect()
    
    try:
        cursor = db.cursor()
        # 查询 proteinsequence
        proteinsequence_query = "SELECT peptidesequence FROM peptides WHERE peptideid = %s"
        cursor.execute(proteinsequence_query, (protein_id,))
        proteinsequence = cursor.fetchone()[0]

        # 查询 peptides
        peptides_query = """
            SELECT pp1.proteinid, p.proteinSequence, pp1.PEI ,pp1.pdbData
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
    finally:
        cursor.close()
        db.close()
    
    return jsonify(result)



@api.route("/pdbdata",methods=["POST"])
def query_pdbdata():
    db=connect()
    data = request.json  # 使用 request.json 获取 JSON 数据
    proteinid=data.get("proteinid")
    peptideid=data.get("peptideid")
    print('hii')
    result=query_pdbdata_info(db,proteinid,peptideid)

    # print(result['pdbData'].split('\n')[0])
    return {"pdbdata":result}

def query_pdbdata_info(connection,proteinid,peptideid):
    result = {}
    try:
        # 创建游标对象
        cursor = connection.cursor()
        sql = """
        SELECT pp.pdbdata,pp.PEI
        FROM protein_peptide pp
        JOIN proteins p ON pp.proteinid = p.proteinid
        JOIN peptides pt ON pp.peptideid = pt.peptideid
        
        WHERE p.proteinid = %s
            AND pt.peptideid = %s;
        """
        print(proteinid, peptideid)
        cursor.execute(sql, (proteinid, peptideid))
        # result['pdbData'] = cursor.fetchone()
        # row = cursor.fetchone()
        # if row:
        #     result['pdbData'] = row[0]
        #     result['PEI'] = row[1]
        # else:
        #     result['error'] = "No data found for the given proteinid and peptideid."
        result['pdbData'] = cursor.fetchone()
        
    except Exception as e:
        result['error'] = f"Error querying pdbdata information: {str(e)}"
    finally:
        cursor.close()
    
    return result


if __name__ == "__main__":
    api.run(debug=True)
