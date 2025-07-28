import os
import logging
from dotenv import load_dotenv
from aixplain.factories import AgentFactory, ModelFactory
from utils.env_writer import save_to_env
from index_creation import create_index_from_pdf  

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
SCRAPE_ID = os.getenv("SCRAPE_ID")
INDEX_ID = os.getenv("INDEX_ID")
LLM_ID = os.getenv("LLM_ID")

def read_prompt(file_path):
    try:
        logger.info(f"Reading prompt from: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except Exception as e:
        logger.exception(f"Error reading prompt file: {e}")
        raise

def create_agent(name: str, description: str, prompt: str):
    try:
        if not INDEX_ID:
            logger.info("INDEX_ID not found in .env, creating index from PDF...")
            INDEX_ID_PATH = "data/policies.pdf"
            create_index_from_pdf(INDEX_ID_PATH)
            load_dotenv()  # Reload to get updated .env values
        else:
            logger.info(f"Using existing index: {INDEX_ID}")

        index = ModelFactory.get(os.getenv("INDEX_ID"))
        scraper = ModelFactory.get(SCRAPE_ID)

        logger.info("Creating agent...")
        agent = AgentFactory.create(
            name=name,
            description=description,
            instructions=prompt,
            tools=[index, scraper],
            llm_id=LLM_ID
        )
        save_to_env("AGENT_ID", agent.id)
        logger.info(f"Agent created and ID saved: {agent.id}")
    except Exception as e:
        logger.exception(f"Failed to create agent: {e}")
        raise



