"""
Test hội tụ 2 estimator HISP trên bộ data mới cô Dung giao:
- estimator 1 (path-sampling): ego-Facebook
- estimator 2 (Hutchinson/vectorized): Wiki-Vote
Kết quả ra bảng giống hệt format đã báo cáo trước đó (Extended_test_LT).
"""
import numpy as np, scipy.sparse as sp, urllib.request, gzip, io, time
rng = np.random.default_rng(0)

def download(url):
    with urllib.request.urlopen(url) as resp:
        data = resp.read()
    return gzip.decompress(data).decode()

def edgelist_to_LT_matrix(text, directed_input=False):
    """Đọc edge list SNAP, chuyển sang ma trận có hướng, trọng số 1/in-degree
    (đúng quy ước file _LT.txt của MONSTOR+ — weighted cascade)."""
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

def path_sample_est(W, dW, v, r, s, rng):
    indptr, indices, data = W.indptr, W.indices, W.data
    vals = np.empty(s)
    for j in range(s):
        x = v; prod = 1.0; dead = False
        for _ in range(r - 1):
            lo, hi = indptr[x], indptr[x+1]
            if lo == hi: dead = True; break
            prod *= dW[x]
            p = data[lo:hi] / dW[x]
            x = indices[lo:hi][rng.choice(hi-lo, p=p)]
        if dead: vals[j] = 0.0
        else:
            lo, hi = indptr[x], indptr[x+1]
            k = np.searchsorted(indices[lo:hi], v)
            vals[j] = prod * (data[lo+k] if k < hi-lo and indices[lo+k]==v else 0.0)
    return vals

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

print("Đang tải ego-Facebook...")
fb_text = download("https://snap.stanford.edu/data/facebook_combined.txt.gz")
W_fb, n_fb = edgelist_to_LT_matrix(fb_text, directed_input=False)
print(f"ego-Facebook: n={n_fb}, m={W_fb.nnz}, bậc TB={W_fb.nnz/n_fb:.1f}")

print("\nĐang tải Wiki-Vote...")
wiki_text = download("https://snap.stanford.edu/data/wiki-Vote.txt.gz")
W_wiki, n_wiki = edgelist_to_LT_matrix(wiki_text, directed_input=True)
print(f"Wiki-Vote: n={n_wiki}, m={W_wiki.nnz}, bậc TB={W_wiki.nnz/n_wiki:.1f}")

print("\n" + "="*70)
print("ESTIMATOR 1 (path-sampling) trên ego-Facebook")
print("="*70)
dW_fb = np.asarray(W_fb.sum(axis=1)).ravel()
C_fb = exact_diag(W_fb, 11)
cand = [v for v in np.argsort(-dW_fb) if C_fb[v, 1] > 0][:8]  # r=3 -> index 1
for r in [3, 5, 8]:
    for s in [100, 1000, 10000]:
        errs, hits = [], 0
        for v in cand:
            x = path_sample_est(W_fb, dW_fb, v, r, s, rng)
            hits += (x > 0).sum()
            true = C_fb[v, r-2]
            errs.append(abs(x.mean() - true) / true if true > 0 else np.nan)
        print(f"  r={r:<2d} s={s:<6d} sai số trung vị {100*np.nanmedian(errs):6.1f}%  tỉ lệ trúng {100*hits/(s*len(cand)):5.2f}%")

print("\n" + "="*70)
print("ESTIMATOR 2 (Hutchinson/vectorized) trên Wiki-Vote")
print("="*70)
C_wiki = exact_diag(W_wiki, 11)
for T in [50, 200, 1000]:
    t0 = time.perf_counter()
    Ch = hisp_vec(W_wiki, 11, T, rng)
    el = time.perf_counter() - t0
    for r in [3, 5, 8]:
        true = C_wiki[:, r-2]; est = Ch[:, r-2]; mask = true > 0
        rel = np.abs(est[mask] - true[mask]) / true[mask]
        print(f"  T={T:<5d} r={r:<2d} sai số trung vị {100*np.median(rel):6.1f}%  ({el:.2f}s)")
