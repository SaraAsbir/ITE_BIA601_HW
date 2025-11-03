import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./Component/Navbar";
import Home from "./Pages/Home";
import Results from "./Pages/Results";
import Upload from "./Pages/Upload";
import Comparison from "./Pages/Comparison";


function App() {
  return (
    <Router>
      <Navbar />
      <div className="page-content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/results" element={<Results />} />
          <Route path="Upload" element={<Upload />} />
          <Route path="Comparison" element={<Comparison />} />

        </Routes>
      </div>
    </Router>
  );
}

export default App;
