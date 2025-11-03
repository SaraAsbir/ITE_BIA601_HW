import React from "react";
import { useNavigate } from "react-router-dom";
import "./style/Comparison.css"; 

function Comparison() {
  const navigate = useNavigate(); // لإنشاء دالة التنقل

  // بيانات مؤقتة للمقارنة بين الطرق المختلفة لاختيار الخصائص
  const data = [
    { method: "الخوارزمية الجينية", accuracy: "94%", color: "#be185d" },
    { method: "Mutual Information (sklearn.feature_selection)", accuracy: "91%", color: "#ec4899" },
    { method: "PCA (Principal Components Analysis)", accuracy: "89%", color: "#f472b6" },
    { method: "Recursive Feature Elimination (RFE) with Logistic Regression", accuracy: "89%", color: "#f472b6" },
    { method: "Chi-Square", accuracy: "89%", color: "#f472b6" },
  ];

  return (
    <div className="comparison-container">
      <h1 className="comparison-title">مقارنة بين طرق اختيار الخصائص</h1>

      {/* وصف بسيط لشرح الجدول */}
      <p className="comparison-description">
        يوضح الجدول التالي دقة النماذج باستخدام طرق مختلفة لاختيار الخصائص 
        في بيانات سرطان الثدي، مع إبراز تفوق الخوارزمية الجينية.
      </p>

      {/* جدول المقارنة بين الطرق المختلفة */}
      <table className="comparison-table">
        <thead>
          <tr>
            <th>الطريقة</th>
            <th>دقة النموذج</th>
          </tr>
        </thead>

        {/* تكرار الصفوف بناءً على البيانات الموجودة في المصفوفة */}
        <tbody>
          {data.map((row, index) => (
            <tr key={index}>
              {/* اسم الطريقة ولونها مميز حسب نوعها */}
              <td style={{ color: row.color, fontWeight: "bold" }}>
                {row.method}
              </td>
              {/* عرض دقة النموذج */}
              <td>{row.accuracy}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* زر للعودة إلى صفحة النتائج */}
      <button onClick={() => navigate("/results")} className="comparison-btn">
        العودة إلى النتائج
      </button>
    </div>
  );
}

export default Comparison;
