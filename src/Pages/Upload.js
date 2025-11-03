import React, { useState } from "react";
<<<<<<< HEAD
import "./style/Upload.css";
import { uploadAndAnalyze, ENDPOINTS } from "../services/api";
import { useNavigate } from "react-router-dom";

function Upload() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [algo, setAlgo] = useState("ga_mi"); // القيمة الافتراضية
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

      // نرسل الملف إلى الخادم
      const data = await uploadAndAnalyze(algo, file);
      console.log("✅ نتائج التحليل:", data);

      // نجلب النتائج السابقة (إن وُجدت)
      const prevResults = JSON.parse(localStorage.getItem("fs_all_results")) || [];

      //  نحضّر النتيجة الجديدة
      const newEntry = {
        endpoint: algo,
        data,
        receivedAt: new Date().toISOString(),
      };

      //  إذا كانت هذه الخوارزمية موجودة مسبقًا، نستبدلها
      const updated = [
        ...prevResults.filter((r) => r.endpoint !== algo),
        newEntry,
      ];

      //  نخزن جميع النتائج مع النتيجة الجديدة
      localStorage.setItem("fs_all_results", JSON.stringify(updated));

      //  نخزن آخر نتيجة فقط لصفحة Results.js
      localStorage.setItem(
        "fs_results",
        JSON.stringify({
          endpoint: algo,
          receivedAt: new Date().toISOString(),
          data,
        })
      );

      setMessage("تم تحليل الملف بنجاح ");
      navigate("/results");
    } catch (err) {
      console.error(" خطأ أثناء التحليل:", err);
      setMessage(err.message || "حدث خطأ أثناء الاتصال بالخادم.");
    } finally {
      setLoading(false);
    }
=======
import "./style/Upload.css"; 

function Upload() {
  // تعريف حالتين لتخزين الملف والرسالة للمستخدم
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  // دالة تُنفذ عند اختيار ملف
  const handleFileChange = (e) => {
    setFile(e.target.files[0]); // حفظ الملف المختار
    setMessage(""); // مسح الرسالة السابقة
  };

  // دالة تُنفذ عند الضغط على زر الرفع
  const handleSubmit = (e) => {
    e.preventDefault(); // منع تحديث الصفحة
    if (!file) {
      setMessage("الرجاء اختيار ملف قبل الرفع."); // إذا لم يتم اختيار ملف
      return;
    }
    setMessage("تم رفع الملف بنجاح (محاكاة)"); // رسالة نجاح مؤقتة
>>>>>>> b9efbc35fb97b2abfd57b077cd82d9de79afcec8
  };

  return (
    <div className="upload-container">
      <h1 className="upload-title">رفع بيانات سرطان الثدي</h1>

<<<<<<< HEAD
      <p className="upload-description">
        يرجى رفع ملف CSV يحتوي على الخصائص الطبية (Features)
        مع عمود الهدف (target) لتحليلها بالخوارزميات المختلفة.
      </p>

      <form className="upload-form" onSubmit={handleSubmit}>
        {/* إدخال الملف */}
=======
      {/* وصف بسيط حول طبيعة الملف المطلوب */}
      <p className="upload-description">
        يرجى رفع ملف CSV يحتوي على الخصائص الطبية (Features)
        مع عمود التشخيص (Diagnosis) لتحليلها بالخوارزمية الجينية.
      </p>

      {/* نموذج رفع الملف */}
      <form className="upload-form" onSubmit={handleSubmit}>
        {/* إدخال نوع الملف */}
>>>>>>> b9efbc35fb97b2abfd57b077cd82d9de79afcec8
        <input
          type="file"
          accept=".csv"
          onChange={handleFileChange}
          className="upload-input"
        />
<<<<<<< HEAD

        {/* اختيار الخوارزمية */}
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

        {/* زر التنفيذ */}
        <button type="submit" className="upload-button" disabled={loading}>
          {loading ? "جارٍ التحليل..." : "رفع + تحليل"}
        </button>
      </form>

      {/* عرض اسم الملف */}
=======
        {/* زر تنفيذ عملية الرفع */}
        <button type="submit" className="upload-button">
          رفع الملف
        </button>
      </form>

      {/* عرض اسم الملف في حال تم اختياره */}
>>>>>>> b9efbc35fb97b2abfd57b077cd82d9de79afcec8
      {file && (
        <p className="file-name">
          📄 الملف المحدد: <strong>{file.name}</strong>
        </p>
      )}

<<<<<<< HEAD
      {/* عرض الرسالة */}
=======
      {/* عرض الرسالة للمستخدم (نجاح أو تنبيه) */}
>>>>>>> b9efbc35fb97b2abfd57b077cd82d9de79afcec8
      {message && <p className="upload-message">{message}</p>}
    </div>
  );
}

export default Upload;
