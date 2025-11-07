from sqlalchemy.orm import Session
from app.db.models import Analysis
from app.schemas import AnalysisCreate


def create_analysis(db: Session, analysis_data: AnalysisCreate, film_id: int) -> Analysis:
    analysis_dict = analysis_data.model_dump()

    db_analysis = Analysis(**analysis_dict, film_id=film_id)
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    return db_analysis
