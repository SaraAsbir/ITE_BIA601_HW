import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./style/Comparison.css";

function Comparison() {
  const [results, setResults] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const allResults = JSON.parse(localStorage.getItem("fs_all_results")) || [];

    const formatted = allResults.map((item) => {
      const data = item.data;

      // استخراج الدقة من الحقول المحتملة
      const accuracy =
        data.accuracy ??
        data.best_fitness ??
        data.fitness ??
        data.model_accuracy ??
        data.result_accuracy ??
        null;

      // استخراج عدد الخصائص من أكثر من احتمال
      let features =
        data.num_selected ??
        data.num_selected_features ??
        data.selected_features_count ??
        null;

      //  إذا كانت الخوارزمية تُرجع مصفوفة خصائص
      if (Array.isArray(data.selected_features)) {
        features = data.selected_features.length;
      }

      // تحويل اسم الخوارزمية إلى اسم قابل للقراءة
      const readableName = {
        ga: "الخوارزمية الجينية (GA)",
        ga_mi: "GA + Mutual Information",
        ga_pca: "GA + PCA",
        ga_rfe: "GA + RFE",
        ga_chi: "GA + Chi-Square",
      }[item.endpoint] || item.endpoint;

      return {
        method: readableName,
        accuracy: accuracy
          ? `${(accuracy * (accuracy <= 1 ? 100 : 1)).toFixed(2)}%`
          : "غير متاح",
        features: features ?? "غير متاح",
      };
    });

    setResults(formatted);
  }, []);

  return (
    <div className="comparison-container">
      <h1 className="comparison-title">مقارنة بين طرق اختيار الخصائص</h1>

      <p className="comparison-description">
        يعرض الجدول أدناه نتائج جميع الخوارزميات التي تم تشغيلها مسبقًا.
        يمكنك رفع ملفات جديدة لتجربة خوارزميات إضافية.
      </p>

      {results.length === 0 ? (
        <p className="error-text">لم يتم بعد تحليل أي خوارزمية.</p>
      ) : (
        <table className="comparison-table">
          <thead>
            <tr>
              <th>الطريقة</th>
              <th>عدد الخصائص المختارة</th>
              <th>دقة النموذج</th>
            </tr>
          </thead>
          <tbody>
            {results.map((row, index) => (
              <tr key={index}>
                <td style={{ fontWeight: "bold", color: "#be185d" }}>
                  {row.method}
                </td>
                <td>{row.features}</td>
                <td>{row.accuracy}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <button onClick={() => navigate("/upload")} className="comparison-btn">
        رفع ملف آخر
      </button>
    </div>
  );
}

export default Comparison;
