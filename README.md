# Job Market Analysis & Recommendation System

A Python web application for exploring Upwork job-posting patterns and finding textually similar job titles. The project combines exploratory data analysis, a TF-IDF-based recommendation workflow, a Flask interface, an interactive dashboard, and Docker deployment.

## Table of Contents

- [Project Overview](#project-overview)
- [Business Problem](#business-problem)
- [Objectives](#objectives)
- [Dataset](#dataset)
- [Analysis and Dashboard](#analysis-and-dashboard)
- [Job Recommendation System](#job-recommendation-system)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Run Locally](#run-locally)
- [Run with Docker](#run-with-docker)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)

## Project Overview

Freelancers need ways to explore job opportunities and understand patterns in job listings. This project analyzes a collected dataset of Upwork postings and provides a web interface for browsing job-related insights and requesting similar job-title recommendations.

## Business Problem

Job seekers may find it difficult to sift through many postings and recognize related opportunities. The application aims to make the collected listings easier to explore and to recommend postings with titles that resemble a user's query.

## Objectives

- Explore job-posting volume and job-title variety.
- Compare hourly and fixed-price postings.
- Review country and popular-title distributions.
- Explore payment fields where data is available.
- Recommend textually similar jobs using TF-IDF and similarity scoring.
- Present summary metrics and charts in a Flask web application.
- Package the application for repeatable execution with Docker Compose.

## Dataset

**Source file:** `all_upwork_jobs_2024-02-07-2024-03-24.csv`

The project dataset has approximately 244,828 records and includes these fields:

| Column | Description |
|---|---|
| `title` | Job-posting title |
| `link` | Link associated with the posting |
| `published_date` | Publication date |
| `is_hourly` | Indicates hourly versus fixed-price payment type |
| `hourly_low` | Lower hourly-rate field, when available |
| `hourly_high` | Upper hourly-rate field, when available |
| `budget` | Fixed-price budget field, when available |
| `country` | Country associated with the posting, when available |

Payment fields and country values may be missing for some records. Confirm counts against the current CSV if the dataset is replaced or updated.

## Analysis and Dashboard

The dashboard is available at `/dashboard` and presents summary metrics and visualizations, including:

- Monthly posting trend
- Hourly versus fixed-price job distribution
- Top countries
- Popular job titles
- Summary KPIs such as total postings, unique titles, countries, and payment-type counts

The dashboard is based on the prepared data stored in `dashboard_data/dashboard.json`.

## Job Recommendation System

The recommendation workflow uses **TF-IDF** to represent job-title text numerically and similarity scoring to retrieve titles that are textually similar to the user's query.

Recommendations indicate text similarity only. They do not guarantee job quality, suitability, hiring likelihood, or future demand.

## Technology Stack

- Python 3.11
- Pandas and NumPy
- Scikit-learn
- Flask
- HTML templates
- Plotly (dashboard charts)
- Docker and Docker Compose

## Project Structure

```text
Project 8/
├── app.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── dashboard_data/
│   └── dashboard.json
├── job_market_model/
│   ├── jobs_data.pkl
│   ├── tfidf_vectorizer.pkl
│   └── job_tfidf_matrix.npz
├── templates/
│   ├── index.html
│   └── dashboard.html
├── all_upwork_jobs_2024-02-07-2024-03-24.csv
└── projet 8.ipynb
```

The CSV and notebook are included in the project workspace; the Docker image copies the application, templates, dashboard data, and prepared model artifacts.

## Run Locally

1. Install Python 3.11.
2. Open a terminal in the project directory.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the Flask application:

   ```bash
   python app.py
   ```

5. Open:
   - Main application: `http://127.0.0.1:5000/`
   - Dashboard: `http://127.0.0.1:5000/dashboard`

## Run with Docker

### Prerequisites

- Docker Desktop installed and running
- Docker Compose available

### Build and start

From the directory containing `docker-compose.yml`, run:

```bash
docker compose up --build -d
```

Check the container:

```bash
docker compose ps
```

View recent logs:

```bash
docker compose logs --tail=50
```

Open the application:

- Main application: `http://127.0.0.1:5000/`
- Dashboard: `http://127.0.0.1:5000/dashboard`

Stop the container:

```bash
docker compose down
```

## Limitations

- The collected dataset represents a limited collection period and may not represent the entire Upwork marketplace.
- Posting counts across months may be affected by uneven data collection; they should not be interpreted as a reliable long-term forecast without further validation.
- The dataset does not include an explicit remote-work classification field, so remote, hybrid, and on-site work cannot be directly compared.
- Payment information is incomplete for some postings.
- Title-based recommendations rely on text similarity and should be validated with user feedback or a labeled evaluation set.
- The application uses Flask's built-in development server; a production deployment should use a production-grade WSGI server and appropriate security configuration.

## Future Improvements

- Refresh the dataset regularly and track data-collection coverage.
- Add filters for date, country, payment type, and job-title keywords.
- Evaluate recommendation quality with a labeled test set and ranking metrics.
- Build and validate forecasting models only when sufficient, consistently collected time-series data is available.
- Add automated tests and production-grade application serving.
- Deploy to a cloud platform and document monitoring and maintenance.

## Conclusion

This project demonstrates an end-to-end workflow for job-posting exploration: data analysis, text-based recommendations, interactive web visualization, and containerized execution.
