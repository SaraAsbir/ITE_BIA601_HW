import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import random


ALPHA = 0.93          # Higher weight for accuracy
POP_SIZE = 30         # Larger population for diversity
NUM_GENERATIONS = 50  # More generations for better evolution
MUTATION_RATE = 0.08  # Slightly higher mutation rate
CROSSOVER_RATE = 0.85 # High crossover rate for diverse offspring
RANDOM_STATE = 42     

np.random.seed(RANDOM_STATE)
random.seed(RANDOM_STATE)


def evaluate_fitness(chromosome, X, y):
    """Evaluate the fitness of a chromosome."""
    
    # Select features where chromosome bit is 1
    selected_indices = [i for i, bit in enumerate(chromosome) if bit == 1]
    if len(selected_indices) == 0:
        return 0.0  # Invalid solution: no features selected

    # Extract selected features
    X_subset = X[:, selected_indices]

    # Standardize features (important for Logistic Regression)
    X_scaled = StandardScaler().fit_transform(X_subset)

    # Use StratifiedKFold to maintain class balance
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)

    # Use 'lbfgs' solver for better stability
    model = LogisticRegression(max_iter=2000, solver='lbfgs', random_state=RANDOM_STATE)

    # Evaluate using cross-validation
    scores = cross_val_score(model, X_scaled, y, cv=cv, scoring='accuracy')
    accuracy = np.mean(scores)

    # Compute feature ratio (selected / total)
    feature_ratio = len(selected_indices) / len(chromosome)

    # Balance accuracy and feature count
    fitness = ALPHA * accuracy + (1 - ALPHA) * (1 - feature_ratio)
    return fitness


def initialize_population(n_features, pop_size):
    """Generate an initial population with bias toward fewer features."""
    population = []
    for _ in range(pop_size):
        # Generate chromosome with 40% chance of selecting a feature
        chrom = np.random.choice([0, 1], size=n_features, p=[0.6, 0.4])

        # Ensure at least one feature is selected
        if sum(chrom) == 0:
            chrom[np.random.randint(0, n_features)] = 1
        population.append(chrom.tolist())
    return population


def selection(population, fitnesses, k=3):
    """Tournament selection: choose the best individual among k random candidates."""
    selected = []
    for _ in range(len(population)):
        contenders = random.sample(range(len(population)), k)
        winner = max(contenders, key=lambda i: fitnesses[i])
        selected.append(population[winner].copy())
    return selected


def crossover(parent1, parent2, crossover_rate):
    """Two-point crossover for better diversity."""
    if random.random() > crossover_rate:
        return parent1.copy(), parent2.copy()

    # Select two random crossover points
    p1, p2 = sorted(random.sample(range(1, len(parent1) - 1), 2))
    child1 = parent1[:p1] + parent2[p1:p2] + parent1[p2:]
    child2 = parent2[:p1] + parent1[p1:p2] + parent2[p2:]
    return child1, child2


def mutate(chromosome, mutation_rate):
    """Flip bits randomly with a given mutation rate."""
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            chromosome[i] = 1 - chromosome[i]

    # Ensure at least one feature remains selected
    if sum(chromosome) == 0:
        chromosome[random.randint(0, len(chromosome) - 1)] = 1
    return chromosome


def run_genetic_algorithm(X, y, verbose=True):
    """Run the genetic algorithm for feature selection."""
    n_features = X.shape[1]
    population = initialize_population(n_features, POP_SIZE)
    history = []

    for gen in range(NUM_GENERATIONS):
        # Evaluate fitness for all individuals
        fitnesses = [evaluate_fitness(ind, X, y) for ind in population]
        best_idx = np.argmax(fitnesses)
        best_fitness = fitnesses[best_idx]
        best_ind = population[best_idx]
        history.append(best_fitness)

        if verbose and (gen % 5 == 0 or gen == NUM_GENERATIONS - 1):
            print(f"Generation {gen}: Best fitness = {best_fitness:.4f} | Features = {sum(best_ind)}")

        # Selection
        selected = selection(population, fitnesses)
        new_population = []
        for i in range(0, len(selected), 2):
            p1 = selected[i]
            p2 = selected[(i + 1) % len(selected)]
            c1, c2 = crossover(p1, p2, CROSSOVER_RATE)
            c1 = mutate(c1, MUTATION_RATE)
            c2 = mutate(c2, MUTATION_RATE)
            new_population.extend([c1, c2])

        # Maintain fixed population size
        population = new_population[:POP_SIZE]

    # Final evaluation
    final_fitnesses = [evaluate_fitness(ind, X, y) for ind in population]
    best_idx = np.argmax(final_fitnesses)
    return population[best_idx], final_fitnesses[best_idx], history