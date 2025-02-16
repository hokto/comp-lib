# EulerTour
根つき木のクエリ処理に対して有効なアルゴリズム．
頂点数 $n$の根付き木 $T$に対して，
- 2頂点のLCA
- 2頂点間のパスクエリ(ex. パスの長さ)
- 2頂点間の頂点クエリ(ex. パスの頂点重みの合計)
が1クエリに対して $O(\log n)$で求められる．

## コンストラクタ
```python
et = EulerTour(n:int, T:list[list[tuple[int,int]]])
et = EulerTour(n:int, T:list[list[tuple[int,int]]],weight: list[int])
```
- `n`が頂点数
- `T`が木の構造．`T[i]`に`i`と接続する辺が含まれていて，その情報は`(j,cost)`のように`(頂点,辺のコスト)`として表現する必要がある．
- `weight`は頂点重みを表現しており，渡さなくても使える．渡さない場合は，全ての頂点重みを1として扱う．

## build
```python
et.build(n:int, T:list[list[tuple[int,int]]]) -> None
```
EulerTourを構築する．`et`の作成時にコンストラクタで呼び出される．

## lca
```python
et.lca(x:int,y:int) -> int
```
`et`に含まれる2つの頂点`x,y`のLCAを返す．

## path_query
```python
et.path_query(x:int,y:int) -> int
```
`et`に含まれる頂点`x,y`の間のパスに対するクエリの結果を返す．現段階では，辺重みのみ計算可能．

## node_query
```python
et.node_query(x:int,y:int) -> int
```
`et`に含まれる頂点`x,y`の間のパスに含まれる頂点に対するクエリの結果を返す．現段階では，パスに含まれる頂点重みの和のみ計算可能．

## subtree_query_of_edge
```python
et.subtree_query_of_edge(x:int) -> int
```
`et`に含まれる頂点`x`を根とする部分木の辺に対してのクエリ結果を返す．

## subtree_query_of_vertex
```python
et.subtree_query_of_vertex(x:int) -> int
```
`et`に含まれる頂点`x`を根とする部分木の頂点に対してのクエリ結果を返す．

## add_edge_cost
```python
et.add_edge_cost(u:int,v:int,cost:int) -> None
```
`et`に含まれる辺`(u,v)`の辺コストを`cost`だけ増やす．

## update_edge_cost
```python
et.update_edge_cost(u:int,v:int,new_cost:int) -> None
```
`et`に含まれる辺`(u,v)`の辺コストを`new_cost`に更新する．

## add_vertex_weight
```python
et.add_vertex_weight(x:int,weight:int) -> None
```
`et`に含まれる頂点`x`の頂点重みを`weight`だけ増やす．

## update_vertex_weight
```python
et.update_vertex_weight(x:int,new_weight:int) -> None
```
`et`に含まれる頂点`x`の頂点重みを`new_weight`に更新する．

# TODO
- `subtree_query_*`のverify
- `node_query/path_query`がモノイドを載せられるように修正
    - `fenwick tree`を使っているため，`segtree`に変更 