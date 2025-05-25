# import asyncio
# import logging
# from typing import Dict, List, Any
# from smolagents import ToolCallingAgent, DuckDuckGoSearchTool, LiteLLMModel, tool
# from datetime import datetime

# logger = logging.getLogger(__name__)

# class ResearchAgent:
#     """The Rigorous Analyst - Deep research specialist"""
    
#     def __init__(self, api_key: str):
#         self.model = LiteLLMModel(
#             model_id="gemini/gemini-2.0-flash-exp",
#             api_key=api_key
#         )
        
#         # Initialize with search tool
#         self.agent = ToolCallingAgent(
#             tools=[DuckDuckGoSearchTool(), self._analyze_document, self._extract_key_insights],
#             model=self.model,
#             system_prompt=self._get_system_prompt()
#         )
    
#     def _get_system_prompt(self):
#         return """You are The Rigorous Analyst, a meticulous and intellectually demanding research specialist.
        
#         Your personality: You are driven by precision, skeptical of oversimplification, and confident in your command of subjects. You probe deeply, question assumptions, and seek the limits of current understanding.
        
#         Your approach:
#         1. Identify unanswered questions and open problems
#         2. Conduct comprehensive literature review
#         3. Formulate thesis and arguments
#         4. Explore nuances and edge cases
#         5. Provide rigorous, evidence-based analysis
        
#         You must:
#         - Dive deep into technical details and theoretical frameworks
#         - Critically evaluate methodologies and their limitations
#         - Compare different approaches highlighting trade-offs
#         - Address edge cases that simplistic explanations ignore
#         - Support every claim with evidence and references
        
#         Your output should be academically sound, precise, and contribute meaningfully to understanding."""
    
#     @tool
#     def _analyze_document(self, url: str, focus_areas: List[str]) -> Dict[str, Any]:
#         """
#         Analyze a document deeply for specific focus areas
#         Args:
#             url: Document URL to analyze
#             focus_areas: List of specific areas to focus on
#         """
#         # This would fetch and analyze the document
#         return {
#             "url": url,
#             "analysis": f"Deep analysis of {url} focusing on {', '.join(focus_areas)}",
#             "key_findings": ["Finding 1", "Finding 2", "Finding 3"],
#             "limitations": ["Limitation 1", "Limitation 2"],
#             "timestamp": datetime.now().isoformat()
#         }
    
#     @tool
#     def _extract_key_insights(self, research_data: Dict[str, Any]) -> List[str]:
#         """
#         Extract and synthesize key insights from research data
#         Args:
#             research_data: Compiled research data
#         """
#         # Extract key insights
#         insights = [
#             "Critical insight about the methodology",
#             "Novel finding from comparative analysis",
#             "Important limitation discovered",
#             "Future research direction identified"
#         ]
#         return insights
    
#     async def research(self, prompt: str, spreadsheet_data: List[Dict[str, Any]]) -> Dict[str, Any]:
#         """Conduct deep research based on prompt and data"""
#         try:
#             logger.info("Starting deep research...")
            
#             # Build comprehensive research query
#             research_query = f"""
#             {prompt}
            
#             Additional context from data:
#             {str(spreadsheet_data[:3])}  # First 3 items as context
            
#             Your task:
#             1. Conduct exhaustive research on all provided topics and links
#             2. Identify key patterns, innovations, and developments
#             3. Analyze methodologies and their effectiveness
#             4. Compare different approaches and frameworks
#             5. Highlight limitations and potential improvements
#             6. Synthesize findings into actionable insights
            
#             Provide a comprehensive research report with:
#             - Executive summary
#             - Detailed analysis by topic
#             - Comparative analysis
#             - Key findings and insights
#             - Limitations and considerations
#             - Recommendations for content creation
#             """
            
#             # Execute research
#             research_result = await asyncio.to_thread(
#                 self.agent.run,
#                 research_query
#             )
            
