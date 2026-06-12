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
    age INT GENERATED ALWAYS AS (TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE())) STORED,
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