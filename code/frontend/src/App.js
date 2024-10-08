import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom'; // Corrected import
import Transpage from './transcription/transpage';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <Routes>
          {/* Define your route paths here */}
          <Route path="/" element={<Transpage />} />
          <Route path="/transcription" element={<Transpage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
