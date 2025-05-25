# import asyncio
# import logging
# from typing import Dict, List, Any
# from smolagents import ToolCallingAgent, DuckDuckGoSearchTool, LiteLLMModel, tool
# from datetime import datetime
# import json

# logger = logging.getLogger(__name__)

# class TwitterAgent:
#     """Creates engaging tweets from blog posts and web searches"""
    
#     def __init__(self, api_key: str):
#         self.model = LiteLLMModel(
#             model_id="gemini/gemini-2.0-flash-exp",
#             api_key=api_key
#         )
        
#         self.agent = ToolCallingAgent(
#             tools=[DuckDuckGoSearchTool(), self._craft_engaging_hook, self._add_hashtags],
#             model=self.model,
#             system_prompt=self._get_system_prompt()
#         )
    
#     def _get_system_prompt(self):
#         return """You are a Twitter content specialist for Agentic Loop, creating engaging AI-focused tweets.
        
#         Your style:
#         - Engaging and conversational, not robotic
#         - Informative yet accessible
#         - Mix of educational and entertaining
#         - Uses relevant hashtags sparingly
#         - Creates tweets that spark conversation
        
#         Tweet categories to create:
#         1. Engaging tweets with questions or calls to action
#         2. Motivational content about AI's potential
#         3. AI humor that's relatable and fun
#         4. Entertaining posts that humanize AI
#         5. Latest AI trends and updates
        
#         Keep tweets under 280 characters, punchy, and shareable."""
    
#     @tool
#     def _craft_engaging_hook(self, topic: str) -> str:
#         """
#         Create an engaging hook for a tweet
#         Args:
#             topic: The topic to create a hook for
#         """
#         hooks = [
#             f"ðŸ¤” Ever wondered how {topic} actually works?",
#             f"ðŸ’¡ Quick insight about {topic}:",
#             f"ðŸš€ The future of {topic} is here:",
#             f"âš¡ Breaking: New development in {topic}"
#         ]
#         return hooks[0]  # In production, this would be more sophisticated
    
#     @tool
#     def _add_hashtags(self, tweet: str, topic: str) -> str:
#         """
#         Add relevant hashtags to tweet
#         Args:
#             tweet: The tweet content
#             topic: The topic for hashtag relevance
#         """
#         hashtags = ["#AI", "#Innovation", "#TechTrends", "#FutureOfWork", "#AgenticLoop"]
#         # Add 2-3 relevant hashtags
#         return f"{tweet} {' '.join(hashtags[:3])}"
    
#     async def generate_tweets(self, blog_posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
#         """Generate 12 tweets - 6 from blogs, 6 from web search"""
#         try:
#             logger.info("Starting tweet generation...")
            
#             tweets = []
            
#             # Generate 6 tweets from blog posts (2 per blog)
#             for i, blog in enumerate(blog_posts):
#                 blog_content = blog.get("content", "")[:1000]  # First 1000 chars
                
#                 blog_tweet_prompt = f"""
#                 Create 2 engaging tweets from this blog post:
                
#                 Title: {blog.get('title', 'AI Innovation')}
#                 Content excerpt: {blog_content}
                
#                 Tweet 1: Educational/informative angle
#                 Tweet 2: Engaging question or thought-provoking angle
                
#                 Make them conversational, add appropriate emojis, under 280 chars each.
#                 """
                
#                 blog_tweets = await asyncio.to_thread(
#                     self.agent.run,
#                     blog_tweet_prompt
#                 )
                
#                 # Parse and structure the tweets
#                 tweet_lines = blog_tweets.strip().split('\n')
#                 for j, tweet_content in enumerate(tweet_lines[:2]):
#                     if tweet_content.strip():
#                         tweets.append({
#                             "id": f"tweet_blog_{i+1}_{j+1}",
#                             "content": tweet_content.strip(),
#                             "type": "blog_based",
#                             "source_blog_id": blog["id"],
#                             "category": "educational" if j == 0 else "engaging",
#                             "created_at": datetime.now().isoformat()
#                         })
            
#             # Generate 6 tweets from web search
#             web_tweet_prompt = """
#             Search for and create 6 engaging tweets about current AI trends:
            
#             1. One engaging tweet with a question about AI
#             2. One motivational tweet about AI's potential
#             3. Two AI humor tweets (funny, relatable)
#             4. One entertaining/relatable AI post
#             5. One tweet about latest AI trends/news
            
#             Each tweet should:
#             - Be under 280 characters
#             - Include relevant emojis
#             - Be conversational and engaging
#             - Spark conversation or shares
#             - Align with Agentic Loop's voice
#             """
            
#             web_tweets = await asyncio.to_thread(
#                 self.agent.run,
#                 web_tweet_prompt
#             )
            
#             # Parse web search tweets
#             web_tweet_lines = web_tweets.strip().split('\n')
#             categories = ["engaging", "motivational", "humor", "humor", "entertaining", "trends"]
            
#             for j, (tweet_content, category) in enumerate(zip(web_tweet_lines[:6], categories)):
#                 if tweet_content.strip():
#                     tweets.append({
#                         "id": f"tweet_web_{j+1}",
#                         "content": tweet_content.strip(),
#                         "type": "web_search",
#                         "category": category,
#                         "created_at": datetime.now().isoformat()
#                     })
            
#             # Ensure we have exactly 12 tweets
#             while len(tweets) < 12:
#                 tweets.append({
#                     "id": f"tweet_extra_{len(tweets)+1}",
#                     "content": "ðŸš€ AI is transforming how we work and create. What's your favorite AI tool? #AI #Innovation",
#                     "type": "filler",
#                     "category": "engaging",
#                     "created_at": datetime.now().isoformat()
#                 })
            
