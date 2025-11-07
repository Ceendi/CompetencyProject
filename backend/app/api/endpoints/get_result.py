from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas import film as film_schema
from app.crud import crud_film

router = APIRouter()


@router.get(
    "/{film_id}",
    response_model=film_schema.Film
)
async def get_analysis_result_endpoint(
        film_id: int,
        db: Session = Depends(get_db)
):
    film_result = crud_film.get_film(db, film_id=film_id)

    if not film_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis result for the specified ID was not found."
        )

    return film_result
