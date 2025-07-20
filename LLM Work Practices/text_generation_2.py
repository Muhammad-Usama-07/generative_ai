# import os
# import json
# from typing import Union, List, Tuple, Dict
# from crewai import Crew, Agent, Task, Process
# from langchain_community.tools import DuckDuckGoSearchRun
# from langchain_groq import ChatGroq
# from langchain.schema import AgentFinish

# # Set the environment variable
# os.environ["GROQ_API_KEY"] = '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'

# # Initialize global variables
# call_number = 0
# agent_finishes = []

# # Helper function to print agent output
# def print_agent_output(agent_output: Union[str, List[Tuple[Dict, str]], AgentFinish], agent_name: str = 'Generic call'):
#     global call_number
#     call_number += 1
#     with open("crew_callback_logs.txt", "a") as log_file:
#         if isinstance(agent_output, str):
#             try:
#                 agent_output = json.loads(agent_output)
#             except json.JSONDecodeError:
#                 pass

#         if isinstance(agent_output, list) and all(isinstance(item, tuple) for item in agent_output):
#             for action, description in agent_output:
#                 print(f"Agent Name: {agent_name}", file=log_file)

#         elif isinstance(agent_output, AgentFinish):
#             agent_finishes.append(agent_output)
#             output = agent_output.return_values
#             print(f"AgentFinish Output: {output['output']}", file=log_file)

#         else:
#             print(f"Unknown format of agent_output:", file=log_file)
#             print(type(agent_output), file=log_file)
#             print(agent_output, file=log_file)

# # Initialize the LLM
# GROQ_LLM = ChatGroq(model="llama3-70b-8192")

# class EmailAgents:
#     def __init__(self):
#         self.search_tool = DuckDuckGoSearchRun()

#     def make_categorizer_agent(self):
#         return Agent(
#             role='Email Categorizer Agent',
#             goal="""Take in an email from a human that has emailed our company email address and categorize it into one of the following categories: price_enquiry, customer_complaint, product_enquiry, customer_feedback, off_topic.""",
#             backstory="You are a master at understanding what a customer wants when they write an email and are able to categorize it in a useful way",
#             llm=GROQ_LLM,
#             verbose=True,
#             allow_delegation=False,
#             max_iter=5,
#             memory=True,
#             step_callback=lambda x: print_agent_output(x, "Email Categorizer Agent"),
#         )

#     def make_researcher_agent(self):
#         return Agent(
#             role='Info Researcher Agent',
#             goal="""Take in an email from a human that has emailed our company email address and the category that the categorizer agent gave it and decide what information you need to search for the email writer to reply to the email in a thoughtful and helpful way.""",
#             backstory="You are a master at understanding what information our email writer needs to write a reply that will help the customer",
#             llm=GROQ_LLM,
#             verbose=True,
#             max_iter=5,
#             allow_delegation=False,
#             memory=True,
#             tools=[self.search_tool],
#             step_callback=lambda x: print_agent_output(x, "Info Researcher Agent"),
#         )

#     def make_email_writer_agent(self):
#         return Agent(
#             role='Email Writer Agent',
#             goal="""Take in an email from a human that has emailed our company email address, the category that the categorizer agent gave it and the research from the research agent and write a helpful email in a thoughtful and friendly way.""",
#             backstory="You are a master at synthesizing a variety of information and writing a helpful email that will address the customer's issues and provide them with helpful information",
#             llm=GROQ_LLM,
#             verbose=True,
#             allow_delegation=False,
#             max_iter=5,
#             memory=True,
#             step_callback=lambda x: print_agent_output(x, "Email Writer Agent"),
#         )

# class EmailTasks:
#     def __init__(self, categorizer_agent, researcher_agent, email_writer_agent):
#         self.categorizer_agent = categorizer_agent
#         self.researcher_agent = researcher_agent
#         self.email_writer_agent = email_writer_agent

#     def categorize_email(self, email_content):
#         return Task(
#             description=f"Conduct a comprehensive analysis of the email provided and categorize into one of the following categories: price_enquiry, customer_complaint, product_enquiry, customer_feedback, off_topic.\n\nEMAIL CONTENT:\n\n{email_content}",
#             expected_output="A single category for the type of email from the types ('price_enquiry', 'customer_complaint', 'product_enquiry', 'customer_feedback', 'off_topic').",
#             output_file=f"email_category.txt",
#             agent=self.categorizer_agent
#         )

