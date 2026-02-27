from langchain_openai import ChatOpenAI
from models.cv_model import AnalysisCV
from prompts.cv_prompts import crear_sistema_prompts
import streamlit as st


from config import OPENAI_API_KEY



def make_evaluator_cv():
    llm = ChatOpenAI(
    model = "gpt-4o-mini",
    temperature = 0.2,
    )

    structured_model = llm.with_structured_output( AnalysisCV )
    chat_prompt = crear_sistema_prompts()

    chain_evaluation = chat_prompt | structured_model

    return chain_evaluation

def evaluate_candidate( text_cv: str, job_description: str ) -> AnalysisCV:
    try:
        chain_evalutation = make_evaluator_cv()

        result = chain_evalutation.invoke({
            "text_cv": text_cv,
            "job_description": job_description,
        })

        return result
    
    except Exception as e:
        return AnalysisCV(
            name_candidate= "Error en procesamiento",
            years_experience = 0,
            key_skills= ["No se puede determinar"],
            education = "No se puede analizar",
            relevant_experience = "Error durante el análisis",
            strengths = ["Requiere revisión"],
            area_improvement = ["Verificar CV"],
            adjustment_percentage = 0,
        )
