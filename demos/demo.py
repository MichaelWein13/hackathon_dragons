from contradiction_detection.detector import ContradictionDetector

API_KEY = "put_own_API_key_here"
# Replace with your own OpenAI API key

# Example paragraphs for testing
text1 = """
The mountain village of Erengrove is famous for its breathtaking sunrises and serene, untouched landscapes. Tourists often visit in the early spring to hike its winding trails and breathe the crisp, pine-scented air. Local residents, fiercely protective of their traditions, still rely on wood-burning stoves for heat and gather for communal meals in the town square every Sunday. The village has remained largely unchanged for over a century, resisting modern development and clinging to a lifestyle that many outsiders find idyllic and rare.
"""

text2 = """
Meanwhile, just last year, Erengrove was selected as one of the country's leading hubs for experimental 5G infrastructure and AI-driven drone delivery. The initiative, led by a consortium of tech firms, aimed to modernize rural logistics while boosting economic opportunities in isolated regions. Engineers installed signal towers at key points throughout the valley, and residents received tablets and smart speakers as part of the government’s digital inclusion program. The program’s success in this “forward-thinking” town has since become a model for similar efforts nationwide.
"""

# Initialize the contradiction detector
detector = ContradictionDetector(API_KEY)

# Run the contradiction check
result = detector.detect(text1, text2)

# Print the result
print(result)
