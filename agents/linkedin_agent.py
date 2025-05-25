# import asyncio
# import logging
# from typing import Dict, List, Any
# from smolagents import ToolCallingAgent, LiteLLMModel, tool
# from datetime import datetime
# import json

# logger = logging.getLogger(__name__)

# class LinkedinAgent:
#     """Creates professional LinkedIn posts from blog content"""
    
#     def __init__(self, api_key: str):
#         self.model = LiteLLMModel(
#             model_id="gemini/gemini-2.0-flash-exp",
#             api_key=api_key
#         )
        
#         self.agent = ToolCallingAgent(
#             tools=[self._create_professional_hook, self._add_linkedin_formatting],
#             model=self.model,
#             system_prompt=self._get_system_prompt()
#         )
    
#     def _get_system_prompt(self):
#         return """You are a LinkedIn content specialist for Agentic Loop, creating professional yet engaging posts.
        
#         Your style:
#         - Professional but approachable
#         - Educational and value-driven
#         - Mix of thought leadership and entertainment
#         - Uses storytelling when appropriate
#         - Encourages professional discussion
        
#         Post types to create:
#         1. Educational posts (from blog content)
#         2. Humorous but professional posts
#         3. Entertaining and relatable content
        
#         LinkedIn posts should be:
#         - 150-300 words
#         - Well-formatted with line breaks
#         - Include relevant hashtags (5-7)
#         - Have clear call-to-action
#         - Provide genuine value"""
    
#     @tool
#     def _create_professional_hook(self, topic: str, post_type: str) -> str:
#         """
#         Create professional hook for LinkedIn post
#         Args:
#             topic: The topic of the post
#             post_type: Type of post (educational, humorous, entertaining)
#         """
#         if post_type == "educational":
#             return f"ðŸŽ¯ Key insight about {topic} that every professional should know:\n\n"
#         elif post_type == "humorous":
#             return f"ðŸ˜„ A lighter take on {topic} (but with a serious point):\n\n"
#         else:
#             return f"ðŸ’¡ Real talk about {topic} in today's workplace:\n\n"
    
#     @tool
#     def _add_linkedin_formatting(self, content: str) -> str:
#         """
#         Add LinkedIn-appropriate formatting
#         Args:
#             content: The post content
#         """
#         # Add line breaks and formatting
#         formatted = content.replace(". ", ".\n\n")
#         formatted += "\n\n#AI #Innovation #FutureOfWork #TechLeadership #DigitalTransformation"
#         return formatted
    
#     async def generate_posts(self, blog_posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
#         """Generate 6 LinkedIn posts - 3 educational, 3 entertaining"""
#         try:
#             logger.info("Starting LinkedIn post generation...")
            
#             linkedin_posts = []
            
#             # Generate 3 educational posts from blog content
#             for i, blog in enumerate(blog_posts):
#                 educational_prompt = f"""
#                 Create a professional LinkedIn post from this blog content:
                
#                 Blog Title: {blog.get('title', 'AI Innovation')}
#                 Content excerpt: {blog.get('content', '')[:1000]}
                
#                 Requirements:
#                 - Professional yet engaging tone
#                 - 200-250 words
#                 - Include key insight or learning
#                 - End with thought-provoking question
#                 - Add 5-7 relevant hashtags
                
#                 Make it valuable and shareable for professionals.
#                 """
                
#                 educational_post = await asyncio.to_thread(
#                     self.agent.run,
#                     educational_prompt
#                 )
                
#                 linkedin_posts.append({
#                     "id": f"linkedin_edu_{i+1}",
#                     "content": educational_post,
#                     "type": "educational",
#                     "source_blog_id": blog["id"],
#                     "created_at": datetime.now().isoformat(),
#                     "metadata": {
#                         "estimated_read_time": "1 minute",
#                         "target_audience": "Tech professionals and leaders"
#                     }
#                 })
            
#             # Generate 3 entertaining posts (2 humorous, 1 relatable)
#             entertaining_prompts = [
#                 """Create a humorous but professional LinkedIn post about AI in the workplace.
#                 Include a funny observation or anecdote that professionals can relate to.
#                 Keep it light but insightful. 150-200 words.""",
                
#                 """Create another humorous LinkedIn post about common AI misconceptions.
#                 Make it funny but educational. Include a twist or unexpected insight.
#                 150-200 words.""",
                
#                 """Create a relatable LinkedIn post about the human side of working with AI.
#                 Share an experience or observation that resonates with professionals.
#                 Make it warm and encouraging. 200-250 words."""
#             ]
            
#             post_types = ["humorous", "humorous", "entertaining"]
            
#             for i, (prompt, post_type) in enumerate(zip(entertaining_prompts, post_types)):
#                 entertaining_post = await asyncio.to_thread(
#                     self.agent.run,
#                     prompt + "\n\nInclude 5-7 relevant hashtags. Make it engaging and shareable."
#                 )
                
#                 linkedin_posts.append({
#                     "id": f"linkedin_{post_type}_{i+1}",
#                     "content": entertaining_post,
#                     "type": post_type,
#                     "created_at": datetime.now().isoformat(),
#                     "metadata": {
#                         "estimated_reach": "High - entertaining content",
#                         "engagement_type": "Comments and shares"
#                     }
#                 })
            
