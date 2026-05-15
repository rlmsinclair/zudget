# Zudget

Hackathon project: a casino platform where every player's bankroll is their actual budget. Voted most original idea.

## Concept

Normal budgeting apps are boring — you set a budget and feel bad when you exceed it. Zudget gamifies it: your spending limit *is* your stake. You invest it into a shared casino pool, and the house edge means the group as a whole loses money slowly, creating natural spending friction that's actually fun.

## Features

- Group-based casino play (each group shares a bankroll)
- Graph generation for spending/balance history
- User registration and login with bcrypt
- PostgreSQL persistence
- Admin scraper integration

## Stack

- **Flask** + Flask-Login + Flask-WTF
- **SQLAlchemy** + **PostgreSQL**
- **Flask-Bcrypt** — password hashing
- Custom graph generation (`graph_gen.py`)
- **Gunicorn** for production

## Related

- [zudget_mobile](https://github.com/rlmsinclair/zudget_mobile) — Kivy mobile version
