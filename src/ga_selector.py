import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import random


ALPHA = 0.93          #زيادة القيمه لاعطاء وزن اكبر للدقة
POP_SIZE = 30         # زيادة عدد الأفراد للتنوع 
NUM_GENERATIONS = 50  # زيادة عدد الاجيال لتطوير الخوارزمية
MUTATION_RATE = 0.08  #دزيادة الطفرة 
CROSSOVER_RATE = 0.85 # زيادة التقاطع من اجل انتاج ابناء اكثر تنوع
RANDOM_STATE = 42     

np.random.seed(RANDOM_STATE)
random.seed(RANDOM_STATE)


def evaluate_fitness(chromosome, X, y):
    """تقييم لياقة الكروموسوم)."""
    
    # اختيار الكروموسوم الذي قيمته 1 
    selected_indices = [i for i, bit in enumerate(chromosome) if bit == 1]
    if len(selected_indices) == 0:
        return 0.0  # اذا لم يتم اختيار اي ميزة يعيد صفر (حل فاشل)

    # نحدد الميزات اللي اختارها الكروموسوم
    X_subset = X[:, selected_indices]

    # نوحد القيم (من اجل نموذج الانحدار اللوجستي لا يتأثر بالوحدات)
    X_scaled = StandardScaler().fit_transform(X_subset)

    # استخدمت StratifiedKFold بدل cross_val
    # من اجل الحفاظ على توازن الفئات
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)

    # استخدمت  لعطي دقة اكبر solver='lbfgs' 
    model = LogisticRegression(max_iter=2000, solver='lbfgs', random_state=RANDOM_STATE)

    
    scores = cross_val_score(model, X_scaled, y, cv=cv, scoring='accuracy')
    accuracy = np.mean(scores)

    
    feature_ratio = len(selected_indices) / len(chromosome)

    #(نوازن بين الدقة وعدد الميزات)
    fitness = ALPHA * accuracy + (1 - ALPHA) * (1 - feature_ratio)
    return fitness


def initialize_population(n_features, pop_size):
    """توليد سكان أولي بشكل منطقي أكثر."""
    population = []
    for _ in range(pop_size):
       
       
        chrom = np.random.choice([0, 1], size=n_features, p=[0.6, 0.4])

        if sum(chrom) == 0:
            chrom[np.random.randint(0, n_features)] = 1
        population.append(chrom.tolist())
    return population


def selection(population, fitnesses, k=3):
    """نظام الاختيار بالتحدي (Tournament Selection)."""
    selected = []
    for _ in range(len(population)):
        # اختيار المتسابقين الأعلى لياقة
        contenders = random.sample(range(len(population)), k)
        winner = max(contenders, key=lambda i: fitnesses[i])
        selected.append(population[winner].copy())
    return selected


def crossover(parent1, parent2, crossover_rate):
    """التبديل للتقاطع ثنائي النقطة بدل نقطة وحدة."""
    
    if random.random() > crossover_rate:
        return parent1.copy(), parent2.copy()


    p1, p2 = sorted(random.sample(range(1, len(parent1) - 1), 2))
    child1 = parent1[:p1] + parent2[p1:p2] + parent1[p2:]
    child2 = parent2[:p1] + parent1[p1:p2] + parent2[p2:]
    return child1, child2


def mutate(chromosome, mutation_rate):
    """ (نقلب بعض البتات عشوائيًا)."""
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            chromosome[i] = 1 - chromosome[i]

    if sum(chromosome) == 0:
        chromosome[random.randint(0, len(chromosome) - 1)] = 1
    return chromosome


def run_genetic_algorithm(X, y, verbose=True):
    """تشغيل الخوارزمية الجينية لاختيار الميزات."""
    n_features = X.shape[1]
    population = initialize_population(n_features, POP_SIZE)
    history = []

    for gen in range(NUM_GENERATIONS):
        # حساب اللياقة لكل كروموسوم
        fitnesses = [evaluate_fitness(ind, X, y) for ind in population]
        best_idx = np.argmax(fitnesses)
        best_fitness = fitnesses[best_idx]
        best_ind = population[best_idx]
        history.append(best_fitness)

        if verbose and (gen % 5 == 0 or gen == NUM_GENERATIONS - 1):
            print(f"الجيل {gen}: أفضل لياقة = {best_fitness:.4f} | عدد الميزات = {sum(best_ind)}")

        # اختيار الأفضل لتوليد جيل جديد
        selected = selection(population, fitnesses)
        new_population = []
        for i in range(0, len(selected), 2):
            p1, p2 = selected[i], selected[(i + 1) % len(selected)]
            c1, c2 = crossover(p1, p2, CROSSOVER_RATE)
            c1 = mutate(c1, MUTATION_RATE)
            c2 = mutate(c2, MUTATION_RATE)
            new_population.extend([c1, c2])

        # الاحتفاظ بعدد الأفراد المطلوب فقط
        population = new_population[:POP_SIZE]

    #الخرج النهائي 
    final_fitnesses = [evaluate_fitness(ind, X, y) for ind in population]
    best_idx = np.argmax(final_fitnesses)
    return population[best_idx], final_fitnesses[best_idx], history
