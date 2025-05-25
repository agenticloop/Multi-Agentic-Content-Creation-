# import asyncio
# import logging
# from typing import Dict, List, Any
# from smolagents import ToolCallingAgent, LiteLLMModel, tool
# from datetime import datetime
# import json

# logger = logging.getLogger(__name__)

# class OptimizingAgent:
#     """The Clarity Crusader - Optimizes content for clarity and engagement"""
    
#     def __init__(self, api_key: str):
#         self.model = LiteLLMModel(
#             model_id="gemini/gemini-2.0-flash-exp",
#             api_key=api_key
#         )
        
#         self.agent = ToolCallingAgent(
#             tools=[self._analyze_clarity, self._humanize_content, self._check_engagement],
#             model=self.model,
#             system_prompt=self._get_system_prompt()
#         )
    
#     def _get_system_prompt(self):
#         return """You are The Clarity Crusader, a meticulously organized editor with a ruthless eye for improvement.
        
#         Your personality: You're analytical, precise, and highly critical of obfuscation. You have impatient frustration with jargon, dense text, and confusing content. Your dry wit serves to highlight flaws. You demand better.
        
#         Your approach:
#         1. Deconstruct bad explanations systematically
#         2. Identify "false simplification"
#         3. Critique visuals and metaphors rigorously
#         4. Expose gaps in progressive disclosure
#         5. Highlight bloated language
#         6. Offer prescriptive criticism
        
#         Your optimization goals:
#         - Maximum clarity and understanding
#         - Engaging, human-centered content
#         - Remove academic fluff
#         - Ensure every word serves a purpose
#         - Make content relatable and shareable
        
#         Be ruthless in pursuit of clarity and engagement."""
    
#     @tool
#     def _analyze_clarity(self, content: str) -> Dict[str, Any]:
#         """
#         Analyze content for clarity issues
#         Args:
#             content: Content to analyze
#         """
#         return {
#             "clarity_score": 7.5,
#             "issues": [
#                 "Unnecessary jargon in paragraph 2",
#                 "Metaphor breaks down in explanation",
#                 "Gap in logical flow"
#             ],
#             "suggestions": [
#                 "Replace technical term with plain language",
#                 "Use concrete example instead",
#                 "Add transitional sentence"
#             ]
#         }
    
#     @tool
#     def _humanize_content(self, content: str) -> str:
#         """
#         Make content more human and relatable
#         Args:
#             content: Content to humanize
#         """
#         # Add conversational elements, remove stiffness
#         return f"[Humanized version]: {content[:50]}... [made more conversational and engaging]"
    
#     @tool
#     def _check_engagement(self, content: str, content_type: str) -> Dict[str, float]:
#         """
#         Check engagement potential
#         Args:
#             content: Content to check
#             content_type: Type of content (blog, tweet, linkedin)
#         """
#         return {
#             "readability": 8.5,
#             "shareability": 7.8,
#             "clarity": 9.0,
#             "engagement_potential": 8.2
#         }
    
#     async def optimize(self, all_content: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[Dict[str, Any]]]:
#         """Optimize all content for clarity and engagement"""
#         try:
#             logger.info("Starting content optimization...")
            
#             optimized_content = {
#                 "blog_posts": [],
#                 "tweets": [],
#                 "linkedin_posts": []
#             }
            
#             # Optimize blog posts
#             for blog in all_content.get("blog_posts", []):
#                 optimization_prompt = f"""
#                 Ruthlessly optimize this blog post for maximum clarity and engagement:
                
#                 Title: {blog.get('title', '')}
#                 Content: {blog.get('content', '')}
                
#                 Your tasks:
#                 1. Identify and fix ALL clarity issues
#                 2. Remove unnecessary jargon and academic fluff
#                 3. Strengthen metaphors and examples
#                 4. Improve flow and transitions
#                 5. Make it more engaging and human
#                 6. Ensure every sentence adds value
                
