import os
from datetime import date
from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# Enable CORS for frontend
CORS(app)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "biomed_db"),
        port=int(os.getenv("DB_PORT", 3306))
    )

def calculate_age(born_date):
    if not born_date:
        return None
    today = date.today()
    return today.year - born_date.year - ((today.month, today.day) < (born_date.month, born_date.day))

@app.route('/api/patients', methods=['GET'])
def get_patients():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT p.*,
                   (SELECT phone_number FROM patient_phones WHERE AMKA = p.AMKA LIMIT 1) AS phone_number,
                   (SELECT provider_id FROM has_provider WHERE AMKA = p.AMKA LIMIT 1) AS provider_id,
                   (SELECT name FROM insurance_providers ip JOIN has_provider hp ON ip.provider_id = hp.provider_id WHERE hp.AMKA = p.AMKA LIMIT 1) AS insurance_name,
                   (SELECT phone_number FROM insurance_providers ip JOIN has_provider hp ON ip.provider_id = hp.provider_id WHERE hp.AMKA = p.AMKA LIMIT 1) AS insurance_phone,
                   (SELECT address_id FROM has_address WHERE AMKA = p.AMKA LIMIT 1) AS address_id,
                   (SELECT street FROM addresses a JOIN has_address ha ON a.address_id = ha.address_id WHERE ha.AMKA = p.AMKA LIMIT 1) AS street,
                   (SELECT number FROM addresses a JOIN has_address ha ON a.address_id = ha.address_id WHERE ha.AMKA = p.AMKA LIMIT 1) AS street_number,
                   (SELECT GROUP_CONCAT(asub.substance_name SEPARATOR ',') FROM active_substances asub JOIN has_allergy ha ON asub.substance_id = ha.substance_id WHERE ha.AMKA = p.AMKA) AS allergies_list
            FROM patients p
        """
        cursor.execute(query)
        patients = cursor.fetchall()
        
        patient_list = []
        for p in patients:
            birth_date = p['date_of_birth']
            birth_date_str = birth_date.strftime('%Y-%m-%d') if birth_date else None
            
            # Map database representation of sex back to frontend expectations
            fe_sex = 'Άνδρας'
            if p['sex'] == 'Θήλυ':
                fe_sex = 'Γυναίκα'
            elif p['sex'] == 'Άλλο':
                fe_sex = 'Άλλο'

            allergies = []
            if p['allergies_list']:
                allergies = p['allergies_list'].split(',')

            insurance_provider = None
            if p['insurance_name']:
                insurance_provider = {
                    "provider_id": p['provider_id'],
                    "name": p['insurance_name'],
                    "phone_number": p['insurance_phone']
                }

            address = None
            if p['street']:
                address = {
                    "address_id": p['address_id'],
                    "street": p['street'],
                    "number": p['street_number']
                }

            patient_list.append({
                "patient": {
                    "AMKA": p['AMKA'],
                    "first_name": p['first_name'],
                    "last_name": p['last_name'],
                    "patronym": p['patronym'],
                    "date_of_birth": birth_date_str,
                    "age": calculate_age(birth_date),
                    "sex": fe_sex,
                    "weight": float(p['weight']) if p['weight'] is not None else None,
                    "height": float(p['height']) if p['height'] is not None else None,
                    "email": p['email'],
                    "occupation": p['occupation'],
                    "nationality": p['nationality'],
                    "phone_number": p['phone_number'],
                    "insurance_provider": insurance_provider,
                    "address": address,
                    "allergies": allergies
                }
            })
            
        return jsonify(patient_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/api/patients', methods=['POST'])
def add_patient():
    data = request.json
    if not data or 'patient' not in data:
        return jsonify({"error": "Missing patient data"}), 400
    
    p = data['patient']
    
    # Map sex from frontend to database
    db_sex = 'Άρρεν'
    if p.get('sex') == 'Γυναίκα':
        db_sex = 'Θήλυ'
    elif p.get('sex') == 'Άλλο':
        db_sex = 'Άλλο'

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO patients (AMKA, first_name, last_name, patronym, date_of_birth, sex, weight, height, email, occupation, nationality)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            p['AMKA'],
            p['first_name'],
            p['last_name'],
            p['patronym'],
            p['date_of_birth'],
            db_sex,
            p.get('weight'),
            p.get('height'),
            p.get('email'),
            p.get('occupation'),
            p.get('nationality')
        )
        
        cursor.execute(query, values)
        
        # Insert phone number if provided
        if p.get('phone_number'):
            cursor.execute("""
                INSERT INTO patient_phones (AMKA, phone_number)
                VALUES (%s, %s)
            """, (p['AMKA'], p['phone_number']))
            
        conn.commit()
        return jsonify({"message": "Patient added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/api/patients/<amka>/health-file', methods=['GET'])
def get_patient_health_file(amka):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True, buffered=True)
        
        # 1. Fetch patient personal info
        cursor.execute("SELECT * FROM patients WHERE AMKA = %s", (amka,))
        p = cursor.fetchone()
        if not p:
            return jsonify({"error": "Patient not found"}), 404
            
        birth_date = p['date_of_birth']
        birth_date_str = birth_date.strftime('%Y-%m-%d') if birth_date else None
        
        fe_sex = 'Άνδρας'
        if p['sex'] == 'Θήλυ':
            fe_sex = 'Γυναίκα'
        elif p['sex'] == 'Άλλο':
            fe_sex = 'Άλλο'
            
        patient_data = {
            "AMKA": p['AMKA'],
            "first_name": p['first_name'],
            "last_name": p['last_name'],
            "patronym": p['patronym'],
            "date_of_birth": birth_date_str,
            "age": calculate_age(birth_date),
            "sex": fe_sex,
            "weight": float(p['weight']) if p['weight'] is not None else None,
            "height": float(p['height']) if p['height'] is not None else None,
            "email": p['email'],
            "occupation": p['occupation'],
            "nationality": p['nationality'],
            "phone_number": None,
            "allergies": [],
            "address": None,
            "insurance_provider": None
        }
        
        # Fetch phone number
        cursor.execute("SELECT phone_number FROM patient_phones WHERE AMKA = %s LIMIT 1", (amka,))
        phone_row = cursor.fetchone()
        if phone_row:
            patient_data["phone_number"] = phone_row["phone_number"]
        
        # Fetch address
        cursor.execute("""
            SELECT a.* FROM addresses a
            JOIN has_address ha ON a.address_id = ha.address_id
            WHERE ha.AMKA = %s
        """, (amka,))
        addr = cursor.fetchone()
        if addr:
            patient_data["address"] = {
                "address_id": addr["address_id"],
                "street": addr["street"],
                "number": addr["number"]
            }
            
        # Fetch insurance provider
        cursor.execute("""
            SELECT ip.* FROM insurance_providers ip
            JOIN has_provider hp ON ip.provider_id = hp.provider_id
            WHERE hp.AMKA = %s
        """, (amka,))
        ip = cursor.fetchone()
        if ip:
            patient_data["insurance_provider"] = {
                "provider_id": ip["provider_id"],
                "name": ip["name"],
                "phone_number": ip["phone_number"]
            }
            
        # Fetch allergies (active substances)
        cursor.execute("""
            SELECT substance_name FROM active_substances asub
            JOIN has_allergy ha ON asub.substance_id = ha.substance_id
            WHERE ha.AMKA = %s
        """, (amka,))
        allergies = cursor.fetchall()
        patient_data["allergies"] = [a["substance_name"] for a in allergies]
        
        # 2. Fetch diagnoses history
        cursor.execute("""
            SELECT dh.diagnosis_id, dh.ICD10_code, d.description, dh.diagnosis_date
            FROM diagnosis_history dh
            JOIN diagnosis d ON dh.ICD10_code = d.ICD10_code
            WHERE dh.patient_AMKA = %s
            ORDER BY dh.diagnosis_date DESC
        """, (amka,))
        diagnoses = cursor.fetchall()
        for d in diagnoses:
            if d['diagnosis_date']:
                d['diagnosis_date'] = d['diagnosis_date'].strftime('%Y-%m-%d')
                
        # 3. Fetch doctor visits
        cursor.execute("""
            SELECT dv.visit_id, dv.visit_datetime, doc.first_name, doc.last_name, doc.specialty
            FROM doc_visits dv
            JOIN doctors doc ON dv.doctor_AMKA = doc.AMKA
            WHERE dv.patient_AMKA = %s
            ORDER BY dv.visit_datetime DESC
        """, (amka,))
        visits = cursor.fetchall()
        for v in visits:
            if v['visit_datetime']:
                v['visit_datetime'] = v['visit_datetime'].strftime('%Y-%m-%d %H:%M')
            v['doctor_name'] = f"δρ. {v['last_name']} {v['first_name']}"
            v['doctor_specialty'] = v['specialty']
            del v['first_name']
            del v['last_name']
            del v['specialty']
            
        # 4. Fetch prescriptions with active substances
        cursor.execute("""
            SELECT pr.prescription_id, pr.start_date, pr.end_date, pr.dosage, pr.frequency,
                   m.product_name, m.med_id, doc.first_name, doc.last_name
            FROM prescriptions pr
            JOIN medications m ON pr.med_id = m.med_id
            JOIN doctors doc ON pr.doctor_AMKA = doc.AMKA
            WHERE pr.patient_AMKA = %s
            ORDER BY pr.start_date DESC
        """, (amka,))
        prescriptions = cursor.fetchall()
        for p in prescriptions:
            if p['start_date']:
                p['start_date'] = p['start_date'].strftime('%Y-%m-%d')
            if p['end_date']:
                p['end_date'] = p['end_date'].strftime('%Y-%m-%d')
            p['doctor_name'] = f"δρ. {p['last_name']} {p['first_name']}"
            p['medication_name'] = p['product_name']
            
            # Fetch active substances for the med
            cursor.execute("""
                SELECT substance_name FROM active_substances asub
                JOIN med_contains mc ON asub.substance_id = mc.substance_id
                WHERE mc.med_id = %s
            """, (p['med_id'],))
            subs = cursor.fetchall()
            p['active_substances'] = [s['substance_name'] for s in subs]
            
            del p['first_name']
            del p['last_name']
            del p['product_name']
            del p['med_id']
            
        # 5. Fetch referrals
        cursor.execute("""
            SELECT rf.referral_id, rf.issue_date, rf.expiration_date, lt.lab_test_type, lt.lab_test_description,
                   doc.first_name, doc.last_name
            FROM referrals rf
            JOIN lab_tests lt ON rf.lab_test_id = lt.lab_test_id
            JOIN doctors doc ON rf.doctor_AMKA = doc.AMKA
            WHERE rf.patient_AMKA = %s
            ORDER BY rf.issue_date DESC
        """, (amka,))
        referrals = cursor.fetchall()
        for r in referrals:
            if r['issue_date']:
                r['issue_date'] = r['issue_date'].strftime('%Y-%m-%d')
            if r['expiration_date']:
                r['expiration_date'] = r['expiration_date'].strftime('%Y-%m-%d')
            r['doctor_name'] = f"δρ. {r['last_name']} {r['first_name']}"
            del r['first_name']
            del r['last_name']
            
        # 6. Fetch external lab tests performed
        cursor.execute("""
            SELECT elt.ex_lab_test_id, elt.datetime, elt.results, elt.cost, lt.lab_test_type
            FROM ex_lab_tests elt
            JOIN lab_tests lt ON elt.lab_test_id = lt.lab_test_id
            WHERE elt.patient_AMKA = %s
            ORDER BY elt.datetime DESC
        """, (amka,))
        lab_tests = cursor.fetchall()
        for lt in lab_tests:
            if lt['datetime']:
                lt['datetime'] = lt['datetime'].strftime('%Y-%m-%d %H:%M')
            if lt['cost']:
                lt['cost'] = float(lt['cost'])
                
        # 7. Fetch hospitalizations
        cursor.execute("""
            SELECT hp.hospitalization_id, hp.date_of_admission, hp.date_of_discharge, hosp.hospital_name
            FROM hospitalizations hp
            JOIN hospitals hosp ON hp.hospital_id = hosp.hospital_id
            WHERE hp.patient_AMKA = %s
            ORDER BY hp.date_of_admission DESC
        """, (amka,))
        hospitalizations = cursor.fetchall()
        for h in hospitalizations:
            if h['date_of_admission']:
                h['date_of_admission'] = h['date_of_admission'].strftime('%Y-%m-%d')
            if h['date_of_discharge']:
                h['date_of_discharge'] = h['date_of_discharge'].strftime('%Y-%m-%d')
                
        return jsonify({
            "patient": patient_data,
            "diagnoses": diagnoses,
            "visits": visits,
            "prescriptions": prescriptions,
            "referrals": referrals,
            "lab_tests": lab_tests,
            "hospitalizations": hospitalizations
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/api/diagnoses', methods=['GET'])
def get_diagnoses():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT ICD10_code, description FROM diagnosis ORDER BY ICD10_code")
        diagnoses = cursor.fetchall()
        return jsonify(diagnoses)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT AMKA, first_name, last_name, specialty FROM doctors ORDER BY last_name, first_name")
        doctors = cursor.fetchall()
        return jsonify(doctors)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/api/medications', methods=['GET'])
def get_medications():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT med_id, product_name, administration_route FROM medications ORDER BY product_name")
        medications = cursor.fetchall()
        return jsonify(medications)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/api/patients/<amka>/diagnoses', methods=['POST'])
def add_patient_diagnosis(amka):
    data = request.json
    if not data or 'ICD10_code' not in data or 'diagnosis_date' not in data:
        return jsonify({"error": "Missing diagnosis data"}), 400
        
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO diagnosis_history (ICD10_code, diagnosis_date, patient_AMKA)
            VALUES (%s, %s, %s)
        """, (data['ICD10_code'], data['diagnosis_date'], amka))
        conn.commit()
        return jsonify({"message": "Diagnosis added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/api/patients/<amka>/prescriptions', methods=['POST'])
def add_patient_prescription(amka):
    data = request.json
    if not data or 'med_id' not in data or 'doctor_AMKA' not in data or 'start_date' not in data or 'dosage' not in data or 'frequency' not in data:
        return jsonify({"error": "Missing prescription data"}), 400
        
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO prescriptions (start_date, end_date, dosage, frequency, patient_AMKA, doctor_AMKA, med_id, visit_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NULL)
        """, (data['start_date'], data.get('end_date') or None, data['dosage'], data['frequency'], amka, data['doctor_AMKA'], data['med_id']))
        conn.commit()
        return jsonify({"message": "Prescription added successfully"}), 201
    except mysql.connector.Error as err:
        if err.sqlstate == '45000':
            return jsonify({"error": err.msg}), 400
        return jsonify({"error": str(err)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
