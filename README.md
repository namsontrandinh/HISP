# HISP: Hybrid Stochastic Structural Preprocessing for GNN-based Influence Maximization

This repository accompanies the HISP paper (SoICT 2026). It extends the MONSTOR+ code base (Ko et al., 2025). The original MONSTOR+ README is kept below.

HISP replaces the exact matrix-power structural features of MONSTOR+ with two stochastic estimators: HISP-I (importance-sampled closed walks) and HISP-Vec (vectorized Rademacher diagonal estimation).

## Files added for HISP

- `estimators.py`: exact features (`exact_diag`), HISP-I (`PathSampler`), and HISP-Vec (`hisp_vec`).
- `utils.py`: `compute_structural_features` selects the feature type through `feature_mode` (`exact`, `est1` for HISP-I, `est2` for HISP-Vec).
- `train_LT_hisp.py`: the LT training script used for the paper, with the synthetic training graphs.
- `IM.py`: influence maximization with CELF. `--feature-mode`, `--est-s` and `--est-T` select the features.
- `gen_synthetic_graphs.py` and `graphs/synth-*_train_LT.txt`: the 130 synthetic training graphs. `TRAINING_GRAPHS.md` lists the graphs used by each model.
- `table1_feature_accuracy.py` (Table 2 of the paper), `table2_preprocessing_time.py` (Table 3), `tau_d_hisp1.py` (hybrid check), `measure_IM_3models.py` (Table 4). The file names predate the paper numbering.
- `diag_val.py`: a diagnostic script that has not been run on the released data.

## Reproducing the tables

Tables 2 and 3 need `estimators.py` and the test graphs `graphs/{Extended,Celebrity,WannaCry}_test_LT.txt`. They need no GPU.

```
python table1_feature_accuracy.py      # Table 2
python table2_preprocessing_time.py    # Table 3
```

Each script performs a single run with random seed 0. The times in Table 3 were measured with `tracemalloc` enabled, so they include its overhead.

## Training data

The 130 synthetic graphs are already in `graphs/`. To regenerate the labels (1,000 Monte Carlo simulations per seed set), compile the two OpenMP programs `fast_monte_carlo_LT_random.cpp` and `fast_monte_carlo_LT_degree.cpp` (for example with `g++ -O3 -fopenmp -std=c++11 <file>.cpp -o <name>`) and run:

```
for f in graphs/synth-*_train_LT.txt; do
  name=$(basename "$f" .txt); mkdir -p "raw_data/$name"
  ./fast_monte_carlo_LT_random "$f"; ./fast_monte_carlo_LT_degree "$f"
done
for f in graphs/synth-*_train_LT.txt; do python processing.py "$(basename "$f" .txt)"; done
```

Then build the graph matrices:

```python
import glob, os
from generate_graph_pkl import generate_all
names = tuple(sorted(os.path.basename(f).replace('_train_LT.txt', '')
                     for f in glob.glob('graphs/synth-*_train_LT.txt')))
generate_all(graphs_dir='graphs', out_dir='datadir', graph_names=names, prob_names=('LT',))
```

## Training the three models

All models use the same architecture and 100 epochs. They differ in two places of `train_LT_hisp.py`: the constant `MAX_SYNTH_GRAPHS` and the arguments of `load_data(...)`.

| Model | `MAX_SYNTH_GRAPHS` | `load_data` arguments |
|---|---|---|
| MONSTOR+ | 8 | `feature_mode='exact'` |
| HISP-I | 15 | `feature_mode='est1', est_s=1000` |
| HISP-Vec | 15 | `feature_mode='est2', est_T=1000` |

```
python train_LT_hisp.py --target <name> --epochs 100
```

`--target` only names the checkpoint folder. The version of the script in this repository is configured for HISP-Vec.

## Influence maximization

```
python IM.py --checkpoint-path checkpoints/<name>_4_3_32_0.3/1.pkt --input-dim 4 \
  --hidden-dim 32 --layer-num 3 --prob LT --n-stacks 1 --gpu 0 \
  --feature-mode exact|est1|est2 [--est-s 1000] [--est-T 1000]
```

The printed seeds are pasted into `measure_IM_3models.py`, which estimates their influence with the `test_LT` program (build it from `test_LT.cpp`, see `compile.sh`).

