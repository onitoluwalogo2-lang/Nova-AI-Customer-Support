# Nova AI Customer Support System

## Overview

Nova is an AI-powered customer-support system designed to help customers get accurate answers about products and company policies while identifying situations that require human assistance.

The system combines structured business knowledge, natural-language intent detection, conversation memory, support-case tracking, and escalation logic to simulate a practical customer-support workflow.

## Project Goals

* Provide accurate product information
* Answer customer questions using structured company knowledge
* Apply company policies consistently
* Maintain context across customer follow-up questions
* Identify customer intent automatically
* Track the current support case
* Escalate sensitive, disputed, or unusual issues to human support
* Reduce repetitive customer-support work

## Products

The initial Nova product catalog includes:

* Nova Play Station
* Nova Smart Glasses
* Nova Camera
* Nova WiFi Router

## Current Features

### Product Knowledge

Nova can retrieve structured information about products, including:

* Product names
* Categories
* Prices
* Descriptions
* Features
* Stock information
* Warranty periods

### Knowledge Base

Nova retrieves information from structured company knowledge covering:

* Returns and refunds
* Shipping and delivery
* Payments
* Privacy and security
* Product warranties

### Intent Detection

Nova currently recognizes several customer-support intents:

* Price
* Warranty
* Return
* Shipping
* Payment
* Security
* Unknown requests

### Conversation Memory

Nova can remember the customer's:

* Product
* Intent

This allows follow-up questions such as:

> "What is the price of the Nova Play Station?"

followed by:

> "What about the warranty?"

without requiring the customer to repeat the product name.

Nova can also switch product context when the customer introduces a different product.

### Support Case Tracking

Nova maintains a support case containing:

* Product
* Intent
* Status
* Human-support requirement
* Next action

Example:

```text
----- Support Case -----
Product: Nova Play Station
Intent: Return
Status: Needs verification
Needs human: False
Next action: Verify order information
------------------------
```

### Intelligent Escalation

Nova distinguishes between normal requests and situations that may require human intervention.

Examples include:

**Late or missing delivery**

> "My order is late."

→ Human review recommended.

**Payment dispute**

> "I was charged twice."

→ Human review recommended.

**Missing refund**

> "I never got my refund."

→ Human review recommended.

**Security incident**

> "Someone accessed my account without permission."

→ Human support.

**Unknown question**

> "Can you tell me tomorrow's weather?"

→ Escalated rather than answered with unsupported information.

### Automated Testing

The project includes automated tests for:

* Intent detection
* Knowledge retrieval
* Support-case memory

Current test suites:

```text
test_app.py
test_knowledge.py
test_cases.py
```

All current test suites pass successfully.

## Project Structure

```text
Nova-AI-Customer-Support/
│
├── app.py
├── app_backup.py
├── test_app.py
├── test_knowledge.py
├── test_cases.py
├── api_test.py
│
├── knowledge/
│   └── knowledge_base.py
│
├── data/
│   ├── products.json
│   └── policies.json
│
└── README.md
```

## Technology

* Python
* JSON
* Structured knowledge retrieval
* Natural-language intent detection
* Conversation-state management
* Rule-based escalation
* Automated testing
* Git and GitHub
* OpenAI API integration (planned)

## Architecture

The current workflow can be summarized as:

```text
Customer Question
       ↓
Intent Detection
       ↓
Product Identification
       ↓
Conversation Memory
       ↓
Knowledge Retrieval
       ↓
Response Logic
       ↓
Support Case Update
       ↓
Human Escalation When Necessary
```

## Example Conversation

```text
Customer: What is the price of the Nova Play Station?

Nova: Nova Play Station costs $350.

Customer: What about the warranty?

Nova: Nova Play Station has a 2-year warranty.

Customer: I was charged twice.

Nova: I'm sorry you're experiencing a payment issue. I'll need to
verify the transaction details. Because this may involve a disputed
or unauthorized charge, the issue may need to be escalated to human support.
```

## Project Status

**Core customer-support workflow completed.**

The local application currently supports product knowledge retrieval, intent detection, multi-turn conversation context, support-case tracking, and intelligent escalation.

The next development stage is to further polish the application and prepare it for public GitHub presentation before connecting the OpenAI API.

## Future Improvements

Planned improvements include:

* OpenAI-powered natural-language responses
* More advanced retrieval/RAG
* Expanded product and policy knowledge
* Customer order lookup
* Authentication and security controls
* More comprehensive automated evaluation
* Web-based customer-support interface
* Logging and monitoring
* Production deployment

## Purpose

This project is being developed as a practical AI engineering and consulting portfolio project.

It demonstrates how AI systems can combine structured business knowledge, workflow logic, conversation state, evaluation, and human escalation to solve real-world customer-support problems.
