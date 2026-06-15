import { useState, useEffect } from 'react';
import './index.css';
import type { Patient, PatientHealthFile } from './types';

import PatientList from './components/PatientList';
import AddPatient from './components/AddPatient';
import PatientProfileCard from './components/PatientProfileCard';
import PatientHealthFileView from './components/PatientHealthFileView';

const API_BASE_URL = 'http://localhost:5000/api';

export default function App() {
  const [healthFiles, setHealthFiles] = useState<PatientHealthFile[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentView, setCurrentView] = useState<'list' | 'add' | 'profile' | 'healthfile'>('list');
  const [selectedAmka, setSelectedAmka] = useState<string | null>(null);

  const fetchPatients = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/patients`);
      if (!response.ok) {
        throw new Error(`Σφάλμα κατά τη φόρτωση των δεδομένων: ${response.statusText}`);
      }
      const data = await response.json();
      setHealthFiles(data);
      setError(null);
    } catch (err) {
      console.error(err);
      setError(err instanceof Error ? err.message : 'Αποτυχία σύνδεσης με το backend.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    Promise.resolve().then(() => {
      fetchPatients();
    });
  }, []);

  const handleAddPatientSubmit = async (newPatient: Patient) => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/patients`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ patient: newPatient }),
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Αποτυχία αποθήκευσης ασθενούς.');
      }
      
      await fetchPatients();
      setCurrentView('list');
    } catch (err) {
      console.error(err);
      alert(err instanceof Error ? err.message : 'Αποτυχία αποθήκευσης ασθενούς.');
    } finally {
      setLoading(false);
    }
  };

  const handleViewProfile = (amka: string) => {
    setSelectedAmka(amka);
    setCurrentView('profile');
  };

  const handleViewHealthFile = (amka: string) => {
    setSelectedAmka(amka);
    setCurrentView('healthfile');
  };

  const selectedPatient = healthFiles.find(f => f.patient.AMKA === selectedAmka)?.patient;

  return (
    <div className="app-wrapper">
      <nav className="navbar">
        <div className="navbar-brand">
          <div className="navbar-logo-icon">ΗΦΥ</div>
          <div>
            <div className="navbar-title">Σύστημα ΗΦΥ</div>
            <div className="navbar-subtitle">Biomed EMR 2026</div>
          </div>
        </div>
      </nav>

      <main className="main-content">
        {loading && <div style={{ textAlign: 'center', padding: '2rem' }}>Φόρτωση δεδομένων...</div>}
        {error && <div style={{ color: 'red', textAlign: 'center', padding: '2rem' }}>Σφάλμα: {error}</div>}
        
        {!loading && !error && currentView === 'list' && (
          <PatientList
            healthFiles={healthFiles}
            onViewProfile={handleViewProfile}
            onViewHealthFile={handleViewHealthFile}
            onAddPatient={() => setCurrentView('add')}
          />
        )}
        {!loading && !error && currentView === 'add' && (
          <AddPatient
            onSubmit={handleAddPatientSubmit}
            onCancel={() => setCurrentView('list')}
          />
        )}
        {!loading && !error && currentView === 'profile' && selectedPatient && (
          <PatientProfileCard
            patient={selectedPatient}
            onBack={() => {
              setCurrentView('list');
              setSelectedAmka(null);
            }}
          />
        )}
        {!loading && !error && currentView === 'healthfile' && selectedAmka && (
          <PatientHealthFileView
            amka={selectedAmka}
            apiBaseUrl={API_BASE_URL}
            onBack={() => {
              setCurrentView('list');
              setSelectedAmka(null);
            }}
          />
        )}
      </main>
    </div>
  );
}
