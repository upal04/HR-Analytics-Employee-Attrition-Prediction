## HR Analytics – Predict Employee Attrition (Project 1)
(ELEVATE LABS INTERNSHIP PROJECT)

## 📌 Project Overview

Employee attrition is a major challenge for organizations, leading to increased hiring costs, productivity loss, and decreased morale.
This project uses data analytics and machine learning to identify the main causes of employee resignation and predict future attrition.

## 🎯 Objectives

Perform EDA (Exploratory Data Analysis) to uncover attrition trends.

Build classification models (Logistic Regression & Decision Tree) to predict attrition.

Use SHAP values for model interpretability and feature importance.

Develop an interactive Power BI Dashboard for HR managers.

Provide data-driven suggestions to reduce attrition.

## 🛠️ Tools & Technologies

Python → Pandas, Seaborn, Scikit-learn, SHAP

Power BI → Dashboard & data visualization

Jupyter Notebook → Data analysis and model building

## 📂 Project Structure
HR-Attrition-Project/
│
├── data/
│   └── HR_Analytics.csv                # Dataset
│
├── notebooks/
│   └── HR_Attrition_Analysis.ipynb     # Jupyter notebook with EDA + ML models
│
├── dashboard/
│   └── Employee_Attrition_Rate.pbix    # Power BI dashboard
│   └── Employee_Attrition_Rate.pdf     # Exported Power BI report
│
├── reports/
│   ├── HR_Attrition_Project_Report.pdf # Final 1–2 page project report
│   ├── HR_Attrition_Model_Report.pdf   # Model evaluation summary
│   └── Stemming-the-Tide...pptx        # PPT presentation
│
└── README.md                           # Project documentation

## 📊 Steps Performed

Data Preprocessing

Cleaned dataset, handled missing values, and encoded categorical variables.

Exploratory Data Analysis (EDA)

Department-wise attrition

Salary bands & promotions

Age and tenure distribution

Model Building

Logistic Regression → Accuracy ~86%

Decision Tree → Good interpretability

Confusion matrix and classification reports evaluated performance

Explainability (SHAP Analysis)

Identified top factors influencing attrition (Job Role, Salary, Tenure).

Visualization

Built an interactive Power BI dashboard showing attrition by department, salary, and demographics.

Attrition Prevention Suggestions

Improve career growth opportunities

Conduct competitive salary reviews

Implement work-life balance programs

Train managers in effective leadership

## ✅ Deliverables

## 📊 Power BI Dashboard (.pbix + PDF export)

## 📓 Jupyter Notebook with models & SHAP analysis

## 📑 Final 1–2 page report (PDF)

## 🎥 Presentation slides (PPT)

## 📈 Model Accuracy Report

## 🚀 Conclusion

This project demonstrates how HR data can be leveraged to predict employee attrition and design proactive retention strategies.
By integrating predictive analytics with HR decision-making, organizations can reduce attrition, improve employee satisfaction, and save costs.


## 📊 LinkedIn Job Trend Analysis (Project 2)

Analyze job posting trends (skills, roles, and locations) using Python, BeautifulSoup, Pandas, and Excel. This project generates insights like **top skills by city**, **skill vs role matrices**, and **recommendations for in-demand skills**.

⚠️ **Important Note**: Direct scraping of LinkedIn is against its Terms of Service. This project provides a **template** for parsing **saved HTML files** or **legally obtained datasets**. Please use responsibly.

---

## 🚀 Features

* Extract job titles, skills, and locations from saved HTML pages or CSV datasets.
* Clean and normalize skill tags for consistent analysis.
* Generate **heatmaps of top skills by city**.
* Build **Skill vs Role** and **City vs Skill** matrices.
* Export results to **Excel** and **PNG visuals**.

---

## 🛠️ Tech Stack

* **Python**
* **BeautifulSoup** (HTML parsing)
* **Pandas** (data cleaning & analysis)
* **Matplotlib** (visualizations)
* **Excel (xlsxwriter)** (report exports)

---

## 📂 Project Structure

```
├── collector_template.py   # Template parser for saved HTML pages
├── analyze_jobs.py         # Data analysis & visualization script
├── sample_jobs.csv         # Example dataset
├── outputs/                # Generated charts & reports
└── README.md               # Project documentation
```

---

## ⚡ Quick Start

### 1️⃣ Setup Environment

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2️⃣ Run Analysis

```bash
python analyze_jobs.py --input sample_jobs.csv --outdir outputs
```

### 3️⃣ Outputs

* `heatmap_top10_overall_skills_by_city.png`
* `heatmap_<City>_top10.png`
* `skill_role_matrix.xlsx`
* `recommendations.txt`
* `recommendations_by_city.csv`

---

## 📊 Sample Results

* 🔥 **Top 10 Skills by City Heatmap**
* 📑 **Skill vs Role Matrix in Excel**
* 💡 **Job Demand Recommendations**

---

## 📌 Customization

* Edit **`normalize_skill()`** in `analyze_jobs.py` to handle synonyms (e.g., `ML` → `Machine Learning`).
* Update **role taxonomy** (e.g., `Data Analyst`, `ML Engineer`) for better grouping.
* Add more columns to the dataset (e.g., company, salary) if available.

---

## ✅ Legal Usage

* Use **saved HTML pages** (File → Save Page As) and parse them with `collector_template.py`.
* Or, use **public job APIs** like Adzuna / Indeed datasets.
* Do **NOT** directly scrape LinkedIn.

---

## 📬 Contact

Made with ❤️ for data analytics learning.

Feel free to fork, improve, and share insights! 🚀
