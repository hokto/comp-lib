# verify: https://judge.yosupo.jp/problem/vertex_add_path_sum
"""
    非再帰版EulerTourの実装
"""

from atcoder.segtree import SegTree
from atcoder.fenwicktree import FenwickTree


class EulerTour:
    _visit: list[int]
    _depth: list[tuple[int, int]]
    _depth_segtree: SegTree
    _inorder: list[int]
    _postorder: list[int]
    _edge_cost1: list[int]
    _edge_cost2: FenwickTree
    _vertex_weight1: FenwickTree
    _vertex_weight2: FenwickTree

    def _dfs(
        self, n: int, r: int, T: list[list[tuple[int, int]]], weight: list[int]
    ) -> None:
        visited = [False] * n
        stack = [(r, 0, 0, weight[r])]  # (v,depth,ecost,vcost)
        now_step = 0
        while stack:
            v, now_depth, edge_cost, vertex_weight = stack.pop()
            if v >= 0:
                # 行きがけ処理
                visited[v] = True
                self._inorder[v] = now_step
                self._depth.append((now_depth, now_step))
                self._visit.append(v)
                self._edge_cost2.add(now_step, edge_cost)
                self._vertex_weight1.add(now_step, vertex_weight)
                self._vertex_weight2.add(now_step, vertex_weight)
                now_step += 1
                # 根でなく葉の場合
                if len(T[v]) == 1 and visited[T[v][0][0]]:
                    self._postorder[v] = now_step
                else:
                    # 再帰と訪問順が一致するように
                    for vv, new_edge_cost in T[v][::-1]:
                        if visited[vv]:
                            continue
                        stack.append(
                            (~v, now_depth, new_edge_cost, weight[vv])
                        )  # 帰りがけ用
                        stack.append(
                            (vv, now_depth + 1, new_edge_cost, weight[vv])
                        )  # 行きがけ用
            else:
                # 帰りがけ処理
                self._visit.append(~v)
                self._depth.append((now_depth, now_step))
                self._edge_cost2.add(now_step, -edge_cost)
                self._vertex_weight2.add(now_step, -vertex_weight)
                now_step += 1
                self._postorder[~v] = now_step  # [inorder,postorder)になるように

    # [l,r)のrmqを求めて返す
    def _solve_rmq(self, segtree_rmq: SegTree, l: int, r: int) -> int:
        return segtree_rmq.prod(l, r)

    # [l,r)のrsqを求めて返す
    def _solve_rsq(self, fenwick_tree: FenwickTree, l: int, r: int) -> int:
        return fenwick_tree.sum(l, r)

    def _dist_from_root(self, x: int) -> int:
        idx = self._inorder[x]
        return self._solve_rsq(self._edge_cost2, 1, idx + 1)  # (0,idx]

    def _weight_from_root(self, x: int) -> int:
        idx = self._inorder[x]
        return self._solve_rsq(self._vertex_weight2, 0, idx + 1)  # [0,idx]

    def __init__(
        self, n: int, T: list[list[tuple[int, int]]], weight: list[int] = []
    ) -> None:
        self.build(n, T, weight)

    # 頂点数nの木T,頂点重みweightに対してEulerTourTreeを作成
    def build(
        self, n: int, T: list[list[tuple[int, int]]], weight: list[int] = []
    ) -> None:
        self._visit = []
        self._depth = []
        self._inorder = [-1] * n
        self._postorder = [-1] * n
        self._edge_cost2 = FenwickTree(n=2 * n)
        self._vertex_weight1 = FenwickTree(n=2 * n)
        self._vertex_weight2 = FenwickTree(n=2 * n)
        self._dfs(
            n, 0, T, weight if weight else [1] * n
        )  # 頂点重みがないなら全て1として渡す
        self._depth_segtree = SegTree(op=min, e=(n, n), v=self._depth)

    # 頂点x,yとのLCA
    def lca(self, x: int, y: int) -> int:
        l = min(self._inorder[x], self._inorder[y])
        r = max(self._postorder[x], self._postorder[y])
        _, idx = self._solve_rmq(self._depth_segtree, l, r)
        return self._visit[idx]

    # (x,y)間におけるパスクエリ
    def path_query(self, x: int, y: int) -> int:
        if x == y:
            return 0
        lca = self.lca(x, y)
        dist_x = self._dist_from_root(x)
        dist_y = self._dist_from_root(y)
        dist_lca = self._dist_from_root(lca)
        return dist_x + dist_y - 2 * dist_lca

    # 頂点x,yの間におけるノードクエリ
    def node_query(self, x: int, y: int) -> int:
        lca = self.lca(x, y)
        weight_x_from_root = self._weight_from_root(x)
        weight_y_from_root = self._weight_from_root(y)
        weight_lca_from_root = self._weight_from_root(lca)
        lca_idx = self._inorder[lca]
        weight_lca = self._vertex_weight2.sum(
            lca_idx, lca_idx + 1
        )  # lcaでの頂点重みを計算
        return (
            weight_x_from_root
            + weight_y_from_root
            - 2 * weight_lca_from_root
            + weight_lca
        )

    # xを根とする部分木の頂点に対するクエリ
    def subtree_query_of_vertex(self, x: int) -> int:
        l = self._inorder[x]
        r = self._postorder[x]
        return self._solve_rsq(self._vertex_weight1, l, r)  # [l,r)

    # 辺(u,v)のコストをcostだけ増やす
    def add_edge_cost(self, u: int, v: int, cost: int) -> None:
        inorder = max(self._inorder[u], self._inorder[v])
        postorder = min(self._postorder[u], self._postorder[v])
        self._edge_cost2.add(inorder, cost)
        self._edge_cost2.add(postorder, -cost)

    # 辺(u,v)のコストをnew_costに更新する
    def update_edge_cost(self, u: int, v: int, new_cost: int) -> None:
        inorder = max(self._inorder[u], self._inorder[v])
        postorder = min(self._postorder[u], self._postorder[v])
        self._edge_cost2.add(
            inorder, -self._edge_cost2.sum(inorder, inorder + 1) + new_cost
        )
        self._edge_cost2.add(
            postorder, -self._edge_cost2.sum(postorder, postorder + 1) - new_cost
        )

    # 頂点xの重みをweightだけ増やす
    def add_vertex_weight(self, x: int, weight: int) -> None:
        inorder = self._inorder[x]
        postorder = self._postorder[x]
        self._vertex_weight1.add(inorder, weight)
        self._vertex_weight2.add(inorder, weight)
        self._vertex_weight2.add(postorder, -weight)

    # 頂点xの重みをnew_weightに更新する
    def update_vertex_weight(self, x: int, new_weight: int) -> None:
        inorder = self._inorder[x]
        postorder = self._postorder[x]
        self._vertex_weight1.add(
            inorder, -self._vertex_weight1.sum(inorder, inorder + 1) + new_weight
        )
        self._vertex_weight2.add(
            inorder, -self._vertex_weight2.sum(inorder, inorder + 1) + new_weight
        )
        self._vertex_weight2.add(
            postorder, -self._vertex_weight2.sum(postorder, postorder + 1) - new_weight
        )


if __name__ == "__main__":
    N, Q = list(map(int, input().split(" ")))
    A = list(map(int, input().split(" ")))
    T = [[] for _ in range(N)]
    for _ in range(N - 1):
        u, v = list(map(int, input().split(" ")))
        T[u].append((v, 1))
        T[v].append((u, 1))
    et = EulerTour(N, T, A)
    for q in range(Q):
        query = list(map(int, input().split(" ")))
        if query[0] == 0:
            u, x = query[1:]
            et.add_vertex_weight(u, x)
        else:
            print(et.node_query(query[1], query[2]))
