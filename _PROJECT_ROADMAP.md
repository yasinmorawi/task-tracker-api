# 🚀 AI Engineering Platform Roadmap

> Project ini dikembangkan sebagai portofolio AI Engineering yang mencakup Backend Engineering, Machine Learning, Deployment, dan Monitoring.

---

# 📊 Project Status

| Phase                   | Status              |
| ----------------------- | ------------------- |
| Backend Development     | ✅ Completed (CRUD) |
| Code Review & Refactor  | ✅ Completed        |
| Testing                 | ✅ Completed        |
| Docker                  | ⏳ Pending          |
| Deployment              | ⏳ Pending          |
| ML Pipeline             | ⏳ Pending          |
| Deep Learning (PyTorch) | ⏳ Pending          |
| Monitoring              | ⏳ Pending          |

---

# 🎯 Current Sprint

## Sprint 1 — ORM Refactor

**Objective**

Menyatukan seluruh project agar hanya menggunakan SQLModel.

### Checklist

- [x] Audit seluruh model
- [x] Migrasi User ke SQLModel
- [x] Menghapus SQLAlchemy Declarative
- [x] Alembic membaca SQLModel.metadata
- [x] CRUD tetap berjalan

Status:

🟡 In Progress

---

## Sprint 2 — Database Layer

### Objective

Menyatukan seluruh dependency database.

Checklist

- [x] Konsisten menggunakan SQLModel Session
- [x] Konsisten menggunakan get_session()
- [x] Menghapus get_db() lama
- [x] Review transaction

Status

⚪ Pending

---

## Sprint 3 — Authentication

Checklist

- [x] Include auth router
- [x] Register
- [x] Login
- [x] JWT
- [x] Current User
- [x] Password Hash

Status

⚪ Pending

---

## Sprint 4 — Data Model

Checklist

- [ ] Tambahkan User Model
- [ ] Tambahkan user_id pada Task
- [ ] Foreign Key
- [ ] Relationship
- [ ] Ownership Validation

Status

⚪ Pending

---

## Sprint 5 — Architecture Cleanup

Checklist

- [ ] Pisahkan Model dan Schema
- [ ] Hapus dead code
- [ ] Rapikan import
- [ ] Konsistensi naming

Status

⚪ Pending

---

## Sprint 6 — Testing

Checklist

- [ ] Unit Test
- [ ] Integration Test
- [ ] Authentication Test
- [ ] Authorization Test
- [ ] Coverage Report

Status

⚪ Pending

---

## Sprint 7 — Docker

Checklist

- [ ] Dockerfile
- [ ] Docker Compose
- [ ] PostgreSQL Container
- [ ] Environment Variable

Status

⚪ Pending

---

## Sprint 8 — Deployment

Checklist

- [ ] Production Build
- [ ] Railway / Render
- [ ] Environment Secret
- [ ] HTTPS
- [ ] API Online

Status

⚪ Pending

---

# 🤖 Phase 2 — AI Engineering

## Sprint 9 — Business Understanding

- [ ] Business Problem
- [ ] Feasibility Study
- [ ] Success Metrics

---

## Sprint 10 — Data Engineering

- [ ] Import Dataset
- [ ] Cleaning
- [ ] EDA
- [ ] Feature Engineering

---

## Sprint 11 — Deep Learning (PyTorch)

- [ ] Tensor
- [ ] Dataset
- [ ] DataLoader
- [ ] Neural Network
- [ ] Loss Function
- [ ] Gradient Descent
- [ ] Backpropagation
- [ ] Optimizer

---

## Sprint 12 — ML Pipeline

- [ ] Training
- [ ] Validation
- [ ] Save Model
- [ ] Inference

---

## Sprint 13 — API Integration

- [ ] Load Model
- [ ] Prediction Endpoint
- [ ] Error Handling

---

## Sprint 14 — Monitoring

- [ ] Logging
- [ ] Metrics
- [ ] Model Versioning
- [ ] Performance Monitoring

---

# 📌 Technical Debt

| ID     | Priority | Status | Description                        |
| ------ | -------- | ------ | ---------------------------------- |
| BE-001 | Critical | ⏳     | Satukan ORM menjadi SQLModel       |
| BE-002 | Critical | ⏳     | Konsisten Session Database         |
| BE-003 | Critical | ⏳     | Include Auth Router                |
| BE-004 | High     | ⏳     | Tambahkan User ↔ Task Relationship |
| BE-005 | Medium   | ⏳     | Pisahkan Models & Schemas          |
| BE-006 | Medium   | ⏳     | Hapus Dead Code                    |

---

# 📅 Progress

## Backend

██████░░░░ 60%

## Refactor

░░░░░░░░░░ 0%

## Testing

░░░░░░░░░░ 0%

## Deployment

░░░░░░░░░░ 0%

## AI Engineering

░░░░░░░░░░ 0%

---

# 🎯 Goal v1.0

- Backend Production Ready
- Dockerized
- Tested
- Deployed
- Siap menjadi fondasi AI Engineering Platform
