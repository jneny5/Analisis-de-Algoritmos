import pandas as pd # type: ignore 
import umap #type: ignore
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans # type: ignore
import mplcursors # type: ignore
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

df = pd.read_csv('fashion-mnist_train.csv')

X = df.drop('label', axis=1)
y = df['label']              

label_names = {
    0: 'Camiseta', 1: 'Pantalon', 2: 'Sueter', 3: 'Vestido', 4: 'Abrigo',
    5: 'Sandalia', 6: 'Camisa', 7: 'Tenis', 8: 'Bolsa', 9: 'Botin'
}

reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, n_components=2, random_state=42)
embedding = reducer.fit_transform(X)

plt.figure(figsize=(9, 7))
scatter = plt.scatter(embedding[:, 0], embedding[:, 1], c=y, cmap='Spectral', s=5)
plt.title('Mapa de Ropa Fashion-MNIST con UMAP', fontsize=18)
plt.xlabel('Dimension UMAP 1')
plt.ylabel('Dimension UMAP 2')

plt.legend(handles=scatter.legend_elements()[0], labels=label_names.values())
plt.show()

id_cluster = 7
nombre_cluster = label_names[id_cluster]
print(f"Vamos a investigar el cluster de: {nombre_cluster}")

X_cluster = X[y == id_cluster]
y_cluster = y[y == id_cluster]

print(f"Encontramos {len(X_cluster)} imágenes de {nombre_cluster}.")

reducer_cluster = umap.UMAP(n_neighbors=10, min_dist=0.05, n_components=2, random_state=42)
embedding_cluster = reducer_cluster.fit_transform(X_cluster)

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
sub_labels = kmeans.fit_predict(embedding_cluster)

fig, ax = plt.subplots(figsize=(9, 7))
plt.scatter(embedding_cluster[:, 0], embedding_cluster[:, 1], s=10)
scatter_sub = ax.scatter(embedding_cluster[:, 0], embedding_cluster[:, 1], c=sub_labels, cmap='viridis', s=15)
ax.set_title(f'Sub-clusters en {nombre_cluster}',fontsize=16)
ax.legend(handles=scatter_sub.legend_elements()[0], labels=['Tenis deportivas', 'Tenis high tops', 'Tenis Casuales'])

imagenes = X_cluster.to_numpy().reshape(-1, 28, 28)

def hover_event(sel):
    idx = sel.index
    
    ab = AnnotationBbox(
        OffsetImage(imagenes[idx], cmap='gray', zoom=3), 
        sel.target,
        frameon=True,
        box_alignment=(0.5, -0.1), 
        pad=0.3
    )
    ax.add_artist(ab)
    sel.extras.append(ab)
mplcursors.cursor(scatter_sub, hover=True).connect(
    "add", hover_event
)

plt.show()