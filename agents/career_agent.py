from agents.sample_agent import base_agent
from utils.text_cleaner import clean_text

async def career_agent(tradition: str , query: str):
    #Base Prompt
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
    ##Agent Task
    prompt += f"""
    TASK:
    List traditional career roles related to {tradition}.

    Give:
    - 5 traditional roles, each on a new line, in this exact format:
    <Traditional Role Name>: <one sentence description>

    Rules:
    -Do not present other traditions as primary systems; mention them only as secondary or complementary if historically appropriate.
    - ONLY traditional roles that existed historically and still exist today
    - NO modern jobs, NO corporate titles, NO IT, NO startups
    - Use authentic Indian role names
    - Plain text only


    """

    text = await base_agent(prompt)
    lines = [l.strip() for l in text.split("\n") if ":" in l]

    careers = []
    for line in lines[:5]:
        title, desc = line.split(":", 1)
        careers.append({
            "title": clean_text(title),
            "description": clean_text(desc)
        })

    return careers