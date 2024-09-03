import hashlib as h
import multiprocessing as m
import getpass as g
def f0(t): return h.md5(t.encode()).hexdigest()
def f1(t): return h.sha256(t.encode()).hexdigest()
def f2(t): return h.sha3_256(t.encode()).hexdigest()
def f3(t): return h.blake2b(t.encode()).hexdigest()
def f4(t): 
    q = h.new('ripemd160')
    q.update(t.encode())
    return q.hexdigest()
def worker(t, i, f):
    return w(t, i, f)
def w(t, i, f): 
    result = t
    for _ in range(i):
        result = f(result)
    return result
def p(t, i, f, n): 
    c = [(t, i // n, f) for _ in range(n)]
    with m.Pool(processes=n) as pool: 
        res = pool.starmap(worker, c)
    r = res[0]
    return w(r, i % n, f)
def pc(c): 
    return g.getpass("Şifre girin:") == c
def main():
    if not pc("black_ghost"):
        print("Şifre yanlış. Program sonlandırılıyor.")
        return
    t = input("Hash'lemek istediğiniz metni girin: ")
    n = m.cpu_count()
    h0 = p(t, 10987, f0, n)
    h1 = p(h0, 13876780, f1, n)
    h2 = p(h1, 30121, f2, n)
    h3 = p(h2, 190780, f3, n)
    h4 = p(h3, 100897865, f4, n)
    print(f"Sonuç: {h4}")
if __name__ == "__main__":
    main()
