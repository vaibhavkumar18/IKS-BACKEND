from agents.sample_agent import base_agent
from utils.text_cleaner import clean_text

async def cultural_ethical_agent(tradition: str, query: str):
    prompt = f"""
    You are helping build an educational hackathon project on Indian Traditional Knowledge.
    Be accurate, culturally respectful, and concise.
    Use plain text only. No markdown.

    IMPORTANT CONTEXT:
    The selected tradition is "{tradition}" and must always be treated as the source of truth.

    The learner may optionally provide a personal interest or goal.
    This interest is ONLY a soft preference.

    Rules:
    - NEVER switch to another tradition.
    - If the learner's interest conflicts with the selected tradition,
    reinterpret the interest so it fits WITHIN the selected tradition.
    - If reinterpretation is not possible, ignore the conflicting part
    and provide guidance strictly based on the selected tradition.
    """
    #If query Exists, add it to the prompt as soft guidance
    if query:
        prompt += f"""
    The learner has expressed this interest:
    "{query}"

    Use this interest only as soft guidance.
    Adapt the response subtly if relevant,
    but remain fully grounded in the "{tradition}" tradition.
    """
    prompt += f"""
TASK:
Provide cultural and ethical guidance for learning {tradition}.

Give:
- 4 guidelines
- Each guideline MUST be a single complete sentence
- Each guideline MUST be on a new line

Rules:
- Use cultural and ethical language, not devotional or religious language
-Do not present other traditions as primary systems; mention them only as secondary or complementary if historically appropriate.
- Do NOT use headings, colons, or sub-points
- Do NOT mention gods, worship, devotion, or sacredness
- Focus on discipline, humility, authenticity, and responsibility
- Avoid government, policy, or certification references
- Plain text only

"""
    text =await base_agent(prompt)
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    return [clean_text(l) for l in lines[:4]]
