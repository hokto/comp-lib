# diameter of a tree: https://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=GRL_5_A&lang=jp

if __name__ == "__main__":
    N = int(input())
    T = [[] for _ in range(N)]
    deg = [0] * N

    for _ in range(N - 1):
        s, t, w = list(map(int, input().split(" ")))
        T[s].append((t, w))
        T[t].append((s, w))
        deg[s] += 1
        deg[t] += 1

    # dp[i][j]:=iを根とする部分木において，iにおけるj番目の有向辺に対応する部分木の最長パス
    dp = [[] for _ in range(N)]

    ans = [0] * N

    def dfs1(r):
        st = [(~r, -1, 0), (r, -1, 0)]  # (v,p,ecost)
        memo = [0] * N
        while st:
            v, p, ecost = st.pop()
            if v >= 0:
                for k, (vv, w) in enumerate(T[v]):
                    if vv == p:
                        continue
                    st.append((~vv, v, w))
                    st.append((vv, v, w))
            else:
                v = ~v
                dp[v] = [0] * deg[v]
                dp_now = 0
                for k, (vv, w) in enumerate(T[v]):
                    if vv == p:
                        continue
                    dp[v][k] = memo[vv]
                    dp_now = max(dp_now, dp[v][k])  # 最長を取る
                memo[v] = dp_now + ecost

        return memo[r]

    def dfs2(r):
        st = [(r, -1, 0)]  # (v,p,d_par)
        while st:
            v, p, d_par = st.pop()
            for k in range(deg[v]):
                if T[v][k][0] == p:
                    dp[v][k] = d_par  # 親で計算した値を保存する
            accum_l = [0] * (deg[v] + 1)
            accum_r = [0] * (deg[v] + 1)
            for k in range(deg[v]):
                accum_l[k + 1] = max(accum_l[k], dp[v][k])
            for k in range(deg[v])[::-1]:
                accum_r[k] = max(accum_r[k + 1], dp[v][k])
            ans[v] = accum_l[-1]  # vから出る辺全体maxが答えになる
            for k, (vv, w) in enumerate(T[v]):
                if vv == p:
                    continue
                st.append(
                    (vv, v, max(accum_l[k], accum_r[k + 1]) + w)
                )  # vのk番目の辺の情報以外で構築されるmax+今の辺のコストwを計算して渡す

    dfs1(0)  # 0を根として木dpする
    dfs2(0)
    print(max(ans))
