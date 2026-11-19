import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import { initializeDefaultData } from './utils/initializeData';
import reportWebVitals from './lib/reportWebVitals';

// Initialize default data
initializeDefaultData();

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// ST-06 (BLG-QA-271, v9.18): Core Web Vitals (performance_budget.md §4.3).
reportWebVitals();