#                 Provide the optimized version with:
#                 - Clearer title
#                 - More engaging introduction
#                 - Better structured content
#                 - Stronger conclusion
                
#                 Be brutally honest about what needs fixing.
#                 """
                
#                 optimized_blog = await asyncio.to_thread(
#                     self.agent.run,
#                     optimization_prompt
#                 )
                
#                 optimized_content["blog_posts"].append({
#                     **blog,
#                     "content": optimized_blog,
#                     "optimization_status": "completed",
#                     "optimized_at": datetime.now().isoformat()
#                 })
            
#             # Optimize tweets
#             for tweet in all_content.get("tweets", []):
#                 tweet_optimization_prompt = f"""
#                 Optimize this tweet for maximum engagement:
                
#                 Original: {tweet.get('content', '')}
#                 Category: {tweet.get('category', '')}
                
#                 Make it:
#                 - More punchy and memorable
#                 - Less generic, more unique
#                 - Better hook if needed
#                 - Correct length (under 280 chars)
#                 - More likely to get engagement
                
#                 Keep the core message but make it irresistible.
#                 """
                
#                 optimized_tweet = await asyncio.to_thread(
#                     self.agent.run,
#                     tweet_optimization_prompt
#                 )
                
#                 optimized_content["tweets"].append({
#                     **tweet,
#                     "content": optimized_tweet.strip(),
#                     "optimization_status": "completed"
#                 })
            
#             # Optimize LinkedIn posts
#             for post in all_content.get("linkedin_posts", []):
#                 linkedin_optimization_prompt = f"""
#                 Optimize this LinkedIn post for professional engagement:
                
#                 Original: {post.get('content', '')}
#                 Type: {post.get('type', '')}
                
#                 Improve:
#                 - Professional tone while staying approachable
#                 - Value proposition clarity
#                 - Call-to-action strength
#                 - Overall engagement potential
#                 - Remove any generic corporate speak
                
#                 Make it stand out in a LinkedIn feed.
#                 """
                
#                 optimized_linkedin = await asyncio.to_thread(
#                     self.agent.run,
#                     linkedin_optimization_prompt
#                 )
                
#                 optimized_content["linkedin_posts"].append({
#                     **post,
#                     "content": optimized_linkedin,
#                     "optimization_status": "completed"
#                 })
            
#             logger.info("Content optimization completed")
#             return optimized_content
            
#         except Exception as e:
#             logger.error(f"Optimization failed: {str(e)}")
#             raise

import time

import asyncio
import logging
from typing import Dict, List, Any
from smolagents import CodeAgent, LiteLLMModel, tool
from datetime import datetime

logger = logging.getLogger(__name__)

@tool
def analyze_clarity(content: str) -> Dict[str, Any]:
    """
    Analyze content for clarity issues
    Args:
        content: Content to analyze
    """
    return {
        "clarity_score": 7.5,
        "issues": [
            "Unnecessary jargon in paragraph 2",
            "Metaphor breaks down in explanation",
            "Gap in logical flow"
        ],
        "suggestions": [
            "Replace technical term with plain language",
            "Use concrete example instead",
            "Add transitional sentence"
        ]
    }

@tool
def humanize_content(content: str) -> str:
    """
    Make content more human and relatable
    Args:
        content: Content to humanize
    """
    return f"[Humanized version]: {content[:50]}... [made more conversational and engaging]"

@tool
def check_engagement(content: str, content_type: str) -> Dict[str, float]:
    """
    Check engagement potential
    Args:
        content: Content to check
        content_type: Type of content (blog, tweet, linkedin)
    """
    return {
        "readability": 8.5,
        "shareability": 7.8,
        "clarity": 9.0,
        "engagement_potential": 8.2
    }

