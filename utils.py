import numpy as np
import pickle as pkl
import gzip

import torch
import dgl
import networkx as nx
import copy, tqdm
import time

from scipy.sparse.linalg import eigs
import scipy
import cupy as cp
import cupyx.scipy.sparse.linalg as cupy
from scipy.sparse import coo_matrix
import cupyx.scipy.sparse
from cupy.cuda import cublas, cusparse
import gc

from estimators import exact_diag, PathSampler, hisp_vec


def compute_structural_features(W, q, mode, s=1000, T=1000, rng=None):
    """DIEM WIRE-UP giua MONSTOR+ va HISP (Strategy Pattern).

    Chon 1 trong 3 cach tinh c_r(v), r=2..q. Ca 3 deu tra ve mang
    (n, q-1) CUNG mot dinh dang (cot j ung voi r=j+2) - vi vay hoan
    doi cho nhau ma khong can sua gi o cho goi ham.

    mode: 'exact' (MONSTOR+ goc, tinh dung, cham) | 'est1' (HISP
          Algorithm 1, path-sampling) | 'est2' (HISP Algorithm 2,
          HISP-Vec).
    s, T: so mau/probe cho est1/est2 - khong dung neu mode='exact'.
    """
    if rng is None:
        rng = np.random.default_rng(0)
    if mode == "exact":
        return exact_diag(W, q)
    elif mode == "est1":
        return PathSampler(W).estimate_all(q, s, rng)
    elif mode == "est2":
        return hisp_vec(W, q, T, rng)
    else:
        raise ValueError(
            f"feature_mode khong hop le: '{mode}' - phai la "
            f"'exact', 'est1', hoac 'est2'")


def _load_data_inner(train, val, test):
    base_path = './datadir'
    targets = {'train': train, 'val': val, 'test': test}
    objs = {'train': [], 'val': [], 'test': []}

    for mark in ('train', 'val', 'test'):
        for name in targets[mark]:
            print('Load data for {}: {}'.format(mark, name))  # Load data for train : ('Extended','train','BT')
            objects = []
            with gzip.open('{}/{}_{}_{}_graph.pkl.gz'.format(base_path, name[0], name[1], name[2]), 'rb') as f:
                objects.append(pkl.load(f))
            labels = ['X', 'y', 'sX', 'sy'] if (mark == 'train') else ['sX', 'sy']
            for label in labels:
                with gzip.open('{}/{}_{}_{}_{}_random.pkl.gz'.format(base_path, name[0], name[1], name[2], label),
                               'rb') as f:
                    seeds_random = pkl.load(f)
                with gzip.open('{}/{}_{}_{}_{}_degree.pkl.gz'.format(base_path, name[0], name[1], name[2], label),
                               'rb') as f:
                    seeds_degree = pkl.load(f)
                print(seeds_random.shape, seeds_degree.shape)
                objects.append(np.concatenate((seeds_random, seeds_degree), axis=0))
            objs[mark].append(tuple(objects))
    return objs['train'], objs['val'], objs['test']


def load_data(train_labels, val_labels, test_labels, k=None,
              feature_mode='exact', est_s=1000, est_T=1000, feature_seed=0):
    rng = np.random.default_rng(feature_seed)
    g, sX, sy, X, y = {}, {}, {}, {}, {}
    _g, _sX, _sy = {}, {}, {}
    g1, _g1 = {}, {}

    train_data, val_data, test_data = _load_data_inner(train=train_labels, val=val_labels, test=test_labels)

    for label, data in zip(train_labels, train_data):
        lstr = '_'.join(label)
        print('train: load {}...'.format(lstr))  # train: load Extended_train_BT...

        g[lstr] = dgl.from_scipy(data[0])
        g1[lstr] = g[lstr].to(torch.device('cuda'))

        ## Creates a new graph from an adjacency matrix given as a SciPy sparse matrix.

        rr = compute_structural_features(
            data[0], q=11, mode=feature_mode, s=est_s, T=est_T, rng=rng)
        g1[lstr].ndata['idfeat'] = torch.from_numpy(np.float32(rr)).cuda()
        g1[lstr].edata['weight'] = torch.from_numpy(np.float32(data[0].data)).cuda()

        X[lstr] = torch.FloatTensor(data[1])
        y[lstr] = torch.FloatTensor(data[2])
        sX[lstr] = torch.FloatTensor(data[3])
        sy[lstr] = torch.FloatTensor(data[4])

    for label, data in zip(val_labels, val_data):
        lstr = '_'.join(label)
        print('val: load {}...'.format(lstr))

        _g[lstr] = dgl.from_scipy(data[0])
        _g1[lstr] = _g[lstr].to(torch.device('cuda:0'))

        rr = compute_structural_features(
            data[0], q=11, mode=feature_mode, s=est_s, T=est_T, rng=rng)
        _g1[lstr].ndata['idfeat'] = torch.from_numpy(np.float32(rr)).cuda()
        _g1[lstr].edata['weight'] = torch.from_numpy(np.float32(data[0].data)).cuda()

        _sX[lstr] = torch.FloatTensor(data[1])
        _sy[lstr] = torch.FloatTensor(data[2])

    for label, data in zip(test_labels, test_data):
        lstr = '_'.join(label)
        print('test: load {}...'.format(lstr))

        _g[lstr] = dgl.from_scipy(data[0])
        _g1[lstr] = _g[lstr].to(torch.device('cuda:0'))

        rr = compute_structural_features(
            data[0], q=11, mode=feature_mode, s=est_s, T=est_T, rng=rng)
        _g1[lstr].ndata['idfeat'] = torch.from_numpy(np.float32(rr)).cuda()
        _g1[lstr].edata['weight'] = torch.from_numpy(np.float32(data[0].data)).cuda()

        _sX[lstr] = torch.FloatTensor(data[1])
        _sy[lstr] = torch.FloatTensor(data[2])

    return g1, sX, sy, X, y, _g1, _sX, _sy