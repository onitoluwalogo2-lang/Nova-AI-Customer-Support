# Nova AI Customer Support System

## Overview

Nova is an AI-powered customer-support system designed to help customers get accurate answers about products and company policies while identifying situations that require human assistance.

The system combines structured business knowledge, natural-language intent detection, conversation memory, support-case tracking, OpenAI-powered response generation, and escalation logic to simulate a practical customer-support workflow.

## Project Goals

- Provide accurate product information
- Answer customer questions using structured company knowledge
- Apply company policies consistently
- Maintain context across customer follow-up questions
- Identify customer intent automatically
- Track the current support case
- Escalate sensitive, disputed, or unusual issues to human support
- Reduce repetitive customer-support work
- Use AI to generate natural customer-facing responses

## Products

The initial Nova product catalog includes:

- Nova Play Station
- Nova Smart Glasses
- Nova Camera
- Nova WiFi Router

## Current Features

### Product Knowledge

Nova can retrieve structured information about products, including:

- Product names
- Categories
- Prices
- Descriptions
- Features
- Stock information
- Warranty periods

### Knowledge Base

Nova retrieves information from structured company knowledge covering:

- Returns and refunds
- Shipping and delivery
- Payments
- Privacy and security
- Product warranties

The knowledge base is separated from the application logic so that company information can be updated without rewriting the main application workflow.

### Intent Detection

Nova recognizes several customer-support intents:

- Price
- Warranty
- Return
- Shipping
- Payment
- Security
- Unknown requests

### Product Detection

Nova identifies the product involved in a customer's question and uses the identified product when retrieving relevant knowledge.

This allows the system to handle questions such as:

> What is the price of the Nova Play Station?

followed by:

> What about the warranty?

without requiring the customer to repeat the product name.

### Conversation Memory

Nova maintains conversation context across follow-up questions.

The system remembers:

- Product
- Intent

This allows Nova to understand follow-up questions while also switching context when a customer introduces a different product.

### Support Case Tracking

Nova maintains a support case containing:

- Product
- Intent
- Status
- Human-support requirement
- Next action

Customers can type:

```text
case
```

### Evaluation

Nova includes a dedicated evaluation suite for testing customer-support behavior.

The evaluation suite currently covers:

- Price handling
- Return handling
- Shipping handling
- Delivery escalation
- Payment escalation
- Security escalation
- Unknown request handling
- Escalation reset
- Product memory
- Product context switching

The evaluation tests use a controlled AI response so the support workflow can be evaluated without depending on the OpenAI API.

Current evaluation result:

```text
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
10/10 evaluation scenarios passed