import os
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker('el_GR')
fake_en = Faker()

NUM_PATIENTS        = 200
NUM_DOCTORS         = 30
NUM_ADDRESSES       = 220
NUM_PROVIDERS       = 10
NUM_HOSPITALS       = 15
NUM_DIAGNOSES       = 50
NUM_LAB_TESTS       = 25
NUM_MEDICATIONS     = 40
NUM_SUBSTANCES      = 60
NUM_VISITS          = 300
NUM_PRESCRIPTIONS   = 250
NUM_REFERRALS       = 180
NUM_EX_LAB_TESTS    = 200
NUM_HOSPITALIZATIONS= 80

SEX_CHOICES = ['Άρρεν', 'Θήλυ', 'Άλλο']

SPECIALTIES = [
    'Παθολόγος', 'Χειρουργός', 'Καρδιολόγος', 'Νευρολόγος', 'Ορθοπεδικός',
    'Δερματολόγος', 'Οφθαλμολόγος', 'Ωτορινολαρυγγολόγος', 'Παιδίατρος',
    'Ψυχίατρος', 'Ουρολόγος', 'Γυναικολόγος', 'Ρευματολόγος', 'Ογκολόγος',
    'Αιματολόγος', 'Ενδοκρινολόγος', 'Πνευμονολόγος', 'Γαστρεντερολόγος',
]

ADMIN_ROUTES = [
    'Από του στόματος', 'Ενδοφλέβια', 'Ενδομυϊκή', 'Υποδόρια',
    'Τοπική εφαρμογή', 'Εισπνοή', 'Υπογλώσσια', 'Ορθική',
]

PROVIDER_NAMES = [
    'ΕΟΠΥΥ', 'ΕΦΚΑ', 'Allianz Ελλάς', 'Interamerican', 'Generali Hellas',
    'Eurolife FFH', 'ΑΧΑ Ασφαλιστική', 'Εθνική Ασφαλιστική',
    'Υδρόγειος Ασφαλιστική', 'Ergo Ασφαλιστική',
]

HOSPITAL_NAMES = [
    'Γενικό Νοσοκομείο Αθηνών «Λαϊκό»',
    'Γενικό Νοσοκομείο Αθηνών «Ευαγγελισμός»',
    'Γενικό Νοσοκομείο «Γ. Γεννηματάς»',
    'Γενικό Νοσοκομείο Αττικής «Σισμανόγλειο»',
    'Νοσοκομείο «Αρεταίειο»',
    'Γενικό Νοσοκομείο Θεσσαλονίκης «ΑΧΕΠΑ»',
    'Γενικό Νοσοκομείο Θεσσαλονίκης «Ιπποκράτειο»',
    'Γενικό Νοσοκομείο Πατρών «Ο Άγιος Ανδρέας»',
    'Πανεπιστημιακό Γενικό Νοσοκομείο Ηρακλείου «ΠΑΓΝΗ»',
    'Γενικό Νοσοκομείο Ιωαννίνων «Γ. Χατζηκώστα»',
    'Γενικό Νοσοκομείο Βόλου «Αχιλλοπούλειο»',
    'Γενικό Νοσοκομείο Λάρισας',
    'Γενικό Νοσοκομείο Καβάλας',
    'Κλινική «Υγεία»',
    'Κλινική «Μητέρα»',
]

