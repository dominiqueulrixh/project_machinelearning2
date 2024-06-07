
## Project Setup and Execution
1. Clone the Project from GitHub
git clone (https://github.com/dominiqueulrixh/project_machinelearning2.git)

2. Create and Activate a virtual Environment
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`

3. Install Required Python Packages
pip install -r requirements.txt

4. Install HTTP Server for Frontend
sudo npm install -g http-server

5. Run the Script to Automatically Download the Latest Civil Code PDF
python scripts/update_pdf.py

6. Start the Backend Server
uvicorn app:app --reload
(Wait until you see "INFO: Application startup complete.")

7. Start the Frontend Server
cd frontend
http-server -p 8001

8. Open localhost:8001 and the chatbot is ready to talk with you :)!


# Detailed Information about my Chatbot-Project

## 1. Project goal/Motivation
The main goal of my project is to create a chatbot capable of providing precise and comprehensible answers regarding the Swiss Civil Code. It is also able to include everyday examples in its responses. Recently, I was in a personal situation where I needed information about inheritance law, and ChatGPT couldn't provide the correct answer because it didn't know the specific laws of Switzerland. This inspired me to pursue this project idea.

What problem are you trying to solve?
The problem I aim to address is the difficulty in quickly and easily finding legal information. Currently, it is challenging to interpret legal texts and extract relevant information, leading to uncertainties and misunderstandings. This can result in poor decision-making and unnecessary legal conflicts in everyday life.

What is the motivation behind it?
My motivation is to bridge the gap between the complex legal world and the general public. By providing a user-friendly chatbot, I want to help people like myself, who are not well-versed in law, to resolve their legal queries without needing extensive legal knowledge or expensive legal consultations.

Why is this project relevant?
In a time when digital solutions are becoming increasingly important, our chatbot offers an innovative way to disseminate knowledge while lowering barriers to accessing legal information. This not only provides individual support but also promotes a broader understanding and acceptance of the legal system.


## 2. Data Collection or Generation (project evaluation relative weight: 30%)

Data Scraping Source: Public PDF
In my project, I implemented a script (update_pdf.py) to automatically collect data from the Swiss government's website that publishes the Civil Code. The script uses web scraping to regularly check the website and download the latest PDF version of the Civil Code. Utilizing libraries like requests, BeautifulSoup, and selenium, the script parses the webpage, finds the relevant PDF link, and downloads the document. If the script runs it runs hourly to ensure the most current version is always available, replacing the old document with the new one. This automated data collection ensures that the chatbot always has access to the latest legal information, enhancing the accuracy and reliability of its responses.

Interactive Data Collection
To ensure that the questions asked are relevant to other people and not just to myself, I conducted interactive data collection. I recorded four questions each from two individuals and posed these questions to the chatbot. These questions cover various aspects of civil law and help prepare the chatbot for real user inquiries.

Synthetic Data Generation
In addition to manual and interactive data collection, the questions posed to the chatbot and the generated answers are stored in a MySQL database. This represents a form of synthetic data generation, as this data is continuously expanded and forms the basis for future improvements and adjustments to the chatbot. This continuous data collection through user interactions ensures that the chatbot can access a growing data set to refine and enhance its responses further.

## 3. Modeling
For the modeling of my project, I primarily relied on the techniques of prompt engineering and zero-shot inference to utilize OpenAI's GPT-4o language model.

Prompt Engineering
Through specific prompt engineering, I trained the model to provide precise and understandable answers to questions about the Swiss Civil Code. I developed and optimized various prompts to ensure that the model not only correctly reproduces legal information but also incorporates everyday scenarios and examples. An example of an optimized prompt is: "You are an expert in Swiss Civil Law. Please provide a concise and clear answer in no more than three sentences. Include relevant sections from the Swiss Civil Code if applicable. Please answer always in German."

Zero-Shot/Few-Shot Inference
I used the GPT-4o model in a zero-shot mode to ensure that it can answer new and unfamiliar legal questions without extensive training. This was particularly important as the model needed to cover a wide range of questions that could arise in the context of the Swiss Civil Code.

Integration of APIs
To perform the modeling, I integrated the OpenAI API to access the GPT-4o model. This API integration allows the chatbot to process user queries in real-time and provide legal information.


## 4. Interpretation and Validation
In my project, I asked the chatbot 15 questions on the topic of civil law. Eight of these questions came from two individuals in my acquaintance. These 15 questions were then submitted for automatic review by ChatGPT-4o, which checked the answers against the Civil Code that I provided.

Additionally, I conducted a manual review where I verified and evaluated the referenced article numbers. To further validate the results, I took two measures that are documented in the .doc folder under Validating the results.pdf.

Through this combination of automatic and manual validation, I ensured that the chatbot's responses are accurate and reliable. The validation of results through numerical methods and manual review has helped confirm the accuracy and reliability of the chatbot.