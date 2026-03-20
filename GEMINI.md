<!-- Note pour Gemini : Ce fichier est ta source de vérité. Pense à le mettre à jour au fur et à mesure des évolutions pour rester synchronisé avec le projet. -->

🚲 Vlille Availability & Prediction Project
📌 Project Overview
This "Fullstack Data" project aims to predict the real-time and future availability of self-service bicycles (V'lille) in the Lille metropolis. It covers the entire data value chain: from high-frequency raw data ingestion to exposing a predictive model via a dedicated API.

🏗️ Technical Architecture (Monorepo)
The project follows a Monorepo structure to ensure service consistency and streamline Application Lifecycle Management (ALM).

/data-ingestion: Serverless micro-services (AWS Lambda) extracting API data (Vlille, Weather) into a PostgreSQL (RDS) database.

/data-science: Exploratory Data Analysis (EDA), feature engineering, and training of regression models (XGBoost/LightGBM).

/api: Service interface (FastAPI) to serve model predictions.

/frontend: Data visualization and forecasting dashboard (Streamlit/React).

### Focus: `vlille` Lambda Structure & CI/CD

The `data-ingestion/vlille` lambda follows a structured layout for testability and maintainability:
- `/src`: Contains the main application logic (`main.py`).
- `/tests`: Contains unit tests for the lambda (`test_unit.py`). all the tests will be done with pytest

The CI/CD is managed by two GitHub Actions workflows:
1.  **Test on Pull Request (`test-vlille-lambda.yml`)**: Automatically runs `pytest` for any PR that modifies the `data-ingestion/vlille/` directory. This ensures that new code is tested before being merged.
2.  **Deploy on Main (`deploy-vlille-lambda.yml`)**: When a change is pushed to the `main` branch, this workflow first runs the tests. If they pass, it packages the lambda and deploys the new version to AWS using `aws lambda update-function-code`.

🛠️ Development Standards & Best Practices
This project adheres to industry-standard software engineering practices to ensure robustness, security, and scalability:

1. CI/CD (Continuous Integration & Deployment)

Automation: Full use of GitHub Actions to eliminate manual interventions.

Targeted Deployment: Intelligent workflows triggered only by specific directory changes (paths-filter), optimizing build times and reducing deployment risks.

Secrets Management: Zero hardcoded API keys or AWS credentials. All sensitive data is handled via GitHub Secrets.

2. Code Quality & Testing

Automated Testing: Integration of unit tests with Pytest, executed on every Pull Request to prevent regressions.

Isolated Environments: Systematic use of venv (virtual environments) and requirements.txt for environment reproducibility.

Identity Management: AWS access is restricted via IAM policies following the Principle of Least Privilege.

3. Monitoring & Resilience

Observability: Implementation of CloudWatch Alarms and SNS notifications for real-time alerting on ingestion failures.

Error Handling: Structured logging and retry mechanisms to handle third-party API instability and network timeouts.

🚀 Upcoming Milestones
Implementation of the Weather ingestion flux (Open-Meteo API).

Dataset construction by merging temporal, holiday, and meteorological features.

Containerization of services for full environment portability.

Pro-tip for your README:

Under the CI/CD section, you could add a small "badge" from your GitHub Actions to show it's currently passing. It adds a very professional touch.