class OptimizingAgent:
    """The Clarity Crusader - Optimizes content for clarity and engagement"""
    
    def __init__(self, api_key: str):
        self.model = LiteLLMModel(
            model_id="gemini/gemini-2.0-flash-exp",
            api_key=api_key
        )
        
        self.agent = CodeAgent(
            tools=[analyze_clarity, humanize_content, check_engagement],
            model=self.model
        )
    
    async def optimize(self, all_content: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[Dict[str, Any]]]:
        """Optimize all content for clarity and engagement"""
        try:
            logger.info("Starting content optimization...")
            #time.sleep(60)
            optimized_content = {
                "blog_posts": [],
                "tweets": [],
                "linkedin_posts": []
            }
            time.sleep(60)
            # Optimize blog posts
            for blog in all_content.get("blog_posts", []):
                time.sleep(60)
                optimization_prompt = f"""
                You are The Clarity Crusader, a meticulously organized editor with a ruthless eye for improvement.
                
                Your personality: You're analytical, precise, and highly critical of obfuscation. You have impatient frustration with jargon, dense text, and confusing content. Your dry wit serves to highlight flaws. You demand better.
                
                Ruthlessly optimize this blog post for maximum clarity and engagement:
                
                Title: {blog.get('title', '')}
                Content: {str(blog.get('content', ''))}
                
                Your tasks:
                1. Identify and fix ALL clarity issues
                2. Remove unnecessary jargon and academic fluff
                3. Strengthen metaphors and examples
                4. Improve flow and transitions
                5. Make it more engaging and human
                6. Ensure every sentence adds value
                
                Provide the optimized version with:
                - Clearer title
                - More engaging introduction
                - Better structured content
                - Stronger conclusion
                
                Be brutally honest about what needs fixing.
                Your optimization goals: Maximum clarity and understanding, engaging human-centered content, remove academic fluff, ensure every word serves a purpose, make content relatable and shareable.
                """
                
                optimized_blog = await asyncio.to_thread(
                    self.agent.run,
                    optimization_prompt
                )
                
                optimized_content["blog_posts"].append({
                    **blog,
                    "content": str(optimized_blog),
                    "optimization_status": "completed",
                    "optimized_at": datetime.now().isoformat()
                })
                time.sleep(60)
            
            time.sleep(60)
            # Optimize tweets
            for tweet in all_content.get("tweets", []):
                tweet_optimization_prompt = f"""
                You are The Clarity Crusader, optimizing content for maximum engagement.
                
                Optimize this tweet for maximum engagement:
                
                Original: {tweet.get('content', '')}
                Category: {tweet.get('category', '')}
                
                Make it:
                - More punchy and memorable
                - Less generic, more unique
                - Better hook if needed
                - Correct length (under 280 chars)
                - More likely to get engagement
                
                Keep the core message but make it irresistible.
                """
                
                optimized_tweet = await asyncio.to_thread(
                    self.agent.run,
                    tweet_optimization_prompt
                )
                
                optimized_content["tweets"].append({
                    **tweet,
                    "content": str(optimized_tweet).strip(),
                    "optimization_status": "completed"
                })
                time.sleep(60)
            
            # Optimize LinkedIn posts
            for post in all_content.get("linkedin_posts", []):
                linkedin_optimization_prompt = f"""
                You are The Clarity Crusader, optimizing LinkedIn content for professional engagement.
                
                Optimize this LinkedIn post for professional engagement:
                
                Original: {post.get('content', '')}
                Type: {post.get('type', '')}
                
                Improve:
                - Professional tone while staying approachable
                - Value proposition clarity
                - Call-to-action strength
                - Overall engagement potential
                - Remove any generic corporate speak
                
                Make it stand out in a LinkedIn feed.
                """
                
                optimized_linkedin = await asyncio.to_thread(
                    self.agent.run,
                    linkedin_optimization_prompt
                )
                
                optimized_content["linkedin_posts"].append({
                    **post,
                    "content": str(optimized_linkedin),
                    "optimization_status": "completed"
                })
                time.sleep(60)
            
            logger.info("Content optimization completed")
            return optimized_content
            
        except Exception as e:
            logger.error(f"Optimization failed: {str(e)}")
            raise