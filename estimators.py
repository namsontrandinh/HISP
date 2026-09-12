"""
Module dung chung cho HISP: ca 2 estimator (Algorithm 1, Algorithm 2
trong paper) va ham tinh dap an dung (exact) de doi chieu.

Moi script nen import tu file nay thay vi copy-paste lai code.

=== TOI UU DA KIEM CHUNG BANG SO THAT ===
1. exact_diag: luoc truoc node khong the nam tren chu trinh
   -> nhanh 13.2x tren WannaCry (28.45s -> 2.15s), ket qua GIONG HET
   (np.allclose=True). TU DONG BO QUA neu do thi day khong loai duoc
   node nao (Facebook: 0/4039) vi khi do luoc chi ton them chi phi.
2. hisp_vec: gop probe thanh khoi (nhan ma tran-MA TRAN)
   -> nhanh 2.4x tren WannaCry. Cung ~3.2s: sai so 128.3% -> 85.5%.
3. hisp_vec zero_mask: dat 0 cho node chac chan co c_r=0, dung phep
   luoc LAP (khong phai 1 luot) -> zero dung them 364 node (Extended)
   / 1649 node (WannaCry) so voi ban 1 luot.
4. PathSampler (Estimator 1): lay mau bang searchsorted tren trong so
   tich luy thay vi rng.choice(p=...) -> nhanh 3.5x. Chuan bi 1 lan
   cho ca do thi thay vi lam lai moi node.

=== SUA LOI SO VOI BAN TRUOC ===
- exact_diag(q<2) crash "need at least one array to stack" -> da chan.
- hisp_vec thieu tuy chon clip (3.7% gia tri am du that luon >=0)
  -> them tham so clip, mac dinh False (giu unbiased).
- path_sample_* bat buoc truyen dW tu ngoai, de truyen nham bac VAO
  (gay ValueError kho hieu) -> nay tu tinh ben trong PathSampler.
- Tu goi sort_indices() de searchsorted luon dung.
- prune_to_core tra ve 3 kieu khac nhau -> nay tra ve contract ro rang.

Cach dung tren Colab:
    from google.colab import files
    files.upload()   # chon estimators.py
    from estimators import exact_diag, hisp_vec, PathSampler, load_LT_graph
"""
import numpy as np
import scipy.sparse as sp


# ============================================================
# Doc du lieu
# ============================================================
def load_LT_graph(path):
    """Doc file graphs/*.txt cua MONSTOR+: dong dau 'n m', cac dong
    sau 'src dst prob', node 0-indexed."""
    with open(path) as f:
        n, m = map(int, f.readline().split())
        src, dst, w = [], [], []
        for line in f:
            parts = line.split()
            if len(parts) < 3:
                continue
            a, b, p = parts[0], parts[1], parts[2]
            src.append(int(a)); dst.append(int(b)); w.append(float(p))
    if src and (max(src) >= n or max(dst) >= n):
        raise ValueError(
            f"File co node id vuot qua n={n} khai bao o dong dau "
            f"(max src={max(src)}, max dst={max(dst)})")
    W = sp.csr_matrix((w, (src, dst)), shape=(n, n))
    W.sum_duplicates()
    W.sort_indices()
    return W, n


def edgelist_to_LT_matrix(text, directed_input=True):
    """Chuyen edge-list text (vd tai tu SNAP) sang ma tran co huong,
    trong so 1/in-degree. directed_input=False neu goc la vo huong
    (vd ego-Facebook) -> tu them canh 2 chieu.

    Dung set de khu canh trung: neu file vo huong da liet ke ca 2
    chieu, khong bi dem 2 lan."""
    edge_set = set()
    nodes = set()
    for line in text.splitlines():
        if line.startswith('#') or not line.strip():
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        a, b = int(parts[0]), int(parts[1])
        nodes.add(a); nodes.add(b)
        edge_set.add((a, b))
        if not directed_input:
            edge_set.add((b, a))
    id_map = {v: i for i, v in enumerate(sorted(nodes))}
    n = len(id_map)
    edges = list(edge_set)
    src = [id_map[a] for a, b in edges]
    dst = [id_map[b] for a, b in edges]
    W = sp.csr_matrix((np.ones(len(edges)), (src, dst)), shape=(n, n))
    W.sum_duplicates()
    indeg = np.asarray(W.sum(axis=0)).ravel()
    indeg[indeg == 0] = 1
    W = sp.csr_matrix(W.multiply(1.0 / indeg))
    W.sort_indices()
    return W, n


