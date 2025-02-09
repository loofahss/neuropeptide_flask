def query_protein_info(connection, protein_id):
    try:
        cursor = connection.cursor()
        sql = "SELECT ProteinId, ProteinSequence FROM Proteins WHERE ProteinId = %s"
        cursor.execute(sql, (protein_id,))
        protein_info = cursor.fetchone()

        if protein_info:
            return {'ProteinId': protein_info[0], 'ProteinSequence': protein_info[1]}
        return {'error': f"No protein found with ID: {protein_id}"}
    except Exception as e:
        return {'error': f"Database error: {str(e)}"}
    finally:
        cursor.close()