# Realistic ICD-10 codes with Greek descriptions
ICD10_POOL = [
    ('I10',   'Υπέρταση'),
    ('E11',   'Σακχαρώδης διαβήτης τύπου 2'),
    ('J45',   'Άσθμα'),
    ('M54.5', 'Οσφυαλγία'),
    ('K21',   'Γαστροοισοφαγική παλινδρόμηση'),
    ('F32',   'Καταθλιπτικό επεισόδιο'),
    ('J06',   'Οξεία λοίμωξη ανώτερου αναπνευστικού'),
    ('N18',   'Χρόνια νεφρική νόσος'),
    ('I25',   'Χρόνια ισχαιμική νόσος καρδίας'),
    ('E78',   'Υπερλιπιδαιμία'),
    ('M05',   'Ρευματοειδής αρθρίτιδα'),
    ('C50',   'Κακόηθες νεόπλασμα μαστού'),
    ('G40',   'Επιληψία'),
    ('K50',   'Νόσος Crohn'),
    ('L40',   'Ψωρίαση'),
    ('J44',   'Χρόνια αποφρακτική πνευμονοπάθεια (ΧΑΠ)'),
    ('H40',   'Γλαύκωμα'),
    ('D50',   'Σιδηροπενική αναιμία'),
    ('B19',   'Χρόνια ηπατίτιδα'),
    ('Z00',   'Τακτικός έλεγχος υγείας'),
    ('A09',   'Γαστρεντερίτιδα'),
    ('R51',   'Κεφαλαλγία'),
    ('M15',   'Πολυαρθρίτιδα'),
    ('I48',   'Κολπική μαρμαρυγή'),
    ('E03',   'Υποθυρεοειδισμός'),
    ('N39',   'Ουρολοίμωξη'),
    ('J18',   'Πνευμονία'),
    ('K57',   'Εκκολπωματίτιδα'),
    ('M17',   'Οστεοαρθρίτιδα γόνατος'),
    ('F41',   'Αγχώδης διαταραχή'),
    ('C18',   'Κακόηθες νεόπλασμα παχέος εντέρου'),
    ('I21',   'Οξύ έμφραγμα μυοκαρδίου'),
    ('G30',   'Νόσος Alzheimer'),
    ('E10',   'Σακχαρώδης διαβήτης τύπου 1'),
    ('H26',   'Καταρράκτης'),
    ('K74',   'Κίρρωση ήπατος'),
    ('M81',   'Οστεοπόρωση'),
    ('R00',   'Αρρυθμία'),
    ('T14',   'Τραυματισμός'),
    ('Z23',   'Εμβολιασμός'),
    ('J20',   'Οξεία βρογχίτιδα'),
    ('N20',   'Νεφρολιθίαση'),
    ('K29',   'Γαστρίτιδα'),
    ('B34',   'Ιογενής λοίμωξη'),
    ('R05',   'Βήχας'),
    ('R50',   'Πυρετός'),
    ('L20',   'Ατοπική δερματίτιδα'),
    ('F10',   'Διαταραχές από αλκοόλ'),
    ('G43',   'Ημικρανία'),
    ('I63',   'Εγκεφαλικό επεισόδιο'),
]

LAB_TEST_POOL = [
    ('Γενική αίματος',                   'Πλήρης αιματολογική εξέταση'),
    ('Βιοχημικές εξετάσεις αίματος',     'Γλυκόζη, ουρία, κρεατινίνη, ηλεκτρολύτες'),
    ('Λιπιδαιμικό προφίλ',               'Ολική χοληστερόλη, LDL, HDL, τριγλυκερίδια'),
    ('Γλυκοζυλιωμένη αιμοσφαιρίνη HbA1c','Έλεγχος μακροπρόθεσμης ρύθμισης σακχαρώδη διαβήτη'),
    ('Θυρεοειδικές ορμόνες TSH/T4',      'Αξιολόγηση λειτουργίας θυρεοειδούς'),
    ('Γενική ούρων',                      'Ανάλυση ούρων για διαγνωστικούς σκοπούς'),
    ('Ακτινογραφία θώρακα',              'Απεικονιστικός έλεγχος θώρακα'),
    ('Ηλεκτροκαρδιογράφημα (ΗΚΓ)',       'Καταγραφή ηλεκτρικής δραστηριότητας καρδιάς'),
    ('Υπερηχογράφημα κοιλίας',           'Απεικόνιση οργάνων κοιλίας με υπέρηχο'),
    ('Τομογραφία (CT) κεφαλής',          'Αξονική τομογραφία εγκεφάλου'),
    ('MRI μυοσκελετικού',                'Μαγνητική τομογραφία αρθρώσεων/μυών'),
    ('Καλλιέργεια ούρων',                'Ανίχνευση και ταυτοποίηση μικροοργανισμών ούρων'),
    ('PSA ολικό',                         'Ειδικό προστατικό αντιγόνο'),
    ('Παπ τεστ',                          'Κυτταρολογική εξέταση τραχήλου μήτρας'),
    ('Ακουόγραμμα',                       'Έλεγχος ακοής'),
    ('Σπιρομέτρηση',                      'Μέτρηση πνευμονικής λειτουργίας'),
    ('Οστεομετρία (DEXA)',                'Μέτρηση οστικής πυκνότητας'),
    ('Μαστογραφία',                       'Απεικόνιση μαστού'),
    ('Γαστροσκόπηση',                     'Ενδοσκόπηση ανώτερου πεπτικού'),
    ('Κολονοσκόπηση',                     'Ενδοσκόπηση παχέος εντέρου'),
    ('Αιμοκαλλιέργεια',                  'Ανίχνευση μικροοργανισμών στο αίμα'),
    ('Ανοσολογικές εξετάσεις',           'Αντισώματα ANA, RF κ.ά.'),
    ('Ηπατικές δοκιμασίες',             'SGOT, SGPT, γ-GT, αλκαλική φωσφατάση'),
    ('Πήξη αίματος (INR/PT/aPTT)',       'Έλεγχος πηκτικότητας'),
    ('Εξέταση κοπράνων',                 'Γενική εξέταση και καλλιέργεια κοπράνων'),
]

