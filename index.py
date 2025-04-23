import openai
import dotenv

dot_env = dotenv.dotenv_values(".env")
API_KEY = dot_env["OPENAI_API_KEY"]
MOVIE = dot_env["MOVIE"]
print(API_KEY, MOVIE)

openai.api_key = API_KEY

class ChatSession:
    def __init__(self, system_prompt="Imagine you are an expert storyteller and film critic.", model_name="gpt-4o"):
        self.messages = [{"role": "system", "content": system_prompt}]
        self.model_name = model_name

    def ask(self, prompt):
        self.messages.append({"role": "user", "content": prompt})
        response = openai.chat.completions.create(
            model=self.model_name,
            messages=self.messages
        )
        reply = response["choices"][0]["message"]["content"]
        self.messages.append({"role": "assistant", "content": reply})
        return reply

chat = ChatSession()

EXPERT_ANALYSIS_PROMPT = f"""
Analyze the plot of the movie {MOVIE} using the following parameters:
    
    Thematic Coherence – Does the story stay true to its themes and central message? Are the themes effectively developed?
    Narrative Structure – How well does the movie follow a compelling structure (e.g., three-act structure, nonlinear storytelling, etc.)? Are there any pacing issues?
    Emotional Depth & Character Arcs – Do the characters experience meaningful growth? Are their motivations and relationships well-developed?
    Pacing & Engagement – Does the movie maintain audience interest throughout, or are there slow or rushed sections?
    Dialogue & Writing – Are the dialogues natural, impactful, and reflective of the characters' personalities?
    Narrative Consistency & Logic – Are there plot holes or inconsistencies? Does the story follow its own internal logic?
    Symbolism & Subtext – Does the film use deeper storytelling elements (symbolism, metaphor, allegory) effectively?
"""

SHORTCOMINGS_PROMPT = f"""
Based on the above parameters, where do you see potential shortcomings or areas for improvement? Provide a critical but constructive evaluation of how these elements could be strengthened.
"""

JUSTIFICATIONS_PROMPT = f"""
What reasoning or evidence supports your analysis? If applicable, refer to widely recognized storytelling principles, film theory, or similar films that succeeded in these areas.
"""

FIXES_PROMPT = "For each identified shortcoming, suggest a refined or alternative approach that could enhance the plot and storytelling. These improvements should align with the film’s core themes and audience expectations."

REVISED_PLOT_PROMPT = "Using the suggested improvements, rewrite the plot in a more compelling way. Keep it concise yet engaging, ensuring the revised version strengthens the thematic depth, emotional resonance, and narrative consistency."

expert_analysis = chat.ask(EXPERT_ANALYSIS_PROMPT)
shortcomings = chat.ask(SHORTCOMINGS_PROMPT)
justifications = chat.ask(JUSTIFICATIONS_PROMPT)
fixes = chat.ask(FIXES_PROMPT)
revised_plot = chat.ask(REVISED_PLOT_PROMPT)

responses = {
    "expert_analysis": expert_analysis,
    "shortcomings": shortcomings,
    "justifications": justifications,
    "fixes": fixes,
    "revised_plot": revised_plot
}