import React, { useState } from "react";
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
  };

  return (
    <div className="upload-container">
      <h1 className="upload-title">رفع بيانات سرطان الثدي</h1>

      {/* وصف بسيط حول طبيعة الملف المطلوب */}
      <p className="upload-description">
        يرجى رفع ملف CSV يحتوي على الخصائص الطبية (Features)
        مع عمود التشخيص (Diagnosis) لتحليلها بالخوارزمية الجينية.
      </p>

      {/* نموذج رفع الملف */}
      <form className="upload-form" onSubmit={handleSubmit}>
        {/* إدخال نوع الملف */}
        <input
          type="file"
          accept=".csv"
          onChange={handleFileChange}
          className="upload-input"
        />
        {/* زر تنفيذ عملية الرفع */}
        <button type="submit" className="upload-button">
          رفع الملف
        </button>
      </form>

      {/* عرض اسم الملف في حال تم اختياره */}
      {file && (
        <p className="file-name">
          📄 الملف المحدد: <strong>{file.name}</strong>
        </p>
      )}

      {/* عرض الرسالة للمستخدم (نجاح أو تنبيه) */}
      {message && <p className="upload-message">{message}</p>}
    </div>
  );
}

export default Upload;