MEDICATION_POOL = [
    ('Depakin',        'Εισπνοή',          'Ελλάδα',  'valproic acid'),
    ('Lisinopril',     'Από του στόματος', 'Ελλάδα',  'lisinopril'),
    ('Metformin',      'Από του στόματος', 'Ελλάδα',  'metformin'),
    ('Atorvastatin',   'Από του στόματος', 'Ελλάδα',  'atorvastatin'),
    ('Omeprazole',     'Από του στόματος', 'Ελλάδα',  'omeprazole'),
    ('Amoxicillin',    'Από του στόματος', 'Ελλάδα',  'amoxicillin'),
    ('Paracetamol',    'Από του στόματος', 'Ελλάδα',  'paracetamol'),
    ('Ibuprofen',      'Από του στόματος', 'Ελλάδα',  'ibuprofen'),
    ('Amlodipine',     'Από του στόματος', 'Ελλάδα',  'amlodipine'),
    ('Losartan',       'Από του στόματος', 'Ελλάδα',  'losartan'),
    ('Sertraline',     'Από του στόματος', 'Ελλάδα',  'sertraline'),
    ('Alprazolam',     'Από του στόματος', 'Ελλάδα',  'alprazolam'),
    ('Furosemide',     'Από του στόματος', 'Ελλάδα',  'furosemide'),
    ('Warfarin',       'Από του στόματος', 'Ελλάδα',  'warfarin'),
    ('Insulin Glargine','Υποδόρια',        'Γερμανία', 'insulin glargine'),
    ('Levothyroxine',  'Από του στόματος', 'Ελλάδα',  'levothyroxine'),
    ('Prednisolone',   'Από του στόματος', 'Ελλάδα',  'prednisolone'),
    ('Salbutamol',     'Εισπνοή',          'Ελλάδα',  'salbutamol'),
    ('Azithromycin',   'Από του στόματος', 'Ελλάδα',  'azithromycin'),
    ('Pantoprazole',   'Από του στόματος', 'Ελλάδα',  'pantoprazole'),
    ('Bisoprolol',     'Από του στόματος', 'Ελλάδα',  'bisoprolol'),
    ('Clopidogrel',    'Από του στόματος', 'Ελλάδα',  'clopidogrel'),
    ('Escitalopram',   'Από του στόματος', 'Ελλάδα',  'escitalopram'),
    ('Tramadol',       'Από του στόματος', 'Ελλάδα',  'tramadol'),
    ('Codeine',        'Από του στόματος', 'Ελλάδα',  'codeine'),
    ('Cetirizine',     'Από του στόματος', 'Ελλάδα',  'cetirizine'),
    ('Valsartan',      'Από του στόματος', 'Ελλάδα',  'valsartan'),
    ('Enoxaparin',     'Υποδόρια',         'Γαλλία',  'enoxaparin'),
    ('Metoprolol',     'Από του στόματος', 'Ελλάδα',  'metoprolol'),
    ('Gabapentin',     'Από του στόματος', 'Ελλάδα',  'gabapentin'),
    ('Ciprofloxacin',  'Από του στόματος', 'Ελλάδα',  'ciprofloxacin'),
    ('Doxycycline',    'Από του στόματος', 'Ελλάδα',  'doxycycline'),
    ('Naproxen',       'Από του στόματος', 'Ελλάδα',  'naproxen'),
    ('Simvastatin',    'Από του στόματος', 'Ελλάδα',  'simvastatin'),
    ('Clindamycin',    'Από του στόματος', 'Ελλάδα',  'clindamycin'),
    ('Carvedilol',     'Από του στόματος', 'Ελλάδα',  'carvedilol'),
    ('Fluoxetine',     'Από του στόματος', 'Ελλάδα',  'fluoxetine'),
    ('Spironolactone', 'Από του στόματος', 'Ελλάδα',  'spironolactone'),
    ('Quetiapine',     'Από του στόματος', 'Ελλάδα',  'quetiapine'),
    ('Hydrochlorothiazide', 'Από του στόματος', 'Ελλάδα', 'hydrochlorothiazide'),
]

