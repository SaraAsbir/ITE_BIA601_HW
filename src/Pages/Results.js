import React, { useMemo } from "react";
import { useNavigate } from "react-router-dom";
import "./style/Results.css";

function Results() {
  const navigate = useNavigate();

  // نجلب آخر نتائج تم حفظها
  const saved = useMemo(() => {
    try {
      return JSON.parse(localStorage.getItem("fs_results")) || null;
    } catch {
      return null;
    }
  }, []);

  const data = saved?.data || {};
  const endpoint = saved?.endpoint || "";

  // نحاول استخراج الدقة وعدد الخصائص من أي صيغة ممكنة
  const accuracy =
    data.accuracy ??
    data.model_accuracy ??
    data.best_fitness ??
    data.fitness ??
    data.fitness_score ??
    data.result_accuracy ??
    null;

  const numSelected =
    data.num_selected ??
    data.num_selected_features ??
    data.selected_features_count ??
    data.best_features ??
    data.feature_count ??
    null;

  return (
    <div className="results-container">
      <h1 className="results-title">نتائج التحليل</h1>

      {!saved ? (
        <p className="results-description">
          لا توجد نتائج محفوظة. الرجاء العودة ورفع ملف جديد.
        </p>
      ) : (
        <>
          <p className="results-description">
            آخر تشغيل:{" "}
            <strong>{new Date(saved.receivedAt).toLocaleString()}</strong> — Endpoint:{" "}
            <strong style={{ direction: "ltr" }}>{endpoint}</strong>
          </p>

          <div className="results-box">
            {numSelected != null && (
              <p>
                عدد الخصائص المختارة:{" "}
              </p>
            )}
            {accuracy != null && (
              <p>
                دقة النموذج:{" "}
                <strong style={{ color: "#be185d" }}>
                  {(accuracy * (accuracy <= 1 ? 100 : 1)).toFixed(2)}%
                </strong>
              </p>
            )}
          </div>

          {/*  الأزرار */}
          <div className="results-buttons">
            <button
              onClick={() => navigate("/comparison")}
              className="results-btn"
            >
              الانتقال إلى المقارنة
            </button>

            <button
              onClick={() => navigate("/upload")}
              className="results-btn"
            >
              رفع ملف آخر
            </button>
          </div>
        </>
      )}
    </div>
  );
}

export default Results;
