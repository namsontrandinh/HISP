"""
Sinh 130 do thi tong hop theo dung cong thuc paper GLIE (Panagopoulos
et al. 2023) de dung lam du lieu TRAIN cho GNN (theo chi dao cua co
Dung: train tren do thi tu sinh, khong can dung Extended/Celebrity/
WannaCry - nhung dataset that CHi giu lai de TEST).

Dung nguyen cong thuc GLIE:
  - 100 do thi Barabasi-Albert + Holme-Kim, 100-200 node
  - 30 do thi Barabasi-Albert + Holme-Kim, 300-500 node
  - Chuyen vo huong -> co huong bang cach them canh nguoc (dung nhu GLIE)
  - Gan xac suat theo weighted cascade: p(u,v) = 1/bac-vao(v)
    (dung cong thuc GLIE mo ta: "node u co xac suat 1/deg(u) bi
    anh huong boi tung hang xom" - tuong duong voi quy uoc da dung
    xuyen suot du an nay cho Facebook/Wiki-Vote)

XUAT RA dung dinh dang graphs/*.txt cua MONSTOR+ (0-indexed, dong dau
'n m', cac dong sau 'src dst prob') - de dung THANG duoc voi binary
fast_monte_carlo_LT_* va processing.py da co san, KHONG can sua code.

Chay tren May co it nhat vai chuc MB dia trong (130 do thi nho, nhe).
"""
import networkx as nx
import numpy as np
import os

rng_master = np.random.default_rng(42)

def make_ba_or_hk(n_nodes, seed, kind):
    """kind: 'ba' (Barabasi-Albert) hoac 'hk' (Holme-Kim).
    m (so canh moi node moi them vao) chon hop ly theo kich thuoc,
    dam bao do thi lien thong tot, khop tinh chat 'giong mang xa hoi
    that' ma GLIE de cap (phan bo bac long-tail)."""
    m = max(2, n_nodes // 25)  # ty le hop ly, khong qua thua/qua day
    if kind == 'ba':
        return nx.barabasi_albert_graph(n_nodes, m, seed=seed)
    else:  # Holme-Kim: giong BA nhung them xac suat tao tam giac (p)
        return nx.powerlaw_cluster_graph(n_nodes, m, p=0.1, seed=seed)

def to_directed_weighted_cascade(G):
    """Chuyen vo huong -> co huong (them canh nguoc, dung nhu GLIE),
    gan xac suat 1/bac-vao(v) cho moi canh (u,v) - dung cong thuc
    weighted cascade chuan (Kempe et al.), khop quy uoc da dung cho
    Facebook/Wiki-Vote truoc do trong du an nay."""
    n = G.number_of_nodes()
    nodes = sorted(G.nodes())
    id_map = {v: i for i, v in enumerate(nodes)}  # dam bao 0-indexed lien tuc

    edges = set()
    for a, b in G.edges():
        edges.add((id_map[a], id_map[b]))
        edges.add((id_map[b], id_map[a]))  # them canh nguoc

    indeg = np.zeros(n)
    for _, v in edges:
        indeg[v] += 1
    indeg[indeg == 0] = 1  # tranh chia 0 (node co lap, khong xay ra thuc te sau khi them canh nguoc)

    return sorted(edges), indeg, n

def write_graph_txt(path, edges, indeg, n):
    with open(path, 'w') as f:
        f.write(f"{n}\t{len(edges)}\n")
        for u, v in edges:
            p = 1.0 / indeg[v]
            f.write(f"{u}\t{v}\t{p:.6f}\n")

def gen_batch(n_graphs, size_range, kind, prefix, out_dir):
    sizes = rng_master.integers(size_range[0], size_range[1] + 1, size=n_graphs)
    meta = []
    for i, n_nodes in enumerate(sizes):
        seed = int(rng_master.integers(0, 1_000_000))
        G = make_ba_or_hk(int(n_nodes), seed, kind)
        edges, indeg, n = to_directed_weighted_cascade(G)
        name = f"synth_{prefix}_{kind}_{i:03d}"   # tien to 'synth_' de khong dung ten voi Extended/Celebrity/WannaCry
        write_graph_txt(f"{out_dir}/{name}_LT.txt", edges, indeg, n)
        meta.append((name, n, len(edges)))
    return meta

def main():
    out_dir = "graphs"   # DAT THANG VAO graphs/, KHONG dat thu muc rieng
    # (ly do: code C++ sinh Monte Carlo hardcode gia dinh tien to
    # "graphs/" dai dung 7 ky tu - dat thu muc rieng "graphs_synthetic/"
    # se lam sai ten thu muc output, gay Segmentation fault am tham -
    # da tu kiem chung loi nay bang binary that truoc khi sua)
    os.makedirs(out_dir, exist_ok=True)

    all_meta = []
    # Dung theo dung so lieu GLIE: 100 do thi nho (100-200 node),
    # 30 do thi lon hon (300-500 node) - moi nhom chia deu 2 loai (ba/hk)
    all_meta += gen_batch(50, (100, 200), 'ba', 'small', out_dir)
    all_meta += gen_batch(50, (100, 200), 'hk', 'small', out_dir)
    all_meta += gen_batch(15, (300, 500), 'ba', 'medium', out_dir)
    all_meta += gen_batch(15, (300, 500), 'hk', 'medium', out_dir)

    print(f"Da sinh {len(all_meta)} do thi vao thu muc '{out_dir}/'")
    print(f"{'Ten':<22}{'So node':<10}{'So canh'}")
    for name, n, m in all_meta[:5]:
        print(f"{name:<22}{n:<10}{m}")
    print("...")
    ns = [n for _, n, _ in all_meta]
    print(f"\nTong ket: {len(all_meta)} do thi, node tu {min(ns)} den {max(ns)}")
    print(f"60% train / 20% val / 20% test (theo dung ty le GLIE) neu can chia sau nay")

    # Ghi danh sach de dung lai o buoc sau (sinh Monte Carlo, chia train/val/test)
    with open(f"{out_dir}/_manifest.txt", "w") as f:
        for name, n, m in all_meta:
            f.write(f"{name}\t{n}\t{m}\n")

if __name__ == "__main__":
    main()
