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