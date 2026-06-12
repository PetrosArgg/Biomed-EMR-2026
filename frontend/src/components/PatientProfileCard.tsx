import type { Patient } from '../types';

interface PatientProfileCardProps {
  patient: Patient;
  onBack: () => void;
}

export default function PatientProfileCard({ patient, onBack }: PatientProfileCardProps) {
  return (
    <div>
      <div className="page-header">
        <h1>Προφίλ Ασθενούς</h1>
      </div>

      <div className="card">
        <div style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <div>
            <h2 style={{ fontSize: '1.1rem', marginBottom: '4px' }}>
              {patient.last_name} {patient.first_name} {patient.patronym}
            </h2>
            <p className="text-muted text-small">ΑΜΚΑ: {patient.AMKA}</p>
          </div>

          <div className="form-grid" style={{ gap: '16px' }}>
            <div>
              <strong style={{ display: 'block', fontSize: '0.8rem', color: '#666' }}>Ημερομηνία Γέννησης</strong>
              <span>{patient.date_of_birth}</span>
            </div>
            <div>
              <strong style={{ display: 'block', fontSize: '0.8rem', color: '#666' }}>Φύλο</strong>
              <span>{patient.sex}</span>
            </div>
            <div>
              <strong style={{ display: 'block', fontSize: '0.8rem', color: '#666' }}>Επάγγελμα</strong>
              <span>{patient.occupation ?? '—'}</span>
            </div>
            <div>
              <strong style={{ display: 'block', fontSize: '0.8rem', color: '#666' }}>Εθνικότητα</strong>
              <span>{patient.nationality ?? '—'}</span>
            </div>
            <div>
              <strong style={{ display: 'block', fontSize: '0.8rem', color: '#666' }}>Τηλέφωνο</strong>
              <span>{patient.phone_number ?? '—'}</span>
            </div>
            <div>
              <strong style={{ display: 'block', fontSize: '0.8rem', color: '#666' }}>Email</strong>
              <span>{patient.email ?? '—'}</span>
            </div>
            <div>
              <strong style={{ display: 'block', fontSize: '0.8rem', color: '#666' }}>Ύψος / Βάρος</strong>
              <span>
                {patient.height != null ? `${patient.height} cm` : '—'} /{' '}
                {patient.weight != null ? `${patient.weight} kg` : '—'}
              </span>
            </div>
            <div>
              <strong style={{ display: 'block', fontSize: '0.8rem', color: '#666' }}>Ασφαλιστής</strong>
              <span>{patient.insurance_provider?.name ?? '—'}</span>
            </div>
          </div>

          {patient.address && (
            <div style={{ borderTop: '1px solid #eee', paddingTop: '16px' }}>
              <h3 style={{ fontSize: '0.9rem', marginBottom: '8px' }}>Διεύθυνση Κατοικίας</h3>
              <div>{patient.address.street} {patient.address.number}</div>
            </div>
          )}

          <div className="action-group-right" style={{ borderTop: '1px solid #eee', paddingTop: '16px' }}>
            <button className="btn" onClick={onBack}>
              Επιστροφή
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
