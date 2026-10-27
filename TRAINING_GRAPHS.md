# Training graphs used for the GNNs

The GNNs are trained on random subsets of a pool of 130 synthetic directed graphs (Barabási–Albert and Holme–Kim models; 100 graphs with 100–200 nodes and 30 graphs with 300–500 nodes). The pool is stored as `graphs/synth-*_train_LT.txt`.

Selection: the graph names are sorted, then drawn once with `random.Random(42).sample(names, k)` and sorted again, with `k = 8` for MONSTOR+ and `k = 15` for HISP-I and HISP-Vec (`MAX_SYNTH_GRAPHS` in `train_LT.py`). The eight graphs are contained in the fifteen.

`n` is the number of nodes and `m` the number of directed edges (non-zeros of W, reverse edges included), read from the first line of each graph file.

| Graph | Generator | Size group | n | m | Used by |
|---|---|---|---|---|---|
| synth-medium-ba-006 | Barabási–Albert | medium | 453 | 15660 | MONSTOR+, HISP-I, HISP-Vec |
| synth-medium-ba-007 | Barabási–Albert | medium | 494 | 18050 | HISP-I, HISP-Vec |
| synth-medium-ba-008 | Barabási–Albert | medium | 352 | 9464 | HISP-I, HISP-Vec |
| synth-medium-hk-007 | Holme–Kim | medium | 386 | 11054 | MONSTOR+, HISP-I, HISP-Vec |
| synth-medium-hk-008 | Holme–Kim | medium | 362 | 9666 | HISP-I, HISP-Vec |
| synth-medium-hk-011 | Holme–Kim | medium | 417 | 12736 | MONSTOR+, HISP-I, HISP-Vec |
| synth-medium-hk-013 | Holme–Kim | medium | 430 | 13948 | MONSTOR+, HISP-I, HISP-Vec |
| synth-small-ba-005 | Barabási–Albert | small | 186 | 2506 | MONSTOR+, HISP-I, HISP-Vec |
| synth-small-ba-025 | Barabási–Albert | small | 165 | 1908 | HISP-I, HISP-Vec |
| synth-small-ba-027 | Barabási–Albert | small | 183 | 2464 | MONSTOR+, HISP-I, HISP-Vec |
| synth-small-ba-029 | Barabási–Albert | small | 144 | 1390 | HISP-I, HISP-Vec |
| synth-small-ba-032 | Barabási–Albert | small | 109 | 840 | MONSTOR+, HISP-I, HISP-Vec |
| synth-small-ba-040 | Barabási–Albert | small | 116 | 896 | MONSTOR+, HISP-I, HISP-Vec |
| synth-small-hk-028 | Holme–Kim | small | 158 | 1814 | HISP-I, HISP-Vec |
| synth-small-hk-049 | Holme–Kim | small | 105 | 806 | HISP-I, HISP-Vec |

## Totals

- Fifteen graphs (HISP-I, HISP-Vec): 4060 nodes, 103202 directed edges; 9 Barabási–Albert and 6 Holme–Kim; 8 small and 7 medium.
- Eight graphs (MONSTOR+): 2280 nodes, 60104 directed edges; 5 Barabási–Albert and 3 Holme–Kim; 4 small and 4 medium.

The MONSTOR+ model was therefore trained on fewer and smaller graphs than the HISP models.
