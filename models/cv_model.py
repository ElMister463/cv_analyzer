from pydantic import BaseModel, Field

class AnalysisCV( BaseModel ):
    """
    Docstring for AnalysisCV

    Modelo de datos para el análisis completo de un CV
    """

    name_candidate: str = Field( 
        description = "Nombre completo del candidato extraido del CV.")
    years_experience: int = Field( 
        description = "Años totales de experiencia laboral relevante.")
    key_skills: list[str] = Field( 
        description = "Lista de las 5-7 habilidades del candidato para el puesto." )
    education: str = Field( 
        description = "Nivel educarivo más alto y especilización principal del candidato." )
    relevant_experience: str = Field( 
        description = "Resumen conciso de la experiencia más relevante del candidato." )
    strengths: list[str] = Field( 
        description = "3-5 principales fortalezas del candidato basadas en su perfil." )
    area_improvement: list[str] = Field( 
        description = "2-4 áreas donde el candidato podría mejorar." )
    adjustment_percentage: int = Field( 
        description = "Porcentaje de ajuste al puesto (0-100) basado en experiencia, habilidades y formación.", 
                                       ge = 0, le = 100 )
    



