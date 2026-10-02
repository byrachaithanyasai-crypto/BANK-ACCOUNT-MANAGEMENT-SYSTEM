# BANKX - Database Implementation Documentation

This document outlines the Phase 2 implementation of the BANKX DBMS.

## 1. Schema & Constraints
- **Core Entities**: CUSTOMER, ACCOUNT, TRANSACTION, BRANCH, EMPLOYEE, LOAN.
- **Supporting Tables**: USER_ACCOUNT, AUDIT_LOG, BENEFICIARY, LOGIN_HISTORY, NOTIFICATION, TRANSACTION_ALERT.
- **Referential Integrity**: Implemented using strict `FOREIGN KEY` constraints.
- **Data Integrity**: Used `ENUM`, `NOT NULL`, and `DEFAULT` to prevent invalid states (e.g., negative balances handled via transaction blocks).

## 2. Stored Procedures
We have encapsulated critical banking operations within Stored Procedures to ensure consistency:
- `sp_create_account`: Validates inputs and creates a new account.
- `sp_deposit_money`: Handles deposits within a transaction, ensuring atomicity.
- `sp_withdraw_money`: Checks for sufficient balance, handles withdrawals securely within a transaction.
- `sp_get_customer_summary`: Aggregates customer data and their total holdings.
- `sp_get_account_statement`: Retrieves transaction history efficiently.
- `sp_apply_loan`: Validates and records loan applications.

## 3. Triggers
Automated database actions without relying on application-level logic:
- `trg_transaction_alert`: Creates a `TRANSACTION_ALERT` if a deposit or withdrawal exceeds 50,000.
- `trg_account_status_notification`: Logs a notification if an account's status changes.
- `trg_audit_customer_update`: Records changes to customer KYC details in `AUDIT_LOG`.
- `trg_audit_loan_update`: Records loan status changes in `AUDIT_LOG`.

## 4. Views
Pre-computed virtual tables for reporting:
- `v_customer_account_summary`
- `v_account_transaction_history`
- `v_branch_performance`
- `v_active_loans`

## 5. Indexes
Optimized queries using indexes on frequent lookup columns:
- Foreign keys (`customer_id`, `branch_id`, `account_id`)
- Searching (`email`, `phone`, `username`)
- Status filtering (`status`, `transaction_date`)

## 6. ACID Properties
The procedures `sp_deposit_money` and `sp_withdraw_money` explicitly use `START TRANSACTION` and `COMMIT` or `ROLLBACK`. The `FOR UPDATE` lock ensures concurrent operations on the same account do not result in race conditions.

## Execution Order
To deploy this database, run the SQL scripts in this exact order:
1. `schema.sql`
2. `indexes.sql`
3. `procedures.sql`
4. `triggers.sql`
5. `views.sql`
6. `seed.sql`
7. `analytics.sql` (For reporting purposes)