#             logger.info(f"Generated {len(linkedin_posts)} LinkedIn posts")
#             return linkedin_posts
            
#         except Exception as e:
#             logger.error(f"LinkedIn post generation failed: {str(e)}")
#             raise



import asyncio
import logging
from typing import Dict, List, Any
from smolagents import CodeAgent, LiteLLMModel, tool
from datetime import datetime
import time

logger = logging.getLogger(__name__)

@tool
def create_professional_hook(topic: str, post_type: str) -> str:
    """
    Create professional hook for LinkedIn post
    Args:
        topic: The topic of the post
        post_type: Type of post (educational, humorous, entertaining)
    """
    time.sleep(60)
    if post_type == "educational":
        return f"🎯 Key insight about {topic} that every professional should know:\n\n"
    elif post_type == "humorous":
        return f"😄 A lighter take on {topic} (but with a serious point):\n\n"
    else:
        return f"💡 Real talk about {topic} in today's workplace:\n\n"

@tool
def add_linkedin_formatting(content: str) -> str:
    """
    Add LinkedIn-appropriate formatting
    Args:
        content: The post content
    """
    time.sleep(60)
    formatted = content.replace(". ", ".\n\n")
    formatted += "\n\n#AI #Innovation #FutureOfWork #TechLeadership #DigitalTransformation"
    return formatted

class LinkedinAgent:
    """Creates professional LinkedIn posts from blog content"""
    
    def __init__(self, api_key: str):
        self.model = LiteLLMModel(
            model_id="gemini/gemini-2.0-flash-exp",
            api_key=api_key
        )
        
        self.agent = CodeAgent(
            tools=[create_professional_hook, add_linkedin_formatting],
            model=self.model
        )
    
    async def generate_posts(self, blog_posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate 6 LinkedIn posts - 3 educational, 3 entertaining"""
        try:
            logger.info("Starting LinkedIn post generation...")
            
            linkedin_posts = []
            
            # Generate 3 educational posts from blog content
            for i, blog in enumerate(blog_posts):
                educational_prompt = f"""
                You are a LinkedIn content specialist for Agentic Loop, creating professional yet engaging posts.
                
                Your style:
                - Professional but approachable
                - Educational and value-driven
                - Mix of thought leadership and entertainment
                - Uses storytelling when appropriate
                - Encourages professional discussion
                
                Create a professional LinkedIn post from this blog content:
                
                Blog Title: {blog.get('title', 'AI Innovation')}
                Content excerpt: {str(blog.get('content', ''))[:1000]}
                
                Requirements:
                - Professional yet engaging tone
                - 200-250 words
                - Include key insight or learning
                - End with thought-provoking question
                - Add 5-7 relevant hashtags
                
                Make it valuable and shareable for professionals.
                LinkedIn posts should be 150-300 words, well-formatted with line breaks, and provide genuine value.
                """
                time.sleep(60)
                educational_post = await asyncio.to_thread(
                    self.agent.run,
                    educational_prompt
                )
                
                linkedin_posts.append({
                    "id": f"linkedin_edu_{i+1}",
                    "content": str(educational_post),
                    "type": "educational",
                    "source_blog_id": blog["id"],
                    "created_at": datetime.now().isoformat(),
                    "metadata": {
                        "estimated_read_time": "1 minute",
                        "target_audience": "Tech professionals and leaders"
                    }
                })
            
            # Generate 3 entertaining posts
            entertaining_prompts = [
                """You are a LinkedIn content specialist for Agentic Loop. Create a humorous but professional LinkedIn post about AI in the workplace.
                Include a funny observation or anecdote that professionals can relate to.
                Keep it light but insightful. 150-200 words. Include 5-7 relevant hashtags. Make it engaging and shareable.""",
                
                """You are a LinkedIn content specialist for Agentic Loop. Create another humorous LinkedIn post about common AI misconceptions.
                Make it funny but educational. Include a twist or unexpected insight.
                150-200 words. Include 5-7 relevant hashtags. Make it engaging and shareable.""",
                
                """You are a LinkedIn content specialist for Agentic Loop. Create a relatable LinkedIn post about the human side of working with AI.
                Share an experience or observation that resonates with professionals.
                Make it warm and encouraging. 200-250 words. Include 5-7 relevant hashtags. Make it engaging and shareable."""
            ]
            
            post_types = ["humorous", "humorous", "entertaining"]
            
            for i, (prompt, post_type) in enumerate(zip(entertaining_prompts, post_types)):
                time.sleep(60)
                entertaining_post = await asyncio.to_thread(
                    self.agent.run,
                    prompt
                )
                
                linkedin_posts.append({
                    "id": f"linkedin_{post_type}_{i+1}",
                    "content": str(entertaining_post),
                    "type": post_type,
                    "created_at": datetime.now().isoformat(),
                    "metadata": {
                        "estimated_reach": "High - entertaining content",
                        "engagement_type": "Comments and shares"
                    }
                })
                time.sleep(60)
            
            logger.info(f"Generated {len(linkedin_posts)} LinkedIn posts")
            return linkedin_posts
            
        except Exception as e:
            logger.error(f"LinkedIn post generation failed: {str(e)}")
            raise