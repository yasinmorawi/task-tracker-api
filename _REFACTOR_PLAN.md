# Backend Refactor Plan v1.0

## Tujuan
Membuat backend konsisten menggunakan SQLModel sebelum masuk ke tahap testing.

---

## Sprint 1 - ORM
- [x] Samakan seluruh model menggunakan SQLModel
- [ ] Hapus penggunaan SQLAlchemy Declarative
- [ ] Pastikan Alembic membaca SQLModel.metadata

---

## Sprint 2 - Database
- [ ] Konsisten menggunakan satu dependency database
- [ ] Konsisten menggunakan Session SQLModel

---

## Sprint 3 - Authentication
- [ ] Perbaiki auth router
- [ ] Tambahkan auth ke main.py
- [ ] Review JWT dan dependency

---

## Sprint 4 - Data Model
- [ ] Tambahkan user_id pada Task
- [ ] Tambahkan Foreign Key
- [ ] Tambahkan Relationship User ↔ Task

---

## Sprint 5 - Cleanup
- [ ] Pisahkan Model dan Schema
- [ ] Hapus dead code
- [ ] Rapikan import

---

## Sprint 6 - Ready for Testing
- [ ] Backend siap masuk tahap testing