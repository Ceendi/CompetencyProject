from sqlalchemy.orm import Session
from app.db.models import Film

def get_film(db: Session, film_id: int) -> Film | None:
    return db.query(Film).filter(Film.id == film_id).first()

def get_film_by_url(db: Session, url: str) -> Film | None:
    return db.query(Film).filter(Film.url == url).first()

def create_film(db: Session, url: str) -> Film:
    db_film = get_film_by_url(db, url)
    if db_film:
        return db_film
    db_film = Film(url=url)
    db.add(db_film)
    db.commit()
    db.refresh(db_film)
    return db_film
