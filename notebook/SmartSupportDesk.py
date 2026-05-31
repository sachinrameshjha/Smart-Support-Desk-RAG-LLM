from openai import OpenAI
import chromadb
import requests
import os
from dotenv import load_dotenv
load_dotenv()


client = OpenAI(
    base_url="https://api.modelbest.cn/v1",
    api_key=os.environ['MINICPM_KEY']
)


def chat_minicpm(question):
    response = client.chat.completions.create(
        model="MiniCPM-V-4.6-Thinking",
        messages=[
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content


# Sample Data on policies

company_knowledge = {
    "ids": [
        "policy_1",
        "policy_2",
        "policy_3",
        "policy_4",
        "policy_5",
        "policy_6",
    ],
    "chunks": [
        "Refund Policy: Customers can get a full refund within 30 days of purchase if the item is unused.",
        "Shipping Delay: standard delivery takes 3-5 business days. Express shipping takes 1-2 days.",
        "Technical Crash: If the app crashes, instruct user to clear cache, restart app, or re-install.",
        "Exchange Policy: Items can be exchanged for a different size or color within 45 days of purchase, even if opened, as long as they are undamaged.",
        "Damaged Items: If an item arrives damaged, the customer must provide a photo within 48 hours of delivery to receive a free replacement.",
        "Payment Methods: We accept all major credit cards, PayPal, and Apple Pay. We do not accept cash on delivery or personal checks.",
    ],
}

client_chroma = chromadb.Client()

collection = client_chroma.get_or_create_collection("company_policies")

collection.add(
    documents=company_knowledge["chunks"],
    ids=company_knowledge["ids"]
)


# Querying the chroma db with the user question, and creating context for LLM
def process_incoming_ticket(email_text):
    search_results = collection.query(query_texts=[email_text], n_results=2)
    matched_policy = search_results['documents'][0][0] 
    
    context = f"""You are an experienced customer support representative. 
Analyze the customer email using the provided Company Policy.
keep close eye to detail and reply thinking twice about the question and its details.

Company Policy:
{matched_policy}

Customer Email:
"{email_text}"

Your output must follow this exact template:
PRIORITY: [Urgent / Low]
CATEGORY: [Refund / Shipping / Technical]
DRAFT REPLY: [Write a polite reply based ONLY on the company policy. If policy doesn't match, say a human agent will review it shortly.]
"""

    return chat_minicpm(context)


# Testing the LLM response
print(chat_minicpm("Hello MiniCPM!!"))

questions = [
    "I ordered a blue shirt last week, but I received a red one. What should I do?",
    "The app keeps crashing every time I try to open it. Help!",
    "I need to return the headphones I bought because they are not working properly.",
    "Is it possible to exchange the shoes I bought for a larger size?",
    "I haven't received my package yet, and it's been 6 days.",
]

for i in questions:
    print("\n------------------- Email ----------------------")
    print("Email: ",i)
    print("----------------- Response ----------------------")
    print("Response: ",process_incoming_ticket(i))
    print("----------------x Response x---------------------")
    print()
