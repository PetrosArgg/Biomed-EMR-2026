SET NAMES utf8mb4;
DROP DATABASE IF EXISTS biomed_db;
CREATE DATABASE IF NOT EXISTS biomed_db;
USE biomed_db;

CREATE TABLE doctors(
    AMKA CHAR(11) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    doc_license_number VARCHAR(20) NOT NULL,
    specialty VARCHAR(50) NOT NULL,
    PRIMARY KEY(AMKA),
    UNIQUE(doc_license_number)
)ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE patients(
    AMKA CHAR(11) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    patronym VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    sex VARCHAR(10) NOT NULL CHECK(sex IN ('Άρρεν', 'Θήλυ', 'Άλλο')),
    weight DECIMAL(5,2),
    height DECIMAL(3,2),
    email VARCHAR(50),
    occupation VARCHAR(50),
    nationality VARCHAR(50) NOT NULL,
    PRIMARY KEY(AMKA)
)ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE patient_phones(
    AMKA CHAR(11) NOT NULL,
    phone_number VARCHAR(13) NOT NULL,
    PRIMARY KEY(AMKA, phone_number),
    CONSTRAINT fk_patients_patient_phones FOREIGN KEY(AMKA) REFERENCES patients(AMKA)
    ON DELETE CASCADE ON UPDATE CASCADE
)ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE patient_contact(
    AMKA CHAR(11) NOT NULL,
    contact_first_name VARCHAR(50) NOT NULL,
    contact_last_name VARCHAR(50) NOT NULL,
    contact_phone_number VARCHAR(13) NOT NULL,
    PRIMARY KEY(AMKA, contact_first_name, contact_last_name, contact_phone_number),
    CONSTRAINT fk_patients_patient_contacts FOREIGN KEY(AMKA) REFERENCES patients(AMKA)
    ON DELETE CASCADE ON UPDATE CASCADE
)ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE addresses(
    address_id INT NOT NULL AUTO_INCREMENT,
    street VARCHAR(100) NOT NULL,
    number VARCHAR(10) NOT NULL,
    PRIMARY KEY(address_id)
)ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE insurance_providers(
    provider_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(13),
    PRIMARY KEY(provider_id)
)ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE hospitals(
    hospital_id INT NOT NULL AUTO_INCREMENT,
    hospital_name VARCHAR(100) NOT NULL,
    PRIMARY KEY(hospital_id)
)ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE hospital_contact(
    hospital_id INT NOT NULL,
    contact_info VARCHAR(100) NOT NULL,
    PRIMARY KEY(hospital_id, contact_info),
    CONSTRAINT fk_hospital_contact_hospitals FOREIGN KEY(hospital_id) REFERENCES hospitals(hospital_id)
    ON DELETE CASCADE ON UPDATE CASCADE
)ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE diagnosis(
    ICD10_code VARCHAR(10) NOT NULL,
    description VARCHAR(255) NOT NULL,
    PRIMARY KEY(ICD10_code)
)ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE lab_tests(
    lab_test_id INT NOT NULL AUTO_INCREMENT,
    lab_test_type VARCHAR(100) NOT NULL,
    lab_test_description VARCHAR(255),
    PRIMARY KEY(lab_test_id)
)ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE medications(
    med_id INT NOT NULL AUTO_INCREMENT,
    product_name VARCHAR(100) NOT NULL,
    administration_route VARCHAR(50) NOT NULL,
    authorisation_country VARCHAR(50),
    marketing_authorization VARCHAR(100),
    pharmacovigilance_system_location VARCHAR(100),
    pharmacovigilance_email VARCHAR(50),
    pharmacovigilance_phone_number VARCHAR(13),
    PRIMARY KEY(med_id)
)ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE active_substances(
    substance_id INT NOT NULL AUTO_INCREMENT,
    substance_name VARCHAR(100) NOT NULL,
    PRIMARY KEY(substance_id),
    UNIQUE(substance_name)
)ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE med_contains(
    med_id INT NOT NULL,
    substance_id INT NOT NULL,
    PRIMARY KEY(med_id, substance_id),
    CONSTRAINT fk_med_contains_medications FOREIGN KEY(med_id) REFERENCES medications(med_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_med_contains_active_substances FOREIGN KEY(substance_id) REFERENCES active_substances(substance_id)
    ON DELETE CASCADE ON UPDATE CASCADE
)ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE has_allergy(
    AMKA CHAR(11) NOT NULL,
    substance_id INT NOT NULL,
    PRIMARY KEY(AMKA, substance_id),
    CONSTRAINT fk_has_allergy_patients FOREIGN KEY(AMKA) REFERENCES patients(AMKA)
    ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_has_allergy_active_substances FOREIGN KEY(substance_id) REFERENCES active_substances(substance_id)
    ON DELETE CASCADE ON UPDATE CASCADE
)ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE doc_visits(
    visit_id INT NOT NULL AUTO_INCREMENT,
    visit_datetime DATETIME NOT NULL,
    patient_AMKA CHAR(11) NOT NULL,
    doctor_AMKA CHAR(11) NOT NULL,
    PRIMARY KEY(visit_id),
    CONSTRAINT fk_doc_visits_patients FOREIGN KEY(patient_AMKA) REFERENCES patients(AMKA)
    ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_doc_visits_doctors FOREIGN KEY(doctor_AMKA) REFERENCES doctors(AMKA)
    ON DELETE RESTRICT ON UPDATE CASCADE
)ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE prescriptions(
    prescription_id INT NOT NULL AUTO_INCREMENT,
    start_date DATE NOT NULL,
    end_date DATE,
    dosage VARCHAR(50) NOT NULL,
    frequency VARCHAR(50) NOT NULL,
    patient_AMKA CHAR(11) NOT NULL,
    doctor_AMKA CHAR(11) NOT NULL,
    med_id INT NOT NULL,
    visit_id INT,
    PRIMARY KEY(prescription_id),
    CONSTRAINT fk_prescriptions_patients FOREIGN KEY(patient_AMKA) REFERENCES patients(AMKA)
    ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_prescriptions_doctors FOREIGN KEY(doctor_AMKA) REFERENCES doctors(AMKA)
    ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_prescriptions_medications FOREIGN KEY(med_id) REFERENCES medications(med_id)
    ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_prescriptions_doc_visits FOREIGN KEY(visit_id) REFERENCES doc_visits(visit_id)
    ON DELETE SET NULL ON UPDATE CASCADE,
    CHECK(end_date IS NULL OR end_date >= start_date)
)ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE referrals(
    referral_id INT NOT NULL AUTO_INCREMENT,
    issue_date DATE NOT NULL,
    expiration_date DATE,
    patient_AMKA CHAR(11) NOT NULL,
    doctor_AMKA CHAR(11) NOT NULL,
    lab_test_id INT NOT NULL,
    visit_id INT,
    PRIMARY KEY(referral_id),
    CONSTRAINT fk_referrals_patients FOREIGN KEY(patient_AMKA) REFERENCES patients(AMKA)
    ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_referrals_doctors FOREIGN KEY(doctor_AMKA) REFERENCES doctors(AMKA)
    ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_referrals_lab_tests FOREIGN KEY(lab_test_id) REFERENCES lab_tests(lab_test_id)
    ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_referrals_doc_visits FOREIGN KEY(visit_id) REFERENCES doc_visits(visit_id)
    ON DELETE SET NULL ON UPDATE CASCADE,
    CHECK(expiration_date IS NULL OR expiration_date >= issue_date)
)ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE ex_lab_tests(
    ex_lab_test_id INT NOT NULL AUTO_INCREMENT,
    datetime DATETIME NOT NULL,
    results TEXT,
    cost DECIMAL(8,2),
    patient_AMKA CHAR(11) NOT NULL,
    lab_test_id INT NOT NULL,
    referral_id INT,
    PRIMARY KEY(ex_lab_test_id),
    CONSTRAINT fk_ex_lab_tests_patients FOREIGN KEY(patient_AMKA) REFERENCES patients(AMKA)
    ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_ex_lab_tests_lab_tests FOREIGN KEY(lab_test_id) REFERENCES lab_tests(lab_test_id)
    ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_ex_lab_tests_referrals FOREIGN KEY(referral_id) REFERENCES referrals(referral_id)
    ON DELETE SET NULL ON UPDATE CASCADE,
    CHECK(cost IS NULL OR cost >= 0)
)ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE diagnosis_history(
    diagnosis_id INT NOT NULL AUTO_INCREMENT,
    ICD10_code VARCHAR(10) NOT NULL,
    diagnosis_date DATE NOT NULL,
    patient_AMKA CHAR(11) NOT NULL,
    PRIMARY KEY(diagnosis_id),
    CONSTRAINT fk_diagnosis_history_diagnosis FOREIGN KEY(ICD10_code) REFERENCES diagnosis(ICD10_code)
    ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_diagnosis_history_patients FOREIGN KEY(patient_AMKA) REFERENCES patients(AMKA)
    ON DELETE CASCADE ON UPDATE CASCADE
)ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE hospitalizations(
    hospitalization_id INT NOT NULL AUTO_INCREMENT,
    date_of_admission DATE NOT NULL,
    date_of_discharge DATE,
    patient_AMKA CHAR(11) NOT NULL,
    hospital_id INT NOT NULL,
    PRIMARY KEY(hospitalization_id),
    CONSTRAINT fk_hospitalizations_patients FOREIGN KEY(patient_AMKA) REFERENCES patients(AMKA)
    ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_hospitalizations_hospitals FOREIGN KEY(hospital_id) REFERENCES hospitals(hospital_id)
    ON DELETE RESTRICT ON UPDATE CASCADE,
    CHECK(date_of_discharge IS NULL OR date_of_discharge >= date_of_admission)
)ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE has_address(
    AMKA CHAR(11) NOT NULL,
    address_id INT NOT NULL,
    PRIMARY KEY(AMKA, address_id),
    CONSTRAINT fk_has_address_patients FOREIGN KEY(AMKA) REFERENCES patients(AMKA)
    ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_has_address_addresses FOREIGN KEY(address_id) REFERENCES addresses(address_id)
    ON DELETE RESTRICT ON UPDATE CASCADE
)ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE has_provider(
    AMKA CHAR(11) NOT NULL,
    provider_id INT NOT NULL,
    PRIMARY KEY(AMKA, provider_id),
    CONSTRAINT fk_has_provider_patients FOREIGN KEY(AMKA) REFERENCES patients(AMKA)
    ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_has_provider_insurance_providers FOREIGN KEY(provider_id) REFERENCES insurance_providers(provider_id)
    ON DELETE RESTRICT ON UPDATE CASCADE
)ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE INDEX idx_patients_last_name ON patients(last_name);
CREATE INDEX idx_doctors_last_name ON doctors(last_name);
CREATE INDEX idx_doc_visits_patient ON doc_visits(patient_AMKA);
CREATE INDEX idx_doc_visits_doctor ON doc_visits(doctor_AMKA);
CREATE INDEX idx_doc_visits_datetime ON doc_visits(visit_datetime);
CREATE INDEX idx_prescriptions_patient ON prescriptions(patient_AMKA);
CREATE INDEX idx_prescriptions_doctor ON prescriptions(doctor_AMKA);
CREATE INDEX idx_prescriptions_medication ON prescriptions(med_id);
CREATE INDEX idx_referrals_patient ON referrals(patient_AMKA);
CREATE INDEX idx_referrals_doctor ON referrals(doctor_AMKA);
CREATE INDEX idx_ex_lab_tests_patient ON ex_lab_tests(patient_AMKA);
CREATE INDEX idx_diagnosis_history_patient ON diagnosis_history(patient_AMKA);
CREATE INDEX idx_hospitalizations_patient ON hospitalizations(patient_AMKA);

CREATE VIEW patient_age_view AS
SELECT
    AMKA,
    first_name,
    last_name,
    date_of_birth,
    TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) AS age
