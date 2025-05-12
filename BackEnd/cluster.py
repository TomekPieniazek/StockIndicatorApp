from sklearn.cluster import KMeans
import numpy as np

class ClusterManager:
    def __init__(self, n_clusters=2):
        self.n_clusters = n_clusters
        self.model = KMeans(n_clusters=self.n_clusters, random_state=42)

    def fit(self, features: np.ndarray):
        self.labels = self.model.fit_predict(features)
        return self.labels

    def get_cluster(self, idx):
        return int(self.labels[idx])
