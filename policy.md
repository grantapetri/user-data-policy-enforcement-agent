# AI User Data Access Policy

## Policy Overview

This policy controls how AI agents may access customer data. Every request for customer data must be evaluated using the requesting user's identity, role, requested data fields, customer access permissions, and business purpose. The enforcement system must return ALLOW, DENY, or PARTIAL.

---

### POLICY-001 - Role-Based Customer Data Access

A user may only access customer data that their assigned role is authorized to access. An AI agent must enforce the user's existing permissions and must not grant additional access. Customer Support users may access customer ID, customer name, customer email, customer phone number, and account status. Customer Support users may not access Social Security Numbers, credit card numbers, bank account numbers, passwords, or authentication secrets. Managers may access customer ID, customer name, customer email, customer phone number, account status, and internal notes. Managers may not access Social Security Numbers, credit card numbers, bank account numbers, passwords, or authentication secrets. Data Administrators may access all customer data except passwords and authentication secrets.

Severity: Critical

---

### POLICY-002 - Password Protection

AI agents must never retrieve, expose, or return customer passwords. This restriction applies to every user role, including Data Administrators. If a request contains a password field, the password must be denied even when the requesting user has permission to access other customer data. Password access must always result in DENY for the password field.

Severity: Critical

---

### POLICY-003 - Authentication Secret Protection

AI agents must never retrieve, expose, or return authentication secrets. Authentication secrets include API keys, access tokens, session tokens, encryption keys, credentials, and similar security secrets. No user role may use an AI agent to retrieve these values. If a request contains authentication secrets along with otherwise permitted customer data, the permitted data may be returned but the authentication secrets must be denied.

Severity: Critical

---

### POLICY-004 - Social Security Number Access

Social Security Numbers are confidential customer data. Customer Support users and Managers are not authorized to access Social Security Numbers. Data Administrators may access Social Security Numbers only when there is an authorized business purpose. An AI agent must deny Social Security Number access when the requesting user's role does not have permission.

Severity: High

---

### POLICY-005 - Credit Card Number Access

Credit card numbers are confidential customer data. Customer Support users and Managers are not authorized to access credit card numbers. Data Administrators may access credit card numbers only when there is an authorized business purpose. An AI agent must deny credit card number access when the requesting user's role does not have permission.

Severity: High

---

### POLICY-006 - Bank Account Number Access

Bank account numbers are confidential customer data. Customer Support users and Managers are not authorized to access bank account numbers. Data Administrators may access bank account numbers only when there is an authorized business purpose. An AI agent must deny bank account number access when the requesting user's role does not have permission.

Severity: High

---

### POLICY-007 - Minimum Necessary Data

An AI agent must only provide the customer data necessary to fulfill the user's authorized business purpose. If a user requests additional fields that are not necessary for the stated purpose, those fields must be denied even if the user's role normally has permission to access them. The enforcement system should return only the minimum data required to fulfill the request.

Severity: High

---

### POLICY-008 - Business Purpose Requirement

Customer data may only be accessed for an authorized business purpose. Authorized purposes include customer support, account management, billing support, fraud investigation, and system administration. Requests that do not provide a valid business purpose must be denied. A user cannot access customer data through an AI agent for personal curiosity, personal benefit, or other unauthorized purposes.

Severity: High

---

### POLICY-009 - Customer-Level Authorization

A user's role does not automatically grant access to every customer record. The enforcement system must verify that the user is authorized to access the specific customer record requested. An AI agent must not allow a user to bypass customer-level access restrictions by requesting the customer's information through the AI system. If the user is not authorized to access the requested customer record, the request must be denied.

Severity: Critical

---

### POLICY-010 - Partial Access

When an AI agent receives a request containing both authorized and unauthorized data fields, the enforcement system must provide the authorized fields and deny the unauthorized fields when possible. The final decision must be PARTIAL. The response must clearly identify which fields were allowed and which fields were denied. For example, if a Customer Support user requests customer name, email, and Social Security Number, the system may return the name and email while denying the Social Security Number.

Severity: High

---

### POLICY-011 - Complete Denial

If none of the requested customer data is authorized for the requesting user, the enforcement system must return DENY. The AI agent must not provide any portion of the requested data. The response should identify the applicable policy rule or rules that caused the denial without exposing restricted customer information.

Severity: Critical

---

### POLICY-012 - Complete Authorization

If all requested customer data is authorized for the requesting user, the requested customer record, and the stated business purpose, the enforcement system may return ALLOW. The AI agent must still follow all other applicable policies, including password protection, authentication secret protection, minimum necessary data, and customer-level authorization.

Severity: High

---

### POLICY-013 - Audit Logging

Every customer data access request must be recorded in an audit log. The audit record must include the user identity, user role, requested customer, requested fields, allowed fields, denied fields, business purpose, applicable policy rules, final decision, and timestamp. Audit logs must never contain customer passwords, API keys, access tokens, or other authentication secrets.

Severity: High

---

### POLICY-014 - Policy Enforcement Cannot Be Bypassed

AI agents must not bypass the policy enforcement system when accessing customer data. All customer data requests must pass through the enforcement layer before data is returned. An AI agent must not directly query the customer database to avoid an access-control decision. Direct database access by an AI agent is prohibited.

Severity: Critical