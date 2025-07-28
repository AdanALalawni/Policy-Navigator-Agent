# Policy-Navigator-Agent
**Policy Navigator Agent**: is an AI-powered assistant that answers questions about complex policy and regulatory documents.
It retrieves relevant content from indexed files or APIs, summarizes it using language models, and returns clear, cited answers.
Responses are displayed on a web interface and sent in real time to a connected Slack channel.


# What This Agent Does:
* Answers user questions about policy/regulation documents using the retrieved data from the specific tools:
  * It starts to search for the data in the index.
  * If the data is about federal policy, regulations, laws, or executive orders, search the Federal Register API using the screp tool.
  * If the data is about court cases, court rulings, legal disputes, or judicial matters, use the CourtListener API using the screp tool.

* It summarizes long-form regulations into clear, concise responses.
* It added the citations or source of the data (Index, Federal Register API, or CourtListener API).
* If it doesn't find any data or if the query was out of the scope of the agent, it will not answer the query and notify the user that it can't answer it.


# Tool Integrations
In this agent, I used some tools from the marketplace of Aixplain:
* Scrape: to retrieve data from Federal Register API or CourtListener API
* LLM (from the marketplace): use it as an LLM for the agent.
* Created index: I created an index to store the privacy documents and search for them using `IndexFactory`

  
# Data Sources:
* In this project, I used Federal Register API and CourtListener API.
* I use this PDF document [policies.pdf](https://github.com/AdanALalawni/Policy-Navigator-Agent/blob/main/src/data/policies.pdf) that I took from (American Data Privacy and Protection Act document).
  
# Setup Instructions
To create the agent and deploy it using a Flask server to type a question in the HTML page and receive the response in this page and Slack channel:
* Clone the repo.
* Optional: create and activate a Python environment. 
* Create a file called `.env` in the parent folder and add:
  ```
   AIXPLAIN_API_KEY = YOUR_KEY
   SCRAPE_ID = SCRAPE_ID_FROM_AIEXPLAIN
   LLM_ID = LLM_SELECTED_ID
   SLACK_TOKEN = YOIUR_SLACK_TOKEN
   CHANNEL =  CHANNEL_ID 
  ```
  * In the terminal, write this prompt:
    ```pip install -r requirements.txt```
  * To create the agent in the terminal, run:
    ``` python main.py```
  * To run the Flask server, run this command:
     ``` python app.py```
    Then open `index.html`.This page will appear:
    
    ![Web page](https://github.com/AdanALalawni/Policy-Navigator-Agent/blob/main/assert/Screenshot%202025-07-28%20211843.png)
    
# Examples:
* * **The quary** : " What does Sec. 103 say about data minimization?"
  * **The response** :  "I found in Internal Policy Index – Sec. 103: Companies would only be allowed to collect/make use of user data in a way that minimizes the amount of data collected and used."
 
* * **The quary** : " What was the ruling in the case of Dobbs v. Jackson Women's Health Organization?"
  * **The response** :  "I checked the CourtListener API: The ruling in the case of Dobbs v. Jackson Women's Health Organization was a significant decision by the U.S. Supreme Court that overturned Roe v. Wade, effectively ending the constitutional right to abortion. The Court held that the Constitution does not confer a right to abortion, and that states have the authority to regulate or prohibit abortion as they see fit."

* * **The quary** : " Is Executive Order 14067 still in effect?"
  * **The response** :  "checked the Federal Register API: yes it executive."
# 	Future Improvements:
* Add speech to text tool to recive the quraies as a voice.
* Add a tool to read multiple quaries from text file.
* Add multilingual support, fine‑tuned summarizers, or explainability tools.


 

