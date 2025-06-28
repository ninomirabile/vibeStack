# 🧱 VibeStack – Fullstack Starter Kit (Flutter + FastAPI)

> Acceleratore di sviluppo per progetti moderni, cross-platform e modulari. Costruito per chi scrive codice ogni giorno.

---

## 🚀 Cos'è VibeStack?

VibeStack è un progetto starter **fullstack** che combina:
- **Flutter** (Web, Mobile, Desktop)
- **FastAPI** (Python 3.11)

Con architettura **modulare**, supporto **multi-piattaforma** e setup **Docker/CI** già pronti.

Perfetto per MVP, prototipi, sviluppo R&D o come base personalizzabile.

---

## ⚙️ Stack Tecnologico

### Frontend (Flutter)
- Material 3
- State Management con BLoC
- Codegen: `freezed`, `json_serializable`, `flutter_gen`
- Routing modulare (GoRouter)
- UI responsive & testata

### Backend (FastAPI)
- Python 3.11 + FastAPI
- Autenticazione JWT (con refresh)
- SQLAlchemy 2 + Pydantic
- Hashing password sicuro con `bcrypt`
- Healthcheck (`/health`) e route modulari
- Test automatizzati (unit e integrazione)

### DevOps & Tooling
- Docker Compose
- CI/CD con GitHub Actions
- Makefile per operazioni rapide
- Linting: `ruff`, `black`
- Gestione `secrets` via `.env`

---

## 📦 Come usarlo

```bash
# Clona il repo
$ git clone https://github.com/ninomirabile/vibeStack

# Lancia tutto (frontend + backend + db)
$ make up

# Accedi a:
# - Frontend: http://localhost:3000
# - Backend: http://localhost:8000/docs
```

---

## 🎯 Per chi è pensato

✔️ Sviluppatori singoli che vogliono partire da una base solida  
✔️ Team che cercano un'architettura pulita per progetti condivisi  
✔️ Formatori o mentor che vogliono un progetto da far estendere  
✔️ Chi esplora la sinergia Flutter + Python (non sempre ovvia!)

---

## 📈 Roadmap

- [ ] OAuth login (Google, GitHub)
- [ ] Verticalizzazione task manager / mini CRM
- [ ] Deploy demo pubblico (Railway / Render)
- [ ] Moduli riutilizzabili su pub.dev

---

## 🤝 Contribuire

Pull request benvenute! Oppure forkalo, usalo, e dammi feedback. 
È un progetto vivo, pensato per imparare, creare e migliorare insieme.

---

## 🧠 Filosofia

> "Non è (solo) un template. È un *vibe* di sviluppo."

Architettura pulita, strumenti moderni, produttività reale. Se anche tu sviluppi pensando all’eleganza del codice, sei nel posto giusto.

---

## 📎 Link utili

- 🔗 [Repo GitHub](https://github.com/ninomirabile/vibeStack)
- 📸 Screenshot e prompt iniziale su LinkedIn (in arrivo)

---

**Licenza**: MIT

---

📬 _Hai dubbi o vuoi proporre una collaborazione?_  
Scrivimi direttamente qui su GitHub o su [LinkedIn](https://www.linkedin.com/in/antoninomirabile)