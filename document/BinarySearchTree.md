# Binary Search Tree
管理するデータ群に対して，

- 追加
- 削除
- 探索

といった操作をデータ数$n$に対して$O(\log n)$で行う．

## コンストラクタ
```python
bst = BinarySearchTree(max_e:Any,min_e:Any,init_tree:list[Any])
```
- $\max$演算の単位元を`max_e`(デフォルトは`max_e=-10**10`)
- $\min$演算の単位元を`min_e`(デフォルトは`min_e=10**10`)
- `init_tree`に追加したい要素を入れておけば，生成時に追加した状態で扱える

## insert
```python
bst.insert(z: Any) -> None
```
要素`z`を`bst`に追加する．

## delete
```python
bst.delete(key: Any) -> None
```
要素`key`を持つノードを削除する．

## is_contain
```python
bst.is_contain(z: Any) -> bool
```
要素`z`を持つノードが存在するかどうか判定する

## is_empty
```python
bst.is_empty() -> bool
```
`bst`に含まれるノードが空かどうかを判定する

## get_size
```python
bst.get_size() -> int
```
`bst`に含まれるノードの個数を返す．

## clear
```python
bst.clear() -> None
```
`bst`に含まれるノードを初期化する．実際にはルートの宛先を割り当て直すだけなので$O(1)$で可能．

## count
```python
bst.count(key: Any) -> None
```
`bst`に含まれるノードの中で`key`と一致するものの個数を返す．

## lower_bound
```python
bst.lower_bound(key: Any) -> Any
```
`bst`に含まれるノードの中で，$key\leq z.key$なるノード`z`のうち最小のものを返す．

## upper_bound
```python
bst.upper_bound(key: Any) -> Any
```
`bst`に含まれるノードの中で，$key< z.key$なるノード`z`のうち最小のものを返す．

## get_kth
```python
bst.get_kth(k: int) -> Any
```
`bst`に含まれるノードの中で，昇順に並べた時に`k`番目となる要素の値を返す．(0-indexed)

## index
```python
bst.index(x: Any) -> int
```
`bst`にノード`x`が含まれていて，それが`bst`内のノードを昇順に並び替えた時に何番目になるかを返す．(0-indexed)

## sort/get_inorders
```python
bst.sort() -> list[Any]
```
`bst`に含まれるノードの値を昇順にしたリストを返す．

## get_preorder
調整中
## get_postorder
調整中