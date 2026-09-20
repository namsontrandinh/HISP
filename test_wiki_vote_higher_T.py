"""
Test tiếp Estimator 2 (Hutchinson/vectorized) trên Wiki-Vote với T lớn hơn
(T=1000 ở lần trước sai số vẫn 84.6% -> thử T cao hơn xem có về mức
dùng được không). Không chạy lại ego-Facebook (estimator 1 đã ổn).
"""
import numpy as np, scipy.sparse as sp, urllib.request, gzip, time
rng = np.random.default_rng(0)

def download(url):
    with urllib.request.urlopen(url) as resp:
        data = resp.read()
    return gzip.decompress(data).decode()

def edgelist_to_LT_matrix(text, directed_input=True):
    edges = []
    nodes = set()
    for line in text.splitlines():
        if line.startswith('#') or not line.strip():
            continue
        a, b = map(int, line.split()[:2])
        nodes.add(a); nodes.add(b)
        edges.append((a, b))
        if not directed_input:
            edges.append((b, a))
    id_map = {v: i for i, v in enumerate(sorted(nodes))}
    n = len(id_map)
    src = [id_map[a] for a, b in edges]
    dst = [id_map[b] for a, b in edges]
    W = sp.csr_matrix((np.ones(len(edges)), (src, dst)), shape=(n, n))
    W.sum_duplicates()
    indeg = np.asarray(W.sum(axis=0)).ravel(); indeg[indeg == 0] = 1
    W = sp.csr_matrix(W.multiply(1.0 / indeg))
    W.sort_indices()
    return W, n

def hisp_vec(W, q, T, rng):
    n = W.shape[0]; acc = np.zeros((n, q-1))
    for t in range(T):
        z = rng.choice([-1.0, 1.0], size=n); y = z.copy()
        for l in range(1, q+1):
            y = W @ y
            if l >= 2: acc[:, l-2] += z * y
    return acc / T

def exact_diag(W, q):
    cur = W.copy(); diags = []
    for r in range(2, q+1):
        cur = cur @ W; diags.append(cur.diagonal())
    return np.stack(diags, axis=-1)

print("Đang tải Wiki-Vote...")
wiki_text = download("https://snap.stanford.edu/data/wiki-Vote.txt.gz")
W_wiki, n_wiki = edgelist_to_LT_matrix(wiki_text, directed_input=True)
print(f"Wiki-Vote: n={n_wiki}, m={W_wiki.nnz}, bậc TB={W_wiki.nnz/n_wiki:.1f}")

C_wiki = exact_diag(W_wiki, 11)

print("\n" + "="*70)
print("ESTIMATOR 2 (Hutchinson/vectorized) trên Wiki-Vote — T cao hơn")
print("="*70)
for T in [2000, 5000, 10000, 20000]:
    t0 = time.perf_counter()
    Ch = hisp_vec(W_wiki, 11, T, rng)
    el = time.perf_counter() - t0
    for r in [3, 5, 8]:
        true = C_wiki[:, r-2]; est = Ch[:, r-2]; mask = true > 0
        rel = np.abs(est[mask] - true[mask]) / true[mask]
        print(f"  T={T:<6d} r={r:<2d} sai số trung vị {100*np.median(rel):6.1f}%  ({el:.1f}s)")
