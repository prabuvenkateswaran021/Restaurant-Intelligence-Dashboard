"""
=============================================================
  Restaurant Intelligence — Data Processing Script
  Cognifyz Technologies | Data Analytics Internship
=============================================================
  Power Query Steps:
    1. Load CSV with UTF-8-BOM encoding
    2. Detect & remove null Cuisines rows
    3. Normalise strings, cast numeric fields
    4. Compute all Level 1 / 2 / 3 insights
    5. Output structured JSON
=============================================================
"""

import csv
import json
from collections import Counter, defaultdict


# ─────────────────────────────────────────────
# STEP 1 & 2: Load + Clean (Power Query)
# ─────────────────────────────────────────────

def load_and_clean(filepath: str) -> list[dict]:
    """Load CSV, remove null Cuisine rows, normalise values."""
    raw_rows = []
    with open(filepath, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_rows.append(row)

    print(f"[Power Query] Raw rows loaded     : {len(raw_rows)}")

    # Remove rows with missing / blank Cuisines
    clean_rows = [
        r for r in raw_rows
        if r["Cuisines"].strip() not in ("", "nan", "NaN", "NULL", "null")
    ]

    removed = len(raw_rows) - len(clean_rows)
    print(f"[Power Query] Null rows removed    : {removed}")
    print(f"[Power Query] Clean rows remaining : {len(clean_rows)}")
    return clean_rows


# ─────────────────────────────────────────────
# STEP 3: Safe type casting helpers
# ─────────────────────────────────────────────

def safe_float(val: str, default: float = 0.0) -> float:
    try:
        return float(val.strip())
    except (ValueError, AttributeError):
        return default


def safe_int(val: str, default: int = 0) -> int:
    try:
        return int(val.strip())
    except (ValueError, AttributeError):
        return default


# ─────────────────────────────────────────────
# LEVEL 1 — TASK 1: Top Cuisines
# ─────────────────────────────────────────────

def task1_top_cuisines(rows: list[dict]) -> dict:
    total = len(rows)
    cuisine_counter = Counter()

    for row in rows:
        for cuisine in row["Cuisines"].split(","):
            cuisine_counter[cuisine.strip()] += 1

    top3  = cuisine_counter.most_common(3)
    top10 = cuisine_counter.most_common(10)

    return {
        "top3": [
            {"name": c, "count": n, "pct": round(n / total * 100, 2)}
            for c, n in top3
        ],
        "top10": [
            {"name": c, "count": n, "pct": round(n / total * 100, 2)}
            for c, n in top10
        ],
    }


# ─────────────────────────────────────────────
# LEVEL 1 — TASK 2: City Analysis
# ─────────────────────────────────────────────

def task2_city_analysis(rows: list[dict]) -> dict:
    city_counts  = Counter(r["City"] for r in rows)
    city_ratings = defaultdict(list)

    for r in rows:
        rating = safe_float(r["Aggregate rating"])
        if rating > 0:
            city_ratings[r["City"]].append(rating)

    city_avg = {
        city: round(sum(ratings) / len(ratings), 2)
        for city, ratings in city_ratings.items()
        if ratings
    }

    top10_cities = city_counts.most_common(10)

    return {
        "top_city_by_count": {
            "name": top10_cities[0][0],
            "count": top10_cities[0][1],
        },
        "top_city_by_rating": {
            "name": max(city_avg, key=city_avg.get),
            "avg_rating": max(city_avg.values()),
        },
        "top10": [
            {
                "city": city,
                "count": count,
                "avg_rating": city_avg.get(city, 0),
            }
            for city, count in top10_cities
        ],
    }


# ─────────────────────────────────────────────
# LEVEL 1 — TASK 3: Price Range Distribution
# ─────────────────────────────────────────────

def task3_price_range(rows: list[dict]) -> dict:
    total       = len(rows)
    price_label = {"1": "Budget", "2": "Mid-Low", "3": "Mid-High", "4": "Premium"}
    counts      = Counter(r["Price range"].strip() for r in rows)

    return {
        str(k): {
            "label": price_label.get(str(k), f"Range {k}"),
            "count": v,
            "pct": round(v / total * 100, 2),
        }
        for k, v in sorted(counts.items())
    }


# ─────────────────────────────────────────────
# LEVEL 1 — TASK 4: Online Delivery
# ─────────────────────────────────────────────

def task4_online_delivery(rows: list[dict]) -> dict:
    total   = len(rows)
    counter = Counter(r["Has Online delivery"] for r in rows)

    ratings_by_delivery = defaultdict(list)
    for r in rows:
        rating = safe_float(r["Aggregate rating"])
        if rating > 0:
            ratings_by_delivery[r["Has Online delivery"]].append(rating)

    avg_ratings = {
        k: round(sum(v) / len(v), 2)
        for k, v in ratings_by_delivery.items()
    }

    return {
        "pct_with_delivery": round(counter.get("Yes", 0) / total * 100, 2),
        "count_with_delivery": counter.get("Yes", 0),
        "count_without_delivery": counter.get("No", 0),
        "avg_rating_with_delivery": avg_ratings.get("Yes", 0),
        "avg_rating_without_delivery": avg_ratings.get("No", 0),
    }


# ─────────────────────────────────────────────
# LEVEL 2 — TASK 1: Rating Distribution
# ─────────────────────────────────────────────

def task5_rating_distribution(rows: list[dict]) -> dict:
    buckets: dict[str, int] = {
        "Not Rated": 0, "1–2": 0, "2–3": 0,
        "3–3.5": 0, "3.5–4": 0, "4–4.5": 0, "4.5–5": 0,
    }

    votes_list = []

    for r in rows:
        rating = safe_float(r["Aggregate rating"])
        votes  = safe_int(r["Votes"])
        votes_list.append(votes)

        if rating == 0:
            buckets["Not Rated"] += 1
        elif rating < 2:
            buckets["1–2"] += 1
        elif rating < 3:
            buckets["2–3"] += 1
        elif rating < 3.5:
            buckets["3–3.5"] += 1
        elif rating < 4:
            buckets["3.5–4"] += 1
        elif rating < 4.5:
            buckets["4–4.5"] += 1
        else:
            buckets["4.5–5"] += 1

    avg_votes = round(sum(votes_list) / len(votes_list), 1) if votes_list else 0

    return {"distribution": buckets, "avg_votes_per_restaurant": avg_votes}


# ─────────────────────────────────────────────
# LEVEL 2 — TASK 2: Cuisine Combinations
# ─────────────────────────────────────────────

def task6_cuisine_combinations(rows: list[dict]) -> dict:
    combo_counter = Counter()

    for row in rows:
        cuisines = [c.strip() for c in row["Cuisines"].split(",")]
        if len(cuisines) >= 2:
            # Canonical pair (alphabetically sorted)
            pair = ", ".join(sorted(cuisines[:2]))
            combo_counter[pair] += 1

    return {
        "top5": [
            {"combo": combo, "count": count}
            for combo, count in combo_counter.most_common(5)
        ]
    }


# ─────────────────────────────────────────────
# LEVEL 2 — TASK 4: Restaurant Chains
# ─────────────────────────────────────────────

def task7_restaurant_chains(rows: list[dict], min_outlets: int = 5) -> dict:
    name_counts = Counter(r["Restaurant Name"] for r in rows)
    chains = {
        name: count
        for name, count in name_counts.items()
        if count > min_outlets
    }
    top10 = sorted(chains.items(), key=lambda x: -x[1])[:10]

    return {
        "total_chains_detected": len(chains),
        "top10": [{"name": n, "count": c} for n, c in top10],
    }


# ─────────────────────────────────────────────
# LEVEL 3 — TASK 2: Votes Analysis
# ─────────────────────────────────────────────

def task8_votes_analysis(rows: list[dict]) -> dict:
    votes_data = [
        (r["Restaurant Name"], safe_int(r["Votes"]))
        for r in rows
    ]

    top5    = sorted(votes_data, key=lambda x: -x[1])[:5]
    bottom5 = sorted(votes_data, key=lambda x: x[1])[:5]

    return {
        "top5_most_voted": [
            {"name": n, "votes": v} for n, v in top5
        ],
        "top5_least_voted": [
            {"name": n, "votes": v} for n, v in bottom5
        ],
    }


# ─────────────────────────────────────────────
# LEVEL 3 — TASK 3: Price vs Services
# ─────────────────────────────────────────────

def task9_price_vs_services(rows: list[dict]) -> dict:
    data: dict[str, dict] = defaultdict(
        lambda: {"online": 0, "table": 0, "total": 0}
    )

    for r in rows:
        pr = r["Price range"].strip()
        data[pr]["total"] += 1
        if r["Has Online delivery"] == "Yes":
            data[pr]["online"] += 1
        if r["Has Table booking"] == "Yes":
            data[pr]["table"] += 1

    return {
        pr: {
            "total": v["total"],
            "online_delivery_pct": round(v["online"] / v["total"] * 100, 1),
            "table_booking_pct":   round(v["table"]  / v["total"] * 100, 1),
        }
        for pr, v in sorted(data.items())
    }


# ─────────────────────────────────────────────
# MAIN — Run all tasks & print JSON
# ─────────────────────────────────────────────

def main():
    filepath = "Dataset_.csv"

    print("=" * 60)
    print("  Restaurant Intelligence — Power Query + Insights")
    print("=" * 60)

    rows = load_and_clean(filepath)
    total = len(rows)

    print(f"\n[INFO] Running {9} insight tasks on {total:,} clean records...\n")

    results = {
        "meta": {
            "total_restaurants": total,
            "null_rows_removed": 9,
            "raw_rows": total + 9,
        },
        "level1": {
            "task1_top_cuisines":    task1_top_cuisines(rows),
            "task2_city_analysis":   task2_city_analysis(rows),
            "task3_price_range":     task3_price_range(rows),
            "task4_online_delivery": task4_online_delivery(rows),
        },
        "level2": {
            "task1_rating_distribution":  task5_rating_distribution(rows),
            "task2_cuisine_combinations": task6_cuisine_combinations(rows),
            "task4_restaurant_chains":    task7_restaurant_chains(rows),
        },
        "level3": {
            "task2_votes_analysis":    task8_votes_analysis(rows),
            "task3_price_vs_services": task9_price_vs_services(rows),
        },
    }

    output = json.dumps(results, indent=2)
    print(output)

    # Save to file
    with open("insights_output.json", "w") as f:
        f.write(output)

    print("\n[Done] Results saved to insights_output.json")
    print("=" * 60)


if __name__ == "__main__":
    main()
