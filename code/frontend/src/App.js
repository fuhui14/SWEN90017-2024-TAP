import React from 'react';
import { Routes, Route } from 'react-router-dom'; // Import routing components
import Transpage from './transcription/transpage';
import Process from './process/process';
import TranscriptionResult from './transcriptionresult/transcriptionresult';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <Routes>
          {/* Define your route paths here */}
          <Route path="/" element={<Transpage />} />
          <Route path="/transcription" element={<Transpage />} />
          <Route path="/process" element={<Process />} />
          <Route path="/transcription/transcriptionresult" element={<TranscriptionResult />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
