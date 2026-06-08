import { useState } from 'react';
import type { PatientHealthFile } from '../types';

interface PatientListProps {
  healthFiles: PatientHealthFile[];
  onViewProfile: (amka: string) => void;
  onViewHealthFile: (amka: string) => void;
  onAddPatient: () => void;
}

export default function PatientList({ healthFiles, onViewProfile, onViewHealthFile, onAddPatient }: PatientListProps) {
  const [searchTerm, setSearchTerm] = useState('');

  const filtered = healthFiles.filter(({ patient: p }) =>
    p.last_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    p.first_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    p.AMKA.includes(searchTerm)
  );



  return (
    <div>
      <div className="page-header">
        <div className="page-header-row">
          <div>
            <h1>Ασθενείς</h1>
          </div>
          <button id="add-patient-btn" className="btn btn-primary" onClick={onAddPatient}>
            + Νέος Ασθενής
          </button>
        </div>
      </div>
      <div className="card card-table">
        <div className="card-header-search">
          <div className="search-wrapper">
            <span className="search-icon">⌕</span>
            <input
              id="patient-search-input"
              type="text"
              className="search-input"
              placeholder="Αναζήτηση με ΑΜΚΑ, Όνομα ή Επώνυμο…"
              value={searchTerm}
              onChange={e => setSearchTerm(e.target.value)}
            />
          </div>
        </div>
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Ασθενής</th>
                <th>ΑΜΚΑ</th>
                <th>Ηλικία / Φύλο</th>
                <th>Επικοινωνία</th>
                <th>Ασφαλιστής</th>
                <th>Αλλεργίες</th>
                <th className="text-right">Ενέργειες</th>
              </tr>
            </thead>
            <tbody>
              {filtered.length === 0 ? (
                <tr>
                  <td colSpan={7}>
                     <div className="empty-state">
                      <div className="empty-state-text">Δεν βρέθηκαν ασθενείς</div>
                    </div>
                  </td>
                </tr>
              ) : (
                filtered.map(({ patient: p }) => (
                  <tr key={p.AMKA}>
                    <td>
                      <div>
                        <strong>{p.last_name} {p.first_name}</strong>
                        <div className="text-muted text-small">{p.occupation ?? '—'}</div>
                      </div>
                    </td>
                    <td>
                      {p.AMKA}
                    </td>
                    <td>
                      <div>{p.age != null ? `${p.age} ετών` : '—'}</div>
                      <div className="text-muted text-small">{p.sex}</div>
                    </td>
                    <td>
                      <div>{p.phone_number ?? '—'}</div>
                      <div className="text-muted text-small">{p.email ?? '—'}</div>
                    </td>
                    <td>
                      <span className="badge badge-neutral">
                        {p.insurance_provider?.name ?? '—'}
                      </span>
                    </td>
                    <td>
                      {p.allergies && p.allergies.length > 0 ? (
                        <div className="tags-row">
                          {p.allergies.map(a => (
                            <span key={a} className="badge badge-danger">{a}</span>
                          ))}
                        </div>
                      ) : (
                        <span className="badge badge-success">Καμία</span>
                      )}
                    </td>
                    <td>
                      <div className="action-group-right">
                        <button
                          id={`profile-btn-${p.AMKA}`}
                          className="btn btn-ghost btn-sm"
                          onClick={() => onViewProfile(p.AMKA)}
                        >
                          Προφίλ
                        </button>
                        <button
                          id={`healthfile-btn-${p.AMKA}`}
                          className="btn btn-secondary btn-sm"
                          onClick={() => onViewHealthFile(p.AMKA)}
                        >
                          Φάκελος
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
        <div className="card-footer">
          Εμφάνιση {filtered.length} από {healthFiles.length} ασθενείς
        </div>
      </div>
    </div>
  );
}