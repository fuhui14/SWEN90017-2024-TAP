import React from 'react';
import { Routes, Route } from 'react-router-dom'; // Import routing components
import Transpage from './transcription/transpage';
import Process from './process/process';
import './App.css';
import History from "./history/history";

function App() {
  return (
    <div className="App">
      <Routes> {/* Define your routes here */}
        <Route path="/" element={<Transpage />} />
        <Route path="/transcription" element={<Transpage />} />
        <Route path="/process" element={<Process />} />
        <Route path="/history" element={<History />} />
      </Routes>
    </div>
  );
}

export default App;
