import { useState } from 'react';
import './index.css';

import type { PatientHealthFile } from './types';
import { mockHealthFiles } from './data/mockData';

import PatientList from './components/PatientList';

export default function App() {
  const [healthFiles] = useState<PatientHealthFile[]>(mockHealthFiles);

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
        <PatientList
          healthFiles={healthFiles}
          onViewProfile={() => {}}
          onViewHealthFile={() => {}}
          onAddPatient={() => {}}
        />
      </main>
    </div>
  );
}