from agents.sample_agent import base_agent
from utils.text_cleaner import clean_text

async def knowledge_agent(tradition: str, query: str):
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
Explain {tradition} as Indian traditional knowledge.

Give:
- One short paragraph overview
- 5 core concepts, each on a new line, in this format:
  <Actual Concept Title>: <one sentence explanation>

Rules:
- Do not present other traditions as primary systems; mention them only as secondary or complementary if historically appropriate.
- Use REAL concept titles (e.g. Asanas, Pranayama, Dhyana)
- Do NOT use placeholders like "Concept Name"
- No markdown
- No bullets
- Plain text only

"""

    text = await base_agent(prompt)

    if not text:
        return {"error": "Empty response from model"}

    lines = [l.strip() for l in text.split("\n") if l.strip()]

    # 1️⃣ First paragraph = overview
    overview = lines[0]

    # 2️⃣ Extract ONLY lines with ":"
    concepts = []
    for line in lines[1:]:
        if ":" in line:
            title, desc = line.split(":", 1)
            concepts.append({
              "title": clean_text(title),
              "description": clean_text(desc)
            })

        if len(concepts) == 5:
            break

    return {
        "overview": overview,
        "core_concepts": concepts
    }