DOSAGES    = ['5mg', '10mg', '20mg', '25mg', '50mg', '100mg', '250mg', '500mg', '1g', '2.5mg', '0.5mg']
FREQUENCIES= ['Μία φορά ημερησίως', 'Δύο φορές ημερησίως', 'Τρεις φορές ημερησίως',
               'Κάθε 8 ώρες', 'Κάθε 12 ώρες', 'Εφάπαξ', 'Εβδομαδιαίως', 'Μήνα']


def escape_str(val):
    
    if val is None or val == r'\N' or val == '':
        return "NULL"
    if isinstance(val, (int, float)):
        return str(val)
    if isinstance(val, bool):
        return "TRUE" if val else "FALSE"
    escaped_val = str(val).replace('\\', '\\\\').replace(chr(39), chr(39)+chr(39))
    return f"'{escaped_val}'"


def write_inserts(f, table_name, data):
    if not data: return
    f.write(f"INSERT INTO {table_name} VALUES\n")
    lines = []
    for row in data:
        lines.append("(" + ", ".join(escape_str(v) for v in row) + ")")
    f.write(",\n".join(lines) + ";\n\n")


def random_phone():
    prefix = random.choice(['69', '21', '22', '23', '24', '25', '26', '27', '28'])
    return prefix + ''.join([str(random.randint(0, 9)) for _ in range(8)])


def random_datetime(start_year=2018, end_year=2024):
    start = datetime(start_year, 1, 1)
    end   = datetime(end_year, 12, 31)
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))


def generate_amka(dob, used_amkas):
    ddmmyy = dob.strftime('%d%m%y')
    while True:
        serial = f"{random.randint(0, 99999):05d}"
        amka   = ddmmyy + serial
        if amka not in used_amkas:
            used_amkas.add(amka)
            return amka


