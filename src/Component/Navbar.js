<<<<<<< HEAD
=======
// src/components/Navbar.jsx
>>>>>>> b9efbc35fb97b2abfd57b077cd82d9de79afcec8
import React from "react";
import { Link, useLocation } from "react-router-dom";
import "./Navbar.css";
import logo from "../assets/Logo.png";

function Navbar() {
  const location = useLocation();

  const isActive = (path) => (location.pathname === path ? "active-link" : "");

  return (
    <nav className="navbar">
<<<<<<< HEAD
=======
      {/* شعار الموقع (يعود للرئيسية عند الضغط) */}
>>>>>>> b9efbc35fb97b2abfd57b077cd82d9de79afcec8
      <div className="navbar-logo">
        <Link to="/" className="logo-link">
          <img src={logo} alt="Breast Cancer Logo" className="logo-img" />
          <span className="logo-text">Breast Cancer Feature Selection</span>
        </Link>
      </div>

      {/* روابط الصفحات */}
      <div className="navbar-links">
        <Link to="/" className={`navbar-link ${isActive("/")}`}>
          الرئيسية
        </Link>

        <Link to="/upload" className={`navbar-link ${isActive("/upload")}`}>
          رفع البيانات
        </Link>

        <Link to="/results" className={`navbar-link ${isActive("/results")}`}>
          النتائج
        </Link>

        <Link
          to="/comparison"
          className={`navbar-link ${isActive("/comparison")}`}
        >
          المقارنة
        </Link>
      </div>

      <div className="navbar-empty"></div>
    </nav>
  );
}

export default Navbar;