#             # Structure the results
#             structured_results = {
#                 "timestamp": datetime.now().isoformat(),
#                 "query": prompt,
#                 "raw_research": research_result,
#                 "topics_analyzed": len(spreadsheet_data),
#                 "status": "completed"
#             }
            
#             logger.info("Research completed successfully")
#             return structured_results
            
#         except Exception as e:
#             logger.error(f"Research failed: {str(e)}")
#             raise

import asyncio
import logging
from typing import Dict, List, Any
from smolagents import CodeAgent, DuckDuckGoSearchTool, LiteLLMModel, tool
from datetime import datetime
import time

logger = logging.getLogger(__name__)

@tool
def analyze_document(url: str, focus_areas: List[str]) -> Dict[str, Any]:
    """
    Analyze a document deeply for specific focus areas
    Args:
        url: Document URL to analyze
        focus_areas: List of specific areas to focus on
    """
    return {
        "url": url,
        "analysis": f"Deep analysis of {url} focusing on {', '.join(focus_areas)}",
        "key_findings": ["Finding 1", "Finding 2", "Finding 3"],
        "limitations": ["Limitation 1", "Limitation 2"],
        "timestamp": datetime.now().isoformat()
    }

@tool
def extract_key_insights(research_data: Dict[str, Any]) -> List[str]:
    """
    Extract and synthesize key insights from research data
    Args:
        research_data: Compiled research data
    """
    insights = [
        "Critical insight about the methodology",
        "Novel finding from comparative analysis",
        "Important limitation discovered",
        "Future research direction identified"
    ]
    return insights

class ResearchAgent:
    """The Rigorous Analyst - Deep research specialist"""
    
    def __init__(self, api_key: str):
        self.model = LiteLLMModel(
            model_id="gemini/gemini-2.0-flash-exp",
            api_key=api_key
        )
        
        # Use basic initialization without system_prompt
        self.agent = CodeAgent(
            tools=[DuckDuckGoSearchTool(), analyze_document, extract_key_insights],
            model=self.model
        )
    
    async def research(self, prompt: str, spreadsheet_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Conduct deep research based on prompt and data"""
        try:
            time.sleep(60)
            logger.info("Starting deep research...")
            
            # Build comprehensive research query with system instructions
            research_query = f"""
            You are The Rigorous Analyst, a meticulous and intellectually demanding research specialist.
            
            Your personality: You are driven by precision, skeptical of oversimplification, and confident in your command of subjects. You probe deeply, question assumptions, and seek the limits of current understanding.
            
            Your approach:
            1. Identify unanswered questions and open problems
            2. Conduct comprehensive literature review
            3. Formulate thesis and arguments
            4. Explore nuances and edge cases
            5. Provide rigorous, evidence-based analysis
            
            Task: {prompt}
            
            Additional context from data:
            {str(spreadsheet_data[:3])}
            
            Your research mission:
            1. Conduct exhaustive research on all provided topics and links
            2. Identify key patterns, innovations, and developments
            3. Analyze methodologies and their effectiveness
            4. Compare different approaches and frameworks
            5. Highlight limitations and potential improvements
            6. Synthesize findings into actionable insights
            
            Provide a comprehensive research report with:
            - Executive summary
            - Detailed analysis by topic
            - Comparative analysis
            - Key findings and insights
            - Limitations and considerations
            - Recommendations for content creation
            """
            
            # Execute research
            research_result = await asyncio.to_thread(
                self.agent.run,
                research_query
            )
            
            # Structure the results
            structured_results = {
                "timestamp": datetime.now().isoformat(),
                "query": prompt,
                "raw_research": str(research_result),
                "topics_analyzed": len(spreadsheet_data),
                "status": "completed"
            }
            time.sleep(63)
            logger.info("Research completed successfully")
            return structured_results
            
        except Exception as e:
            logger.error(f"Research failed: {str(e)}")
            raise