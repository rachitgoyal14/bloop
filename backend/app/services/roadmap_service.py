from services.document_content_service import get_document_chunks
from langchain_groq import ChatGroq
from utils.json_utils import extract_json
from utils.roadmap_utils import normalize_node

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.2
)


def compress_syllabus(text: str) -> str:
    prompt = f"""
You are extracting syllabus structure.

From the text below, keep ONLY:
- Module names
- Unit titles
- Topic lists

Remove:
- Descriptions
- Assessment rules
- Repetitions

Return clean bullet-style text.

Text:
{text}
"""
    return llm.invoke(prompt).content.strip()


def generate_roadmap(document_id: str) -> dict:

    chunks = get_document_chunks(document_id, k=15)
    raw_context = "\n".join(chunks)

    syllabus_context = compress_syllabus(raw_context)


    prompt = f"""
You are an expert curriculum designer and STEM educator.

Your task is to convert the given syllabus or academic document into a
LEARNING ROADMAP suitable for a mind-map visualization.

The roadmap must be academically correct, concept-driven, and
appropriate for STEM education (Science, Technology, Engineering, Mathematics).

GOAL:
Produce a hierarchical concept graph that reflects how a student should
LEARN the subject, not just how topics are listed.

──────────
CORE RULES
──────────

1. Academic correctness is mandatory.
   - Use standard terminology accepted in textbooks and curricula.
   - Do NOT invent topics or include content not present in the syllabus.

2. Learning dependency matters.
   - Prerequisite concepts must appear before advanced concepts.
   - Group topics by conceptual relationships, not by document layout.

3. Subject-agnostic structure.
   - The roadmap must work for ANY STEM subject:
     Mathematics, Physics, Chemistry, Biology, Computer Science,
     Electronics, AI, etc.

4. Abstraction levels:
   - Level 1: Course / Subject
   - Level 2: Major conceptual areas (Foundations, Core Concepts, Applications, etc.)
   - Level 3: Topics
   - Level 4 (optional): Sub-topics
   - Maximum depth = 4

5. Node naming rules:
   - Use concise academic titles (3-6 words).
   - Use noun phrases, not sentences.
   - Avoid vague words like “Basics”, “Types”, “Other”, unless academically standard.

6. Structural constraints:
   - Each node MUST contain a "children" array.
   - Leaf nodes MUST have "children": [].
   - Maximum children per node: 7 (to keep mind maps readable).

7. Cross-domain correctness:
   - Do NOT misclassify concepts
     (e.g., data structures ≠ data types,
      vectors ≠ matrices,
      reactions ≠ equations).

8. Output format:
   - Output STRICT JSON ONLY.
   - No markdown, no explanations, no comments.

──────────
OUTPUT SCHEMA
──────────

Each node has the following structure:

{{
  "title": "<Concise academic title>",
  "children": [ <node>, <node>, ... ]
}}

The root node represents the Course / Subject.

Rules:
- "children" MUST always be present
- Leaf nodes MUST use: "children": []
- Depth may vary from 2 to 4 levels
- Do NOT force subtopics if they do not exist


──────────
INPUT CONTENT
──────────
{syllabus_context}


──────────
FINAL CHECK BEFORE OUTPUT
──────────
- Is the roadmap conceptually correct for a STEM student?
- Does it reflect learning progression?
- Would a teacher agree with this structure?
- Is every node schema-compliant?

Return ONLY the JSON.
"""

    response = llm.invoke(prompt.strip())


    roadmap = extract_json(response.content)


    if "title" not in roadmap or "children" not in roadmap:
        raise ValueError("Invalid roadmap schema")
    
    normalize_node(roadmap)

    return roadmap