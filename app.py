from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import os
import re
import json

from sklearn.metrics.pairwise import cosine_similarity


# ==========================================
# 1. INITIALIZE FLASK APPLICATION
# ==========================================

app = Flask(__name__)

MODEL_DIR = "job_market_model"


# ==========================================
# 2. LOAD SAVED MODEL AND JOB DATA
# ==========================================

tfidf = joblib.load(
    os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")
)

jobs_df = pd.read_pickle(
    os.path.join(MODEL_DIR, "jobs_data.pkl")
)

jobs_df["title"] = (
    jobs_df["title"]
    .fillna("")
    .astype(str)
)


# ==========================================
# 3. JOB RECOMMENDATION FUNCTION
# ==========================================

def recommend_jobs(query, top_n=10):

    query = query.strip().lower()

    if not query:
        return []

    words = re.findall(r"\b\w+\b", query)

    if not words:
        return []

    # Find candidate job titles using query keywords
    pattern = "|".join(
        re.escape(word) for word in words
    )

    candidates = jobs_df[
        jobs_df["title"].str.contains(
            pattern,
            case=False,
            regex=True,
            na=False
        )
    ].copy()

    if candidates.empty:
        return []

    # Convert query and job titles into TF-IDF vectors
    query_vector = tfidf.transform([query])

    title_vectors = tfidf.transform(
        candidates["title"].str.lower().tolist()
    )

    # Calculate cosine similarity
    similarities = cosine_similarity(
        query_vector,
        title_vectors
    ).flatten()

    candidates["similarity"] = similarities

    # Remove zero-similarity results
    candidates = candidates[
        candidates["similarity"] > 0
    ]

    if candidates.empty:
        return []

    # Sort by similarity score
    candidates = candidates.sort_values(
        by="similarity",
        ascending=False
    )

    # Keep unique job titles
    candidates = candidates.drop_duplicates(
        subset=["title"]
    )

    candidates = candidates.head(top_n)

    results = []

    for _, row in candidates.iterrows():

        # Payment type
        if row["is_hourly"]:
            payment_type = "Hourly"
        else:
            payment_type = "Fixed Price"

        # Hourly rate
        low = row["hourly_low"]
        high = row["hourly_high"]

        hourly_rate = "N/A"

        if pd.notna(low) or pd.notna(high):

            low_text = (
                str(low) if pd.notna(low) else "N/A"
            )

            high_text = (
                str(high) if pd.notna(high) else "N/A"
            )

            hourly_rate = f"{low_text} - {high_text}"

        # Country
        country = (
            row["country"]
            if pd.notna(row["country"])
            else "Not specified"
        )

        results.append({
            "title": row["title"],
            "payment_type": payment_type,
            "hourly_rate": hourly_rate,
            "country": country,
            "similarity": round(
                float(row["similarity"]) * 100,
                2
            )
        })

    return results


# ==========================================
# 4. HOME PAGE - JOB SEARCH
# ==========================================

@app.route("/", methods=["GET", "POST"])
def home():

    recommendations = []
    query = ""

    if request.method == "POST":

        query = request.form.get(
            "query", ""
        ).strip()

        if query:

            recommendations = recommend_jobs(
                query,
                top_n=10
            )

    return render_template(
        "index.html",
        recommendations=recommendations,
        query=query
    )


# ==========================================
# 5. DASHBOARD PAGE
# ==========================================

@app.route("/dashboard")
def dashboard():

    return render_template("dashboard.html")


# ==========================================
# 6. DASHBOARD DATA API
# ==========================================

@app.route("/api/dashboard-data")
def dashboard_data():

    file_path = os.path.join(
        "dashboard_data",
        "dashboard.json"
    )

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        return jsonify(data)

    except FileNotFoundError:

        return jsonify({
            "error": "Dashboard data file not found."
        }), 404

    except json.JSONDecodeError:

        return jsonify({
            "error": "Dashboard JSON file is invalid."
        }), 500


# ==========================================
# 7. RUN FLASK APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(host="0.0.0.0", debug=False, use_reloader=False, port=5000)