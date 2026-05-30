import json
from app.database import SessionLocal, engine
from app import models
from datetime import date

# Crea las tablas si no existen
models.Base.metadata.create_all(bind=engine)

def seed():
    with open("matchaes.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    db = SessionLocal()

    try:
        # Evita duplicados si corres el script más de una vez
        existing = db.query(models.Match).count()
        if existing > 0:
            print(f"Ya hay {existing} partidos en la BD. Saltando seed.")
            return

        matches = []
        for m in data["matches"]:
            match = models.Match(
                num        = m.get("num"),
                round      = m["round"],
                date       = date.fromisoformat(m["date"]),
                time_local = m["time"],
                team1      = m["team1"],
                team2      = m["team2"],
                group      = m.get("group"),        # None si no existe
                ground     = m["ground"],
                tournament = data["name"],
            )
            matches.append(match)

        db.bulk_save_objects(matches)
        db.commit()
        print(f"✅ {len(matches)} partidos insertados correctamente.")

    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()