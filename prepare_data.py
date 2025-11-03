import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.datasets import load_iris   # أضفنا هذا الاستيراد الجديد
import numpy as np

# 1. تحميل مجموعة بيانات سرطان الثدي
data = load_breast_cancer()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = pd.Series(data.target, name='target')  # 0 = malignant, 1 = benign

print(f"- Samples Count: {X.shape[0]}")
print(f"- Total Features Before: {X.shape[1]}")

# 2. إنشاء ميزات اصطناعية لزيادة العدد (لجعلها >50)
# سنضيف 40 ميزة عشوائية غير مفيدة (لتمثيل "الضجيج")
np.random.seed(42)
num_noise_features = 40
noise_features = np.random.randn(X.shape[0], num_noise_features)
noise_names = [f"noise_feature_{i}" for i in range(num_noise_features)]

X_noise = pd.DataFrame(noise_features, columns=noise_names)

# دمج الميزات الحقيقية + الضجيج
X_extended = pd.concat([X, X_noise], axis=1)

print(f"- Total Features After: {X_extended.shape[1]}")

# 3. دمج X و y في ملف واحد
df_final = pd.concat([X_extended, y], axis=1)

# 4. حفظ الملف
df_final.to_csv("data/sample_data.csv", index=False)



#اضافة بيانات من iris لاختبار الكود على مجموعة ثانية (زهور ) 
iris = load_iris()
X_iris = pd.DataFrame(iris.data, columns=iris.feature_names)
y_iris = pd.Series(iris.target, name='target')

# اضافة ميزات عشوائية للتنوع
noise_features_iris = np.random.randn(X_iris.shape[0], 10)
noise_names_iris = [f"noise_feature_{i}" for i in range(10)]
X_iris_noise = pd.DataFrame(noise_features_iris, columns=noise_names_iris)
X_iris_extended = pd.concat([X_iris, X_iris_noise], axis=1)

df_iris_final = pd.concat([X_iris_extended, y_iris], axis=1)
df_iris_final.to_csv("data/sample_data_iris.csv", index=False)  # حفظ باسم جديد

print(f"\nتم إنشاء ملف جديد: data/sample_data_iris.csv")
print(f"- عدد العينات: {X_iris.shape[0]}")
print(f"- عدد الميزات بعد الإضافة: {X_iris_extended.shape[1]}")