## Notes

- In our runs the validation criterion of the training script returned identical values for every epoch, so the checkpoint of the first epoch was used for all three models. The paper treats the influence-maximization comparison as exploratory.
- MONSTOR+ was trained on 8 graphs and HISP-I and HISP-Vec on 15, because all training data are loaded into memory at once.
- This code builds on the MONSTOR+ repository. See the license of the original repository.

---

## Citation

If you use this code, please cite MONSTOR+: Ko, J., Kim, S., Lee, K., Kang, S., Hwang, D., Shin, K., Park, N.: Inductive influence estimation and maximization over unseen social networks under two diffusion models. Data Min. Knowl. Discov. 39(5), 55 (2025).

# MONSTOR+ (original README)

# Inductive Influence Estimation and Maximization over Unseen Social Networks under Two Diffusion Models
This is the source code of **MONSTOR+**, *an extended version of the inductive machine learning method, MONSTOR(Ko et al., 2020)*. The preliminary version, MONSTOR, is the first inductive method for estimating the influence of given nodes in social networks with GNN by replacing repeated MC simulations under the IC model. We present the extended version of MONSTOR, MONSTOR+, which enhances MONSTOR by incorporating auxiliary structural node features and an advanced pooling function. Both enhancements lead to improvements in accuracy. Furthermore, while MONSTOR is tailored for the IC model, MONSTOR+ is applied to both the IC and LT models.

## Dataset (Graphs)
We used three real-world social networks: Extended, WannaCry, and Celebrity under the IC model with three activation probabilities BT, JI, and LP and the LT model.
| | \|V\| | \|E\| |
|------|---|---|
|Extended|11,409|58,972|
|WannaCry|35,627|169,419|
|Celebrity|15,184|56,538|

## Requirements
To install requirements, run the following command on your terminal:
```
pip install -r requirements.txt
```

## Generating train data
We generate and preprocess the train data with repeated Monte Carlo simulation under the IC and LT models.
```
./compile.sh
./monte_carlo_[IC|LT]_[random|degree] graphs/[Extended|Celebrity|WannaCry]_[train|test]_[BT|JI|LP|LT].txt
```
```
python processing.py [Extended|Celebrity|WannaCry]_[train|test]_[BT|JI|LP|LT]
```

## Training
In training, we train the model using two of the three networks for inductive setting and tested it with the remaining one, resulting in three scenarios:

  • E+W: Training using Extended and WannaCry; and test using Celebrity,
  
  • E+C: Training using Extended and Celebrity; and test using WannaCry,
  
  • W+C: Training using WannaCry and Celebrity; and test using Extended.
  
"--target" means the masking networks. For example, if the target is 'Extended', train the model with the rest of the two networks('Celebrity' and 'WannaCry').

```
python train.py --target=[Extended|Celebrity|WannaCry] --input-dim=4 --hidden-dim=32 --gpu=0 --layer-num=3 --epochs=100
```
## Experiment
All the details are in our paper.

__IE.py__ : How accurately does MONSTOR+ estimate the influence of seed sets? (Influence Estimation) 

__IM.py__ : How accurate are simulation-based IM algorithms equipped with MONSTOR+, compared to state-of-the-art competitors? (Influence Maximization)

__submodularity.py__ : Is MONSTOR+ submoudular as the ground-truth influence function is?

__scalability.py__ : How rapidly does the estimation time grow as the size of the input graph increase?

```
python [IE|IM|submodularity].py --input-dim=4 --hidden-dim=32 --layer-num=3 --gpu=0 --checkpoint-path=[path_of_target_checkpoint] --prob=[BT|JI|LP|LT] --n-stacks=[number_of_stacks]
```
For showing the scalability, we use the local cycle counts as auxiliary node features with MATLAB (aug_feat.m).

```
python scalability.py --graph-path=graphs/scal_[20|21|22|23|24|].txt --input-dim=4 --hidden-dim=16 --gpu=0 --layer-num=3 --checkpoint-path=[path_of_target_checkpoint]
```

## The average influence of MC simulations
```
./compile.sh
./test_[IC|LT] [path_of_target_graph] [path_of_seeds]
```
