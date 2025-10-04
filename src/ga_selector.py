import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import random

ALPHA = 0.9          # وزن الدقة مقابل عدد الميزات
POP_SIZE = 20        # حجم السكان
NUM_GENERATIONS = 30 # عدد الأجيال
MUTATION_RATE = 0.05 # احتمال الطفرة
CROSSOVER_RATE = 0.8 # احتمال التقاطع
RANDOM_STATE = 42

np.random.seed(RANDOM_STATE)
random.seed(RANDOM_STATE)

def evaluate_fitness(chromosome, X, y):
    """
    chromosome: قائمة ثنائية (مثل [1,0,1,...])
    X: مصفوفة الميزات (numpy array)
    y: متجه الهدف
    """
    if sum(chromosome) == 0:
        return 0.0  # لا ميزات مختارة → غير صالح

    # اختيار الميزات المحددة
    selected_indices = [i for i, bit in enumerate(chromosome) if bit == 1]
    X_subset = X[:, selected_indices]

    # توحيد الميزات (مهم للانحدار اللوجستي)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_subset)

    # تقييم النموذج باستخدام التحقق المتصالب (3-fold)
    model = LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)
    scores = cross_val_score(model, X_scaled, y, cv=3, scoring='accuracy')
    accuracy = np.mean(scores)

    # حساب نسبة الميزات المختارة
    total_features = len(chromosome)
    selected_count = len(selected_indices)
    feature_ratio = selected_count / total_features

    # حساب اللياقة النهائية
    fitness = ALPHA * accuracy + (1 - ALPHA) * (1 - feature_ratio)
    return fitness


def initialize_population(n_features, pop_size):
    """توليد سكان أولي عشوائي"""
    return [np.random.randint(0, 2, n_features).tolist() for _ in range(pop_size)]

def selection(population, fitnesses, k=3):
    """الانتقاء التنافسي (Tournament Selection)"""
    selected = []
    for _ in range(len(population)):
        competitors = random.sample(range(len(population)), k)
        winner = max(competitors, key=lambda i: fitnesses[i])
        selected.append(population[winner].copy())
    return selected

def crossover(parent1, parent2, crossover_rate):
    """تقاطع نقطة واحدة"""
    if random.random() > crossover_rate:
        return parent1.copy(), parent2.copy()
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def mutate(chromosome, mutation_rate):
    """طفرة بت-فلب"""
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            chromosome[i] = 1 - chromosome[i]
    return chromosome

# Main function
def run_genetic_algorithm(X, y, verbose=True):
    """
    تشغيل الخوارزمية الجينية لاختيار الميزات.
    الإرجاع: أفضل كروموسوم، أفضل لياقة، سجل اللياقة عبر الأجيال
    """
    n_features = X.shape[1]
    population = initialize_population(n_features, POP_SIZE)
    history = []

    for gen in range(NUM_GENERATIONS):
        # تقييم اللياقة
        fitnesses = [evaluate_fitness(ind, X, y) for ind in population]
        best_idx = np.argmax(fitnesses)
        best_fitness = fitnesses[best_idx]
        best_ind = population[best_idx]
        num_selected = sum(best_ind)

        history.append(best_fitness)
        if verbose and (gen % 5 == 0 or gen == NUM_GENERATIONS - 1):
            print(f"الجيل {gen}: أفضل لياقة = {best_fitness:.4f}, عدد الميزات = {num_selected}")

        # الانتقاء
        selected = selection(population, fitnesses)

        # توليد جيل جديد
        new_population = []
        for i in range(0, len(selected), 2):
            p1 = selected[i]
            p2 = selected[i+1] if i+1 < len(selected) else selected[0]
            c1, c2 = crossover(p1, p2, CROSSOVER_RATE)
            c1 = mutate(c1, MUTATION_RATE)
            c2 = mutate(c2, MUTATION_RATE)
            new_population.extend([c1, c2])

        population = new_population[:POP_SIZE]

    # تقييم نهائي
    final_fitnesses = [evaluate_fitness(ind, X, y) for ind in population]
    best_idx = np.argmax(final_fitnesses)
    return population[best_idx], final_fitnesses[best_idx], history