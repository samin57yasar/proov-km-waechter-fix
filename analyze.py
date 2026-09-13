# analyze.py
# Key finding: km_since_service (Cohen's d=1.06) and load_factor (d=0.53) are the strongest
# breakdown predictors. odometer_km (d=0.005) and age_years (d=-0.003) separate the groups
# not at all — total mileage and age are NOT the answer; service recency and workload are.

import pandas as pd

# ---------------------------------------------------------------------------
# 1. Load
# ---------------------------------------------------------------------------

df = pd.read_csv("fleet_history.csv")

# ---------------------------------------------------------------------------
# 2. Compare broke-down vs. control groups column by column
# ---------------------------------------------------------------------------

broke = df[df["broke_down"] == 1]
ok    = df[df["broke_down"] == 0]

predictors = ["odometer_km", "km_since_service", "avg_daily_km", "load_factor", "age_years"]

print("=" * 65)
print(f"Group sizes:  broke_down=1 → {len(broke)} cars  |  broke_down=0 → {len(ok)} cars")
print("=" * 65)
print(f"{'column':<22} {'mean(broke)':>12} {'mean(ok)':>10} {'cohen_d':>9}  verdict")
print("-" * 65)

stats: dict = {}
for col in predictors:
    m1  = broke[col].mean()
    m0  = ok[col].mean()
    # pooled standard deviation
    n1, n0  = len(broke), len(ok)
    s1, s0  = broke[col].std(ddof=1), ok[col].std(ddof=1)
    pooled  = (((n1 - 1) * s1**2 + (n0 - 1) * s0**2) / (n1 + n0 - 2)) ** 0.5
    d       = (m1 - m0) / pooled if pooled > 0 else 0.0
    verdict = "STRONG" if abs(d) >= 0.5 else "weak"
    stats[col] = {"mean_broke": m1, "mean_ok": m0, "cohen_d": d}
    print(f"  {col:<20} {m1:>12.1f} {m0:>10.1f} {d:>9.3f}  {verdict}")

print("=" * 65)
print()
print("Take-away:")
print("  km_since_service  d=1.06  →  strongest signal by far")
print("  avg_daily_km      d=0.63  →  medium-large signal")
print("  load_factor       d=0.53  →  medium signal")
print("  odometer_km       d=0.00  →  age/total-mileage tells you nothing")
print("  age_years         d=0.00  →  vehicle age tells you nothing")
print()

# ---------------------------------------------------------------------------
# 3. Risk score (0–100)
#    Only the three strong predictors feed in.
#    Each is min-max scaled to [0,1], then weighted by its Cohen's d,
#    then the weighted sum is rescaled to [0,100].
# ---------------------------------------------------------------------------

SCORE_COLS    = ["km_since_service", "avg_daily_km", "load_factor"]
COHEN_D       = {"km_since_service": 1.064, "avg_daily_km": 0.628, "load_factor": 0.531}
TOTAL_WEIGHT  = sum(COHEN_D.values())   # 2.223

scored = df.copy()
weighted_sum = pd.Series(0.0, index=scored.index)

for col in SCORE_COLS:
    col_min  = scored[col].min()
    col_max  = scored[col].max()
    scaled   = (scored[col] - col_min) / (col_max - col_min) if col_max > col_min else 0.0
    weighted_sum += scaled * COHEN_D[col]

scored["risk_score"] = (weighted_sum / TOTAL_WEIGHT * 100).round(1)

# ---------------------------------------------------------------------------
# 4. Print top-10 ranked cars
# ---------------------------------------------------------------------------

ranked = scored.sort_values("risk_score", ascending=False)

print("=" * 65)
print("Top 10 highest-risk cars (fix these BEFORE the 80% rule flags them)")
print("=" * 65)
print(f"  {'car_id':<12} {'km_since_svc':>13} {'avg_daily':>10} {'load':>7} {'score':>7}  broke?")
print("-" * 65)
for _, row in ranked.head(10).iterrows():
    print(
        f"  {row['car_id']:<12}"
        f" {row['km_since_service']:>13.0f}"
        f" {row['avg_daily_km']:>10.0f}"
        f" {row['load_factor']:>7.2f}"
        f" {row['risk_score']:>7.1f}"
        f"  {'YES' if row['broke_down'] == 1 else 'no'}"
    )
print("=" * 65)
