import React, { useState } from "react";
import "./style/Upload.css";
import { uploadAndAnalyze, ENDPOINTS } from "../services/api";
import { useNavigate } from "react-router-dom";

function Upload() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [algo, setAlgo] = useState("ga_mi");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMessage("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setMessage("الرجاء اختيار ملف قبل الرفع.");
      return;
    }

    try {
      setLoading(true);
      setMessage("...جارٍ التحليل");

      const data = await uploadAndAnalyze(algo, file);
      console.log("✅ نتائج التحليل:", data);

      const prevResults = JSON.parse(localStorage.getItem("fs_all_results")) || [];
      const newEntry = {
        endpoint: algo,
        data,
        receivedAt: new Date().toISOString(),
      };
      const updated = [
        ...prevResults.filter((r) => r.endpoint !== algo),
        newEntry,
      ];
      localStorage.setItem("fs_all_results", JSON.stringify(updated));
      localStorage.setItem(
        "fs_results",
        JSON.stringify({
          endpoint: algo,
          receivedAt: new Date().toISOString(),
          data,
        })
      );

      setMessage("تم تحليل الملف بنجاح");
      navigate("/results");
    } catch (err) {
      console.error("❌ خطأ أثناء التحليل:", err);
      setMessage(err.message || "حدث خطأ أثناء الاتصال بالخادم.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-container">
      <h1 className="upload-title">رفع بيانات سرطان الثدي</h1>

      <p className="upload-description">
        يرجى رفع ملف CSV يحتوي على الخصائص الطبية (Features)
        مع عمود الهدف (target) لتحليلها بالخوارزميات المختلفة.
      </p>

      <form className="upload-form" onSubmit={handleSubmit}>
        <input
          type="file"
          accept=".csv"
          onChange={handleFileChange}
          className="upload-input"
        />

        <select
          className="upload-select"
          value={algo}
          onChange={(e) => setAlgo(e.target.value)}
          style={{ direction: "ltr" }}
        >
          <option value="ga">Genetic Algorithm (GA)</option>
          <option value="ga_mi">GA + Mutual Information</option>
          <option value="ga_chi">GA + Chi-Square</option>
          <option value="ga_pca">GA + PCA</option>
          <option value="ga_rfe">GA + RFE</option>
        </select>

        <button type="submit" className="upload-button" disabled={loading}>
          {loading ? "جارٍ التحليل..." : "رفع + تحليل"}
        </button>
      </form>

      {file && (
        <p className="file-name">
          📄 الملف المحدد: <strong>{file.name}</strong>
        </p>
      )}

      {message && <p className="upload-message">{message}</p>}
    </div>
  );
}

export default Upload;
