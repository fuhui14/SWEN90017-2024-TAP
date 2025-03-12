import React from 'react';
import {Routes, Route } from 'react-router-dom';
import Transpage from './transcription/transpage';
import Process from './process/process';
import TranscriptionResult from './transcriptionresult/transcriptionresult';
import './App.css';

function App() {
  return (
      <div className="App">
        <Routes>
          {/* Define your route paths here */}
          <Route path="/" element={<Transpage />} />
          <Route path="/transcription" element={<Transpage />} />
          <Route path="/process" element={<Process />} />
          <Route path="/transcription/transcriptionresult" element={<TranscriptionResult />} />
        </Routes>
      </div>
  );
}

export default App;
