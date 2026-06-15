export interface Address {
  address_id: number;
  street: string;
  number: string;
}

export interface InsuranceProvider {
  provider_id: number;
  name: string;
  phone_number: string;
}

export interface Patient {
  AMKA: string;
  first_name: string;
  last_name: string;
  patronym: string;
  date_of_birth: string;
  age?: number;
  sex: 'Άνδρας' | 'Γυναίκα' | 'Άλλο';
  weight?: number;
  height?: number;
  email?: string;
  phone_number?: string;
  contact_info?: string;
  occupation?: string;
  nationality?: string;
  allergies?: string[];
  address?: Address;
  insurance_provider?: InsuranceProvider;
}

export interface PatientHealthFile {
  patient: Patient;
}

export interface DiagnosisHistoryEntry {
  diagnosis_id: number;
  ICD10_code: string;
  description: string;
  diagnosis_date: string;
}

export interface DocVisitEntry {
  visit_id: number;
  visit_datetime: string;
  doctor_name: string;
  doctor_specialty: string;
}

export interface PrescriptionEntry {
  prescription_id: number;
  start_date: string;
  end_date: string | null;
  dosage: string;
  frequency: string;
  medication_name: string;
  active_substances: string[];
  doctor_name: string;
}

export interface ReferralEntry {
  referral_id: number;
  issue_date: string;
  expiration_date: string | null;
  lab_test_type: string;
  lab_test_description: string | null;
  doctor_name: string;
}

export interface ExLabTestEntry {
  ex_lab_test_id: number;
  datetime: string;
  results: string | null;
  cost: number | null;
  lab_test_type: string;
}

export interface HospitalizationEntry {
  hospitalization_id: number;
  date_of_admission: string;
  date_of_discharge: string | null;
  hospital_name: string;
}

export interface FullHealthFileResponse {
  patient: Patient;
  diagnoses: DiagnosisHistoryEntry[];
  visits: DocVisitEntry[];
  prescriptions: PrescriptionEntry[];
  referrals: ReferralEntry[];
  lab_tests: ExLabTestEntry[];
  hospitalizations: HospitalizationEntry[];
}

export interface Doctor {
  AMKA: string;
  first_name: string;
  last_name: string;
  specialty: string;
}

export interface Medication {
  med_id: number;
  product_name: string;
  administration_route: string;
}

export interface Diagnosis {
  ICD10_code: string;
  description: string;
}