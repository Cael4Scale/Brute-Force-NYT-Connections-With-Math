import numpy as np

def init_world(r, b, seed=42):
    np.random.seed(seed)

    N = r + b

    true_colors = np.array([1]*r + [0]*b)

    np.random.shuffle(true_colors)

    red_indices = np.where(true_colors == 1)[0]
    blue_indices = np.where(true_colors == 0)[0]

    return true_colors, red_indices, blue_indices


def init_particles(r, b, K, seed = 42):
    np.random.seed(seed)

    N = r + b
    particles = np.zeros((K, N), dtype=int)

    base = np.array([1]*r + [0]*b)

    for k in range(K):
        arr = base.copy()
        np.random.shuffle(arr)
        particles[k] = arr

    return particles



def compute_pij(particles):
    return np.mean(
        particles[:, :, None] == particles[:, None, :],
        axis=0
    )


def uncertainty(pij):
    return np.sum(pij * (1 - pij))



def observe(indices, true_colors):
    sub = true_colors[indices]

    k = np.sum(sub)          
    n = len(indices)

    m = max(k, n - k)            
    minority = n - m               

    return m, minority



def update_particles(indices, m, particles):
    sub = particles[:, indices]            
    k = np.sum(sub, axis=1)                 
    n = len(indices)

    mask = (np.maximum(k, n - k) == m)

    if np.sum(mask) == 0:
        raise ValueError("All particles eliminated")
    new_particles = particles[mask]

    # resample to keep K constant
    K = particles.shape[0]
    idx = np.random.choice(len(new_particles), size=K, replace=True)

    return new_particles[idx]


def possible_m_values(n):


    return list(range((n + 1) // 2, n + 1))


def probability_of_m(indices, m, particles):
    sub = particles[:, indices]         
    k = np.sum(sub, axis=1)              
    n = len(indices)

    matches = (np.maximum(k, n - k) == m)

    return np.mean(matches)  


def simulate_update(indices, m, particles):
    sub = particles[:, indices]
    k = np.sum(sub, axis=1)
    n = len(indices)

    mask = (np.maximum(k, n - k) == m)

    if np.sum(mask) == 0:
        return None

    new_particles = particles[mask]

    K = particles.shape[0]
    idx = np.random.choice(len(new_particles), size=K, replace=True)

    return new_particles[idx]


def expected_uncertainty(indices, particles):
    exp_unc = 0.0
    total_weight = 0.0

    for m in possible_m_values(len(indices)):

        p_m = probability_of_m(indices, m, particles)
        if p_m == 0:
            continue

        new_particles = simulate_update(indices, m, particles)
        if new_particles is None:
            continue

        pij_new = compute_pij(new_particles)
        unc = uncertainty(pij_new)

        exp_unc += p_m * unc
        total_weight += p_m

    if total_weight == 0:
        return np.inf

    return exp_unc / total_weight


def find_best_subset(particles, subset_size, num_candidates=50):
    N = particles.shape[1]

    best_subset = None
    best_score = np.inf

    for _ in range(num_candidates):
        indices = np.random.choice(N, subset_size, replace=False)

        score = expected_uncertainty(indices, particles)

        if score < best_score:
            best_score = score
            best_subset = indices

    return best_subset


def is_converged(pij, threshold=0.95):
    N = pij.shape[0]

    for i in range(N):
        for j in range(i+1, N):
            if threshold > pij[i, j] > (1 - threshold):
                return False

    return True


def extract_solution(pij):
    N = pij.shape[0]

    solution = np.zeros(N, dtype=int)

    for i in range(N):
        if pij[0, i] >= 0.5:
            solution[i] = 1
        else:
            solution[i] = 0

    return solution


def run_experiment(r, b, K=3000, subset_size=4, max_iter=50, seed=42):

    true_colors, _, _ = init_world(r, b, seed)
    particles = init_particles(r, b, K, seed)

    pij = compute_pij(particles)
    Ss = {}
    ms= {}
    for t in range(max_iter):
    
        if t == 0:
            S = np.arange(subset_size)
        else:
            S = find_best_subset(particles, subset_size)
    
        m, _ = observe(S, true_colors)
    
        particles = update_particles(S, m, particles)
        pij = compute_pij(particles)
    
        guess = extract_solution(pij)
    
        #check if THIS move already gives pure subset ---
        if is_pure_subset(S, true_colors):
            return guess, pij, t+1
    
        #check if we now KNOW everything
        if is_converged(pij):
            # next move will be pure for sure
            return guess, pij, t+2
        


    # --- final ---
    # print("\nFINAL RESULT")
    # print("Step:", t+1)
    # print("Final Guess:", guess)
    # print("True Colors:", true_colors)

    return guess, pij, t+2
def is_pure_subset(indices, true_colors):
    sub = true_colors[indices]
    return (np.sum(sub) == 0) or (np.sum(sub) == len(indices))
# h,u, t=run_experiment(r=4, b=4, K=3000, subset_size=4, max_iter=50, seed=5)

import numpy as np
import matplotlib.pyplot as plt

def run_multiple_experiments(num_runs, r, b, K=3000, subset_size=4, max_iter=50):
    steps_list = []
    i = 0 
    i_s = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0}
    p_s = {1:1/6, 2:1/6, 3:1/6, 4:1/6, 5:1/6, 6:1/6, 7:0, 8:0}
    for seed in range(num_runs):
        i = i+1 

        _, _, steps = run_experiment(
            r=r,
            b=b,
            K=K,
            subset_size=subset_size,
            max_iter=max_iter,
            seed=seed
        )
        i_s[steps] = i_s[steps] + 1
        for x, v in p_s.items():
            p_s[x] = round(i_s[x]/i,2)
        print(p_s)
        
        
        steps_list.append(steps)

    return np.array(steps_list)

steps = run_multiple_experiments(num_runs=10000, r=4, b=4, K=10000, subset_size=4, max_iter=50)
