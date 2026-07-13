# config.py
from pptx.util import Pt

MODEL = "llama-3.1-70b-versatile"
TEMPERATURE = 0
MAX_TOKENS = 4096

TITLE_FONT_SIZE = Pt(30)
SLIDE_FONT_SIZE = Pt(16)

CATEGORIES = [
    "Business", "Motivational", "Persuasive", "Demonstrative",
    "Informative", "Storytelling", "Academic", "Sales",
    "Instructional", "Progress", "Coach Style", "Connector Style",
    "Decision-Making", "Instructor Style", "Problem Solving"
]

SYSTEM_PROMPT = """You are an AI-Powered Presentation Generator..."""