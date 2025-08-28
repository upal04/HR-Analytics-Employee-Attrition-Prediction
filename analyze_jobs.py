#!/usr/bin/env python3
"""
analyze_jobs.py

Read a CSV with job postings (job_title, role, location, company, skills),
normalize skills, produce heatmaps and Excel exports, and generate recommendations.

Usage:
  python analyze_jobs.py --input collected_jobs.csv --outdir outputs
"""
import os
import argparse
import re
import numpy as np
import pandas as pd

# Use Agg backend for headless environments (safe for servers)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def normalize_skill(s: str) -> str:
    if not isinstance(s, str):
        return ""
    s = s.strip()
    if not s:
        return ""
    # common normalizations
    mapping = {
        "Pytorch": "PyTorch",
        "Tensorflow": "TensorFlow",
        "Scikit-Learn": "scikit-learn",
        "Scikit learn": "scikit-learn",
        "Power Bi": "Power BI",
        "Powerbi": "Power BI",
        "A/B Testing": "A/B Testing",
    }
    low = s.strip()
    # apply mapping by case-insensitive match
    for k, v in mapping.items():
        if low.lower() == k.lower():
            return v
    # preserve known acronyms
    acronyms = {"SQL", "AWS", "GCP", "BI", "NLP", "ETL", "API", "R", "Git", "ML"}
    parts = re.split(r"[\s/]+", s)
    parts = [p.upper() if p.upper() in acronyms else p for p in parts]
    fixed = " ".join(parts)
    # final tidy-ups
    fixed = fixed.replace("  ", " ").strip()
    return fixed

def parse_skills_column(df, skill_col="skills"):
    all_lists = []
    for val in df[skill_col].fillna(""):
        if isinstance(val, list):
            items = val
        else:
            # split on commas/semicolons/pipe
            items = [x.strip() for x in re.split(r"[;,|\n]", str(val)) if x.strip()]
        items = [normalize_skill(x) for x in items]
        items = [x for x in items if x]
        all_lists.append(items)
    df = df.copy()
    df["skills_list"] = all_lists
    return df

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="CSV with columns: job_title, role, location, company, skills")
    ap.add_argument("--outdir", default="outputs", help="Output folder")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    df = pd.read_csv(args.input)
    # Ensure required columns exist
    for c in ["job_title", "role", "location", "company", "skills"]:
        if c not in df.columns:
            df[c] = ""
    df = parse_skills_column(df, "skills")

    exploded = df.explode("skills_list").rename(columns={"skills_list": "skill"})
    exploded["skill"] = exploded["skill"].str.strip()

    # City x Skill counts
    city_skill = exploded.groupby(["location", "skill"]).size().reset_index(name="count")

    # Determine top N skills overall
    top10_overall = (
        city_skill.groupby("skill")["count"].sum()
        .sort_values(ascending=False)
        .head(10)
        .index.tolist()
    )

    # Heatmap: cities vs top10_overall
    cities_sorted = sorted(df["location"].unique())
    mat = []
    for city in cities_sorted:
        row = []
        for sk in top10_overall:
            c = city_skill[(city_skill["location"] == city) & (city_skill["skill"] == sk)]["count"]
            row.append(int(c.iloc[0]) if len(c) > 0 else 0)
        mat.append(row)
    M = np.array(mat)

    plt.figure(figsize=(10, 6))
    plt.imshow(M, aspect="auto")
    plt.xticks(ticks=np.arange(len(top10_overall)), labels=top10_overall, rotation=45, ha="right")
    plt.yticks(ticks=np.arange(len(cities_sorted)), labels=cities_sorted)
    plt.title("Top 10 Skills by City (Overall Top-10)")
    plt.xlabel("Skill")
    plt.ylabel("City")
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            plt.text(j, i, str(M[i, j]), ha="center", va="center", fontsize=8)
    heatmap_overall_path = os.path.join(args.outdir, "heatmap_top10_overall_skills_by_city.png")
    plt.tight_layout()
    plt.savefig(heatmap_overall_path, dpi=200)
    plt.close()

    # Per-city heatmaps
    for city in cities_sorted:
        sub = city_skill[city_skill["location"] == city].sort_values("count", ascending=False).head(10)
        if sub.empty:
            continue
        skills_city = sub["skill"].tolist()
        counts_city = sub["count"].tolist()
        fig = plt.figure(figsize=(6, 6))
        arr = np.array(counts_city).reshape(-1, 1)
        plt.imshow(arr, aspect="auto")
        plt.yticks(ticks=np.arange(len(skills_city)), labels=skills_city)
        plt.xticks(ticks=[0], labels=[city])
        plt.title(f"{city}: Top 10 Skills")
        for i, val in enumerate(counts_city):
            plt.text(0, i, str(val), ha="center", va="center", fontsize=8)
        path = os.path.join(args.outdir, f"heatmap_{city}_top10.png")
        plt.tight_layout()
        plt.savefig(path, dpi=200)
        plt.close()

    # Skill vs Role matrix + Excel export
    skill_role = exploded.groupby(["skill", "role"]).size().reset_index(name="count")
    pivot_skill_role = skill_role.pivot(index="skill", columns="role", values="count").fillna(0).astype(int)

    excel_path = os.path.join(args.outdir, "skill_role_matrix.xlsx")
    with pd.ExcelWriter(excel_path, engine="xlsxwriter") as writer:
        pivot_skill_role.to_excel(writer, sheet_name="Skill_vs_Role")
        city_skill_pivot = city_skill.pivot(index="location", columns="skill", values="count").fillna(0).astype(int)
        city_skill_pivot.to_excel(writer, sheet_name="City_vs_Skill")
        exploded.to_excel(writer, sheet_name="Tidy_Postings", index=False)

    # Recommendations
    global_counts = city_skill.groupby("skill")["count"].sum().sort_values(ascending=False)
    global_top = set(global_counts.head(15).index.tolist())

    recs = []
    for city in cities_sorted:
        sub = city_skill[city_skill["location"] == city].sort_values("count", ascending=False)
        top5_city = sub.head(5)["skill"].tolist()
        hot_in_city = [s for s in sub["skill"].tolist() if s in global_top][:5]
        recs.append({
            "city": city,
            "recommend_focus_skills": ", ".join(top5_city),
            "hot_skills_here_and_globally": ", ".join(hot_in_city),
            "note": "Focus on the above skills for better interview alignment in this city."
        })
    recs_df = pd.DataFrame(recs)
    recs_csv = os.path.join(args.outdir, "recommendations_by_city.csv")
    recs_txt = os.path.join(args.outdir, "recommendations.txt")
    recs_df.to_csv(recs_csv, index=False)
    with open(recs_txt, "w", encoding="utf-8") as f:
        for r in recs:
            f.write(f"- {r['city']}\n  Focus: {r['recommend_focus_skills']}\n  Hot vs Global: {r['hot_skills_here_and_globally']}\n\n")

    print("Analysis complete. Outputs saved to:", args.outdir)

if __name__ == "__main__":
    main()
