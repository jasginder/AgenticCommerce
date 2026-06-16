# Agentic Payments Demo 🤖💳

> Companion code for the **Payments Deep Dive** newsletter by [Jasginder Singh](https://www.linkedin.com/in/jasginder/).  
> A hands-on introduction to AI agents that talk to payment APIs.

---

## What This Is

You type a plain-English instruction like:

> *"Create a product called 'Agent Guidebook' priced at $17 and give me a payment link."*

An AI reads it, calls the Stripe API to create your product and price, and hands back a live payment URL — automatically.

This repo shows you how to do that with **three different AI providers** so you can pick whichever works best for you.

---

## Files in This Repo

| File | AI Provider | Cost |
|---|---|---|
| `PDD_Stripe_Agent_groq.py` | **Groq** (Llama 3.3) | ✅ Free — best place to start |
| `PDD_Stripe_Agent_openai.py` | **OpenAI** (GPT-4o mini) | ~$0.002 per run |
| `PDD_Stripe_Agent_claude.py` | **Anthropic** (Claude Haiku) | ~$0.001 per run |

> **New here?** Start with `PDD_Stripe_Agent_groq.py` — Groq is completely free, no credit card required.

---

## Before You Begin (One-Time Setup)

### 1 — Install Python
If you don't have Python installed: [python.org/downloads](https://www.python.org/downloads/)  
Verify it's working by opening Terminal (Mac) or Command Prompt (Windows) and typing:
```
python --version
```

### 2 — Get a FREE Stripe Test Key
Stripe test mode is free and won't charge real money.

1. Create a free account at [stripe.com](https://stripe.com)
2. Go to [dashboard.stripe.com/test/apikeys](https://dashboard.stripe.com/test/apikeys)
3. Copy the **Secret key** — it starts with `rk_test_`

---

## Option A — Groq (Free, Recommended for Beginners)

**Install:**
```bash
pip install groq stripe
```

**Get a free Groq API key** (no credit card):
1. Go to [console.groq.com](https://console.groq.com)
2. Sign in with Google
3. Click **API Keys → Create API Key**
4. Copy the key — it starts with `gsk_`

**Configure the file:**  
Open `PDD_Stripe_Agent_groq.py` and paste your keys:
```python
GROQ_KEY   = "gsk_..."       # your Groq key
STRIPE_KEY = "rk_test_..."   # your Stripe test key
```

**Run it:**
```bash
python PDD_Stripe_Agent_groq.py
```

---

## Option B — OpenAI / ChatGPT

**Install:**
```bash
pip install openai stripe
```

**Get an OpenAI API key:**
1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Click **Create new secret key**
3. Copy the key — it starts with `sk-`

> Note: OpenAI is pay-as-you-go. Running this script costs roughly $0.002 (less than a cent). New accounts may receive free starter credits.

**Configure the file:**  
Open `PDD_Stripe_Agent_openai.py` and paste your keys:
```python
OPENAI_KEY = "sk-..."        # your OpenAI key
STRIPE_KEY = "rk_test_..."   # your Stripe test key
```

**Run it:**
```bash
python PDD_Stripe_Agent_openai.py
```

---

## Option C — Claude / Anthropic

**Install:**
```bash
pip install anthropic stripe
```

**Get an Anthropic API key:**
1. Go to [console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys)
2. Click **Create Key**
3. Copy the key — it starts with `sk-ant-`

> Note: Anthropic is pay-as-you-go. Running this script costs roughly $0.001. New accounts may receive free starter credits.

**Configure the file:**  
Open `PDD_Stripe_Agent_claude.py` and paste your keys:
```python
CLAUDE_KEY = "sk-ant-..."    # your Anthropic key
STRIPE_KEY = "rk_test_..."   # your Stripe test key
```

**Run it:**
```bash
python PDD_Stripe_Agent_claude.py
```

---

## What to Expect

When the script runs successfully you'll see:

```
🤖  Instruction → "Create a product called 'Agent Guidebook' priced at $17..."
    Sending to AI...

  ⚙  Creating 'Agent Guidebook' at $17.00 in Stripe...
  AI called: create_stripe_payment_link({'product_name': 'Agent Guidebook', 'price_dollars': 17.0})

✅  Done!  Share this payment link:
    https://buy.stripe.com/test/xxxxxxxxxxxx
```

You can verify the product was created in your [Stripe test dashboard](https://dashboard.stripe.com/test/products).

---

## How It Works (The Concept)

```
Your plain-English instruction
        ↓
    AI Model
  (reads intent, extracts product name + price)
        ↓
  create_stripe_payment_link()
  (Python function that calls the Stripe API)
        ↓
  Payment link URL returned to you
```

The AI doesn't hardcode anything — it reads your sentence, figures out what the product name and price are, and passes them to the function. Change `MY_INSTRUCTION` in any file to create any product at any price.

---

## Common Issues

**`ModuleNotFoundError`** — Run the `pip install` command for your chosen file first.

**Stripe key error** — Make sure you're using the **Secret** key (starts with `rk_test_`), not the Publishable key.

**Groq quota error** — Wait a minute and try again. The free tier has a per-minute rate limit.

**OpenAI/Anthropic billing error** — Add a payment method at your provider's dashboard. Both charge fractions of a cent per run.

---

## Disclaimer

This code is provided for educational and demonstration purposes only. See the full disclaimer at the top of each `.py` file. Use Stripe in **test mode** while learning — test keys (`rk_test_`) never charge real money.

---

## About

**Jasginder Singh** is a Director of Product at Mastercard's Open Finance business team and writes the [Payments Deep Dive](https://www.linkedin.com/newsletters/) newsletter covering payments infrastructure, agentic commerce, and all things payments.

This repo is part of a series on hands-on agentic payments experiments for product and fintech professionals.

---

*Found this useful? ⭐ Star the repo and share the LinkedIn article with your network.*
