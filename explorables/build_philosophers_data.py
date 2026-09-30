"""Precompute the philosopher network for philosophers-backbone.qmd -> philosophers.json.

Run from this folder with the blog's venv:  python build_philosophers_data.py
"""
import collections
import json

import networkx as nx
import numpy as np
import pandas as pd
from infomap import Infomap
from networkx.algorithms.community import louvain_communities

DATA = "../posts/2026-week4-aristotle-is-the-seam/data/"
nodes = pd.read_csv(DATA + "week4_philosophers_nodes.tsv", sep="\t", comment="#", quoting=3).set_index("node_id")
edges = pd.read_csv(DATA + "week4_philosophers_edges.tsv", sep="\t", comment="#", quoting=3)

und = nx.Graph()
for r in edges.itertuples(index=False):
    if r.source != r.target:
        w = r.weight + (und[r.source][r.target]["weight"] if und.has_edge(r.source, r.target) else 0)
        und.add_edge(r.source, r.target, weight=w)
P = und.subgraph(max(nx.connected_components(und), key=len)).copy()
U = sorted(P.nodes(), key=lambda n: -P.degree(n))
idx = {n: i for i, n in enumerate(U)}


def ranked(part):
    """community label per node, 0 = biggest"""
    lab = {}
    for i, c in enumerate(sorted(part, key=len, reverse=True)):
        lab.update({n: i for n in c})
    return [lab[n] for n in U]


lou = louvain_communities(P, weight=None, seed=3)
lou_w = louvain_communities(P, weight="weight", seed=3)
im = Infomap(silent=True, seed=1, num_trials=20, two_level=True)
for u, v in P.edges():
    im.add_link(idx[u], idx[v])
im.run()
modules = collections.defaultdict(set)
for leaf in im.tree:
    if leaf.is_leaf:
        modules[leaf.module_id].add(U[leaf.node_id])

lab_lou = {n: i for i, c in enumerate(lou) for n in c}
layout_graph = P.copy()
for u, v in layout_graph.edges():
    layout_graph[u][v]["layout_w"] = 6.0 if lab_lou[u] == lab_lou[v] else 1.0
rng = np.random.default_rng(7)
centres = {i: 1.4 * np.array([np.cos(2 * np.pi * i / len(lou)), np.sin(2 * np.pi * i / len(lou))]) for i in range(len(lou))}
pos = nx.spring_layout(layout_graph, weight="layout_w", pos={n: centres[lab_lou[n]] + 0.3 * rng.standard_normal(2) for n in U},
                       seed=7, iterations=150, k=0.12)


def top_name(part_labels, k):
    members = [U[i] for i, l in enumerate(part_labels) if l == k]
    return nodes.name[max(members, key=lambda n: P.degree(n))]


L, LW, IM = ranked(lou), ranked(lou_w), ranked(list(modules.values()))
eras = ["centuries BC", "1st through 10th centuries", "11th through 14th centuries", "15th and 16th centuries",
        "17th century", "18th century", "19th century"]

alpha = {}
for u, v, w in P.edges(data="weight"):
    p = [(1 - w / P.degree(x, weight="weight")) ** (P.degree(x) - 1) for x in (u, v) if P.degree(x) > 1]
    alpha[(u, v)] = min(p) if p else 1.0

out = {
    "names": [nodes.name[n] for n in U],
    "x": [round(float(pos[n][0]), 3) for n in U],
    "y": [round(float(pos[n][1]), 3) for n in U],
    "deg": [P.degree(n) for n in U],
    "era": [eras.index(nodes.era[n]) for n in U],
    "eraNames": eras,
    "louvain": L,
    "louvainW": LW,
    "infomap": IM,
    "louvainNames": [top_name(L, k) for k in range(max(L) + 1)],
    "louvainWNames": [top_name(LW, k) for k in range(max(LW) + 1)],
    "infomapNames": [top_name(IM, k) for k in range(max(IM) + 1)],
    "edges": [[idx[u], idx[v], round(a, 5)] for (u, v), a in alpha.items()],
}
with open("philosophers.json", "w") as f:
    json.dump(out, f, separators=(",", ":"))
print(len(U), "nodes,", len(out["edges"]), "edges;", len(eras), "eras:", eras)
