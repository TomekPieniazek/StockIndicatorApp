import numpy as np

class PortfolioManager:
    def __init__(self, strategies, cov_matrix=None, risk_penalty=0.1):
        self.strategies = strategies
        N = len(strategies)
        self.allocation = np.ones(N) / N
        self.cov_matrix = cov_matrix
        self.risk_penalty = risk_penalty

    def evaluate(self, alloc, performances):
        port_return = np.dot(alloc, performances)
        if self.cov_matrix is None:
            risk = np.std(performances * alloc)
        else:
            risk = np.sqrt(alloc @ self.cov_matrix @ alloc)
        return port_return - self.risk_penalty * risk

    def run_ga(self, performances, generations=50, pop_size=30, elite_frac=0.2, mut_rate=0.1):
        N = len(performances)
        pop = [np.random.dirichlet(np.ones(N)) for _ in range(pop_size)]
        n_elite = int(pop_size * elite_frac)

        for _ in range(generations):
            scored = sorted(
                ((self.evaluate(ind, performances), ind) for ind in pop),
                key=lambda x: x[0], reverse=True
            )
            elites = [ind for _, ind in scored[:n_elite]]
            children = []
            while len(children) < pop_size - n_elite:
                p1, p2 = np.random.choice(elites, 2, replace=False)
                cross = np.random.rand(N)
                child = np.abs(cross*p1 + (1-cross)*p2)
                child /= child.sum()
                if np.random.rand() < mut_rate:
                    noise = np.random.normal(scale=0.05, size=N)
                    child = np.abs(child + noise)
                    child /= child.sum()
                children.append(child)
            pop = elites + children

        best = max(pop, key=lambda ind: self.evaluate(ind, performances))
        self.allocation = best
        return best
