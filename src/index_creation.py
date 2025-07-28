import os
import re
import logging
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from aixplain.factories import IndexFactory
from aixplain.modules.model.record import Record
from utils.env_writer import save_to_env

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def extract_sections_from_pdf(file_path):
    try:
        logger.info(f"Reading PDF from: {file_path}")
        reader = PdfReader(file_path)
        full_text = "\n".join(page.extract_text() or "" for page in reader.pages)

        section_pattern = re.compile(r"Sec(?:s?)\. ?([\d\-a-zA-Z(), ]+)\s*\(([^)]+)\)\s*:?\s*", re.MULTILINE)
        bullet_pattern = re.compile(r"•\s+(.*?)(?=(\n•|\n\S|\Z))", re.DOTALL)

        matches = list(section_pattern.finditer(full_text))
        if not matches:
            logger.warning("No sections found in the PDF.")
        
        results = []
        for i, match in enumerate(matches):
            sec_number = str(match.group(1)).strip()
            title = str(match.group(2)).strip()
            start = match.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(full_text)
            section_text = full_text[start:end].strip()

            bullets = [
                b.group(1).strip().replace('\n', ' ')
                for b in bullet_pattern.finditer(section_text)
                if b.group(1).strip()
            ]

            results.append({
                "section": sec_number,
                "title": title,
                "summary": bullets
            })

        logger.info(f"Extracted {len(results)} sections from PDF.")
        return results

    except Exception as e:
        logger.exception(f"Failed to extract sections from PDF: {e}")
        raise

def create_index_from_pdf(pdf_path):
    try:
        logger.info("Starting index creation process...")
        sections = extract_sections_from_pdf(pdf_path)

        index = IndexFactory.create(name="policies", description="Index to save some policies")
        logger.info(f"Created index: {index.id}")

        records = []
        for doc in sections:
            summary_list = doc.get("summary", [])
            if not summary_list or all(not bullet.strip() for bullet in summary_list):
                logger.warning(f"Skipping section {doc.get('section')} due to empty summary.")
                continue

            record = Record(
                id=str(doc["section"]),
                value="\n".join(bullet.strip() for bullet in summary_list),
                attributes={"title": doc.get("title", "")}
            )
            records.append(record)

        if not records:
            raise ValueError("No valid records to upload to index.")

        index.upsert(records)
        save_to_env("INDEX_ID", index.id)
        logger.info(f"Index populated and saved to .env with ID: {index.id}")

    except Exception as e:
        logger.exception(f"Failed to create index: {e}")
        raise

# Example usage
if __name__ == "__main__":
    create_index_from_pdf("data/policies.pdf")