#     def research_info_for_email(self, email_content):
#         return Task(
#             description=f"Conduct a comprehensive analysis of the email provided and the category provided and search the web to find info needed to respond to the email.\n\nEMAIL CONTENT:\n\n{email_content}\n\nOnly provide the info needed.",
#             expected_output="A set of bullet points of useful info for the email writer or clear instructions that no useful material was found.",
#             context=[self.categorize_email(email_content)],
#             output_file=f"research_info.txt",
#             agent=self.researcher_agent
#         )

#     def draft_email(self, email_content):
#         return Task(
#             description=f"Conduct a comprehensive analysis of the email provided, the category provided and the info provided from the research specialist to write an email.\n\nEMAIL CONTENT:\n\n{email_content}",
#             expected_output="A well-crafted email for the customer that addresses their issues and concerns.",
#             context=[self.categorize_email(email_content), self.research_info_for_email(email_content)],
#             agent=self.email_writer_agent,
#             output_file=f"draft_email.txt",
#         )

# def process_email(email_content):
#     agents = EmailAgents()
#     categorizer_agent = agents.make_categorizer_agent()
#     researcher_agent = agents.make_researcher_agent()
#     email_writer_agent = agents.make_email_writer_agent()

#     tasks = EmailTasks(categorizer_agent, researcher_agent, email_writer_agent)

#     categorize_email = tasks.categorize_email(email_content)
#     research_info_for_email = tasks.research_info_for_email(email_content)
#     draft_email = tasks.draft_email(email_content)

#     crew = Crew(
#         agents=[categorizer_agent, researcher_agent, email_writer_agent],
#         tasks=[categorize_email, research_info_for_email, draft_email],
#         verbose=2,
#         process=Process.sequential,
#         full_output=True,
#         share_crew=False,
#         step_callback=lambda x: print_agent_output(x, "MasterCrew Agent")
#     )

#     results = crew.kickoff()

#     jsson_data = {
#         'subject': results['final_output'].split('\n\n')[0].split(':')[-1],
#         'title': results['final_output'].split('\n\n')[1],
#         'content': ' '.join(results['final_output'].split('\n\n')[2:-2]),
#         'last': ' '.join(results['final_output'].split('\n\n')[-1].split('\n'))
#     }

#     return jsson_data

# # Example interaction
# if __name__ == "__main__":
#     EMAIL = input('Enter prompt: ')
#     result = process_email(EMAIL)
#     print(result)


import os
import json
from typing import Union, List, Tuple, Dict
from flask import Flask, request, jsonify
from crewai import Crew, Agent, Task, Process
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_groq import ChatGroq
from langchain.schema import AgentFinish

# Set the environment variable
os.environ["GROQ_API_KEY"] = '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'

# Initialize global variables
call_number = 0
agent_finishes = []

# Helper function to print agent output
def print_agent_output(agent_output: Union[str, List[Tuple[Dict, str]], AgentFinish], agent_name: str = 'Generic call'):
    global call_number
    call_number += 1
    with open("crew_callback_logs.txt", "a") as log_file:
        if isinstance(agent_output, str):
            try:
                agent_output = json.loads(agent_output)
            except json.JSONDecodeError:
                pass

        if isinstance(agent_output, list) and all(isinstance(item, tuple) for item in agent_output):
            for action, description in agent_output:
                print(f"Agent Name: {agent_name}", file=log_file)

        elif isinstance(agent_output, AgentFinish):
            agent_finishes.append(agent_output)
            output = agent_output.return_values
            print(f"AgentFinish Output: {output['output']}", file=log_file)

        else:
            print(f"Unknown format of agent_output:", file=log_file)
            print(type(agent_output), file=log_file)
            print(agent_output, file=log_file)

# Initialize the LLM
GROQ_LLM = ChatGroq(model="llama3-70b-8192")

