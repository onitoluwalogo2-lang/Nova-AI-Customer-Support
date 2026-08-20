Nova AI Customer Support System

Overview

Nova is an AI-powered customer-support system designed to help customers get accurate answers about products and company policies while identifying situations that require human assistance.

The system combines structured business knowledge, natural-language intent detection, conversation memory, support-case tracking, AI-powered response generation, logging, and escalation logic to simulate a practical customer-support workflow.

Project Goals

Provide accurate product information

Answer customer questions using structured company knowledge

Apply company policies consistently

Maintain context across customer follow-up questions

Identify customer intent automatically

Track the current support case

Escalate sensitive, disputed, or unusual issues to human support

Handle AI/API failures gracefully

Reduce repetitive customer-support work

Generate natural customer-facing responses

Products

The initial Nova product catalog includes:

Nova Play Station

Nova Smart Glasses

Nova Camera

Nova WiFi Router

Current Features

Product Knowledge

Nova can retrieve structured information about products, including:

Product names

Categories

Prices

Descriptions

Features

Stock information

Warranty periods

Knowledge Base

Nova retrieves information from structured company knowledge covering:

Returns and refunds

Shipping and delivery

Payments

Privacy and security

Product warranties

The knowledge base is separated from the application logic so that company information can be updated without rewriting the main application workflow.

Intent Detection

Nova recognizes several customer-support intents:

Price

Warranty

Return

Shipping

Payment

Security

Unknown requests

Product Detection

Nova identifies the product involved in a customer's question and uses the identified product when retrieving relevant knowledge.

For example:

What is the price of the Nova Play Station?

followed by:

What about the warranty?

Nova can use the remembered product context without requiring the customer to repeat the product name.

Conversation Memory

Nova maintains conversation context across follow-up questions.

The system remembers:

Product

Intent

Nova can also switch context when the customer introduces a different product.

Support Case Tracking

Nova maintains a support case containing:

Product

Intent

Status

Human-support requirement

Next action

Customers can type:

case

to view the current support case.

Escalation Handling

Nova can identify situations that may require human assistance, including:

Late or problematic deliveries

Payment disputes

Security concerns

Certain return or refund problems

Unknown or unsupported requests

API Failure Handling

Nova includes a fallback mechanism for AI/API failures.

If the AI response generation fails, the system returns a safe fallback response instead of crashing.

Logging

Nova uses structured application logging to record important support events, including:

Product identification

Intent detection

Support-case status changes

Case resolution

Human-support escalation

API activity

This makes the system easier to monitor and debug.

Evaluation

Nova includes a dedicated evaluation suite for testing customer-support behavior.

The evaluation suite currently covers:

Price handling

Return handling

Shipping handling

Delivery escalation

Payment escalation

Security escalation

Unknown request handling

Escalation reset

Product memory

Product context switching

Follow-up questions

API failure fallback

Current evaluation result:

Nova AI Evaluation Report
-------------------------
Price handling                  PASS
Return handling                 PASS
Shipping handling               PASS
Delivery escalation             PASS
Payment escalation              PASS
Security escalation             PASS
Unknown request handling        PASS
Escalation reset                PASS
Product memory                  PASS
Product context switching       PASS
Follow-up question              PASS
API failure fallback            PASS

12/12 evaluation scenarios passed

The evaluation suite uses controlled AI responses where appropriate so that support workflows can be tested without depending on live AI responses.

Project Structure

Nova-AI-Customer-Support/
│
├── app.py
├── README.md
│
├── data/
│   ├── products.json
│   └── policies.json
│
├── knowledge/
│   └── knowledge_base.py
│
├── test_app.py
├── test_knowledge.py
├── test_cases.py
└── test_evaluation.py

Testing

Run the individual test suites with:

python test_app.py
python test_knowledge.py
python test_cases.py
python test_evaluation.py

The evaluation suite currently reports:

12/12 evaluation scenarios passed

Running Nova

Activate the virtual environment:

source .venv/bin/activate

Then run:

python app.py

Nova will start an interactive customer-support session.

You can type:

case

to view the current support case.

Type:

exit

to stop the application.

AI Model

Nova uses the OpenAI API for natural-language response generation.

The model is configured through:

MODEL_NAME = "gpt-5-mini"

An OpenAI API key should be provided through an environment variable and should never be committed to the repository.

Technologies

Python

OpenAI API

JSON

Git

Automated evaluation/testing

Structured logging

What This Project Demonstrates

This project demonstrates practical AI application development concepts including:

LLM-powered customer support

Structured knowledge retrieval

Intent detection

Conversation memory

Support-case management

Human escalation

API failure handling

Automated evaluation

Logging and observability

Modular application design