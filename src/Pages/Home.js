import React from "react";
import { Link } from "react-router-dom";
import "./style/Home.css"; 

function Home() {
  return (
    <div className="home-container">
      <h1 className="home-title">مشروع اكتشاف سرطان الثدي</h1>

      {/* وصف قصير عن فكرة المشروع */}
      <p className="home-description">
        يهدف هذا المشروع إلى استخدام الخوارزميات الجينية لاختيار الخصائص الطبية
        الاكثر تاثيرًا في تشخيص سرطان الثدي بدقة عالية
      </p>

      <p className="home-DR">بإشراف الدكتور: عصام سلمان</p>

      {/* جدول يعرض أسماء وأرقام الطلاب المشاركين في المشروع */}
      <table className="home-table">
        <thead>
          <tr>
            <th>الاسم</th>
            <th>الرقم الجامعي</th>
            <th>الصف</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Dania</td>
            <td>190242</td>
            <td>C4</td>
          </tr>
          <tr>
            <td>Tuka</td>
            <td>189749</td>
            <td>C4</td>
          </tr>
          <tr>
            <td>Lilia</td>
            <td>195438</td>
            <td>C6</td>
          </tr>
          <tr>
            <td>Ghazal</td>
            <td>209514</td>
            <td>C4</td>
          </tr>
          <tr>
            <td>Raja</td>
            <td>162658</td>
            <td>C3</td>
          </tr>
          <tr>
            <td>Sara</td>
            <td>152385</td>
            <td>C3</td>
          </tr>
          <tr>
            <td>Salam</td>
            <td>158996</td>
            <td>C4</td>
          </tr>
          <tr>
            <td>Shaam</td>
            <td>129908</td>
            <td>C5</td>
          </tr>
        </tbody>
      </table>

      {/* زر للتنقل إلى صفحة رفع البيانات */}
      <Link to="/upload">
        <button className="start-button">ابدأ الآن</button>
      </Link>
    </div>
  );
}

export default Home;
