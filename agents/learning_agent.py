from agents.sample_agent import base_agent


async def learning_agent(tradition: str, query: str):
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
- Do not present other traditions as primary systems; mention them only as secondary or complementary if historically appropriate.
Use ONLY the following fixed duration buckets:
- Beginner: 6–12 months
- Intermediate: 1–2 years
- Advanced: 2–4 years
- Expert: 5+ years

Do NOT invent new durations.
Do NOT change wording.
Use EXACT text as given.
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
Create a COMPLETE traditional learning roadmap for {tradition}
from Beginner to Expert / Teacher level.

You MUST follow ALL rules below.

STRUCTURE RULES (MANDATORY):
- Output EXACTLY 6 phases
- EACH phase MUST follow the template exactly
- EACH phase MUST have EXACTLY 3 key activities
- EACH key activities only for one lines.
- Do NOT add or remove sections
- Do NOT add explanations, separators, or extra text
- Do NOT stop mid-phase
- Do NOT use placeholders like "Concept Name"
- No markdown
- No bullets
- Plain text only
- If you cannot complete all phases correctly, output NOTHING

KEY ACTIVITIES RULES (VERY STRICT):

- For EACH learning phase, generate EXACTLY 3 key activities
- EACH key activity MUST be:
  • ONE single short line only
  • Maximum 8–10 words
  • NO commas
  • NO explanations
  • NO examples
  • NO sub-points
  • NO punctuation except full stop at end (optional)
- Each key activity must describe ONE clear action only
- If more than one action is needed, simplify it into one action
- Do NOT write paragraphs
- Do NOT write lists inside activities
- Do NOT exceed 3 activities under any condition

EXAMPLES (FOLLOW THIS STYLE):

GOOD:
- Daily practice of foundational asanas
- Study yamas and niyamas discipline
- Basic pranayama breath awareness

BAD:
- Practice asanas and pranayama together ❌
- Study Yoga Sutras with explanations ❌
- Learn ethics discipline and meditation deeply ❌

ALLOWED DURATIONS (USE ONLY THESE, EXACT TEXT):
- Beginner: 6–12 months
- Intermediate: 1–2 years
- Advanced: 2–4 years
- Expert: 5+ years

TEMPLATE (repeat exactly 6 times):

PHASE: <Phase Name>
LEVEL: <Beginner | Intermediate | Advanced | Expert>
DURATION: <one of the allowed durations>

DESCRIPTION:
<one concise paragraph, 2–3 sentences>

KEY ACTIVITIES:
- <activity 1>
- <activity 2>
- <activity 3>

"""
    
    text = await base_agent(prompt)
    print("text",text)
    blocks = text.split("PHASE:")
    roadmap = []

    blocks = text.split("PHASE:")
    for block in blocks[1:]:
        try:
            phase = block.split("LEVEL:")[0].strip()

            level = block.split("LEVEL:")[1].split("DURATION:")[0].strip()

            duration = block.split("DURATION:")[1].split("DESCRIPTION:")[0].strip()

            description = block.split("DESCRIPTION:")[1].split("KEY ACTIVITIES:")[0].strip()

            activities_raw = block.split("KEY ACTIVITIES:")[1]
            activities = [
                a.strip("- ").strip()
                for a in activities_raw.split("\n")
                if a.strip().startswith("-")
            ]

            roadmap.append({
                "phase": phase,
                "level": level,
                "duration": duration,
                "description": description,
                "key_activities": activities
            })
        except Exception:
            continue
    if len(roadmap) < 6:
        print(f"⚠️ Incomplete roadmap generated: {len(roadmap)} phases")
    return roadmap

