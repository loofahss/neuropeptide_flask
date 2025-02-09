import pymysql
import os
from dotenv import load_dotenv

# 加载 .env 配置
load_dotenv()

def connect():
    """创建数据库连接"""
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "neuropenet"),
        user=os.getenv("DB_USER", "root"),
        passwd=os.getenv("DB_PASS", "your_password"),
        cursorclass=pymysql.cursors.DictCursor  # 以字典格式返回数据
    )

def query_protein_info(protein_id):
    """查询 Protein 的信息"""
    result = {}
    connection = connect()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT ProteinId, ProteinSequence FROM Proteins WHERE ProteinId = %s"
            cursor.execute(sql, (protein_id,))
            protein_info = cursor.fetchone()
            
            if protein_info:
                result = protein_info
            else:
                result["error"] = f"No protein found with ID: {protein_id}"
    except Exception as e:
        result["error"] = str(e)
    finally:
        connection.close()
    
    return result

def query_peptides_by_protein(protein_id):
    """查询 Protein 关联的 Peptide 及 PDB 数据"""
    connection = connect()
    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT pp.PeptideId, p.PeptideSequence, pp.PEI, pp.pdbData
                FROM Protein_Peptide AS pp
                JOIN Peptides AS p ON pp.PeptideId = p.PeptideId
                WHERE pp.ProteinId = %s
            """
            cursor.execute(sql, (protein_id,))
            return cursor.fetchall()
    except Exception as e:
        return {"error": str(e)}
    finally:
        connection.close()

def query_pdbdata(protein_id, peptide_id):
    """查询 PDB 数据"""
    connection = connect()
    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT pp.pdbData, pp.PEI, p.PeptideSequence
                FROM Protein_Peptide pp
                JOIN Proteins pr ON pp.ProteinId = pr.ProteinId
                JOIN Peptides p ON pp.PeptideId = p.PeptideId
                WHERE pr.ProteinId = %s AND p.PeptideId = %s
            """
            cursor.execute(sql, (protein_id, peptide_id))
            return cursor.fetchone()
    except Exception as e:
        return {"error": str(e)}
    finally:
        connection.close()
