# PittFit

> A mobile app to help University of Pittsburgh students plan workouts, check real-time Rec Center occupancy, locate equipment, and manage room bookings.

**Problem Statement:** *"The Pitt Recreation Center is often busy and disorganized, which makes planning workouts and utilizing equipment challenging."*

---

## Table of Contents

- [Overview](#overview)
- [Team](#team)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [Architecture](#architecture)
- [Branching Model](#branching-model)
- [Getting Started](#getting-started)
- [Project Status](#project-status)

---

## Overview

PittFit is a cross-platform mobile application (iOS & Android) that gives Pitt students a single place to:

- Check live Rec Center occupancy before making the trip
- Find exactly where equipment is on each floor
- Build and track personalized workout plans
- Reserve fitness rooms for clubs or groups
- View hours, announcements, and sports equipment availability

---

## Team

| Name | Sprint Role | Contributions |
|---|---| --- |
| Thomas Harrison | Product Owner (PO) | Configured database integration with SQLAlchemy, created initial `User` model, created occupancy and hours API endpoints, worked on presentation slides |
| Kambin Patris Zarei | Scrum Master (SM) | Implemented mock Pitt SSO auth flow, integrated auth endpoints with login screen and database, extended DB schema for core entities, created `.env.example` files |
| Ilya Abbasian | Developer | Implemented JWT session management, token validation for protected routes, logout via token blacklisting, auth unit tests |
| Harris Roberts | Developer | Scaffolded frontend and backend directories, installed core dependencies, implemented announcements API endpoint, removed empty database directory |
| Asliddin Nurboev | Developer | Set up project repo, defined branching model in README, implemented announcements UI screen, updated README for sprint 6 submission |
| Aidan O'Hara | Developer | Built login screen UI, implemented Occupancy and Announcements screens, added post-login navigation, recorded demo video |

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | React Native | Cross-platform iOS & Android app with reusable components and shared business logic |
| Backend | Python Flask | Lightweight framework to get REST endpoints running quickly with minimal boilerplate |
| Database | PostgreSQL | Reliable relational database for structured data; familiar to the whole team |
| Auth | Duo Auth API | Pitt students already use Duo — familiar auth flow reduces friction at login |
| Version Control | Git / GitHub | Industry-standard; team is most comfortable with this toolchain |
| Deployment / Hosting | AWS | Scalable cloud hosting to support the 30,000+ concurrent user requirement |

---

## Features

### MVP (Minimum Viable Product)
Pitt students can log in, check real-time Rec Center occupancy and equipment availability, and manage personalized workout plans — including the ability to reserve equipment and rooms.

| # | Feature | FR Reference |
|---|---|---|
| 1 | Login with Pitt credentials (SSO + Duo) | FR[1] |
| 2 | View real-time facility occupancy | FR[2.2] |
| 3 | View Rec Center map (equipment locations) | FR[2.3] |
| 4 | View hours of operation & announcements | FR[2.1], FR[2.4] |
| 5 | Create and edit custom workout templates | FR[3.0], FR[3.1], FR[3.2] |
| 6 | Track completed workouts | FR[4] |

### Additional Features

| # | Feature | FR Reference |
|---|---|---|
| 7 | View sports equipment availability | FR[5] |
| 8 | Submit and cancel fitness area booking requests | FR[6.0], FR[6.2] |
| 9 | Admin: approve/deny booking requests | FR[6.1] |
| 10 | Submit support tickets for equipment issues | FR[7.0] |
| 11 | Admin: handle support tickets | FR[7.1] |

---

## Architecture

PittFit uses a **Layered Architecture with Client/Service Separation**.

```
┌────────────────────────────────────────────┐
│         React Native Mobile App            │
│      (User Dashboard · Admin Panel)        │
└───────┬──────────┬──────────┬─────────┬───┘
        │          │          │         │
        ▼          ▼          ▼         ▼
┌─────────────────────────────────────────────┐
│           Python Flask REST API             │
│  Auth · Booking · Workout · Support         │
└──────────────────────┬──────────────────────┘
                       │
              ┌────────▼────────┐
              │   PostgreSQL    │
              │   (AWS RDS)     │
              └─────────────────┘
```

### Design Goals

| Goal | Metric | Technology Supporting It |
|---|---|---|
| Performance | User-facing actions < 2 seconds; occupancy refreshes within 30 seconds | Flask async endpoints, React Native local caching |
| Availability | 99.9% uptime during Rec Center operating hours | AWS auto-scaling and managed RDS |
| Data Consistency | Zero double bookings | PostgreSQL transactions and constraints |
| Usability | Common tasks in 3 clicks or fewer | React Native component reuse, clean navigation |
| Scalability | 30,000+ concurrent users | AWS horizontal scaling, stateless Flask services |

### Key Domain Classes

`User` · `Admin` · `PittRecCenter` · `RecCenterRoom` · `Equipment` · `WorkoutTemplate` · `WorkoutLog` · `RoomBooking` · `SupportTicket` · `Announcement`

---

## Branching Model

PittFit uses **GitHub Flow** adapted for Scrum sprints with a protected `main` branch and short-lived feature branches.

### Branch Structure

```
main                        ← production-ready code only
│
├── develop                 ← integration branch for each sprint
│   │
│   ├── feature/pitt-sso-login
│   ├── feature/occupancy-display
│   ├── feature/workout-templates
│   ├── bugfix/booking-double-entry
│   └── chore/update-readme
│
└── release/sprint-N        ← cut from develop at sprint end
```

### Branch Naming Convention

| Type | Pattern | Example |
|---|---|---|
| Feature | `feature/<description>` | `feature/room-booking` |
| Bug fix | `bugfix/<description>` | `bugfix/occupancy-refresh-crash` |
| Chore / docs | `chore/<description>` | `chore/add-sprint4-diagrams` |
| Release | `release/sprint-<n>` | `release/sprint-4` |
| Hotfix | `hotfix/<description>` | `hotfix/login-null-pointer` |

### Rules

1. **`main` is protected** — direct pushes are blocked; all merges require a PR with at least 1 approved review.
2. **`develop` is the sprint integration branch** — all feature branches are cut from `develop` and merged back via PR.
3. **Feature branches are short-lived** — merge within the same sprint; sync from `develop` if a branch runs long.
4. **PRs must pass CI checks** before merging (linting, tests).
5. **At sprint end**, `develop` is merged into `release/sprint-<n>` for the demo, then into `main`.
6. **Hotfixes** branch from `main` and merge back into both `main` and `develop`.

### Commit Message Format

```
feat: add real-time occupancy display
fix: prevent double booking on concurrent requests
docs: update architecture diagram for sprint 4
chore: configure GitHub Actions CI pipeline
refactor: extract booking validation to service layer
test: add unit tests for WorkoutTemplate class
```

---

## Getting Started

### Prerequisites

- Node.js ≥ 18 and npm
- Python ≥ 3.11
- PostgreSQL ≥ 15
- React Native / Expo CLI

### Frontend (React Native)

```bash
cd frontend
npm install
```

Copy the environment template and fill in your values:

```bash
cp .env.example .env
```

Start the app:

```bash
npx expo start
```

### Backend (Flask)

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Copy the environment template and fill in your values:

```bash
cp .env.example .env
```

Start the server:

```bash
flask run
```

### Database

```bash
# Create the database
psql -U postgres -c "CREATE DATABASE pittfit;"

# Run migrations
flask db upgrade
```

> Required environment variables for the backend and frontend are documented in `backend/.env.example` and `frontend/.env.example` respectively.

---

## Project Status

| Sprint | Deliverable | Status |
|---|---|---|
| Sprint 0 | Problem statement & team roles | ✅ Complete |
| Sprint 1 | Functional requirements, use cases, scenarios | ✅ Complete |
| Sprint 2 | Refined requirements, user stories, analysis object model | ✅ Complete |
| Sprint 3 | System architecture, subsystem decomposition, design goals | ✅ Complete |
| Sprint 4 | Tech stack, deployment plan, system infrastructure setup | ✅ Complete |
| Sprint 5 | Feature development, documentation, git workflows + branching strategies & pull requests | ✅ Complete |
| Sprint 6 | Cleanup, polish, final presentation & demo | ✅ Complete |

---

*University of Pittsburgh — CS 1530 Software Engineering*
