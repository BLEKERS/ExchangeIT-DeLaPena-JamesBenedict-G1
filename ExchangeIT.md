# ExchangeIt: A Web-Based Currency Converter — Software Design Document (SDD)

> **Project:** ExchangeIt (Web-Based Currency Converter)
> **Author:** De La Peña, James Benedict G.
> **Course:** CSIT327 — Information Management 2
> **Document Type:** Software Design Document (SDD)
> **Version:** 0.1 (Initial Draft, 10/7/2026)

---

## Document Version History

| Version | Date | Author | Changes Made | Status |
|---------|------|--------|--------------|--------|
| 0.1 | 10/7/2026 | De La Peña, James Benedict G. | Initial draft | Draft |
| 0.2 | [Date] | [Your Name] | Added feature list | Review |
| 0.3 | [Date] | [Your Name] | Added business rules | Review |
| 0.4 | [Date] | [Your Name] | Added data model | Review |
| 0.5 | [Date] | [Your Name] | Incorporated feedback | Revised |
| 0.6 | [Date] | [Your Name] | Final review and corrections | Final |
| 1 | [Date] | [Your Name] | Approved baseline version | Approved |

---

## Table of Contents

1. [Description of the Proposed System](#10-description-of-the-proposed-system)
2. [Feature List](#20-feature-list)
3. [Business Rules](#30-business-rules)
4. [Data Modelling](#40-data-modelling)
5. [Submission Checklist](#submission-checklist)

---

## 1.0 Description of the Proposed System

### 1.1 Project Overview

**ExchangeIt** is a website where users can convert money from one currency to another using **up-to-date exchange rates**. The system keeps its data in a database: user accounts, currencies, exchange rates, saved favorite pairs, and conversion history.

**Core workflow:**
1. A user enters an amount and selects two currencies (source and target).
2. The system retrieves the latest rate from an **online exchange rate API**.
3. The system shows the converted result.
4. The conversion is saved to the user's history.

**Additional capabilities:**
- Users can save their most-used currency pairs for quick access.
- Users can search and filter their history by currency and date.
- Users can view a summary report of their conversions.
- The **Administrator** can add/update currencies, check saved rates, manage user accounts, and view system usage reports.

Everything is in one website, so users no longer need to search online or switch between apps.

### 1.2 Project Information

- **Project Name:** ExchangeIt
- **Domain:** Finance / Currency Exchange

**Primary Users:**

1. **Regular Users** — People who travel, shop online from other countries, or work with international clients. They can:
   - Create an account
   - Convert money
   - Save favorite currency pairs
   - View conversion history
   - View reports

2. **Administrator** — Manages the system:
   - Manages the list of currencies
   - Checks stored exchange rates
   - Manages user accounts
   - Views overall usage reports

### 1.3 Problem Statement

Many people need to convert money (travelers, online shoppers, people working with international clients). Currently, most calculate by hand or search for the rate online every time.

**Key problems:**
- Exchange rates change often, so an old rate gives a wrong result.
- People use several websites or apps just to check a rate and compute the amount — takes time and causes mistakes.
- There is no easy way to keep a record of past conversions.
- Users who want to remember what rate they used, or how much they converted last week, have to write it down or search again.
- Records are not saved in one place, making it hard to look back, compare rates, or see totals over time.

### 1.4 Proposed Solution

ExchangeIt is a **web-based system with a central database** that keeps the following in one place:
- User accounts
- The list of currencies
- Exchange rates
- Favorite currency pairs
- Conversion history

**User capabilities:**
- Register, log in, and convert money using the latest rate from an online API.
- Every conversion is saved automatically.
- Save favorite currency pairs, search/filter history, and view summary reports.

**Administrator capabilities:**
- Manage currencies
- Check saved rates
- Manage users
- View usage reports

Everything is in one website, eliminating the need to search online or switch between apps.

### 1.5 Objectives

1. To allow users to register, log in, and manage their own profile.
2. To allow users to convert an amount between two currencies using the latest exchange rate from an online API.
3. To store and manage exchange rates and the list of currencies in the database.
4. To allow users to save, view, edit, and delete their favorite currency pairs.
5. To save every conversion and show the user's conversion history.
6. To allow users to search and filter their history by currency and date.
7. To generate a summary report of a user's conversions (most used currencies, total number of conversions).
8. To provide an administrator account that manages currencies, users, and system reports.
9. To test all main features and fix errors before the final submission.

### 1.6 Scope

**Included Features:**
- Web system built with **Python and Django**, using a **PostgreSQL (or Supabase PostgreSQL)** database
- Two user roles: **Regular User** and **Administrator**
- User registration, login, logout, and profile management
- Currency converter with currency selection and a swap button
- Getting updated exchange rates from an online API, with a refresh button
- Saving exchange rates in the database
- Favorite currency pairs (add, view, edit, delete)
- Conversion history with search and filter by currency and date
- Summary report for users, and a usage report for the administrator
- Administrator pages to manage currencies and user accounts
- Testing of the main features and final documentation

**Excluded Features:**
- Mobile app (Android or iOS)
- Online banking, money transfer, or actual buying/selling of currencies
- Online payments
- Email or SMS notifications
- Offline use of newly updated exchange rates
- Rate predictions or charts of past rates for many years
- Multi-language support (English only)

### 1.7 Limitations

- The system requires an **internet connection** to work.
- The system depends on the **exchange rate API** being available and staying within its free limits.
- The system does **not support offline use** of newly updated exchange rates.
- The system does **not predict future rates** or show long-term rate charts.
- The system does **not process real money transfers or payments**.
- The system is **only available in English**.

---

## 2.0 Feature List

> Every feature must be supported by at least one table in the data model (Section 4.0).

### 2.1 Feature List (MoSCoW)

**MUST HAVE**
1. User authentication (register, login, logout)
2. User profile management (view, edit)
3. Currency converter (select currencies, enter amount, swap button, refresh rate)
4. Exchange rate storage and management
5. Conversion history (save every conversion, view history)

**SHOULD HAVE**
1. Favorite currency pairs (add, view, edit, delete)
2. Search and filter conversion history by currency and date
3. Summary report for users (most used currencies, total conversions)

**COULD HAVE**
1. Administrator usage report (system-wide stats)
2. Administrator currency management (add, edit, deactivate)

**WON'T HAVE**
1. Mobile app
2. Online payments or money transfer
3. Email or SMS notifications
4. Rate predictions or long-term charts
5. Multi-language support

### 2.2 Feature Descriptions

| ID | Feature | Description | User | Tables Used |
|----|---------|-------------|------|-------------|
| F-01 | User Authentication | Users create an account with a unique email and log in with their password. | Regular User, Admin | `users` |
| F-02 | Profile Management | Users view and update their own profile information. | Regular User | `users` |
| F-03 | Currency Converter | Users enter an amount, select source and target currencies, and view the converted amount using the latest exchange rate. | Regular User | `currencies`, `exchange_rates`, `conversion_history` |
| F-04 | Exchange Rate Management | The system gets updated exchange rates from the online API and stores them in the database. Admins can check the saved exchange rates. | Admin | `currencies`, `exchange_rates` |
| F-05 | Conversion History | Users can view their previous currency conversions, including amount, currencies, exchange rate, and date. | Regular User | `users`, `currencies`, `conversion_history` |
| F-06 | Favorite Currency Pairs | Users can add, view, edit, and delete their frequently used currency pairs. | Regular User | `users`, `currencies`, `favorite_pairs` |
| F-07 | Search and Filter History | Users can search and filter their conversion history by currency and date. | Regular User | `conversion_history`, `currencies` |
| F-08 | Summary Report | Users can view a summary of their conversions (total number of conversions, most-used currencies). | Regular User | `users`, `conversion_history` |
| F-09 | Administrator Usage Report | Admins can view information about how the system is being used. | Admin | `users`, `conversion_history` |
| F-10 | Currency Management | Admins can add, edit, and deactivate currencies available in the system. | Admin | `currencies` |

---

## 3.0 Business Rules

> A business rule defines or constrains how the business operates and what data the system accepts. Each rule is numbered, stated clearly, and has an enforcement method (database constraint or application logic).

### 3.1 Business Rules

| Rule ID | Business Rule | Related Entity | Enforcement |
|---------|---------------|----------------|-------------|
| BR-01 | Each user must register with a unique email address. | `users` | UNIQUE constraint on `email` |
| BR-02 | A user's role must be either `USER` or `ADMIN`. | `users` | CHECK constraint |
| BR-03 | A user's password cannot be empty. | `users` | NOT NULL constraint |
| BR-04 | A currency must have a unique three-letter currency code. | `currencies` | UNIQUE constraint |
| BR-05 | A currency must have a name and currency code. | `currencies` | NOT NULL constraint |
| BR-06 | Only active currencies can be selected for currency conversion. | `currencies` | Application logic |
| BR-07 | An exchange rate must belong to one source currency and one target currency. | `exchange_rates` | Foreign keys |
| BR-08 | The source currency and target currency of an exchange rate cannot be the same. | `exchange_rates` | CHECK constraint |
| BR-09 | An exchange rate must be greater than zero. | `exchange_rates` | CHECK constraint |
| BR-10 | Each conversion must belong to one registered user. | `conversion_history` | Foreign key |
| BR-11 | A conversion amount must be greater than zero. | `conversion_history` | CHECK constraint |
| BR-12 | A converted amount cannot be negative. | `conversion_history` | CHECK constraint |
| BR-13 | A favorite currency pair must belong to one user. | `favorite_pairs` | Foreign key |
| BR-14 | A user cannot save the same currency pair more than once. | `favorite_pairs` | UNIQUE(`user_id`, `from_currency_id`, `to_currency_id`) |
| BR-15 | A user cannot use the same currency as both the source and target currency in a conversion. | `conversion_history` | CHECK constraint / application logic |
| BR-16 | A user can only view, edit, or delete their own favorite pairs and conversion records. | `users`, `favorite_pairs`, `conversion_history` | Application logic |
| BR-17 | Only an administrator can manage currencies and user accounts. | `users`, `currencies` | Application logic |
| BR-18 | Every saved conversion must record the exchange rate used at the time of conversion. | `conversion_history` | NOT NULL constraint |
| BR-19 | Every saved conversion must record the date and time when the conversion was made. | `conversion_history` | NOT NULL and DEFAULT CURRENT_TIMESTAMP |
| BR-20 | Exchange rates received from the API must be stored with the date and time they were retrieved. | `exchange_rates` | NOT NULL and DEFAULT CURRENT_TIMESTAMP |

---

## 4.0 Data Modelling

> The data model must support every feature in Section 2.0 and enforce the business rules in Section 3.0. Use PostgreSQL data types.

### 4.1 Entity Relationship Diagram (ERD)

> Crow's foot notation. All entities, attributes, primary keys (PK), foreign keys (FK), and cardinalities are shown.

**Entities and relationships (text representation of Figure 1):**
users (1) ──< (M) conversion_history
users (1) ──< (M) favorite_pairs
users (1) ──< (M) reports
currencies (1) ──< (M) exchange_rates
currencies (1) ──< (M) favorite_pairs
currencies (1) ──< (M) conversion_history
conversion_history (1) ──< (M) reports [summarized in]

**Entity attribute summary:**

- **users**: `user_id` (PK), `email` (UK), `password_hash`, `full_name`, `role`, `created_at`
- **currencies**: `currency_id` (PK), `currency_code` (UK), `currency_name`, `is_active`, `created_at`
- **favorite_pairs**: `favorite_pair_id` (PK), `user_id` (FK), `from_currency_id` (FK), `to_currency_id` (FK), `created_at`
- **conversion_history**: `conversion_id` (PK), `user_id` (FK), `from_currency_id` (FK), `to_currency_id` (FK), `amount`, `exchange_rate`, `converted_amount`, `converted_at`
- **exchange_rates**: `exchange_rate_id` (PK), `from_currency_id` (FK), `to_currency_id` (FK), `rate`, `retrieved_at`, `source`
- **reports**: `report_id` (PK), `user_id` (FK), `report_type`, `total_conversions`, `generated_at`

**Figure 1:** ExchangeIt MVP Entity Relationship Diagram (original document page 12).

### 4.2 Entities

| Entity | Description |
|--------|-------------|
| `users` | Stores registered users, their account information, and their role. |
| `currencies` | Stores the currencies available in the system. |
| `exchange_rates` | Stores exchange rates received from the online exchange rate API. |
| `favorite_pairs` | Stores currency pairs saved by users for quick access. |
| `conversion_history` | Stores every currency conversion made by a user. |
| `reports` | Stores summary reports generated from the user's conversion records. |

### 4.3 Relationships

| Relationship | Cardinality | Description |
|--------------|-------------|-------------|
| `users` – `conversion_history` | 1 : M | One user can have many conversion records; each conversion record belongs to one user. |
| `users` – `favorite_pairs` | 1 : M | One user can save many favorite currency pairs; each favorite pair belongs to one user. |
| `users` – `reports` | 1 : M | One user can have many reports; each report belongs to one user. |
| `currencies` – `exchange_rates` | 1 : M | One currency can be used in many exchange rate records; each exchange rate uses a currency as either source or target. |
| `currencies` – `favorite_pairs` | 1 : M | One currency can be used in many favorite currency pairs; each favorite pair uses currencies as source and target. |
| `currencies` – `conversion_history` | 1 : M | One currency can be used in many conversion records; each conversion record uses currencies as source and target. |
| `conversion_history` – `reports` | 1 : M | Conversion records can be included in many reports; each report can use conversion records to create its summary. |

### 4.4 Data Dictionary

#### Table: `users`

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `user_id` | SERIAL | PK | Unique ID of the user |
| `email` | VARCHAR(100) | NOT NULL, UNIQUE | User's email address |
| `password_hash` | VARCHAR(255) | NOT NULL | User's encrypted password |
| `full_name` | VARCHAR(100) | NOT NULL | Full name of the user |
| `role` | VARCHAR(10) | NOT NULL, DEFAULT 'USER', CHECK | User type: `USER` or `ADMIN` |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Date and time the account was created |

#### Table: `currencies`

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `currency_id` | SERIAL | PK | Unique ID of the currency |
| `currency_code` | CHAR(3) | NOT NULL, UNIQUE | Three-letter currency code (e.g., USD, PHP) |
| `currency_name` | VARCHAR(100) | NOT NULL | Full name of the currency |
| `is_active` | BOOLEAN | NOT NULL, DEFAULT TRUE | Shows if the currency can be used |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Date and time the currency was added |

#### Table: `exchange_rates`

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `exchange_rate_id` | SERIAL | PK | Unique ID of the exchange rate |
| `from_currency_id` | INTEGER | NOT NULL, FK → `currencies(currency_id)` | Currency being converted from |
| `to_currency_id` | INTEGER | NOT NULL, FK → `currencies(currency_id)` | Currency being converted to |
| `rate` | NUMERIC(18,8) | NOT NULL, CHECK (`rate > 0`) | Exchange rate between the two currencies |
| `retrieved_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Date and time the rate was received |
| `source` | VARCHAR(100) | NOT NULL | Name of the exchange rate API |

**Table constraint:** `CHECK (from_currency_id <> to_currency_id)`

#### Table: `favorite_pairs`

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `favorite_pair_id` | SERIAL | PK | Unique ID of the favorite pair |
| `user_id` | INTEGER | NOT NULL, FK → `users(user_id)` | User who saved the pair |
| `from_currency_id` | INTEGER | NOT NULL, FK → `currencies(currency_id)` | Currency to convert from |
| `to_currency_id` | INTEGER | NOT NULL, FK → `currencies(currency_id)` | Currency to convert to |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Date and time the pair was saved |

**Table constraints:**
- `UNIQUE (user_id, from_currency_id, to_currency_id)`
- `CHECK (from_currency_id <> to_currency_id)`

#### Table: `conversion_history`

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `conversion_id` | SERIAL | PK | Unique ID of the conversion |
| `user_id` | INTEGER | NOT NULL, FK → `users(user_id)` | User who made the conversion |
| `from_currency_id` | INTEGER | NOT NULL, FK → `currencies(currency_id)` | Currency being converted from |
| `to_currency_id` | INTEGER | NOT NULL, FK → `currencies(currency_id)` | Currency being converted to |
| `amount` | NUMERIC(18,2) | NOT NULL, CHECK (`amount > 0`) | Amount entered by the user |
| `exchange_rate` | NUMERIC(18,8) | NOT NULL, CHECK (`exchange_rate > 0`) | Rate used for the conversion |
| `converted_amount` | NUMERIC(18,2) | NOT NULL, CHECK (`converted_amount > 0`) | Result of the conversion |
| `converted_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Date and time of the conversion |

**Table constraint:** `CHECK (from_currency_id <> to_currency_id)`

#### Table: `reports`

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `report_id` | SERIAL | PK | Unique ID of the report |
| `user_id` | INTEGER | NOT NULL, FK → `users(user_id)` | User who generated the report |
| `report_type` | VARCHAR(30) | NOT NULL | Type of report (e.g., `USER_SUMMARY`, `ADMIN_USAGE`) |
| `total_conversions` | INTEGER | NOT NULL, DEFAULT 0, CHECK (`total_conversions > 0`) | Total number of conversions included in the report |
| `generated_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Date and time the report was generated |

---

## Submission Checklist

> The original document's final page (page 16) contains a garbled numbering grid (the "Submission Checklist" table) that could not be reliably extracted. Refer to the original PDF for the checklist items.

---

## Notes for AI Consumption

- **Project stack:** Python + Django, PostgreSQL (or Supabase PostgreSQL), external exchange rate API, English-only web app.
- **Roles:** `USER` (regular user) and `ADMIN`.
- **Core tables:** `users`, `currencies`, `exchange_rates`, `favorite_pairs`, `conversion_history`, `reports`.
- **Key invariants:** `from_currency_id <> to_currency_id` on `exchange_rates`, `favorite_pairs`, and `conversion_history`; unique email per user; unique currency code; unique favorite pair per user.
- **Feature-to-table mapping** is specified in Section 2.2 (F-01 to F-10).
- **Business rules** are numbered BR-01 to BR-20 with enforcement types (DB constraint vs. application logic).
- The document is an **initial draft (v0.1)**; later version entries (v0.2–v1) are placeholders with `[Date]` and `[Your Name]`.
