# Project-AI-Financial-Risk-Management
- Project Summary

— Fraud Detection Using Machine Learning

Our project focuses on building a robust machine learning pipeline to detect fraudulent financial transactions. The dataset contains 27 anonymized (hashed) features to preserve confidentiality, and the objective is to classify each transaction as fraudulent or legitimate.
We will experiment with three different machine learning models: `XGBoostClassifier`, `RangomForestClassifier`, `LogisticRegression`, and we will applying a range of hyperparameter optimization techniques to systematically improve performance—particularly recall, which is critical in fraud detection. After finalizing the best-performing model, we will migrate the full workflow into a clean, modular Python codebase that follows production-grade structure and best practices.
Once the model is operational in code, we will containerize the application using Docker, ensuring reproducibility and ease of deployment. Finally, we will develop a user-friendly front-end interface using FastAPI and/or Streamlit, enabling real-time predictions and making the system accessible to end users through a cloud deployment.

However, because nearly all features in the dataset are hashed or anonymized, interpreting the model’s decisions and presenting meaningful explanations in the front-end application will be challenging. This limitation affects both model interpretability and user-facing insights. Addressing this will require additional research into techniques such as feature importance mapping, surrogate models, and explainability tools (e.g., SHAP or LIME) that can provide interpretable outputs without exposing sensitive information.


### Our current project structure

![project_structure](../Project-AI-Financial-Risk-Management/resource/Ai_financial_risk_mgt_proj_structure.png)
