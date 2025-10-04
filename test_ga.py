import pandas as pd
from src.ga_selector import run_genetic_algorithm

# 1. تحميل البيانات
print("تحميل البيانات...")
df = pd.read_csv("data/sample_data.csv")
X = df.drop(columns=["target"]).values  # جميع الأعمدة عدا 'target'
y = df["target"].values                 # عمود الهدف

print(f"شكل البيانات: {X.shape[0]} عينة، {X.shape[1]} ميزة")

# 2. تشغيل الخوارزمية الجينية
print("\nتشغيل الخوارزمية الجينية...")
best_chromosome, best_fitness, history = run_genetic_algorithm(X, y, verbose=True)

# 3. عرض النتائج
selected_features = [i for i, bit in enumerate(best_chromosome) if bit == 1]
num_selected = len(selected_features)
total_features = X.shape[1]

print("\n" + "="*50)
print("أفضل حل :")
print(f"- عدد الميزات المختارة: {num_selected} / {total_features}")
print(f"- درجة اللياقة: {best_fitness:.4f}")
print(f"- مؤشرات الميزات المختارة (أول 10): {selected_features[:10]}")
if num_selected > 10:
    print(f"  ... (و{num_selected - 10} ميزات أخرى)")
print("="*50)