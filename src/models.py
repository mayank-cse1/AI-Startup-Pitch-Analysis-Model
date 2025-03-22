from pydantic import BaseModel, Field
from typing import List, Optional, Dict
# import google.generativeai as genai
from google import genai
from google.genai import types
import os
class ProblemStatement(BaseModel):
    clarity: int = Field(..., ge=1, le=5, description="How well is the problem explained? (1-5 scale)")
    relevance: int = Field(..., ge=1, le=5, description="Is the problem significant in the market? (1-5 scale)")
    feedback: str = Field(..., description="Suggestions to improve problem clarity and relevance")

class Solution(BaseModel):
    uniqueness: int = Field(..., ge=1, le=5, description="How unique is the solution? (1-5 scale)")
    feasibility: int = Field(..., ge=1, le=5, description="Can this solution be implemented effectively? (1-5 scale)")
    feedback: str = Field(..., description="Suggestions to improve uniqueness and feasibility")

class MarketAnalysis(BaseModel):
    market_size: str = Field(..., description="TAM, SAM, and SOM details")
    competitors: List[str] = Field(..., description="List of competitors")
    competitive_advantage: str = Field(..., description="What differentiates this startup from competitors?")
    feedback: str = Field(..., description="Recommendations on market positioning and competition")

class BusinessModel(BaseModel):
    revenue_streams: List[str] = Field(..., description="How does the startup generate revenue?")
    scalability: int = Field(..., ge=1, le=5, description="How scalable is the business model? (1-5 scale)")
    feedback: str = Field(..., description="Suggestions for improving scalability and revenue strategy")

class Traction(BaseModel):
    users: int = Field(..., description="Number of active users/customers")
    revenue: float = Field(..., description="Revenue generated so far")
    partnerships: List[str] = Field(..., description="List of partnerships/collaborations")
    feedback: str = Field(..., description="Suggestions to enhance traction and partnerships")

class Financials(BaseModel):
    funding_raised: float = Field(..., description="Total funding raised (USD)")
    burn_rate: float = Field(..., description="Monthly cash burn rate (USD)")
    revenue_projection: List[str] = Field(..., description="Projected revenue for upcoming years (e.g., Year 1, Year 2)")
    feedback: str = Field(..., description="Improvements for financial planning and projections")

class TeamMember(BaseModel):
    name: str = Field(..., description="Full name of the team member")
    role: str = Field(..., description="Role in the startup")
    experience: str = Field(..., description="Relevant experience")

class FundingAsk(BaseModel):
    amount_requested: float = Field(..., description="Funding amount requested (USD)")
    equity_offered: float = Field(..., ge=0, le=100, description="Percentage of equity offered")
    funding_usage: List[str] = Field(..., description="How the funds will be used")
    feedback: str = Field(..., description="Recommendations for refining the funding request")

class PitchQuality(BaseModel):
    design: int = Field(..., ge=1, le=5, description="Visual appeal of the pitch deck (1-5)")
    clarity: int = Field(..., ge=1, le=5, description="Clarity and conciseness of the pitch (1-5)")
    engagement: int = Field(..., ge=1, le=5, description="How engaging is the pitch? (1-5)")
    feedback: str = Field(..., description="Suggestions for improving pitch clarity, engagement, and design")

class StrengthWeaknessAnalysis(BaseModel):
    strengths: List[str] = Field(..., description="Key strengths of the startup and pitch deck")
    weaknesses: List[str] = Field(..., description="Key weaknesses or areas needing improvement")
    suggested_improvements: List[str] = Field(..., description="Personalized feedback on improving weaknesses")

class StartupPitchDeck(BaseModel):
    startup_name: str = Field(..., description="Name of the startup")
    industry: str = Field(..., description="Industry the startup operates in")
    problem_statement: ProblemStatement
    solution: Solution
    market_analysis: MarketAnalysis
    business_model: BusinessModel
    traction: Traction
    financials: Financials
    team: List[TeamMember]
    funding_ask: FundingAsk
    risks_and_challenges: List[str] = Field(..., description="Potential risks and challenges")
    pitch_quality: PitchQuality
    strength_weakness_analysis: StrengthWeaknessAnalysis
    final_evaluation: str = Field(..., description="Overall assessment of the startup")

def get_llm_score(content):
    prompt = f"""
    You are an AI working for a company that specializes in analyzing startup pitch decks.
    Given the following Start up pitch deck, analyze it to extract the information:

    Start Up Pitch Deck:
    {content}

    """
    # model = genai.GenerativeModel("gemini-1.5-pro")
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt,
        config={
            'response_mime_type': 'application/json',
            'response_schema': StartupPitchDeck,
        },
    )
    return response.text