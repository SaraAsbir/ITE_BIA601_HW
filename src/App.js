import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./Component/Navbar";
import Home from "./Pages/Home";
import Results from "./Pages/Results";
import Upload from "./Pages/Upload";
<<<<<<< HEAD
import Comparison from "./Pages/Comparison";
=======
import Comparison from "./Pages/Comarison";
>>>>>>> b9efbc35fb97b2abfd57b077cd82d9de79afcec8


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
