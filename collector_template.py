"""
collector_template.py

Safe, reusable template to parse locally-saved job listing HTML pages
(or to normalize allowed CSVs). Edit CSS selectors to match how you saved pages.

Usage:
  python collector_template.py --source saved_pages --out collected_jobs.csv
"""
import os
import re
import argparse
import pandas as pd
from bs4 import BeautifulSoup

SOURCE_DIR = "saved_pages"

def parse_saved_html(path):
    """Parse a saved HTML page and return list of dicts with job fields."""
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")

    items = []
    # Candidate selectors — adapt to the HTML you saved
    cards = soup.select("[data-job-card], .job-card, .result-card, .job-listing, .occludable-update")
    for card in cards:
        title_el = card.select_one(".job-title, .result-card__title, h3, h2, .title")
        title = title_el.get_text(strip=True) if title_el else ""

        company_el = card.select_one(".company, .result-card__subtitle, .company-name")
        company = company_el.get_text(strip=True) if company_el else ""

        location_el = card.select_one(".job-location, .job-result-card__location, .location")
        location = location_el.get_text(strip=True) if location_el else ""

        # Collect candidate skill text: bullets, short paragraphs, or card text
        texts = []
        for li in card.select("li"):
            txt = li.get_text(" ", strip=True)
            if txt:
                texts.append(txt)
        if not texts:
            for p in card.select("p"):
                txt = p.get_text(" ", strip=True)
                if txt:
                    texts.append(txt)
        if not texts:
            texts = [card.get_text(" ", strip=True)]

        # Naive skill extraction: split on common separators, keep short tokens
        skills = set()
        for t in texts:
            for token in (tok.strip() for tok in re.split(r"[,;•\n\r\u2022\-\u2023]", t) if tok.strip()):
                if len(token) > 1 and len(token.split()) <= 6:
                    skills.add(token)
        skills_text = ", ".join(sorted(skills))

        # Simple role inference — customize ROLES as needed
        ROLES = ["Data Scientist", "Data Analyst", "Business Analyst", "ML Engineer", "BI Developer"]
        role = ""
        tl = title.lower()
        for cand in ROLES:
            if cand.lower() in tl:
                role = cand
                break

        items.append({
            "job_title": title,
            "role": role,
            "location": location,
            "company": company,
            "skills": skills_text
        })
    return items

def collect_to_csv(source_dir=SOURCE_DIR, out_csv="collected_jobs.csv"):
    rows = []
    if not os.path.isdir(source_dir):
        raise FileNotFoundError(f"Source directory not found: {source_dir}")

    for fname in sorted(os.listdir(source_dir)):
        path = os.path.join(source_dir, fname)
        if fname.lower().endswith((".html", ".htm")):
            try:
                rows.extend(parse_saved_html(path))
            except Exception as e:
                print(f"Warning: failed to parse {path} ({e})")
        elif fname.lower().endswith(".csv"):
            df = pd.read_csv(path)
            expected = ["job_title", "role", "location", "company", "skills"]
            df2 = df[[c for c in df.columns if c in expected]].copy()
            for c in expected:
                if c not in df2.columns:
                    df2[c] = ""
            rows.extend(df2[expected].to_dict(orient="records"))

    out_df = pd.DataFrame(rows)
    out_df.to_csv(out_csv, index=False)
    print(f"Wrote {out_csv} with {len(out_df)} rows.")
    return out_df

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default=SOURCE_DIR, help="Folder containing saved HTML or CSV files")
    ap.add_argument("--out", default="collected_jobs.csv", help="Output CSV filename")
    args = ap.parse_args()
    collect_to_csv(source_dir=args.source, out_csv=args.out)
