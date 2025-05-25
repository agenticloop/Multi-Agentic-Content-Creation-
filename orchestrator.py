import os
import json
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

from agents.research_agent import ResearchAgent
from agents.blog_writer_agent import BlogWriterAgent
from agents.twitter_agent import TwitterAgent
from agents.linkedin_agent import LinkedinAgent
from agents.optimizing_agent import OptimizingAgent
from utils.spreadsheet_handler import SpreadsheetHandler
from utils.email_sender import EmailSender
import time
load_dotenv()

logger = logging.getLogger(__name__)

class Orchestrator:
    """Main orchestrator that coordinates all agents"""
    
    def __init__(self):
        # Initialize API keys
        self.api_keys = {
            "research": os.getenv("GEMINI_API_KEY_1"),
            "content": os.getenv("GEMINI_API_KEY_2"),
            "optimization": os.getenv("GEMINI_API_KEY_3"),
            "twitterlinkedin":os.getenv("GEMINI_API_KEY_4")
        }
        
        # Initialize agents
        self.research_agent = ResearchAgent(self.api_keys["research"])
        self.blog_writer_agent = BlogWriterAgent(self.api_keys["content"])
        self.twitter_agent = TwitterAgent(self.api_keys["twitterlinkedin"])
        self.linkedin_agent = LinkedinAgent(self.api_keys["twitterlinkedin"])
        self.optimizing_agent = OptimizingAgent(self.api_keys["optimization"])
        
        # Initialize utilities
        self.spreadsheet_handler = SpreadsheetHandler()
        self.email_sender = EmailSender()
        
        # Results storage
        self.results = {
            "task_id": None,
            "status": "pending",
            "spreadsheet_data": None,
            "research_data": None,
            "blog_posts": None,
            "tweets": None,
            "linkedin_posts": None,
            "optimized_content": None,
            "errors": []
        }
    
    async def run(self, task_id: str):
        """Main orchestration flow"""
        self.results["task_id"] = task_id
        self.results["start_time"] = datetime.now().isoformat()
        
        try:
            logger.info(f"Starting orchestration for task {task_id}")
            
            # Step 1: Get spreadsheet data
            await self._get_spreadsheet_data()
            
            # Step 2: Research phase
            await self._research_phase()
            
            # Step 3: Blog writing phase
            await self._blog_writing_phase()
            
            # Step 4: Social media content phase
            await self._social_media_phase()
            
            # Step 5: Optimization phase
            await self._optimization_phase()
            
            # Mark as completed
            self.results["status"] = "completed"
            self.results["end_time"] = datetime.now().isoformat()
            logger.info(f"Orchestration completed for task {task_id}")
            
        except Exception as e:
            logger.error(f"Orchestration failed for task {task_id}: {str(e)}")
            self.results["status"] = "failed"
            self.results["errors"].append({
                "phase": "orchestration",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
        
        finally:
            # Always send email with results
            await self._send_results_email()
    
    async def _get_spreadsheet_data(self):
        """Get data from Google Sheets"""
        try:
            logger.info("Fetching spreadsheet data...")
            self.results["spreadsheet_data"] = await self.spreadsheet_handler.get_data()
            logger.info(f"Retrieved {len(self.results['spreadsheet_data'])} rows from spreadsheet")
        except Exception as e:
            logger.error(f"Failed to get spreadsheet data: {str(e)}")
            self.results["errors"].append({
                "phase": "spreadsheet",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            raise
    
    async def _research_phase(self):
        """Execute research phase"""
        try:
            logger.info("Starting research phase...")
            research_prompt = self._build_research_prompt()
            self.results["research_data"] = await self.research_agent.research(
                research_prompt,
                self.results["spreadsheet_data"]
            )
            logger.info("Research phase completed")
        except Exception as e:
            logger.error(f"Research phase failed: {str(e)}")
            self.results["errors"].append({
                "phase": "research",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            raise
    
    async def _blog_writing_phase(self):
        """Execute blog writing phase"""
        try:
            logger.info("Starting blog writing phase...")
            self.results["blog_posts"] = await self.blog_writer_agent.write_blogs(
                self.results["research_data"],
                self.results["spreadsheet_data"]
            )
            logger.info(f"Generated {len(self.results['blog_posts'])} blog posts")
        except Exception as e:
            logger.error(f"Blog writing phase failed: {str(e)}")
            self.results["errors"].append({
                "phase": "blog_writing",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            raise
    
    async def _social_media_phase(self):
        """Execute social media content generation"""
        try:
            logger.info("Starting social media phase...")
            
            # Generate tweets
            twitter_task = self.twitter_agent.generate_tweets(self.results["blog_posts"])
            
            logger.info("Waiting for 60 seconds to avoid rate limits...")
            # Generate LinkedIn posts
            time.sleep(60)  # Wait for 60 seconds to avoid rate limits
            
            linkedin_task = self.linkedin_agent.generate_posts(self.results["blog_posts"])
            
            # Wait for both to complete
            self.results["tweets"], self.results["linkedin_posts"] = await asyncio.gather(
                twitter_task, linkedin_task
            )
            
            logger.info(f"Generated {len(self.results['tweets'])} tweets and {len(self.results['linkedin_posts'])} LinkedIn posts")
        except Exception as e:
            logger.error(f"Social media phase failed: {str(e)}")
            self.results["errors"].append({
                "phase": "social_media",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            raise
    
    async def _optimization_phase(self):
        """Execute content optimization"""
        try:
            logger.info("Starting optimization phase...")
            
            all_content = {
                "blog_posts": self.results["blog_posts"],
                "tweets": self.results["tweets"],
                "linkedin_posts": self.results["linkedin_posts"]
            }
            
            self.results["optimized_content"] = await self.optimizing_agent.optimize(all_content)
            logger.info("Optimization phase completed")
        except Exception as e:
            logger.error(f"Optimization phase failed: {str(e)}")
            self.results["errors"].append({
                "phase": "optimization",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            # Don't raise here - we want to send results even if optimization fails
    
    async def _send_results_email(self):
        """Send results via email"""
        try:
            logger.info("Sending results email...")
            
            # Prepare email content
            email_data = {
                "task_id": self.results["task_id"],
                "status": self.results["status"],
                "start_time": self.results.get("start_time"),
                "end_time": self.results.get("end_time"),
                "errors": self.results["errors"]
            }
            
            # Prepare attachments
            attachments = []
            
            # Add blog posts
            if self.results.get("optimized_content") and self.results["optimized_content"].get("blog_posts"):
                attachments.append({
                    "filename": f"blog_posts_{self.results['task_id']}.json",
                    "content": json.dumps(self.results["optimized_content"]["blog_posts"], indent=2)
                })
            elif self.results.get("blog_posts"):
                attachments.append({
                    "filename": f"blog_posts_{self.results['task_id']}.json",
                    "content": json.dumps(self.results["blog_posts"], indent=2)
                })
            
            # Add tweets
            if self.results.get("optimized_content") and self.results["optimized_content"].get("tweets"):
                attachments.append({
                    "filename": f"tweets_{self.results['task_id']}.json",
                    "content": json.dumps(self.results["optimized_content"]["tweets"], indent=2)
                })
            elif self.results.get("tweets"):
                attachments.append({
                    "filename": f"tweets_{self.results['task_id']}.json",
                    "content": json.dumps(self.results["tweets"], indent=2)
                })
            
            # Add LinkedIn posts
            if self.results.get("optimized_content") and self.results["optimized_content"].get("linkedin_posts"):
                attachments.append({
                    "filename": f"linkedin_posts_{self.results['task_id']}.json",
                    "content": json.dumps(self.results["optimized_content"]["linkedin_posts"], indent=2)
                })
            elif self.results.get("linkedin_posts"):
                attachments.append({
                    "filename": f"linkedin_posts_{self.results['task_id']}.json",
                    "content": json.dumps(self.results["linkedin_posts"], indent=2)
                })
            
            await self.email_sender.send_results(email_data, attachments)
            logger.info("Results email sent successfully")
            
        except Exception as e:
            logger.error(f"Failed to send results email: {str(e)}")
            # Log but don't raise - email failure shouldn't crash the system
    
    def _build_research_prompt(self):
        """Build research prompt from spreadsheet data"""
        topics = []
        links = []
        
        for row in self.results["spreadsheet_data"]:
            if row.get("topic"):
                topics.append(row["topic"])
            if row.get("links"):
                links.extend(row["links"].split(","))
        
        prompt = f"""
        Research the following topics deeply and comprehensively:
        
        Topics: {', '.join(topics)}
        
        Resources to analyze:
        {chr(10).join(links)}
        
        Provide in-depth analysis, key insights, and relevant information for creating engaging blog content.
        Focus on practical applications, recent developments, and unique perspectives.
        """
        
        return prompt
