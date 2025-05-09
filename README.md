# Tracker - Personal Finance Tracking Web Application

## 1. Environment

This project was developed using the standard course environment.

Python : 3.12.9
Django : 3.2.25

No additional packages are required outside of the base environment.


## Application Description

This application allows users to:

Track and manage expenses by category and tag
Set and monitor saving gaols
Create and monitor budgets
Manage recurring expenses
View transaction history logs
Receive budget notifications
Edit personal profile (timezone)

User communities:

Regular Users: Can manage their own data (expenses, goals, catgories, etc.)
Admin Users: (superuser): Full access via Django Admin App

## Authentication and Authorization 

All views are protected with Django authentication system. Regular users can only access their own data. Admin users can manage all data via Django Admin interface.

Superuser - username : tester, password : {iSchoolUI}
Regular user - username : tester2, password : {iSchoolUI}

## Testing Instructions

Login as tester or tester 2 after running the local server with python manage.py runserver, edit any of the expenses, budgets, goals, etc.


## Django Admin Customizations

1. Custom List Displays : ExpenseAdmin shows amount, category. amd date in the admin list
2. Search Fields : Tags and categories are searchable in admin for faster access
3. List Filters : Added filters by user or category in several admin panels

To test, log in with tester and go to the /admin url

## Final notes

I deployed originally through Vercel (wasn't sure if deployment was required for assignment), however the database (SQLite) does not work with Vercel so deployed application is not functional and can only be used locally.
