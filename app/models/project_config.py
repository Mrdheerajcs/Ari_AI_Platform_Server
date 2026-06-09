from pydantic import BaseModel
from typing import List, Dict


class ProjectConfig(BaseModel):

    allowed_tables: List[str] = []

    hidden_fields: List[str] = []

    allowed_sources: List[str] = []

    question_mappings: Dict[str, str] = {}