FROM patients;

CREATE VIEW patient_medical_summary AS
SELECT
    p.AMKA,
    p.first_name,
    p.last_name,
    p.date_of_birth,
    TIMESTAMPDIFF(YEAR, p.date_of_birth, CURDATE()) AS age,
    p.sex,
    p.email,
    p.nationality,
    COUNT(DISTINCT dv.visit_id) AS total_visits,
    COUNT(DISTINCT pr.prescription_id) AS total_prescriptions,
    COUNT(DISTINCT rf.referral_id) AS total_referrals,
    COUNT(DISTINCT elt.ex_lab_test_id) AS total_lab_tests,
    COUNT(DISTINCT dh.diagnosis_id) AS total_diagnoses,
    COUNT(DISTINCT hp.hospitalization_id) AS total_hospitalizations
FROM patients p
LEFT JOIN doc_visits dv ON p.AMKA = dv.patient_AMKA
LEFT JOIN prescriptions pr ON p.AMKA = pr.patient_AMKA
LEFT JOIN referrals rf ON p.AMKA = rf.patient_AMKA
LEFT JOIN ex_lab_tests elt ON p.AMKA = elt.patient_AMKA
LEFT JOIN diagnosis_history dh ON p.AMKA = dh.patient_AMKA
LEFT JOIN hospitalizations hp ON p.AMKA = hp.patient_AMKA
GROUP BY
    p.AMKA,
    p.first_name,
    p.last_name,
    p.date_of_birth,
    p.sex,
    p.email,
    p.nationality;

