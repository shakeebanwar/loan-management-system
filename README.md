# Loan Management System

This is a loan management system that allows users to sign up, sign in, request loans, and track loan request status. It also includes functionality for managers to approve or reject loans and block users. Additionally, there is a notification feature to remind users of their upcoming loan due dates.

## Features

1. *Signup / Sign in Mechanism:* Users can sign up for an account or sign in if they already have one.

2. *Loan Request Status:* After logging in, users can view the status of their loan requests, which can be pending, approved, or rejected.

3. *Loan Request:* Users can request a loan with an amount that is a multiple of 500 (e.g., 500, 1000, 1500, 2000, etc.).

4. *Loan Due Date:* The system implements a due date for loans to track black-listed users or those with overdue payments.

5. *Restrictions on Multiple Loan Requests:* Users cannot create multiple loan requests within a single day.

6. *Restrictions on Concurrent Loan Requests:* Users cannot submit a new loan request if they have a previous loan application in progress or open.

7. *Loan Approval / Rejection:* Managers have the authority to approve or reject loan requests and can provide comments explaining their decisions.

8. *User Blocking:* Managers can block users from applying for loans.



## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/shakeebanwar/loan-management-system.git