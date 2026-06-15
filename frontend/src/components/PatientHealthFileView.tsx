import { useState, useEffect } from 'react';
import type { FullHealthFileResponse, Doctor, Medication, Diagnosis } from '../types';

interface PatientHealthFileViewProps {
  amka: string;
  onBack: () => void;
  apiBaseUrl: string;
}

type TabType = 'diagnoses' | 'visits' | 'prescriptions' | 'referrals' | 'labtests' | 'hospitalizations';

export default function PatientHealthFileView({ amka, onBack, apiBaseUrl }: PatientHealthFileViewProps) {
  const [data, setData] = useState<FullHealthFileResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<TabType>('diagnoses');

  // New form states
  const [showAddDiagnosis, setShowAddDiagnosis] = useState(false);
  const [showAddPrescription, setShowAddPrescription] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);
  const [formSuccess, setFormSuccess] = useState<string | null>(null);

  // Available metadata
  const [availableDiagnoses, setAvailableDiagnoses] = useState<Diagnosis[]>([]);
  const [availableDoctors, setAvailableDoctors] = useState<Doctor[]>([]);
  const [availableMedications, setAvailableMedications] = useState<Medication[]>([]);

  // Form inputs
  const [diagnosisInput, setDiagnosisInput] = useState({
    ICD10_code: '',
    diagnosis_date: new Date().toISOString().split('T')[0]
  });

  const [prescriptionInput, setPrescriptionInput] = useState({
    med_id: '',
    doctor_AMKA: '',
    start_date: new Date().toISOString().split('T')[0],
    end_date: '',
    dosage: '',
    frequency: ''
  });

  const fetchHealthFile = async () => {
    try {
      const response = await fetch(`${apiBaseUrl}/patients/${amka}/health-file`);
      if (!response.ok) {
        throw new Error(`Σφάλμα κατά τη φόρτωση του φακέλου: ${response.statusText}`);
      }
      const healthData = await response.json();
      setData(healthData);
    } catch (err) {
      console.error(err);
      setError(err instanceof Error ? err.message : 'Αποτυχία σύνδεσης με το backend.');
    }
  };

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      await fetchHealthFile();
      setLoading(false);
    };
    loadData();
  }, [amka, apiBaseUrl]);

  useEffect(() => {
    const fetchMetadata = async () => {
      try {
        const [diagnosesRes, doctorsRes, medsRes] = await Promise.all([
          fetch(`${apiBaseUrl}/diagnoses`),
          fetch(`${apiBaseUrl}/doctors`),
          fetch(`${apiBaseUrl}/medications`)
        ]);
        if (diagnosesRes.ok) setAvailableDiagnoses(await diagnosesRes.json());
        if (doctorsRes.ok) setAvailableDoctors(await doctorsRes.json());
        if (medsRes.ok) setAvailableMedications(await medsRes.json());
      } catch (err) {
        console.error("Error fetching form metadata:", err);
      }
    };
    fetchMetadata();
  }, [apiBaseUrl]);

  if (loading) {
    return <div style={{ textAlign: 'center', padding: '2rem' }}>Φόρτωση ιατρικού φακέλου...</div>;
  }

  if (error || !data) {
    return (
      <div style={{ padding: '2rem', textAlign: 'center' }}>
        <p style={{ color: 'red', marginBottom: '1rem' }}>Σφάλμα: {error || 'Δεν βρέθηκαν δεδομένα.'}</p>
        <button className="btn" onClick={onBack}>Επιστροφή</button>
      </div>
    );
  }

  const handleAddDiagnosisSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError(null);
    setFormSuccess(null);
    try {
      const response = await fetch(`${apiBaseUrl}/patients/${amka}/diagnoses`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(diagnosisInput)
      });
      const resData = await response.json();
      if (!response.ok) {
        throw new Error(resData.error || 'Αποτυχία καταχώρισης διάγνωσης');
      }
      setFormSuccess('Η διάγνωση καταχωρήθηκε επιτυχώς.');
      setShowAddDiagnosis(false);
      setDiagnosisInput({
        ICD10_code: '',
        diagnosis_date: new Date().toISOString().split('T')[0]
      });
      await fetchHealthFile();
    } catch (err) {
      setFormError(err instanceof Error ? err.message : 'Σφάλμα κατά την καταχώριση.');
    }
  };

  const handleAddPrescriptionSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError(null);
    setFormSuccess(null);
    try {
      const response = await fetch(`${apiBaseUrl}/patients/${amka}/prescriptions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(prescriptionInput)
      });
      const resData = await response.json();
      if (!response.ok) {
        throw new Error(resData.error || 'Αποτυχία καταχώρισης συνταγογράφησης');
      }
      setFormSuccess('Η συνταγογράφηση καταχωρήθηκε επιτυχώς.');
      setShowAddPrescription(false);
      setPrescriptionInput({
        med_id: '',
        doctor_AMKA: '',
        start_date: new Date().toISOString().split('T')[0],
        end_date: '',
        dosage: '',
        frequency: ''
      });
      await fetchHealthFile();
    } catch (err) {
      setFormError(err instanceof Error ? err.message : 'Σφάλμα κατά την καταχώριση.');
    }
  };

  const { patient, diagnoses, visits, prescriptions, referrals, lab_tests, hospitalizations } = data;

  return (
    <div>
      <div className="page-header">
        <div className="page-header-row">
          <div>
            <h1>Ηλεκτρονικός Φάκελος Υγείας (ΗΦΥ)</h1>
            <p className="text-muted" style={{ marginTop: '4px' }}>
              Ασθενής: <strong>{patient.last_name} {patient.first_name}</strong> | ΑΜΚΑ: {patient.AMKA}
            </p>
          </div>
          <button className="btn" onClick={onBack}>
            ← Επιστροφή
          </button>
        </div>
      </div>

      <div style={{ display: 'flex', gap: '20px', alignItems: 'flex-start' }}>
        {/* Left column: Summary info */}
        <div className="card" style={{ flex: '0 0 280px', padding: '16px' }}>
          <h3 style={{ fontSize: '0.95rem', borderBottom: '1px solid #eee', paddingBottom: '8px', marginBottom: '12px' }}>
            Στοιχεία Ασθενούς
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', fontSize: '0.85rem' }}>
            <div>
              <span className="text-muted" style={{ display: 'block' }}>Πατρώνυμο</span>
              <strong>{patient.patronym}</strong>
            </div>
            <div>
              <span className="text-muted" style={{ display: 'block' }}>Ηλικία / Φύλο</span>
              <strong>{patient.age ? `${patient.age} ετών` : '—'} / {patient.sex}</strong>
            </div>
            <div>
              <span className="text-muted" style={{ display: 'block' }}>Εθνικότητα</span>
              <span>{patient.nationality}</span>
            </div>
            <div>
              <span className="text-muted" style={{ display: 'block' }}>Επάγγελμα</span>
              <span>{patient.occupation ?? '—'}</span>
            </div>
            <div>
              <span className="text-muted" style={{ display: 'block' }}>Ασφαλιστικός Φορέας</span>
              <span className="badge badge-neutral">{patient.insurance_provider?.name ?? '—'}</span>
            </div>
            <div>
              <span className="text-muted" style={{ display: 'block', marginBottom: '4px' }}>Γνωστές Αλλεργίες</span>
              {patient.allergies && patient.allergies.length > 0 ? (
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
                  {patient.allergies.map(a => (
                    <span key={a} className="badge badge-danger">{a}</span>
                  ))}
                </div>
              ) : (
                <span className="badge badge-success">Καμία αλλεργία</span>
              )}
            </div>
          </div>
        </div>

        {/* Right column: Records and Tabs */}
        <div style={{ flex: 1 }}>
          {/* Custom functional tabs header */}
          <div style={{ display: 'flex', gap: '4px', borderBottom: '1px solid #ddd', marginBottom: '16px' }}>
            {[
              { id: 'diagnoses', label: `Διαγνώσεις (${diagnoses.length})` },
              { id: 'visits', label: `Επισκέψεις (${visits.length})` },
              { id: 'prescriptions', label: `Συνταγές (${prescriptions.length})` },
              { id: 'referrals', label: `Παραπεμπτικά (${referrals.length})` },
              { id: 'labtests', label: `Εξετάσεις (${lab_tests.length})` },
              { id: 'hospitalizations', label: `Νοσηλείες (${hospitalizations.length})` },
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as TabType)}
                style={{
                  padding: '8px 12px',
                  background: activeTab === tab.id ? '#fff' : 'transparent',
                  border: '1px solid',
                  borderColor: activeTab === tab.id ? '#ddd #ddd transparent #ddd' : 'transparent',
                  borderBottom: activeTab === tab.id ? '2px solid #2563eb' : 'none',
                  borderRadius: '4px 4px 0 0',
                  cursor: 'pointer',
                  fontSize: '0.82rem',
                  fontWeight: activeTab === tab.id ? '600' : 'normal',
                  color: activeTab === tab.id ? '#2563eb' : '#555',
                  marginBottom: '-1px'
                }}
              >
                {tab.label}
              </button>
            ))}
          </div>

          <div className="card" style={{ padding: '16px' }}>
            {activeTab === 'diagnoses' && (
              <div>
                {formSuccess && <div style={{ color: '#166534', background: '#dcfce7', padding: '8px', borderRadius: '4px', marginBottom: '12px', fontSize: '0.8rem' }}>✓ {formSuccess}</div>}
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                  <h4 style={{ fontSize: '0.95rem' }}>Ιστορικό Διαγνώσεων</h4>
                  <button className="btn btn-primary btn-sm" onClick={() => {
                    setShowAddDiagnosis(!showAddDiagnosis);
                    setFormError(null);
                    setFormSuccess(null);
                  }}>
                    {showAddDiagnosis ? 'Ακύρωση' : '+ Νέα Διάγνωση'}
                  </button>
                </div>

                {showAddDiagnosis && (
                  <form onSubmit={handleAddDiagnosisSubmit} style={{ padding: '12px', border: '1px solid #ddd', borderRadius: '4px', marginBottom: '16px', background: '#fafafa' }}>
                    <h5 style={{ marginBottom: '10px', fontSize: '0.85rem' }}>Καταχώριση Νέας Διάγνωσης</h5>
                    {formError && <div style={{ color: '#b91c1c', fontSize: '0.8rem', marginBottom: '8px' }}>❌ {formError}</div>}
                    <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap', alignItems: 'flex-end' }}>
                      <div className="form-group" style={{ flex: '1 1 200px', marginBottom: '0' }}>
                        <label style={{ fontSize: '0.75rem', fontWeight: 'bold' }}>Διάγνωση (ICD10)</label>
                        <select
                          required
                          value={diagnosisInput.ICD10_code}
                          onChange={(e) => setDiagnosisInput(prev => ({ ...prev, ICD10_code: e.target.value }))}
                          style={{ width: '100%', padding: '6px' }}
                        >
                          <option value="">Επιλέξτε Διάγνωση...</option>
                          {availableDiagnoses.map(d => (
                            <option key={d.ICD10_code} value={d.ICD10_code}>
                              {d.ICD10_code} - {d.description}
                            </option>
                          ))}
                        </select>
                      </div>
                      <div className="form-group" style={{ flex: '0 0 150px', marginBottom: '0' }}>
                        <label style={{ fontSize: '0.75rem', fontWeight: 'bold' }}>Ημερομηνία</label>
                        <input
                          type="date"
                          required
                          value={diagnosisInput.diagnosis_date}
                          onChange={(e) => setDiagnosisInput(prev => ({ ...prev, diagnosis_date: e.target.value }))}
                          style={{ width: '100%', padding: '5px' }}
                        />
                      </div>
                      <div>
                        <button type="submit" className="btn btn-primary btn-sm">Αποθήκευση</button>
                      </div>
                    </div>
                  </form>
                )}

                {diagnoses.length === 0 ? (
                  <p className="text-muted text-small">Δεν υπάρχουν καταγεγραμμένες διαγνώσεις.</p>
                ) : (
                  <div className="table-wrapper">
                    <table>
                      <thead>
                        <tr>
                          <th>Κωδικός ICD10</th>
                          <th>Περιγραφή</th>
                          <th>Ημερομηνία</th>
                        </tr>
                      </thead>
                      <tbody>
                        {diagnoses.map(d => (
                          <tr key={d.diagnosis_id}>
                            <td><strong style={{ color: '#b91c1c' }}>{d.ICD10_code}</strong></td>
                            <td>{d.description}</td>
                            <td>{d.diagnosis_date}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'visits' && (
              <div>
                <h4 style={{ marginBottom: '12px', fontSize: '0.95rem' }}>Ιστορικό Επισκέψεων</h4>
                {visits.length === 0 ? (
                  <p className="text-muted text-small">Δεν υπάρχουν καταγεγραμμένες επισκέψεις.</p>
                ) : (
                  <div className="table-wrapper">
                    <table>
                      <thead>
                        <tr>
                          <th>Ημερομηνία & Ώρα</th>
                          <th>Ιατρός</th>
                          <th>Ειδικότητα</th>
                        </tr>
                      </thead>
                      <tbody>
                        {visits.map(v => (
                          <tr key={v.visit_id}>
                            <td>{v.visit_datetime}</td>
                            <td><strong>{v.doctor_name}</strong></td>
                            <td><span className="badge badge-neutral">{v.doctor_specialty}</span></td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'prescriptions' && (
              <div>
                {formSuccess && <div style={{ color: '#166534', background: '#dcfce7', padding: '8px', borderRadius: '4px', marginBottom: '12px', fontSize: '0.8rem' }}>✓ {formSuccess}</div>}
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                  <h4 style={{ fontSize: '0.95rem' }}>Συνταγογραφημένα Φάρμακα</h4>
                  <button className="btn btn-primary btn-sm" onClick={() => {
                    setShowAddPrescription(!showAddPrescription);
                    setFormError(null);
                    setFormSuccess(null);
                  }}>
                    {showAddPrescription ? 'Ακύρωση' : '+ Νέα Συνταγή'}
                  </button>
                </div>

                {showAddPrescription && (
                  <form onSubmit={handleAddPrescriptionSubmit} style={{ padding: '16px', border: '1px solid #ddd', borderRadius: '4px', marginBottom: '16px', background: '#fafafa' }}>
                    <h5 style={{ marginBottom: '12px', fontSize: '0.85rem' }}>Καταχώριση Νέας Συνταγογράφησης</h5>
                    {formError && (
                      <div style={{ color: '#b91c1c', background: '#fee2e2', padding: '10px', borderRadius: '4px', fontSize: '0.85rem', marginBottom: '12px', fontWeight: '500' }}>
                        ⚠️ {formError}
                      </div>
                    )}
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '12px', marginBottom: '12px' }}>
                      <div className="form-group" style={{ marginBottom: '0' }}>
                        <label style={{ fontSize: '0.75rem', fontWeight: 'bold' }}>Φάρμακο</label>
                        <select
                          required
                          value={prescriptionInput.med_id}
                          onChange={(e) => setPrescriptionInput(prev => ({ ...prev, med_id: e.target.value }))}
                          style={{ width: '100%', padding: '6px' }}
                        >
                          <option value="">Επιλέξτε Φάρμακο...</option>
                          {availableMedications.map(m => (
                            <option key={m.med_id} value={m.med_id}>
                              {m.product_name} ({m.administration_route})
                            </option>
                          ))}
                        </select>
                      </div>

                      <div className="form-group" style={{ marginBottom: '0' }}>
                        <label style={{ fontSize: '0.75rem', fontWeight: 'bold' }}>Συνταγογραφών Ιατρός</label>
                        <select
                          required
                          value={prescriptionInput.doctor_AMKA}
                          onChange={(e) => setPrescriptionInput(prev => ({ ...prev, doctor_AMKA: e.target.value }))}
                          style={{ width: '100%', padding: '6px' }}
                        >
                          <option value="">Επιλέξτε Ιατρό...</option>
                          {availableDoctors.map(d => (
                            <option key={d.AMKA} value={d.AMKA}>
                              δρ. {d.last_name} {d.first_name} ({d.specialty})
                            </option>
                          ))}
                        </select>
                      </div>

                      <div className="form-group" style={{ marginBottom: '0' }}>
                        <label style={{ fontSize: '0.75rem', fontWeight: 'bold' }}>Δοσολογία</label>
                        <input
                          type="text"
                          required
                          placeholder="π.χ. 500mg, 1 δισκίο"
                          value={prescriptionInput.dosage}
                          onChange={(e) => setPrescriptionInput(prev => ({ ...prev, dosage: e.target.value }))}
                          style={{ width: '100%', padding: '5px' }}
                        />
                      </div>

                      <div className="form-group" style={{ marginBottom: '0' }}>
                        <label style={{ fontSize: '0.75rem', fontWeight: 'bold' }}>Συχνότητα</label>
                        <input
                          type="text"
                          required
                          placeholder="π.χ. 3 φορές την ημέρα"
                          value={prescriptionInput.frequency}
                          onChange={(e) => setPrescriptionInput(prev => ({ ...prev, frequency: e.target.value }))}
                          style={{ width: '100%', padding: '5px' }}
                        />
                      </div>

                      <div className="form-group" style={{ marginBottom: '0' }}>
                        <label style={{ fontSize: '0.75rem', fontWeight: 'bold' }}>Ημερομηνία Έναρξης</label>
                        <input
                          type="date"
                          required
                          value={prescriptionInput.start_date}
                          onChange={(e) => setPrescriptionInput(prev => ({ ...prev, start_date: e.target.value }))}
                          style={{ width: '100%', padding: '5px' }}
                        />
                      </div>

                      <div className="form-group" style={{ marginBottom: '0' }}>
                        <label style={{ fontSize: '0.75rem', fontWeight: 'bold' }}>Ημερομηνία Λήξης (Προαιρετικό)</label>
                        <input
                          type="date"
                          value={prescriptionInput.end_date}
                          onChange={(e) => setPrescriptionInput(prev => ({ ...prev, end_date: e.target.value }))}
                          style={{ width: '100%', padding: '5px' }}
                        />
                      </div>
                    </div>

                    <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '8px' }}>
                      <button type="submit" className="btn btn-primary btn-sm">Αποθήκευση</button>
                    </div>
                  </form>
                )}

                {prescriptions.length === 0 ? (
                  <p className="text-muted text-small">Δεν υπάρχουν καταγεγραμμένες συνταγές.</p>
                ) : (
                  <div className="table-wrapper">
                    <table>
                      <thead>
                        <tr>
                          <th>Φάρμακο</th>
                          <th>Δραστικές Ουσίες</th>
                          <th>Δοσολογία & Συχνότητα</th>
                          <th>Ιατρός</th>
                          <th>Διάρκεια</th>
                        </tr>
                      </thead>
                      <tbody>
                        {prescriptions.map(p => {
                          const hasAllergyConflict = p.active_substances.some(sub =>
                            patient.allergies?.includes(sub)
                          );

                          return (
                            <tr key={p.prescription_id} style={hasAllergyConflict ? { background: '#fef2f2' } : {}}>
                              <td>
                                <strong>{p.medication_name}</strong>
                                {hasAllergyConflict && (
                                  <div style={{ color: '#b91c1c', fontSize: '0.75rem', fontWeight: 'bold' }}>
                                    ⚠️ ΠΡΟΣΟΧΗ: Αλλεργία!
                                  </div>
                                )}
                              </td>
                              <td>
                                <div style={{ display: 'flex', gap: '3px', flexWrap: 'wrap' }}>
                                  {p.active_substances.map(sub => {
                                    const isAllergic = patient.allergies?.includes(sub);
                                    return (
                                      <span key={sub} className={isAllergic ? "badge badge-danger" : "badge badge-neutral"}>
                                        {sub}
                                      </span>
                                    );
                                  })}
                                </div>
                              </td>
                              <td>{p.dosage} / {p.frequency}</td>
                              <td>{p.doctor_name}</td>
                              <td>
                                <div className="text-small">{p.start_date}</div>
                                <div className="text-muted text-small">έως {p.end_date ?? '—'}</div>
                              </td>
                            </tr>
                          );
                        })}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'referrals' && (
              <div>
                <h4 style={{ marginBottom: '12px', fontSize: '0.95rem' }}>Εκδοθέντα Παραπεμπτικά</h4>
                {referrals.length === 0 ? (
                  <p className="text-muted text-small">Δεν υπάρχουν εκκρεμή ή εκδοθέντα παραπεμπτικά.</p>
                ) : (
                  <div className="table-wrapper">
                    <table>
                      <thead>
                        <tr>
                          <th>Τύπος Εξέτασης</th>
                          <th>Περιγραφή</th>
                          <th>Ιατρός</th>
                          <th>Ημ. Έκδοσης</th>
                          <th>Λήξη</th>
                        </tr>
                      </thead>
                      <tbody>
                        {referrals.map(r => (
                          <tr key={r.referral_id}>
                            <td><strong>{r.lab_test_type}</strong></td>
                            <td className="text-small">{r.lab_test_description ?? '—'}</td>
                            <td>{r.doctor_name}</td>
                            <td>{r.issue_date}</td>
                            <td>
                              {r.expiration_date ? (
                                <span className="text-small">{r.expiration_date}</span>
                              ) : (
                                <span className="text-muted">—</span>
                              )}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'labtests' && (
              <div>
                <h4 style={{ marginBottom: '12px', fontSize: '0.95rem' }}>Αποτελέσματα Εργαστηριακών Εξετάσεων</h4>
                {lab_tests.length === 0 ? (
                  <p className="text-muted text-small">Δεν υπάρχουν αποτελέσματα εργαστηριακών εξετάσεων.</p>
                ) : (
                  <div className="table-wrapper">
                    <table>
                      <thead>
                        <tr>
                          <th>Εξέταση</th>
                          <th>Ημερομηνία</th>
                          <th>Αποτελέσματα / Τιμές</th>
                          <th>Κόστος</th>
                        </tr>
                      </thead>
                      <tbody>
                        {lab_tests.map(lt => (
                          <tr key={lt.ex_lab_test_id}>
                            <td><strong>{lt.lab_test_type}</strong></td>
                            <td>{lt.datetime}</td>
                            <td style={{ whiteSpace: 'pre-line' }}>{lt.results ?? 'Εκκρεμεί'}</td>
                            <td>{lt.cost != null ? `${lt.cost.toFixed(2)} €` : '—'}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'hospitalizations' && (
              <div>
                <h4 style={{ marginBottom: '12px', fontSize: '0.95rem' }}>Ιστορικό Νοσηλειών</h4>
                {hospitalizations.length === 0 ? (
                  <p className="text-muted text-small">Δεν υπάρχουν καταγεγραμμένες νοσηλείες.</p>
                ) : (
                  <div className="table-wrapper">
                    <table>
                      <thead>
                        <tr>
                          <th>Νοσοκομείο</th>
                          <th>Ημερομηνία Εισαγωγής</th>
                          <th>Ημερομηνία Εξιτηρίου</th>
                          <th>Κατάσταση</th>
                        </tr>
                      </thead>
                      <tbody>
                        {hospitalizations.map(h => (
                          <tr key={h.hospitalization_id}>
                            <td><strong>{h.hospital_name}</strong></td>
                            <td>{h.date_of_admission}</td>
                            <td>{h.date_of_discharge ?? '—'}</td>
                            <td>
                              {h.date_of_discharge ? (
                                <span className="badge badge-success">Ολοκληρώθηκε</span>
                              ) : (
                                <span className="badge badge-danger">Ενεργή Νοσηλεία</span>
                              )}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