DELIMITER //

CREATE TRIGGER prevent_allergic_reactions_insert
BEFORE INSERT ON prescriptions
FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT 1
        FROM med_contains mc
        JOIN has_allergy ha ON mc.substance_id = ha.substance_id
        WHERE mc.med_id = NEW.med_id
          AND ha.AMKA = NEW.patient_AMKA
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Prescription rejected: patient is allergic to one or more active substances of this medication.';
    END IF;
END//

CREATE TRIGGER prevent_allergic_reactions_update
BEFORE UPDATE ON prescriptions
FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT 1
        FROM med_contains mc
        JOIN has_allergy ha ON mc.substance_id = ha.substance_id
        WHERE mc.med_id = NEW.med_id
          AND ha.AMKA = NEW.patient_AMKA
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Prescription update rejected: patient is allergic to one or more active substances of this medication.';
    END IF;
END//

DELIMITER ;

DELIMITER //

CREATE TRIGGER prescriptions_visit_consistency_insert
BEFORE INSERT ON prescriptions
FOR EACH ROW
BEGIN
    IF NEW.visit_id IS NOT NULL AND NOT EXISTS (
        SELECT 1
        FROM doc_visits dv
        WHERE dv.visit_id = NEW.visit_id
          AND dv.patient_AMKA = NEW.patient_AMKA
          AND dv.doctor_AMKA = NEW.doctor_AMKA
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Prescription rejected: patient and doctor must match the selected visit.';
    END IF;
END//

CREATE TRIGGER prescriptions_visit_consistency_update
BEFORE UPDATE ON prescriptions
FOR EACH ROW
BEGIN
    IF NEW.visit_id IS NOT NULL AND NOT EXISTS (
        SELECT 1
        FROM doc_visits dv
        WHERE dv.visit_id = NEW.visit_id
          AND dv.patient_AMKA = NEW.patient_AMKA
          AND dv.doctor_AMKA = NEW.doctor_AMKA
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Prescription update rejected: patient and doctor must match the selected visit.';
    END IF;
END//

DELIMITER ;

DELIMITER //

CREATE TRIGGER referrals_visit_consistency_insert
BEFORE INSERT ON referrals
FOR EACH ROW
BEGIN
    IF NEW.visit_id IS NOT NULL AND NOT EXISTS (
        SELECT 1
        FROM doc_visits dv
        WHERE dv.visit_id = NEW.visit_id
          AND dv.patient_AMKA = NEW.patient_AMKA
          AND dv.doctor_AMKA = NEW.doctor_AMKA
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Referral rejected: patient and doctor must match the selected visit.';
    END IF;
END//

CREATE TRIGGER referrals_visit_consistency_update
BEFORE UPDATE ON referrals
FOR EACH ROW
BEGIN
    IF NEW.visit_id IS NOT NULL AND NOT EXISTS (
        SELECT 1
        FROM doc_visits dv
        WHERE dv.visit_id = NEW.visit_id
          AND dv.patient_AMKA = NEW.patient_AMKA
          AND dv.doctor_AMKA = NEW.doctor_AMKA
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Referral update rejected: patient and doctor must match the selected visit.';
    END IF;
END//

DELIMITER ;