class EmailAgents:
    def __init__(self):
        self.search_tool = DuckDuckGoSearchRun()

    def make_categorizer_agent(self):
        return Agent(
            role='Email Categorizer Agent',
            goal="""Take in an email from a human that has emailed our company email address and categorize it into one of the following categories: price_enquiry, customer_complaint, product_enquiry, customer_feedback, off_topic.""",
            backstory="You are a master at understanding what a customer wants when they write an email and are able to categorize it in a useful way",
            llm=GROQ_LLM,
            verbose=True,
            allow_delegation=False,
            max_iter=5,
            memory=True,
            step_callback=lambda x: print_agent_output(x, "Email Categorizer Agent"),
        )

    def make_researcher_agent(self):
        return Agent(
            role='Info Researcher Agent',
            goal="""Take in an email from a human that has emailed our company email address and the category that the categorizer agent gave it and decide what information you need to search for the email writer to reply to the email in a thoughtful and helpful way.""",
            backstory="You are a master at understanding what information our email writer needs to write a reply that will help the customer",
            llm=GROQ_LLM,
            verbose=True,
            max_iter=5,
            allow_delegation=False,
            memory=True,
            tools=[self.search_tool],
            step_callback=lambda x: print_agent_output(x, "Info Researcher Agent"),
        )

    def make_email_writer_agent(self):
        return Agent(
            role='Email Writer Agent',
            goal="""Take in an email from a human that has emailed our company email address, the category that the categorizer agent gave it and the research from the research agent and write a helpful email in a thoughtful and friendly way.""",
            backstory="You are a master at synthesizing a variety of information and writing a helpful email that will address the customer's issues and provide them with helpful information",
            llm=GROQ_LLM,
            verbose=True,
            allow_delegation=False,
            max_iter=5,
            memory=True,
            step_callback=lambda x: print_agent_output(x, "Email Writer Agent"),
        )

class EmailTasks:
    def __init__(self, categorizer_agent, researcher_agent, email_writer_agent):
        self.categorizer_agent = categorizer_agent
        self.researcher_agent = researcher_agent
        self.email_writer_agent = email_writer_agent

    def categorize_email(self, email_content):
        return Task(
            description=f"Conduct a comprehensive analysis of the email provided and categorize into one of the following categories: price_enquiry, customer_complaint, product_enquiry, customer_feedback, off_topic.\n\nEMAIL CONTENT:\n\n{email_content}",
            expected_output="A single category for the type of email from the types ('price_enquiry', 'customer_complaint', 'product_enquiry', 'customer_feedback', 'off_topic').",
            output_file=f"email_category.txt",
            agent=self.categorizer_agent
        )

    def research_info_for_email(self, email_content):
        return Task(
            description=f"Conduct a comprehensive analysis of the email provided and the category provided and search the web to find info needed to respond to the email.\n\nEMAIL CONTENT:\n\n{email_content}\n\nOnly provide the info needed.",
            expected_output="A set of bullet points of useful info for the email writer or clear instructions that no useful material was found.",
            context=[self.categorize_email(email_content)],
            output_file=f"research_info.txt",
            agent=self.researcher_agent
        )

    def draft_email(self, email_content):
        return Task(
            description=f"Conduct a comprehensive analysis of the email provided, the category provided and the info provided from the research specialist to write an email.\n\nEMAIL CONTENT:\n\n{email_content}",
            expected_output="A well-crafted email for the customer that addresses their issues and concerns.",
            context=[self.categorize_email(email_content), self.research_info_for_email(email_content)],
            agent=self.email_writer_agent,
            output_file=f"draft_email.txt",
        )

def process_email(email_content):
    agents = EmailAgents()
    categorizer_agent = agents.make_categorizer_agent()
    researcher_agent = agents.make_researcher_agent()
    email_writer_agent = agents.make_email_writer_agent()

    tasks = EmailTasks(categorizer_agent, researcher_agent, email_writer_agent)

    categorize_email = tasks.categorize_email(email_content)
    research_info_for_email = tasks.research_info_for_email(email_content)
    draft_email = tasks.draft_email(email_content)

    crew = Crew(
        agents=[categorizer_agent, researcher_agent, email_writer_agent],
        tasks=[categorize_email, research_info_for_email, draft_email],
        verbose=2,
        process=Process.sequential,
        full_output=True,
        share_crew=False,
        step_callback=lambda x: print_agent_output(x, "MasterCrew Agent")
    )

    results = crew.kickoff()
    print('resulttttttttt-----', results)

    jsson_data = {
        'subject': results['final_output'].split('\n\n')[0].split(':')[-1],
        'title': results['final_output'].split('\n\n')[1],
        'content': ' '.join(results['final_output'].split('\n\n')[2:-2]),
        'last': ' '.join(results['final_output'].split('\n\n')[-1].split('\n'))
    }

    return jsson_data

# Flask API
app = Flask(__name__)

@app.route('/process_email', methods=['POST'])
def process_email_endpoint():
    # data = request.get_json()
    # email_content = data.get('email')
    email_content =  request.form.get('email')
    if not email_content:
        return jsonify({'error': 'No email content provided'}), 400

    result = process_email(email_content)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port = 8867)
