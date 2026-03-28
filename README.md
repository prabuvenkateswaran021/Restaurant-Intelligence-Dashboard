# 🍽️ Restaurant Intelligence Dashboard
### Cognifyz Technologies — Data Analytics Internship Project

![Dashboard Preview](https://img.shields.io/badge/Dashboard-Live%20HTML-f97316?style=for-the-badge&logo=html5&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8%2B-38bdf8?style=for-the-badge&logo=python&logoColor=white)
![Chart.js](https://img.shields.io/badge/Chart.js-4.4.1-a78bfa?style=for-the-badge&logo=chartdotjs&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-34d399?style=for-the-badge)

---

## 📌 Project Overview

This project is a **full-stack data analytics dashboard** built as part of the **Cognifyz Technologies Data Analytics Internship**. It processes a real-world restaurant dataset (9,551 records), applies **Power Query-style data cleaning**, and renders an interactive **3-Level Insights Dashboard** directly in the browser — no backend required.

> **9 null cuisine rows removed · 9,542 clean records analysed · 15 insights across 3 levels**

---

## 🗂️ Repository Structure

```
restaurant-intelligence-dashboard/
│
├── Dataset_.csv                  # Raw dataset (9,551 rows)
├── data_processing.py            # Power Query — cleaning & insight extraction
├── restaurant_dashboard.html     # Live interactive dashboard (open in browser)
└── README.md                     # Project documentation (this file)
```

---

## 🧹 Data Cleaning (Power Query Steps)

All cleaning is handled by `data_processing.py` using Python's built-in `csv` module — mimicking Power Query transformations:

| Step | Action | Result |
|------|--------|--------|
| 1 | Load raw CSV with UTF-8-BOM encoding | 9,551 rows |
| 2 | Detect null/empty values per column | Found 9 nulls in `Cuisines` |
| 3 | Remove rows where `Cuisines` is blank | 9,542 clean rows |
| 4 | Normalise cuisine strings (strip whitespace) | Consistent lookup |
| 5 | Cast numeric fields (`Aggregate rating`, `Votes`, etc.) | Safe float/int parsing |
| 6 | Export structured JSON for dashboard | All insight objects |

---

## 📊 Dashboard — 3 Levels of Analysis

### 🔶 Level 1 — Foundational Analysis

| Task | Insight |
|------|---------|
| **Task 1 · Top Cuisines** | North Indian leads at **41.5%** (3,960 restaurants), followed by Chinese (28.7%) and Fast Food (20.8%) |
| **Task 2 · City Analysis** | New Delhi has the most restaurants (**5,473**); Lucknow has the highest average rating (4.2 ★) |
| **Task 3 · Price Range** | **46.5%** of restaurants fall in the budget tier (Range 1); only 6.1% are premium (Range 4) |
| **Task 4 · Online Delivery** | Only **25.7%** offer delivery — but they score significantly higher: avg **3.25** vs **2.46** without delivery |

---

### 🔷 Level 2 — Pattern Discovery

| Task | Insight |
|------|---------|
| **Task 1 · Rating Distribution** | Most restaurants rated **3–3.5 ★** (2,487). 2,148 are "Not Rated" — a large unengaged segment |
| **Task 2 · Cuisine Combinations** | **Chinese + North Indian** is the most popular combo (1,044 restaurants) |
| **Task 4 · Restaurant Chains** | **Cafe Coffee Day** leads with 83 outlets, followed by Domino's Pizza (79) and Subway (63) |

---

### 🔹 Level 3 — Deep Dive

| Task | Insight |
|------|---------|
| **Task 2 · Votes Analysis** | **Toit** tops with 10,934 votes. Average votes per restaurant: 156.8 |
| **Task 3 · Price vs Services** | Budget restaurants offer **0% table booking**. Mid-range leads online delivery (41.3%). Premium tier leads table booking (46.8%) |

---

## 🚀 How to Run

### Option A — Open the Dashboard Directly
```bash
# Just open the HTML file in any modern browser
open restaurant_dashboard.html
# or double-click the file in Finder / File Explorer
```
No server, no dependencies — it's fully self-contained.

---

### Option B — Re-run Data Processing
```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/restaurant-intelligence-dashboard.git
cd restaurant-intelligence-dashboard

# 2. Make sure Python 3.8+ is installed
python --version

# 3. Run the data processing script
python data_processing.py

# Output: Prints all insight JSON to console (can be piped to a file)
python data_processing.py > insights_output.json
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Data Cleaning | Python 3 — `csv`, `collections`, `json` (stdlib only) |
| Visualisation | [Chart.js 4.4.1](https://www.chartjs.org/) via CDN |
| Frontend | Vanilla HTML5, CSS3, JavaScript (ES6+) |
| Fonts | [Syne](https://fonts.google.com/specimen/Syne) + [DM Sans](https://fonts.google.com/specimen/DM+Sans) via Google Fonts |
| Hosting | Static — GitHub Pages compatible |

---

## 📁 Dataset Description

**File:** `Dataset_.csv`  
**Source:** Zomato Restaurant Dataset (Cognifyz Internship)  
**Records:** 9,551 (raw) → 9,542 (after cleaning)

| Column | Type | Description |
|--------|------|-------------|
| Restaurant ID | int | Unique identifier |
| Restaurant Name | str | Name of the restaurant |
| Country Code | int | Numeric country code |
| City | str | City of the restaurant |
| Address | str | Full address |
| Locality | str | Locality / area |
| Longitude / Latitude | float | Geo coordinates |
| Cuisines | str | Comma-separated cuisine types |
| Average Cost for two | int | Cost in local currency |
| Currency | str | Currency name |
| Has Table booking | bool (Yes/No) | Table reservation available |
| Has Online delivery | bool (Yes/No) | Online delivery available |
| Price range | int (1–4) | 1 = Budget → 4 = Premium |
| Aggregate rating | float | Average rating (0–5) |
| Rating color | str | Color band for rating |
| Rating text | str | Textual rating label |
| Votes | int | Total number of votes |

---

## 📸 Dashboard Screenshots

> **Level 1 — Basics:** Cuisine breakdown, city analysis, price distribution, delivery insights  
> **Level 2 — Patterns:** Rating histogram, cuisine combos, chain outlet ranking  
> **Level 3 — Deep Dive:** Top-voted restaurants, price vs. service matrix

*(Open `restaurant_dashboard.html` in your browser to explore all tabs interactively)*

---

## 🌐 Deploy to GitHub Pages

1. Push this repo to GitHub
2. Go to **Settings → Pages**
3. Set source to `main` branch, root folder `/`
4. Your dashboard will be live at:
   ```
    https://prabuvenkateswaran021.github.io/Restaurant-Intelligence-Dashboard/
   ```

---

## 🤝 Internship Details

| Field | Details |
|-------|---------|
| **Organisation** | Cognifyz Technologies |
| **Domain** | Data Analytics |
| **Tasks Completed** | Level 1 (Tasks 1–4), Level 2 (Tasks 1, 2, 4), Level 3 (Tasks 2–3) |
| **Tools Used** | Python, Chart.js, HTML/CSS/JS |

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use, modify, and distribute with attribution.

---

<p align="center">Built with ❤️ for Cognifyz Technologies Data Analytics Internship</p>
