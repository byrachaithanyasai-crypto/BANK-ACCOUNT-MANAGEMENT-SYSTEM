# BANKX - Smart Banking Database Management & Analytics System

## 1. Project Overview
BANKX is a premium, institutional-grade banking platform designed as a comprehensive DBMS capstone project.

## Installation & Running the Application

**Database Setup**
`sql
SOURCE database/schema.sql;
SOURCE database/indexes.sql;
SOURCE database/procedures.sql;
SOURCE database/triggers.sql;
SOURCE database/views.sql;
SOURCE database/seed.sql;
SOURCE database/analytics.sql;
`

**Backend Setup**
`ash
cd backend
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
`

**Frontend Setup**
`ash
cd frontend
npm install
cp .env.example .env
npm run dev
`
