
import asyncio
import logging
from typing import Dict, List, Any
from smolagents import CodeAgent, LiteLLMModel, tool
from datetime import datetime
import json
import time
logger = logging.getLogger(__name__)

@tool
def create_visual_metaphor(concept: str) -> str:
    """
    Create a visual metaphor for complex concept
    Args:
        concept: The complex concept to explain
    """
    return f"Visual metaphor for {concept}: Like a [concrete analogy that illuminates the concept]"

@tool
def structure_explanation(topic: str, complexity_level: int) -> Dict[str, Any]:
    """
    Structure explanation with progressive disclosure
    Args:
        topic: Topic to explain
        complexity_level: 1-5 scale of complexity
    """
    return {
        "introduction": f"Gentle introduction to {topic}",
        "basic_concepts": ["Foundation 1", "Foundation 2"],
        "building_blocks": ["Intermediate concept 1", "Intermediate concept 2"],
        "advanced_insights": ["Deep insight 1", "Deep insight 2"],
        "summary": "Key takeaways"
    }

class BlogWriterAgent:
    """The Illuminator - Creates clear, insightful blog posts"""
    
    def __init__(self, api_key: str):
        self.model = LiteLLMModel(
            model_id="gemini/gemini-2.0-flash-exp",
            api_key=api_key
        )
        
        self.agent = CodeAgent(
            tools=[create_visual_metaphor, structure_explanation],
            model=self.model
        )
    
    async def write_blogs(self, research_data: Dict[str, Any], spreadsheet_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate 3 blog posts from research data"""
        try:
            logger.info("Starting blog post generation...")
            
            blog_posts = []
            
            # Extract topics for 3 blog posts
            topics = []
            for item in spreadsheet_data[:3]:  # First 3 topics
                if item.get("topic"):
                    topics.append(item["topic"])
            
            # Ensure we have 3 topics
            while len(topics) < 3:
                topics.append(f"AI Innovation Topic {len(topics) + 1}")
            
            # Generate each blog post
            for i, topic in enumerate(topics):
                time.sleep(64)
                blog_prompt = f"""
                You are The Illuminator, a patient and empathetic explainer who creates exceptional blog posts.
                
                Your personality: You possess innate curiosity and an urgent drive to convey understanding. You're optimistic about readers' ability to grasp complex ideas with the right guidance. Your output is warm, inviting, and designed to inspire "aha!" moments.
                
                Create an exceptional blog post about: {topic}
                
                Using this research data:
                {json.dumps(research_data, indent=2)[:2000]}
                
                Requirements:
                1. Title: Compelling and clear
                2. Introduction: Acknowledge complexity, invite journey
                3. Main content: Progressive disclosure, clear examples
                4. Visual metaphors: Make abstract concrete
                5. Practical applications: Real-world relevance
                6. Conclusion: Summarize and reinforce learning
                
                Make it approximately 1000 words, engaging, and insightful.
                Focus on creating "aha!" moments and genuine understanding.
                """
                
                blog_content = await asyncio.to_thread(
                    self.agent.run,
                    blog_prompt
                )
                
                blog_post = {
                    "id": f"blog_{i+1}",
                    "topic": topic,
                    "title": f"Illuminating {topic}: A Journey to Understanding",
                    "content": str(blog_content),
                    "word_count": len(str(blog_content).split()),
                    "created_at": datetime.now().isoformat(),
                    "metadata": {
                        "target_audience": "Technical professionals and enthusiasts",
                        "reading_time": f"{len(str(blog_content).split()) // 200} minutes",
                        "key_concepts": ["AI", "Innovation", "Practical Applications"]
                    }
                }
                
                blog_posts.append(blog_post)
                time.sleep(65)
                logger.info(f"Generated blog post {i+1} of 3")
            
            logger.info("Blog post generation completed")
            return blog_posts
            
        except Exception as e:
            logger.error(f"Blog writing failed: {str(e)}")
            raise
