# https://atcoder.jp/contests/tdpc/tasks/tdpc_tree


class Math:
    _MOD: int
    _MAX_SIZE: int
    _fact: list[int]
    _fact_inv: list[int]
    _inv: list[int]

    def __init__(self, mod=998244353, MAX_SIZE=10**6) -> None:
        self._MOD = mod
        self._MAX_SIZE = MAX_SIZE
        self.build()

    def build(self) -> None:
        self._fact = [0] * self._MAX_SIZE
        self._fact_inv = [0] * self._MAX_SIZE
        self._inv = [0] * self._MAX_SIZE
        self.comb_init()

    def comb_init(self) -> None:
        self._fact[0] = self._fact[1] = 1
        self._fact_inv[0] = self._fact_inv[1] = 1
        self._inv[1] = 1

        for i in range(2, self._MAX_SIZE):
            self._fact[i] = (self._fact[i - 1] * i) % self._MOD
            self._inv[i] = (
                self._MOD - self._inv[self._MOD % i] * (self._MOD // i)
            ) % self._MOD
            self._fact_inv[i] = (self._fact_inv[i - 1] * self._inv[i]) % self._MOD

    def comb(self, n, r) -> int:
        if n < r:
            return 0
        if n < 0 or r < 0:
            return 0
        return (self._fact[n] * self._fact_inv[r] * self._fact_inv[n - r]) % self._MOD

    def fact(self, n) -> int:
        if n < 0:
            return 0
        return self._fact[n]

    # x**y(mod _MOD)
    def pow(self, x, y) -> int:
        res = 1
        b = x
        while y:
            if y & 1:
                res *= b
                res %= self._MOD
            b = (b * b) % self._MOD
            y //= 2
        return res

    def inv(self, n) -> int:
        if n < 0:
            return 0
        return self.pow(n, self._MOD - 2)


if __name__ == "__main__":
    MOD = 10**9 + 7
    N = int(input())
    T = [[] for _ in range(N)]
    deg = [0] * N
    for _ in range(N - 1):
        a, b = list(map(int, input().split(" ")))
        a -= 1
        b -= 1
        T[a].append(b)
        T[b].append(a)
        deg[a] += 1
        deg[b] += 1
    math = Math(mod=MOD)
    ans = 0
    # dp[i][j]:=iを部分木として，辺jの有向辺に対応する部分木で辺を書く順番の数
    dp = [[] for _ in range(N)]

    # size[i][j]:=iを部分木，辺jの有向辺に対応する部分木のサイズ
    size = [[] for _ in range(N)]

    # 各部分木に対して，それぞれ辺を書く順番の数はmemo[v]で決まる
    # 各部分木に割り当てられる辺の順番は各部分木の辺のサイズS_vを用いて，\sum_{S_v}!/\prod_{S_v !}
    # 実際は，combで分解できるため，積の演算で実現できる
    def dfs1(r):
        st = [(~r, -1), (r, -1)]
        memo1 = [1] * N  # vに対してのdpの答え
        memo2 = [0] * N  # vに対しての辺のサイズ
        while st:
            v, p = st.pop()
            if v >= 0:
                for k, vv in enumerate(T[v]):
                    if vv == p:
                        continue
                    st.append((~vv, v))
                    st.append((vv, v))
            else:
                v = ~v
                dp[v] = [0] * deg[v]
                size[v] = [0] * deg[v]
                s = 0  # サイズの総和を取る
                dp_now = 1
                for k, vv in enumerate(T[v]):
                    if vv == p:
                        continue
                    dp[v][k] = memo1[vv]
                    size[v][k] = memo2[vv]
                    s += size[v][k]
                    dp_now *= dp[v][k] * math.comb(s, size[v][k])
                    dp_now %= MOD
                memo1[v] = dp_now
                memo2[v] = s + 1
        return memo1[r], memo2[r]

    def dfs2(v, p, d_par1, d_par2):
        global ans
        for k, vv in enumerate(T[v]):
            if vv == p:
                dp[v][k] = d_par1
                size[v][k] = d_par2

        # accum1:=サイズの和,accum2:=各部分木ごとのdpの結果
        accum1_l = [0] * (deg[v] + 1)
        accum1_r = [0] * (deg[v] + 1)
        accum2_l = [1] * (deg[v] + 1)
        accum2_r = [1] * (deg[v] + 1)
        for k in range(deg[v]):
            accum1_l[k + 1] = accum1_l[k] + size[v][k]
            accum2_l[k + 1] = (
                accum2_l[k] * dp[v][k] * math.comb(accum1_l[k + 1], size[v][k])
            ) % MOD

        for k in range(deg[v])[::-1]:
            accum1_r[k] = accum1_r[k + 1] + size[v][k]
            accum2_r[k] = (
                accum2_r[k + 1] * dp[v][k] * math.comb(accum1_r[k], size[v][k])
            ) % MOD

        ans += accum2_l[-1]
        for k, vv in enumerate(T[v]):
            if vv == p:
                continue
            dp_now = (
                accum2_l[k]
                * accum2_r[k + 1]
                * math.comb(accum1_l[k] + accum1_r[k + 1], accum1_r[k + 1])
            ) % MOD
            dfs2(vv, v, dp_now, accum1_l[k] + accum1_r[k + 1] + 1)

    dfs1(0)
    dfs2(0, -1, 1, 0)
    print((ans * math.inv(2)) % MOD)