def generate_license(used_licenses):
    while True:
        lic = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))
        if lic not in used_licenses:
            used_licenses.add(lic)
            return lic


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(current_dir, "load.sql")

    with open(output_file, 'w', encoding='utf-8') as f:

        f.write("SET FOREIGN_KEY_CHECKS = 0;\n")
        f.write("SET NAMES utf8mb4;\n\n")
        f.write("USE biomed_db;\n\n")

        tables_to_truncate = [
            'has_provider', 'has_address', 'hospitalizations', 'diagnosis_history',
            'ex_lab_tests', 'referrals', 'prescriptions', 'doc_visits',
            'has_allergy', 'med_contains', 'medications', 'active_substances',
            'lab_tests', 'diagnosis', 'hospital_contact', 'hospitals',
            'insurance_providers', 'addresses', 'patient_contact',
            'patient_phones', 'patients', 'doctors',
        ]
        for t in tables_to_truncate:
            f.write(f"TRUNCATE TABLE {t};\n")
        f.write("\n")

        amkas = set()
        used_licenses = set()
        doctors_data  = []
        doctor_amkas  = []


        #doctors
        for _ in range(NUM_DOCTORS):
            sex        = random.choice(['Άρρεν', 'Θήλυ'])
            first_name = fake.first_name_male() if sex == 'Άρρεν' else fake.first_name_female()
            last_name  = fake.last_name_male()  if sex == 'Άρρεν' else fake.last_name_female()
            dob        = fake.date_of_birth(minimum_age=30, maximum_age=65)
            amka       = generate_amka(dob, amkas)
            license_no = generate_license(used_licenses)
            specialty  = random.choice(SPECIALTIES)
            doctor_amkas.append(amka)
            doctors_data.append([amka, first_name, last_name, license_no, specialty])

        write_inserts(f, 'doctors', doctors_data)


        #patients                                                            
        patients_data = []
        patient_amkas = []

        for _ in range(NUM_PATIENTS):
            sex = random.choices(SEX_CHOICES, weights=[49, 49, 2])[0]
            if sex == 'Άρρεν':
                first_name = fake.first_name_male()
                last_name  = fake.last_name_male()
            elif sex == 'Θήλυ':
                first_name = fake.first_name_female()
                last_name  = fake.last_name_female()
            else:
                first_name = fake.first_name()
                last_name  = fake.last_name()

            patronym    = fake.first_name_male()
            dob         = fake.date_of_birth(minimum_age=18, maximum_age=90)
            dob_str     = dob.strftime('%Y-%m-%d')
            amka        = generate_amka(dob, amkas)
            weight      = round(random.uniform(45.0, 120.0), 2)
            height      = round(random.uniform(1.45, 2.00), 2)
            email       = fake_en.free_email()
            occupation  = fake.job()
            if len(occupation) > 50:
                occupation = occupation[:47] + "..."
            nationality = random.choices(
                ['Ελληνική', 'Αλβανική', 'Γερμανική', 'Ιταλική', 'Γαλλική'],
                weights=[90, 5, 2, 2, 1]
            )[0]

            patient_amkas.append(amka)
            patients_data.append([
                amka, first_name, last_name, patronym, dob_str, sex,
                weight, height, email, occupation, nationality
            ])

        write_inserts(f, 'patients', patients_data)


        #patient_phones  (1–2 phones per patient)                            
        phones_data = []
        for pamka in patient_amkas:
            seen = set()
            for _ in range(random.randint(1, 2)):
                phone = random_phone()
                if phone not in seen:
                    seen.add(phone)
                    phones_data.append([pamka, phone])

        write_inserts(f, 'patient_phones', phones_data)


        #patient_contact  (0–1 emergency contact per patient)                
        contacts_data = []
        for pamka in patient_amkas:
            if random.random() < 0.75:
                c_sex        = random.choice(['male', 'female'])
                c_first_name = fake.first_name_male() if c_sex == 'male' else fake.first_name_female()
                c_last_name  = fake.last_name_male()  if c_sex == 'male' else fake.last_name_female()
                c_phone      = random_phone()
                contacts_data.append([pamka, c_first_name, c_last_name, c_phone])

        write_inserts(f, 'patient_contact', contacts_data)

    
        #addresses                                                            
        addresses_data = []
        greek_streets  = [
            'Λεωφόρος Αθηνών', 'Οδός Σόλωνος', 'Οδός Πανεπιστημίου', 'Λεωφόρος Βασιλίσσης Σοφίας',
            'Οδός Ερμού', 'Λεωφόρος Κηφισίας', 'Οδός Σταδίου', 'Οδός Πατησίων',
            'Λεωφόρος Αλεξάνδρας', 'Οδός Ακαδημίας', 'Οδός Μιχαλακοπούλου',
            'Λεωφόρος Μεσογείων', 'Οδός Μαραθώνος', 'Οδός Αγίου Δημητρίου',
            'Λεωφόρος Βουλιαγμένης', 'Οδός Πειραιώς', 'Οδός Ιπποκράτους',
            'Λεωφόρος Συγγρού', 'Οδός Καποδιστρίου', 'Οδός Κολοκοτρώνη',
        ]
        for addr_id in range(1, NUM_ADDRESSES + 1):
            street = random.choice(greek_streets)
            number = str(random.randint(1, 200))
            addresses_data.append([addr_id, street, number])

        write_inserts(f, 'addresses', addresses_data)

        
        #insurance_providers                                                  
        providers_data = []
        provider_ids   = list(range(1, NUM_PROVIDERS + 1))

        for pid in provider_ids:
            name  = PROVIDER_NAMES[pid - 1]
            phone = random_phone() if random.random() < 0.9 else None
            providers_data.append([pid, name, phone])

        write_inserts(f, 'insurance_providers', providers_data)


        #hospitals                                                            
        hospitals_data = []
        hospital_ids   = list(range(1, NUM_HOSPITALS + 1))

        for hid in hospital_ids:
            hospitals_data.append([hid, HOSPITAL_NAMES[hid - 1]])

        write_inserts(f, 'hospitals', hospitals_data)


        #hospital_contact  (1–3 contacts per hospital)                       
        hosp_contact_data = []
        for hid in hospital_ids:
            seen = set()
            for _ in range(random.randint(1, 3)):
                ci = random_phone()
                if ci not in seen:
                    seen.add(ci)
                    hosp_contact_data.append([hid, ci])

        write_inserts(f, 'hospital_contact', hosp_contact_data)


        #diagnosis  (ICD-10 codes)                                           
        diagnosis_data = []
        selected_icd   = random.sample(ICD10_POOL, min(NUM_DIAGNOSES, len(ICD10_POOL)))
        icd10_codes    = []

        for code, desc in selected_icd:
            icd10_codes.append(code)
            diagnosis_data.append([code, desc])

        write_inserts(f, 'diagnosis', diagnosis_data)

        
        #lab_tests                                                            
        lab_tests_data = []
        lab_test_ids   = list(range(1, NUM_LAB_TESTS + 1))
        selected_labs  = random.sample(LAB_TEST_POOL, min(NUM_LAB_TESTS, len(LAB_TEST_POOL)))

        for ltid, (lt_type, lt_desc) in enumerate(selected_labs, start=1):
            lab_tests_data.append([ltid, lt_type, lt_desc])

        write_inserts(f, 'lab_tests', lab_tests_data)

        
        #active_substances                                                    
        substances_data = []
        substance_ids   = list(range(1, NUM_SUBSTANCES + 1))


        # Build pool from medication substances and extra synthetic ones
        substance_names_pool = list({row[3] for row in MEDICATION_POOL})
        extra = [
            'aspirin', 'ceftriaxone', 'morphine', 'diazepam', 'lithium',
            'rifampicin', 'isoniazid', 'ethambutol', 'chloroquine', 'metronidazole',
            'vancomycin', 'ampicillin', 'acyclovir', 'oseltamivir', 'ribavirin',
            'dexamethasone', 'hydrocortisone', 'epinephrine', 'atropine', 'digoxin',
        ]
        substance_names_pool.extend(extra)
        substance_names_pool = list(set(substance_names_pool))
        random.shuffle(substance_names_pool)

        if len(substance_names_pool) < NUM_SUBSTANCES:
            while len(substance_names_pool) < NUM_SUBSTANCES:
                substance_names_pool.append(fake_en.word() + '_substance_' + str(len(substance_names_pool)))

        substance_names = substance_names_pool[:NUM_SUBSTANCES]
        substance_name_to_id = {}

        for sid, sname in enumerate(substance_names, start=1):
            substances_data.append([sid, sname])
            substance_name_to_id[sname] = sid

        write_inserts(f, 'active_substances', substances_data)

    
        #medications                                                          
        medications_data    = []
        med_ids             = list(range(1, NUM_MEDICATIONS + 1))
        med_substance_map   = {}   
        selected_meds       = random.sample(MEDICATION_POOL, min(NUM_MEDICATIONS, len(MEDICATION_POOL)))

        for mid, (prod_name, adm_route, country, sub_name) in enumerate(selected_meds, start=1):
            ma_number  = 'MA-' + ''.join(random.choices('0123456789', k=8))
            pv_city    = random.choice(['Αθήνα', 'Θεσσαλονίκη', 'Πάτρα', 'Λονδίνο', 'Παρίσι'])
            pv_email   = fake_en.company_email()
            pv_phone   = random_phone() if random.random() < 0.8 else None
            medications_data.append([
                mid, prod_name, adm_route, country, ma_number, pv_city, pv_email, pv_phone
            ])
        
            subs = [substance_name_to_id[sub_name]] if sub_name in substance_name_to_id else [random.choice(substance_ids)]
            if random.random() < 0.3:
                extra_sid = random.choice(substance_ids)
                if extra_sid not in subs:
                    subs.append(extra_sid)
            med_substance_map[mid] = subs

        write_inserts(f, 'medications', medications_data)


        #med_contains                                                         
        med_contains_data = []
        for mid, subs in med_substance_map.items():
            for sid in subs:
                med_contains_data.append([mid, sid])

        write_inserts(f, 'med_contains', med_contains_data)

        
        #has_allergy  (0–2 allergies per patient)              
        #Track which substances each patient is allergic to
        patient_allergies = {pamka: set() for pamka in patient_amkas}
        has_allergy_data  = []
        seen_allergy      = set()

        for pamka in patient_amkas:
            if random.random() < 0.30:
                for _ in range(random.randint(1, 2)):
                    sid = random.choice(substance_ids)
                    key = (pamka, sid)
                    if key not in seen_allergy:
                        seen_allergy.add(key)
                        patient_allergies[pamka].add(sid)
                        has_allergy_data.append([pamka, sid])

        write_inserts(f, 'has_allergy', has_allergy_data)

       
        #doc_visits                                                           
        visits_data = []
        visit_ids   = list(range(1, NUM_VISITS + 1))
        visit_map   = {}

        for vid in visit_ids:
            pamka    = random.choice(patient_amkas)
            damka    = random.choice(doctor_amkas)
            vdt      = random_datetime()
            vdt_str  = vdt.strftime('%Y-%m-%d %H:%M:%S')
            visit_map[vid] = (pamka, damka)
            visits_data.append([vid, vdt_str, pamka, damka])

        write_inserts(f, 'doc_visits', visits_data)


        #prescriptions      
        prescriptions_data = []

        for prid in range(1, NUM_PRESCRIPTIONS + 1):
            # Pick a random visit for consistency
            vid              = random.choice(visit_ids)
            pamka, damka     = visit_map[vid]
            allergic_subs    = patient_allergies[pamka]

            #Finds a medication that does not contain any substance the patient is allergic to
            attempts = 0
            mid = None
            for _ in range(50):
                candidate = random.choice(med_ids)
                med_subs  = set(med_substance_map.get(candidate, []))
                if not med_subs.intersection(allergic_subs):
                    mid = candidate
                    break
                attempts += 1

            if mid is None:
                #Skip this prescription if no safe medication found
                continue

            start_dt   = random_datetime(2020, 2024)
            start_date = start_dt.strftime('%Y-%m-%d')
            end_date   = None
            if random.random() < 0.7:
                end_dt   = start_dt + timedelta(days=random.randint(7, 180))
                end_date = end_dt.strftime('%Y-%m-%d')

            dosage    = random.choice(DOSAGES)
            frequency = random.choice(FREQUENCIES)
    
            linked_vid = vid if random.random() < 0.6 else None

            prescriptions_data.append([
                prid, start_date, end_date, dosage, frequency,
                pamka, damka, mid, linked_vid
            ])

        write_inserts(f, 'prescriptions', prescriptions_data)

        
        #referrals  (visit-consistent)                                        
        referrals_data = []
        referral_ids   = []

        for rid in range(1, NUM_REFERRALS + 1):
            vid          = random.choice(visit_ids)
            pamka, damka = visit_map[vid]
            ltid         = random.choice(lab_test_ids)

            issue_dt   = random_datetime(2020, 2024)
            issue_date = issue_dt.strftime('%Y-%m-%d')
            exp_date   = None
            if random.random() < 0.8:
                exp_dt   = issue_dt + timedelta(days=random.randint(30, 180))
                exp_date = exp_dt.strftime('%Y-%m-%d')

            linked_vid = vid if random.random() < 0.6 else None
            referral_ids.append(rid)
            referrals_data.append([rid, issue_date, exp_date, pamka, damka, ltid, linked_vid])

        write_inserts(f, 'referrals', referrals_data)
 

        #ex_lab_tests                                                            
        ex_lab_tests_data = []

        for eid in range(1, NUM_EX_LAB_TESTS + 1):
            pamka  = random.choice(patient_amkas)
            ltid   = random.choice(lab_test_ids)
            dt     = random_datetime(2020, 2024)
            dt_str = dt.strftime('%Y-%m-%d %H:%M:%S')
            results = random.choice([
                'Φυσιολογικά', 'Παθολογικά', 'Υψηλές τιμές', 'Χαμηλές τιμές',
                'Εντός φυσιολογικών ορίων', 'Ανεπαρκή δείγματα', None
            ])
            cost   = round(random.uniform(20.0, 350.0), 2) if random.random() < 0.85 else None
            ref_id = random.choice(referral_ids) if random.random() < 0.5 else None
            ex_lab_tests_data.append([eid, dt_str, results, cost, pamka, ltid, ref_id])

        write_inserts(f, 'ex_lab_tests', ex_lab_tests_data)


        #diagnosis_history                                                    
        diag_history_data = []

        for did in range(1, NUM_PATIENTS * 2 + 1):
            pamka = random.choice(patient_amkas)
            code  = random.choice(icd10_codes)
            ddate = random_datetime(2010, 2024).strftime('%Y-%m-%d')
            diag_history_data.append([did, code, ddate, pamka])

        write_inserts(f, 'diagnosis_history', diag_history_data)


        #hospitalizations                                                     
        hospitalizations_data = []

        for hzid in range(1, NUM_HOSPITALIZATIONS + 1):
            pamka       = random.choice(patient_amkas)
            hid         = random.choice(hospital_ids)
            adm_dt      = random_datetime(2015, 2024)
            adm_date    = adm_dt.strftime('%Y-%m-%d')
            disc_date   = None
            if random.random() < 0.85:
                disc_dt   = adm_dt + timedelta(days=random.randint(1, 30))
                disc_date = disc_dt.strftime('%Y-%m-%d')
            hospitalizations_data.append([hzid, adm_date, disc_date, pamka, hid])

        write_inserts(f, 'hospitalizations', hospitalizations_data)

        #has_address  (1–2 addresses per patient)                            
        has_address_data = []
        addr_ids         = list(range(1, NUM_ADDRESSES + 1))
        seen_has_addr    = set()

        for pamka in patient_amkas:
            assigned = random.sample(addr_ids, k=random.randint(1, 2))
            for aid in assigned:
                key = (pamka, aid)
                if key not in seen_has_addr:
                    seen_has_addr.add(key)
                    has_address_data.append([pamka, aid])

        write_inserts(f, 'has_address', has_address_data)


        #has_provider  (1–2 insurance providers per patient)                 
        has_provider_data = []
        seen_has_prov     = set()

        for pamka in patient_amkas:
            assigned = random.sample(provider_ids, k=random.randint(1, 2))
            for pid in assigned:
                key = (pamka, pid)
                if key not in seen_has_prov:
                    seen_has_prov.add(key)
                    has_provider_data.append([pamka, pid])

        write_inserts(f, 'has_provider', has_provider_data)

        f.write("SET FOREIGN_KEY_CHECKS = 1;\n")

    total_rows = (
        len(doctors_data) + len(patients_data) + len(phones_data) + len(contacts_data) +
        len(addresses_data) + len(providers_data) + len(hospitals_data) + len(hosp_contact_data) +
        len(diagnosis_data) + len(lab_tests_data) + len(substances_data) + len(medications_data) +
        len(med_contains_data) + len(has_allergy_data) + len(visits_data) + len(prescriptions_data) +
        len(referrals_data) + len(ex_lab_tests_data) + len(diag_history_data) +
        len(hospitalizations_data) + len(has_address_data) + len(has_provider_data)
    )
    print(f"Επιτυχής δημιουργία {total_rows} εγγραφών σε {output_file}")
    print(f"Πίνακες που φορτώθηκαν: 22")