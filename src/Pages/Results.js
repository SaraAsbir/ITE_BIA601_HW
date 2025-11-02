import React from "react";
import { useNavigate } from "react-router-dom";
import "./style/Results.css"; 

function Results() {
  const navigate = useNavigate(); // لإنشاء دالة التنقل

  return (
    <div className="results-container">
      <h1 className="results-title">نتائج التحليل</h1>

      {/* وصف قصير للنتائج المعروضة */}
      <p className="results-description">
        الخوارزمية الجينية اختارت المجموعة المثلى من الخصائص الطبية
        التي تحقق أفضل دقة للنموذج.
      </p>

      {/* صندوق يحتوي على النتائج الأساسية */}
      <div className="results-box">
        <p>
          عدد الخصائص المختارة: <strong>6</strong>
        </p>
        <p>
          دقة النموذج: <strong>94%</strong>
        </p>
      </div>

      {/* زر للعودة إلى صفحة رفع البيانات */}
      <button onClick={() => navigate("/upload")} className="results-btn">
        العودة إلى رفع البيانات
      </button>
    </div>
  );
}

export default Results;
