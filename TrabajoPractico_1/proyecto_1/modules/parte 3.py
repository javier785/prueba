import os
from collections import deque

# -----------------------------
# 1. Estructura Union-Find (para Kruskal)
# -----------------------------

class UnionFind:
    """Estructura disjoint-set para el algoritmo de Kruskal."""
    def _init_(self):
        self.parent = {}
        self.rank = {}

    def make_set(self, x):
        self.parent[x] = x
        self.rank[x] = 0

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        else:
            self.parent[ry] = rx
            if self.rank[rx] == self.rank[ry]:
                self.rank[rx] += 1
        return True


# -----------------------------
# 2. Leer archivo aldeas.txt
# -----------------------------

archivo = "aldeas.txt"
if not os.path.exists(archivo):
    raise FileNotFoundError("No se encontró el archivo 'aldeas.txt' en el directorio actual.")

edges = []
with open(archivo, "r", encoding="utf-8") as f:
    for i, linea in enumerate(f):
        linea = linea.strip()
        if not linea:
            continue
        partes = [p.strip() for p in linea.split(",")]
        if len(partes) == 3:
            a, b, w = partes
            try:
                w = int(w)
            except ValueError:
                raise ValueError(f"Error en línea {i+1}: peso no válido → {linea}")
            edges.append((a, b, w))
        elif len(partes) == 1:
            # línea suelta tipo "Diosleguarde" → ignorar
            continue
        else:
            raise ValueError(f"Formato inesperado en línea {i+1}: {linea}")

# Lista de aldeas únicas
nodes = sorted({n for e in edges for n in e[:2]}, key=lambda s: s.lower())

# -----------------------------
# 3. Algoritmo de Kruskal (MST)
# -----------------------------

uf = UnionFind()
for n in nodes:
    uf.make_set(n)

mst_edges = []
for u, v, w in sorted(edges, key=lambda x: x[2]):
    if uf.union(u, v):
        mst_edges.append((u, v, w))

# -----------------------------
# 4. Construir grafo MST y orientar desde 'Peligros'
# -----------------------------

adj = {n: [] for n in nodes}
for u, v, w in mst_edges:
    adj[u].append((v, w))
    adj[v].append((u, w))

root = "Peligros"
if root not in adj:
    raise ValueError(f"No se encontró la aldea raíz '{root}' en el archivo.")

parent = {root: None}
children = {n: [] for n in nodes}
edge_weight_to_parent = {}

cola = deque([root])
visitados = {root}

while cola:
    actual = cola.popleft()
    for vecino, w in adj[actual]:
        if vecino not in visitados:
            visitados.add(vecino)
            parent[vecino] = actual
            children[actual].append(vecino)
            edge_weight_to_parent[vecino] = w
            cola.append(vecino)

# -----------------------------
# 5. Calcular distancias totales
# -----------------------------

outgoing_sum = {n: sum(edge_weight_to_parent[ch] for ch in children[n]) for n in nodes}
total_distance = sum(w for _, _, w in mst_edges)

# -----------------------------
# 6. Mostrar resultados
# -----------------------------

print("\n=== LISTA ALFABÉTICA DE ALDEAS ===")
for n in nodes:
    print(n)

print("\n=== RUTAS DE COMUNICACIÓN (desde 'Peligros') ===")
print(f"{'Aldea':20s} | {'Recibe de':15s} | {'Envía a':40s}")
print("-" * 80)
for n in nodes:
    recibe = parent[n] if parent[n] else "-"
    envia = ", ".join(children[n]) if children[n] else "-"
    print(f"{n:20s} | {recibe:15s} | {envia:40s}")

print(f"\n=== DISTANCIA TOTAL RECORRIDA ===")
print(f"Suma total de todas las distancias: {total_distance} leguas\n")

# -----------------------------
# 7. (Opcional) Visualización del MST
# -----------------------------
try:
    import networkx as nx
    import matplotlib.pyplot as plt

    G = nx.Graph()
    G.add_nodes_from(nodes)
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)

    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(8, 8))
    nx.draw_networkx_nodes(G, pos, node_size=300)
    nx.draw_networkx_labels(G, pos, font_size=8)
    nx.draw_networkx_edges(G, pos, edgelist=edges, alpha=0.2)
    nx.draw_networkx_edges(G, pos, edgelist=[(u, v) for u, v, _ in mst_edges], width=2.2, edge_color='blue')
    plt.title("Árbol de expansión mínima (MST) desde Peligros")
    plt.axis("off")
    plt.tight_layout()
    plt.show()

except ImportError:
    print("No se generó la visualización porque falta el paquete 'networkx'.")