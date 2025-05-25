import os
import asyncio
import logging
from typing import List, Dict, Any
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class SpreadsheetHandler:
    """Handle Google Sheets operations"""
    
    def __init__(self):
        self.sheet_id = os.getenv("GOOGLE_SHEETS_ID")
        self.range_name = os.getenv("GOOGLE_SHEETS_RANGE", "Sheet1!A:Z")
        
        # Initialize Google Sheets API
        try:
            credentials_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_KEY")
            if credentials_path and os.path.exists(credentials_path):
                self.creds = service_account.Credentials.from_service_account_file(
                    credentials_path,
                    scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
                )
                self.service = build('sheets', 'v4', credentials=self.creds)
            else:
                logger.warning("Google service account key not found. Using mock data.")
                self.service = None
        except Exception as e:
            logger.error(f"Failed to initialize Google Sheets: {str(e)}")
            self.service = None
    
    async def get_data(self) -> List[Dict[str, Any]]:
        """Get data from Google Sheets"""
        try:
            if not self.service:
                # Return mock data if no service
                return self._get_mock_data()
            
            # Get data from Google Sheets
            sheet = self.service.spreadsheets()
            result = await asyncio.to_thread(
                sheet.values().get(
                    spreadsheetId=self.sheet_id,
                    range=self.range_name
                ).execute
            )
            
            values = result.get('values', [])
            
            if not values:
                logger.warning("No data found in spreadsheet")
                return self._get_mock_data()
            
            # Convert to list of dicts
            headers = values[0]
            data = []
            
            for row in values[1:]:
                row_dict = {}
                for i, header in enumerate(headers):
                    if i < len(row):
                        row_dict[header.lower().replace(' ', '_')] = row[i]
                    else:
                        row_dict[header.lower().replace(' ', '_')] = ""
                data.append(row_dict)
            
            logger.info(f"Retrieved {len(data)} rows from spreadsheet")
            return data
            
        except HttpError as e:
            logger.error(f"Google Sheets API error: {str(e)}")
            return self._get_mock_data()
        except Exception as e:
            logger.error(f"Failed to get spreadsheet data: {str(e)}")
            return self._get_mock_data()
    
    def _get_mock_data(self) -> List[Dict[str, Any]]:
        """Return mock data for testing"""
        return [
            {
                "topic": "AI Agents and Automation",
                "links": "https://arxiv.org/papers/ai-agents,https://openai.com/research",
                "description": "Latest developments in autonomous AI agents",
                "keywords": "AI agents, automation, LLM, multi-agent systems"
            },
            {
                "topic": "Machine Learning in Production",
                "links": "https://ml-ops.org/,https://papers.nips.cc/",
                "description": "Best practices for deploying ML models",
                "keywords": "MLOps, production ML, model deployment"
            },
            {
                "topic": "Future of Human-AI Collaboration",
                "links": "https://hai.stanford.edu/research,https://deepmind.com/blog",
                "description": "How humans and AI will work together",
                "keywords": "human-AI collaboration, augmented intelligence"
            }
        ]
