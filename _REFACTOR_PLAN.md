# Backend Refactor Plan v1.0

## Tujuan

Membuat backend konsisten menggunakan SQLModel sebelum masuk ke tahap testing.

---

## Sprint 1 - ORM

- [x] Samakan seluruh model menggunakan SQLModel
- [x] Hapus penggunaan SQLAlchemy Declarative
- [x] Pastikan Alembic membaca SQLModel.metadata

---

## Sprint 2 - Database

- [x] Konsisten menggunakan satu dependency database
- [x] Konsisten menggunakan Session SQLModel

---

## Sprint 3 - Authentication

- [x] Perbaiki auth router
- [x] Tambahkan auth ke main.py
- [x] Review JWT dan dependency

---

## Sprint 4 - Data Model

- [x] Tambahkan user_id pada Task
- [x] Tambahkan Foreign Key
- [x] Tambahkan Relationship User ↔ Task

---

## Sprint 5 - Cleanup

- [x] Pisahkan Model dan Schema
- [x] Hapus dead code
- [x] Rapikan import

---

## Sprint 6 - Ready for Testing

- [x] Backend siap masuk tahap testing
