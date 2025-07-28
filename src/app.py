from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import time
import os
import logging
from dotenv import load_dotenv
from slack_notifier import notifier

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Aixplain setup
AIXPLAIN_API_KEY = os.getenv("AIXPLAIN_API_KEY")
AGENT_ID = os.getenv("AGENT_ID")
POST_URL = f"https://platform-api.aixplain.com/sdk/agents/{AGENT_ID}/run"

app = Flask(__name__)
CORS(app)

@app.route("/ask", methods=["POST"])
def ask_agent():
    try:
        query = request.json.get("query")
        logger.info(f"Received query: {query}")

        headers = {
            "x-api-key": AIXPLAIN_API_KEY,
            "Content-Type": "application/json"
        }
        data = {"query": query}

        response = requests.post(POST_URL, headers=headers, json=data)
        response.raise_for_status()
        response_data = response.json()

        request_id = response_data.get("requestId")
        if not request_id:
            logger.error("No requestId received from Aixplain.")
            return jsonify({"error": "Failed to get requestId"}), 500

        logger.info(f"Polling results for requestId: {request_id}")
        get_url = f"https://platform-api.aixplain.com/sdk/agents/{request_id}/result"

        while True:
            try:
                get_response = requests.get(get_url, headers=headers)
                get_response.raise_for_status()
                result = get_response.json()

                if result.get("completed"):
                    output = result.get("data", {}).get("output", "No output")
                    logger.info("Result received from Aixplain.")
                    if notifier:
                        notifier.send_message(f"Aixplain Agent Result:\n{output}")
                    return jsonify({"result": output})
                else:
                    time.sleep(3)

            except requests.RequestException as e:
                logger.exception(f"Error during polling: {e}")
                return jsonify({"error": "Polling failed"}), 500

    except requests.RequestException as e:
        logger.exception(f"Error communicating with Aixplain API: {e}")
        return jsonify({"error": "API request failed"}), 500

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    logger.info("Starting Flask app...")
    app.run(debug=True)