#             logger.info(f"Generated {len(tweets)} tweets")
#             return tweets[:12]  # Return exactly 12 tweets
            
#         except Exception as e:
#             logger.error(f"Tweet generation failed: {str(e)}")
#             raise

import asyncio
import logging
from typing import Dict, List, Any
from smolagents import CodeAgent, DuckDuckGoSearchTool, LiteLLMModel, tool
from datetime import datetime
import time

logger = logging.getLogger(__name__)

@tool
def craft_engaging_hook(topic: str) -> str:
    """
    Create an engaging hook for a tweet
    Args:
        topic: The topic to create a hook for
    """
    time.sleep(60)
    hooks = [
        f"🤔 Ever wondered how {topic} actually works?",
        f"💡 Quick insight about {topic}:",
        f"🚀 The future of {topic} is here:",
        f"⚡ Breaking: New development in {topic}"
    ]
    return hooks[0]

@tool
def add_hashtags(tweet: str, topic: str) -> str:
    """
    Add relevant hashtags to tweet
    Args:
        tweet: The tweet content
        topic: The topic for hashtag relevance
    """
    hashtags = ["#AI", "#Innovation", "#TechTrends", "#FutureOfWork", "#AgenticLoop"]
    time.sleep(60)
    return f"{tweet} {' '.join(hashtags[:3])}"

class TwitterAgent:
    """Creates engaging tweets from blog posts and web searches"""
    
    def __init__(self, api_key: str):
        self.model = LiteLLMModel(
            model_id="gemini/gemini-2.0-flash-exp",
            api_key=api_key
        )
        
        self.agent = CodeAgent(
            tools=[DuckDuckGoSearchTool(), craft_engaging_hook, add_hashtags],
            model=self.model
        )
    
    async def generate_tweets(self, blog_posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate 12 tweets - 6 from blogs, 6 from web search"""
        try:
            logger.info("Starting tweet generation...")
            
            tweets = []
            
            # Generate 6 tweets from blog posts (2 per blog)
            for i, blog in enumerate(blog_posts):
                time.sleep(60)
                blog_content = str(blog.get("content", ""))[:1000]
                
                blog_tweet_prompt = f"""
                You are a Twitter content specialist for Agentic Loop, creating engaging AI-focused tweets.
                
                Your style:
                - Engaging and conversational, not robotic
                - Informative yet accessible
                - Mix of educational and entertaining
                - Uses relevant hashtags sparingly
                - Creates tweets that spark conversation
                
                Create 2 engaging tweets from this blog post:
                
                Title: {blog.get('title', 'AI Innovation')}
                Content excerpt: {blog_content}
                
                Tweet 1: Educational/informative angle
                Tweet 2: Engaging question or thought-provoking angle
                
                Make them conversational, add appropriate emojis, under 280 chars each.
                Keep tweets under 280 characters, punchy, and shareable.
                """
                
                blog_tweets = await asyncio.to_thread(
                    self.agent.run,
                    blog_tweet_prompt
                )
                
                # Parse and structure the tweets
                tweet_lines = str(blog_tweets).strip().split('\n')
                for j, tweet_content in enumerate(tweet_lines[:2]):
                    if tweet_content.strip():
                        tweets.append({
                            "id": f"tweet_blog_{i+1}_{j+1}",
                            "content": tweet_content.strip(),
                            "type": "blog_based",
                            "source_blog_id": blog["id"],
                            "category": "educational" if j == 0 else "engaging",
                            "created_at": datetime.now().isoformat()
                        })
            
            # Generate 6 tweets from web search
            web_tweet_prompt = """
            You are a Twitter content specialist for Agentic Loop, creating engaging AI-focused tweets.
            
            Search for and create 6 engaging tweets about current AI trends:
            
            1. One engaging tweet with a question about AI
            2. One motivational tweet about AI's potential
            3. Two AI humor tweets (funny, relatable)
            4. One entertaining/relatable AI post
            5. One tweet about latest AI trends/news
            
            Each tweet should:
            - Be under 280 characters
            - Include relevant emojis
            - Be conversational and engaging
            - Spark conversation or shares
            - Align with Agentic Loop's voice
            """
            
            web_tweets = await asyncio.to_thread(
                self.agent.run,
                web_tweet_prompt
            )
            
            # Parse web search tweets
            web_tweet_lines = str(web_tweets).strip().split('\n')
            categories = ["engaging", "motivational", "humor", "humor", "entertaining", "trends"]
            
            for j, (tweet_content, category) in enumerate(zip(web_tweet_lines[:6], categories)):
                if tweet_content.strip():
                    tweets.append({
                        "id": f"tweet_web_{j+1}",
                        "content": tweet_content.strip(),
                        "type": "web_search",
                        "category": category,
                        "created_at": datetime.now().isoformat()
                    })
            
            # Ensure we have exactly 12 tweets
            while len(tweets) < 12:
                tweets.append({
                    "id": f"tweet_extra_{len(tweets)+1}",
                    "content": "🚀 AI is transforming how we work and create. What's your favorite AI tool? #AI #Innovation",
                    "type": "filler",
                    "category": "engaging",
                    "created_at": datetime.now().isoformat()
                })
            
            logger.info(f"Generated {len(tweets)} tweets")
            return tweets[:12]
            
        except Exception as e:
            logger.error(f"Tweet generation failed: {str(e)}")
            raise