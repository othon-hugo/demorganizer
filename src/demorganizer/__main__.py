from demorganizer.algo import apply_bisection_by_steps

f = lambda x: 3 * x**2 + 5 * x + 12

for i, x in enumerate(apply_bisection_by_steps(f, (-2, -1), 6)):
    print(f"[{i}] x = {x:.6f}")
