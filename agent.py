import os
import json
from openai import OpenAI
from tools import generate_slide_content, fetch_image, create_slide, build_ppt, get_llm_client_and_model

class AutoPPTAgent:
    def __init__(self):
        self.client, self.model = get_llm_client_and_model()

    def plan_slides(self, topic: str, num_slides: int) -> list:
        """
        Plans the slide subtopics based on the main topic.
        """
        prompt = f"""
        You are an expert presentation planner.
        Main Topic: {topic}
        Number of Slides: {num_slides}
        
        Provide exactly {num_slides} logical subtopics for a presentation on this topic.
        Output MUST be a JSON object with a single key "subtopics" containing an array of strings. Example:
        {{
            "subtopics": [
                "Introduction to Topic",
                "Core Concepts",
                "Conclusion"
            ]
        }}
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            content = response.choices[0].message.content
            return json.loads(content).get("subtopics", [])
        except Exception as e:
            print(f"Error planning slides: {e}")
            return [f"Section {i+1}" for i in range(num_slides)]

    def generate_ppt(self, topic: str, num_slides: int, file_name: str):
        print(f"--- Starting Auto PPT Agent ---")
        print(f"Topic: {topic}")
        print(f"Planning {num_slides} slides...")
        
        subtopics = self.plan_slides(topic, num_slides)
        if not subtopics:
            print("No subtopics generated. Aborting.")
            return None
            
        print(f"Plan generated: {subtopics}")
        
        final_slides = []
        for i, subtopic in enumerate(subtopics):
            print(f"\nGenerating Slide {i+1}: {subtopic}")
            
            # Content Generator Tool
            content = generate_slide_content(topic, subtopic)
            title = content.get("title", subtopic)
            bullets = content.get("bullets", [])
            
            # Image Fetch Tool
            image_query = f"{topic} {title}"
            print(f"  Fetching image for query: {image_query}")
            image_url = fetch_image(image_query)
            
            # Slide Structurer Tool
            slide = create_slide(title, bullets, image_url)
            final_slides.append(slide)
            
            print(f"  Slide {i+1} structure created.")
            
        print(f"\nBuilding PPT file...")
        
        # Output Generator & PPT Builder Tool
        output_path = build_ppt(final_slides, file_name)
        print(f"Success! Presentation saved to: {output_path}")
        return output_path
