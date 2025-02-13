# verify: https://yukicoder.me/problems/no/649


"""
    Implement BinarySearchTree by RedBlackTree.
"""

from __future__ import annotations
from typing import Any, List, Optional
from enum import Enum


class BinarySearchTree:
    # color attribute class
    class _RB_Color(Enum):
        BLACK = 0
        RED = 1

    # include some attribute(parent,left-child,right-child,key,color,subroot-size,subroot-min,subroot-max)
    class _Node:
        def __init__(
            self,
            p: Optional[BinarySearchTree._Node] = None,
            l: Optional[BinarySearchTree._Node] = None,
            r: Optional[BinarySearchTree._Node] = None,
            key: Any = None,
            color: Optional[BinarySearchTree._RB_Color] = None,
        ) -> None:
            self.p: BinarySearchTree._Node = p
            self.l: BinarySearchTree._Node = l
            self.r: BinarySearchTree._Node = r
            self.key: Any = key
            self.color: BinarySearchTree._RB_Color = color
            self.size: int = 1
            self.min: Any = key
            self.max: Any = key

    _NIL: BinarySearchTree._Node
    _root: BinarySearchTree._Node
    _inorder_list: List[Any]
    _preorder_list: List[Any]
    _postorder_list: List[Any]
    _is_init_orders: bool

    def _left_rotate(self, x: _Node) -> None:
        y = x.r
        x.r = y.l
        if y.l != self._NIL:
            y.l.p = x
        y.p = x.p
        if x.p == self._NIL:
            self._root = y
        elif x == x.p.l:
            x.p.l = y
        else:
            x.p.r = y
        y.l = x
        x.p = y
        y.size = x.size
        x.size = x.l.size + x.r.size + 1
        y.min = x.min
        if x.key < x.l.min:
            x.min = x.key
        else:
            x.min = x.l.min
        y.max = x.max
        if x.key > x.r.max:
            x.max = x.key
        else:
            x.max = x.r.max

    def _right_rotate(self, x: _Node) -> None:
        y = x.l
        x.l = y.r
        if y.r != self._NIL:
            y.r.p = x
        y.p = x.p
        if x.p == self._NIL:
            self._root = y
        elif x == x.p.l:
            x.p.l = y
        else:
            x.p.r = y
        y.r = x
        x.p = y
        y.size = x.size
        x.size = x.l.size + x.r.size + 1
        y.min = x.min
        if x.key < x.l.min:
            x.min = x.key
        else:
            x.min = x.l.min
        y.max = x.max
        if x.key > x.r.max:
            x.max = x.key
        else:
            x.max = x.r.max

    def _insert_fixup(self, z: _Node) -> None:
        while z.p.color == BinarySearchTree._RB_Color.RED:
            if z.p == z.p.p.l:
                y = z.p.p.r
                if y.color == BinarySearchTree._RB_Color.RED:
                    z.p.p.color = BinarySearchTree._RB_Color.RED
                    z.p.color = BinarySearchTree._RB_Color.BLACK
                    y.color = BinarySearchTree._RB_Color.BLACK
                    z = z.p.p
                else:
                    if z == z.p.r:
                        z = z.p
                        self._left_rotate(z)
                    z.p.color = BinarySearchTree._RB_Color.BLACK
                    z.p.p.color = BinarySearchTree._RB_Color.RED
                    self._right_rotate(z.p.p)
            else:
                y = z.p.p.l
                if y.color == BinarySearchTree._RB_Color.RED:
                    z.p.p.color = BinarySearchTree._RB_Color.RED
                    z.p.color = BinarySearchTree._RB_Color.BLACK
                    y.color = BinarySearchTree._RB_Color.BLACK
                    z = z.p.p
                else:
                    if z == z.p.l:
                        z = z.p
                        self._right_rotate(z)
                    z.p.color = BinarySearchTree._RB_Color.BLACK
                    z.p.p.color = BinarySearchTree._RB_Color.RED
                    self._left_rotate(z.p.p)
        self._root.color = BinarySearchTree._RB_Color.BLACK

    def _delete_at_fixup(self, x: _Node) -> None:
        while x != self._root and x.color == BinarySearchTree._RB_Color.BLACK:
            if x.p.l == x:
                w = x.p.r
                if w.color == BinarySearchTree._RB_Color.RED:
                    w.color = BinarySearchTree._RB_Color.BLACK
                    x.p.color = BinarySearchTree._RB_Color.RED
                    self._left_rotate(x.p)
                    w = x.p.r
                if (
                    w.l.color == BinarySearchTree._RB_Color.BLACK
                    and w.r.color == BinarySearchTree._RB_Color.BLACK
                ):
                    w.color = BinarySearchTree._RB_Color.RED
                    x = x.p
                else:
                    if w.r.color == BinarySearchTree._RB_Color.BLACK:
                        w.l.color = BinarySearchTree._RB_Color.BLACK
                        w.color = BinarySearchTree._RB_Color.RED
                        self._right_rotate(w)
                        w = x.p.r
                    w.color = x.p.color
                    x.p.color = BinarySearchTree._RB_Color.BLACK
                    w.r.color = BinarySearchTree._RB_Color.BLACK
                    self._left_rotate(x.p)
                    x = self._root
            else:
                w = x.p.l
                if w.color == BinarySearchTree._RB_Color.RED:
                    w.color = BinarySearchTree._RB_Color.BLACK
                    x.p.color = BinarySearchTree._RB_Color.RED
                    self._right_rotate(x.p)
                    w = x.p.l

                if (
                    w.r.color == BinarySearchTree._RB_Color.BLACK
                    and w.l.color == BinarySearchTree._RB_Color.BLACK
                ):
                    w.color = BinarySearchTree._RB_Color.RED
                    x = x.p
                else:
                    if w.l.color == BinarySearchTree._RB_Color.BLACK:
                        w.r.color = BinarySearchTree._RB_Color.BLACK
                        w.color = BinarySearchTree._RB_Color.RED
                        self._left_rotate(w)
                        w = x.p.l

                    w.color = x.p.color
                    x.p.color = BinarySearchTree._RB_Color.BLACK
                    w.l.color = BinarySearchTree._RB_Color.BLACK
                    self._right_rotate(x.p)
                    x = self._root
        x.color = BinarySearchTree._RB_Color.BLACK

    def _transplant(self, u: _Node, v: _Node) -> None:
        if u.p == self._NIL:
            self._root = v
        if u.p.l == u:
            u.p.l = v
        else:
            u.p.r = v
        v.p = u.p

    def __init__(
        self, max_e: Any = -(10**10), min_e: Any = 10**10, init_tree: List[Any] = []
    ) -> None:
        self._NIL = BinarySearchTree._Node()
        self._NIL.l = self._NIL
        self._NIL.r = self._NIL
        self._NIL.color = BinarySearchTree._RB_Color.BLACK
        self._NIL.size = 0
        self._NIL.min = min_e
        self._NIL.max = max_e
        self._root = self._NIL
        self.init_orders()
        for key in init_tree:
            node = BinarySearchTree._Node(key=key)
            self.insert_node(node)

    def _min(self, subroot: _Node) -> _Node:
        z = subroot
        while z.l != self._NIL:
            z = z.l

        return z

    def min(self) -> Any:
        return self._root.min

    def _max(self, subroot: _Node) -> _Node:
        z = subroot
        while z.r != self._NIL:
            z = z.r
        return z

    def max(self) -> Any:
        return self._root.max

    def insert_node(self, z: _Node) -> None:
        y = self._NIL
        x = self._root
        while x != self._NIL:
            x.size += 1
            if x.min > z.key:
                x.min = z.key
            if x.max < z.key:
                x.max = z.key
            y = x
            if z.key < x.key:
                x = x.l
            else:
                x = x.r
            x.p = y
        z.p = y
        z.l = self._NIL
        z.r = self._NIL
        z.color = BinarySearchTree._RB_Color.RED
        if y == self._NIL:
            self._root = z
        elif y.key > z.key:
            y.l = z
        else:
            y.r = z
        self._insert_fixup(z)

    def insert(self, z: Any) -> None:
        node = BinarySearchTree._Node(key=z)
        self.insert_node(node)

    def delete_at_node(self, z: _Node) -> None:
        y = z
        y_origin_color = y.color
        x = self._NIL
        w = self._NIL
        if z.l == self._NIL:
            x = z.r
            self._transplant(z, z.r)
            w = z.r.p
        elif z.r == self._NIL:
            x = z.l
            self._transplant(z, z.l)
            w = z.l.p
        else:
            y = self._min(z.r)
            y_origin_color = y.color
            x = y.r
            if y.p == z:
                x.p = y
                w = y
            else:
                w = y.p
                self._transplant(y, y.r)
                y.r = z.r
                y.r.p = y
            self._transplant(z, y)
            y.l = z.l
            y.l.p = y
            y.color = z.color
        while y != self._NIL:
            y.size -= 1
            y = y.p
        while w != self._NIL:
            w.size = w.l.size + w.r.size + 1
            if w.key < w.l.min:
                w.min = w.key
            else:
                w.min = w.l.min
            if w.key > w.r.max:
                w.max = w.key
            else:
                w.max = w.r.max
            w = w.p
        # fix parameters
        if y_origin_color == BinarySearchTree._RB_Color.BLACK:
            self._delete_at_fixup(x)

    def delete(self, key: Any) -> None:
        if self.is_contain(key):
            z = self.find_node_by_key(key)
            self.delete_at_node(z)

    def init_orders(self) -> None:
        self._preorder_list = []
        self._postorder_list = []
        self._inorder_list = []
        self._is_init_orders = True

    def get_inorder(self) -> List[Any]:
        if not self._is_init_orders:
            return self._inorder_list
        self.solve_orders(self._root)
        self._is_init_orders = False
        return self._inorder_list

    def sort(self) -> List[Any]:
        return self.get_inorder()

    def get_preorder(self) -> List[Any]:
        if not self._is_init_orders:
            return self._preorder_list
        self.solve_orders(self._root)
        self._is_init_orders = False
        return self._preorder_list

    def get_postorder(self) -> List[Any]:
        if not self._is_init_orders:
            return self._postorder_list
        self.solve_orders(self._root)
        self._is_init_orders = False
        return self._postorder_list

    def solve_orders(self, subroot: _Node) -> None:
        if subroot == self._NIL:
            return
        self._preorder_list.append(subroot.key)
        self.solve_orders(subroot.l)
        self._inorder_list.append(subroot.key)
        self.solve_orders(subroot.r)
        self._postorder_list.append(subroot.key)

    def find_node_by_key(self, z: Any) -> _Node:
        x = self._root
        while x != self._NIL:
            if x.key == z:
                return x
            elif x.key > z:
                x = x.l
            else:
                x = x.r
        return self._NIL

    def is_contain(self, z: Any) -> bool:
        node = self.find_node_by_key(z)
        if node != self._NIL:
            return True
        else:
            return False

    def is_empty(self) -> bool:
        if self._root == self._NIL:
            return True
        else:
            return False

    def get_size(self) -> int:
        return self._root.size

    def clear(self) -> None:
        self._root = self._NIL

    def count(self, key: Any) -> None:
        x = self._root
        cnt = 0
        while x != self._NIL:
            if x.key == key:
                cnt += 1
            if key < x.key:
                x = x.l
            else:
                x = x.r
        return cnt

    def lower_bound(self, key: Any) -> Any:
        y = self._NIL
        x = self._root
        while x != self._NIL:
            if x.key >= key:
                y = x
                x = x.l
            else:
                x = x.r
        return y.key

    def upper_bound(self, key: Any) -> Any:
        y = self._NIL
        x = self._root
        while x != self._NIL:
            if x.key > key:
                y = x
                x = x.l
            else:
                x = x.r
        return y.key

    def get_kth(self, k: int) -> Any:
        x = self._root
        while x != self._NIL:
            if k == x.l.size:
                return x.key
            elif k <= x.l.size:
                x = x.l
            else:
                k -= x.l.size + 1
                x = x.r
        return None


if __name__ == "__main__":
    Q, K = list(map(int, input().split(" ")))
    bst = BinarySearchTree(min_e=10**18 + 100)
    for q in range(Q):
        query = list(map(int, input().split(" ")))
        if query[0] == 1:
            bst.insert(query[1])
        else:
            val = bst.get_kth(K - 1)
            if val is not None:
                print(val)
                bst.delete(val)
            else:
                print(-1)
