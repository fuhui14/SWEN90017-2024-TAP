import React from 'react';
import {Routes, Route } from 'react-router-dom';
import Transpage from './transcription/transpage';
import Process from './process/process';
import TranscriptionResult from './transcriptionresult/transcriptionresult';
import HistoryLogin from './historylogin/historylogin';
import History from './history/history';
import About from './about/about';
import './App.css';

function App() {
  return (
      <div className="App">
        <Routes>
          {/* Define your route paths here */}
          <Route path="/" element={<About />} />
          <Route path="/transcription" element={<Transpage />} />
          <Route path="/process" element={<Process />} />
          <Route path="/transcription/transcriptionresult" element={<TranscriptionResult />} />
          <Route path="/historylogin" element={<HistoryLogin />} />
          <Route path="/history" element={<History />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </div>
  );
}

export default App;
