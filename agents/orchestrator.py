import asyncio
from agents.knowledge import knowledge_agent
from agents.career_agent import career_agent
from agents.learning_agent import learning_agent
from agents.cultural_ethical_agent import cultural_ethical_agent

CACHE={}
async def analyze_tradition(tradition: str, query: str):
    key = f"{tradition.lower()}::{query.lower()}"

    if key in CACHE:
        return CACHE[key]
    (
        knowledge,
        careers,
        learning_roadmap,
        cultural_guidelines
    ) = await asyncio.gather(
        knowledge_agent(tradition, query),
        career_agent(tradition, query),
        learning_agent(tradition, query),
        cultural_ethical_agent(tradition, query),
    )

    result= {
        "tradition": tradition,
        "overview": knowledge["overview"],
        "core_concepts": knowledge["core_concepts"],
        "careers": careers,
        "learning_roadmap": learning_roadmap,
        "cultural_guidelines": cultural_guidelines
    }
    CACHE[key]=result
    return result