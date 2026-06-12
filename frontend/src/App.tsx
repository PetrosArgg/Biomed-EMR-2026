import { useState } from 'react';
import './index.css';
import type { Patient, PatientHealthFile } from './types';
import { mockHealthFiles } from './data/mockData';

import PatientList from './components/PatientList';
import AddPatient from './components/AddPatient';
import PatientProfileCard from './components/PatientProfileCard';

export default function App() {
  const [healthFiles, setHealthFiles] = useState<PatientHealthFile[]>(mockHealthFiles);
  const [currentView, setCurrentView] = useState<'list' | 'add' | 'profile'>('list');
  const [selectedAmka, setSelectedAmka] = useState<string | null>(null);

  const handleAddPatientSubmit = (newPatient: Patient) => {
    const newHealthFile: PatientHealthFile = {
      patient: newPatient,
    };
    setHealthFiles(prev => [newHealthFile, ...prev]);
    setCurrentView('list');
  };

  const handleViewProfile = (amka: string) => {
    setSelectedAmka(amka);
    setCurrentView('profile');
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
        {currentView === 'list' && (
          <PatientList
            healthFiles={healthFiles}
            onViewProfile={handleViewProfile}
            onViewHealthFile={() => {}}
            onAddPatient={() => setCurrentView('add')}
          />
        )}
        {currentView === 'add' && (
          <AddPatient
            onSubmit={handleAddPatientSubmit}
            onCancel={() => setCurrentView('list')}
          />
        )}
        {currentView === 'profile' && selectedPatient && (
          <PatientProfileCard
            patient={selectedPatient}
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