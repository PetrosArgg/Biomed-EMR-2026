import { useState } from 'react';
import type { Patient } from '../types';

interface AddPatientProps {
  onSubmit: (patient: Patient) => void;
  onCancel: () => void;
}

export default function AddPatient({ onSubmit, onCancel }: AddPatientProps) {
  const [formData, setFormData] = useState({
    AMKA: '',
    first_name: '',
    last_name: '',
    patronym: '',
    date_of_birth: '',
    sex: 'Άνδρας' as 'Άνδρας' | 'Γυναίκα' | 'Άλλο',
    weight: '',
    height: '',
    email: '',
    phone_number: '',
    occupation: '',
    nationality: 'Ελληνική',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const patientData: Patient = {
      AMKA: formData.AMKA,
      first_name: formData.first_name,
      last_name: formData.last_name,
      patronym: formData.patronym,
      date_of_birth: formData.date_of_birth,
      sex: formData.sex,
      nationality: formData.nationality || undefined,
      occupation: formData.occupation || undefined,
      email: formData.email || undefined,
      phone_number: formData.phone_number || undefined,
      weight: formData.weight ? parseFloat(formData.weight) : undefined,
      height: formData.height ? parseFloat(formData.height) : undefined,
      allergies: [],
    };

    onSubmit(patientData);
  };

  return (
    <div>
      <div className="page-header">
        <h1>Νέος Ασθενής</h1>
      </div>
      <div className="card">
        <form onSubmit={handleSubmit} className="patient-form">
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="AMKA">ΑΜΚΑ</label>
              <input
                type="text"
                id="AMKA"
                name="AMKA"
                required
                maxLength={11}
                pattern="\d{11}"
                placeholder="π.χ. 01015012345"
                value={formData.AMKA}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="last_name">Επώνυμο</label>
              <input
                type="text"
                id="last_name"
                name="last_name"
                required
                value={formData.last_name}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="first_name">Όνομα</label>
              <input
                type="text"
                id="first_name"
                name="first_name"
                required
                value={formData.first_name}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="patronym">Πατρώνυμο</label>
              <input
                type="text"
                id="patronym"
                name="patronym"
                required
                value={formData.patronym}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="date_of_birth">Ημερομηνία Γέννησης</label>
              <input
                type="date"
                id="date_of_birth"
                name="date_of_birth"
                required
                value={formData.date_of_birth}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="sex">Φύλο</label>
              <select
                id="sex"
                name="sex"
                value={formData.sex}
                onChange={handleChange}
              >
                <option value="Άνδρας">Άνδρας</option>
                <option value="Γυναίκα">Γυναίκα</option>
                <option value="Άλλο">Άλλο</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="phone_number">Τηλέφωνο</label>
              <input
                type="text"
                id="phone_number"
                name="phone_number"
                value={formData.phone_number}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="occupation">Επάγγελμα</label>
              <input
                type="text"
                id="occupation"
                name="occupation"
                value={formData.occupation}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="nationality">Εθνικότητα</label>
              <input
                type="text"
                id="nationality"
                name="nationality"
                value={formData.nationality}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="weight">Βάρος (kg)</label>
              <input
                type="number"
                id="weight"
                name="weight"
                step="0.1"
                value={formData.weight}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="height">Ύψος (cm)</label>
              <input
                type="number"
                id="height"
                name="height"
                value={formData.height}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className="action-group-right" style={{ borderTop: '1px solid #d8e0e9', paddingTop: '20px', marginTop: '12px' }}>
            <button type="button" className="btn btn-ghost" onClick={onCancel}>
              Ακύρωση
            </button>
            <button type="submit" className="btn btn-primary">
              Αποθήκευση
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