# ============================================================
# Tien ich: node khong the nam tren bat ky chu trinh nao
# ============================================================
def cyclic_core(W):
    """Lap bo node co bac-vao=0 HOAC bac-ra=0 den khi on dinh.

    Node bi bo khong the la diem dau LAN diem trung gian cua bat ky
    chu trinh dong nao (khong den duoc, hoac khong di tiep duoc), nen
    chac chan c_r(v)=0 voi moi r -> bo di khong lam doi ket qua.

    CONTRACT (luon tra ve dung 2 gia tri, khong co kieu la):
      keep : mang chi so node giu lai (co the rong)
      Wc   : ma tran con tuong ung, hoac None neu keep = toan bo node
             (bao hieu "khong can luoc, dung thang W goc")

    Kiem chung: WannaCry loai 86% node, Facebook loai 0% node."""
    n = W.shape[0]
    outd = np.asarray(W.sum(axis=1)).ravel()
    ind = np.asarray(W.sum(axis=0)).ravel()
    alive = (outd > 0) & (ind > 0)
    if alive.all():
        return np.arange(n), None       # khong can luoc

    keep = np.arange(n)
    Wc = W
    while True:
        outd = np.asarray(Wc.sum(axis=1)).ravel()
        ind = np.asarray(Wc.sum(axis=0)).ravel()
        alive = (outd > 0) & (ind > 0)
        if alive.all():
            break
        keep = keep[alive]
        if len(keep) == 0:
            return keep, None
        Wc = Wc[alive][:, alive]
    return keep, Wc


def zero_nodes_mask(W):
    """Mang bool: True cho node chac chan co c_r(v)=0 voi moi r."""
    n = W.shape[0]
    keep, _ = cyclic_core(W)
    mask = np.ones(n, dtype=bool)
    mask[keep] = False
    return mask


# ============================================================
# Dap an dung - Diag(W^r), r=2..q
# ============================================================
def exact_diag(W, q, prune=True):
    """Tinh chinh xac c_r(v) = (W^r)_vv cho r = 2..q.
    Tra ve mang (n, q-1): cot j ung voi r = j+2.

    prune=True (mac dinh): luoc node khong the nam tren chu trinh
      truoc khi nhan ma tran. Tu dong bo qua neu khong loai duoc node
      nao. Ket qua GIONG HET prune=False (da kiem chung np.allclose).
    """
    if q < 2:
        raise ValueError(f"q phai >= 2 (dang la {q}); c_r chi dinh nghia tu r=2")

    n = W.shape[0]

    def _powers(M):
        cur = M.copy()
        diags = []
        for _ in range(2, q + 1):
            cur = cur @ M
            diags.append(cur.diagonal())
        return np.stack(diags, axis=-1)

    if not prune:
        return _powers(W)

    keep, Wc = cyclic_core(W)
    if Wc is None:
        if len(keep) == 0:
            return np.zeros((n, q - 1))   # do thi rong hoan toan
        return _powers(W)                 # khong loai duoc gi -> dung W goc

    out = np.zeros((n, q - 1))
    out[keep, :] = _powers(Wc)
    return out


