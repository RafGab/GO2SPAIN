import os
import sqlite3

DATABASE_NAME = os.getenv("DATABASE_PATH", "go2spain.db")


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS study_leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            nationality TEXT,
            admission TEXT,
            city TEXT,
            start_date TEXT,
            message TEXT,
            contacted BOOLEAN NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            rating INTEGER,
            text TEXT NOT NULL,
            published BOOLEAN NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Contador de visitas anónimo: solo cuántas veces se carga cada página
    # por día y de qué tipo de sitio llega la gente. No guarda IP ni nada
    # que identifique a la persona.
    connection.execute("""
        CREATE TABLE IF NOT EXISTS visits (
            day TEXT NOT NULL,
            page TEXT NOT NULL,
            source TEXT NOT NULL,
            count INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (day, page, source)
        )
    """)

    connection.commit()
    connection.close()
