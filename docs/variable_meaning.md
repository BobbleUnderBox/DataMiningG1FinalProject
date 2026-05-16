## About Dataset
💳 BNPL Credit Risk & Default Prediction
Buy Now, Pay Later (BNPL) is one of the fastest-growing fintech segments globally. This synthetic dataset simulates 10,345 BNPL transactions across 6 countries (2023–2024), designed for building credit risk and default prediction models.

**Target Variable: default_flag — 1 = Defaulted, 0 = Paid on time**

## 🎯 Use Cases
Binary Classification — Predict whether a user will default (default_flag)
Customer Segmentation — Cluster users into Low / Medium / High Risk groups
Risk Scoring — Build composite risk models using financial + behavioural features
Repayment Behaviour Analysis — Understand delay patterns across employment types
Feature Engineering Practice — DTI ratio, missed payments, credit score interactions

## 📋 Column Guide
Column	Type	Description
user_id	int	Unique user identifier
age	int	User age (18–59)
employment_type	str	Salaried / Self-Employed / Student / Unemployed
monthly_income	float	Monthly income in USD
credit_score	int	Standard credit score (300–850)
purchase_amount	float	BNPL transaction value in USD
product_category	str	Electronics, Fashion, Sports, Home, Beauty
bnpl_installments	int	Number of repayment installments (3, 6, 9, 12)
repayment_delay_days	int	Days delayed beyond due date (0–33)
missed_payments	int	Total missed payments (0–7)
default_flag	int	Target: 1 = Defaulted, 0 = Paid ✅
app_usage_frequency	float	App opens per week
location	str	Country (USA, India, UK, Germany, Canada, Australia)
transaction_date	str	Date of purchase (YYYY-MM-DD)
debt_to_income_ratio	float	DTI ratio (monthly debt / monthly income)
risk_score	float	Composite risk score (0–398) — higher = more risky
customer_segment	str	Low Risk / Medium Risk / High Risk