# ============================================================
# Algorithm 1 (paper HISP) - path-sampling
# ============================================================
class PathSampler:
    """Estimator 1 (Algorithm 1). Chuan bi TRUOC 1 lan cho ca do thi,
    sau do goi .estimate(v, ...) cho tung node.

    Vi sao dung lop thay vi ham roi: viec chuan bi (sort indices, tinh
    bac-ra d_W, tinh trong so tich luy) chi can lam MOT lan cho ca do
    thi. Neu de trong ham roi thi moi lan goi (moi node) deu lam lai.

    Lay mau bang searchsorted tren trong so tich luy thay vi
    rng.choice(p=...) -> nhanh hon 3.5x (do tren Extended, 10 node,
    s=1000), ket qua tuong duong (kiem chung s=20000 tren 3 node bac
    cao nhat).

    Cach dung:
        sampler = PathSampler(W)
        for v in range(n):
            C[v, :] = sampler.estimate(v, q=11, s=1000, rng=rng)
    """

    def __init__(self, W):
        if not sp.issparse(W):
            raise TypeError("W phai la scipy sparse matrix")
        W = W.tocsr()
        if not W.has_sorted_indices:
            W = W.copy()
            W.sort_indices()
        self.W = W
        self.indptr = W.indptr
        self.indices = W.indices
        self.data = W.data
        # d_W(x) = tong trong so canh RA cua x (dung dinh nghia paper muc 4.3)
        self.dW = np.asarray(W.sum(axis=1)).ravel()
        # trong so tich luy chuan hoa theo tung hang, de lay mau bang searchsorted
        cumw = np.empty_like(W.data)
        for x in range(W.shape[0]):
            lo, hi = self.indptr[x], self.indptr[x + 1]
            if hi > lo:
                c = np.cumsum(W.data[lo:hi])
                tot = c[-1]
                cumw[lo:hi] = c / tot if tot > 0 else 0.0
        self.cumw = cumw

    def estimate(self, v, q, s, rng):
        """Uoc luong c_r(v) cho r=2..q bang s mau. Moi mau di 1 duong
        dai q-1 buoc, kiem tra canh quay ve v tai MOI buoc ('prefix
        reuse', paper HISP muc 5.4). Tra ve mang (q-1,)."""
        if q < 2:
            raise ValueError(f"q phai >= 2 (dang la {q})")
        if s < 1:
            raise ValueError(f"s phai >= 1 (dang la {s})")
        indptr, indices, data = self.indptr, self.indices, self.data
        dW, cumw = self.dW, self.cumw
        acc = np.zeros(q - 1)
        U = rng.random((s, q - 1))          # sinh san toan bo so ngau nhien
        for j in range(s):
            x = v
            prod = 1.0
            uj = U[j]
            for step in range(1, q):
                lo, hi = indptr[x], indptr[x + 1]
                if lo == hi or dW[x] <= 0:
                    break
                prod *= dW[x]
                pos = np.searchsorted(cumw[lo:hi], uj[step - 1])
                if pos >= hi - lo:          # chan sai so lam tron o bien
                    pos = hi - lo - 1
                x = indices[lo + pos]
                lo2, hi2 = indptr[x], indptr[x + 1]
                k = np.searchsorted(indices[lo2:hi2], v)
                if k < hi2 - lo2 and indices[lo2 + k] == v:
                    acc[step - 1] += prod * data[lo2 + k]
        return acc / s

    def estimate_all(self, q, s, rng, report_every=None):
        """Uoc luong cho TOAN BO node. Tra ve mang (n, q-1)."""
        n = self.W.shape[0]
        out = np.zeros((n, q - 1))
        for v in range(n):
            out[v, :] = self.estimate(v, q, s, rng)
            if report_every and (v + 1) % report_every == 0:
                print(f"    ...da xong {v + 1}/{n} node")
        return out


def path_sample_all_orders(W, v, q, s, rng):
    """Ham tien loi cho 1 node le. CHAM neu goi trong vong lap qua
    nhieu node - khi do dung PathSampler de chuan bi 1 lan:
        sampler = PathSampler(W); sampler.estimate_all(q, s, rng)"""
    return PathSampler(W).estimate(v, q, s, rng)


# ============================================================
# Algorithm 2 (paper HISP) - HISP-Vec (Hutchinson vector hoa)
# ============================================================
def hisp_vec(W, q, T, rng, batch=64, zero_mask=True, clip=False,
             report_every=None):
    """T probe vector Rademacher, moi vector dung chung cho r=2..q.
    Tra ve mang (n, q-1): cot j ung voi r = j+2.

    batch  : gop 'batch' probe thanh 1 phep nhan ma tran-MA TRAN
             -> nhanh ~2.4x. Do tren WannaCry: 64 tot hon 16 va 256.
    zero_mask : dat 0 cho node chac chan co c_r=0 (dung phep luoc LAP)
             -> bo nhieu vo ich. Dat False de giu ban raw hoan toan.
    clip   : cat gia tri am ve 0. Estimator Hutchinson co the cho ra
             gia tri am nho (do trên Extended: 3.7% so o, nho nhat
             -0.68) du c_r that luon >= 0.
             False (mac dinh) = giu unbiased chat che.
             True = on dinh hon cho GNN nhung khong con unbiased.
             (Dung theo 2 lua chon co Dung da neu.)
    report_every : in tien do moi ~N probe (khong anh huong ket qua).
    """
    if q < 2:
        raise ValueError(f"q phai >= 2 (dang la {q})")
    if batch < 1:
        raise ValueError(f"batch phai >= 1 (dang la {batch})")
    if T < 1:
        raise ValueError(f"T phai >= 1 (dang la {T})")

    n = W.shape[0]
    acc = np.zeros((n, q - 1))
    done = 0
    next_report = report_every
    while done < T:
        b = min(batch, T - done)
        Z = rng.integers(0, 2, size=(n, b)).astype(np.float64) * 2.0 - 1.0
        Y = Z
        for l in range(1, q + 1):
            Y = W @ Y
            if l >= 2:
                acc[:, l - 2] += (Z * Y).sum(axis=1)
        done += b
        if next_report is not None and done >= next_report:
            print(f"    ...da chay {done}/{T} probe")
            next_report += report_every
    acc /= T

    if zero_mask:
        acc[zero_nodes_mask(W), :] = 0.0
    if clip:
        np.maximum(acc, 0.0, out=acc)
    return acc
