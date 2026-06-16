"""
DISCLAIMER
──────────
This code is provided for educational and demonstration purposes only.
By using or adapting this code, you agree to the following:

  • No warranty — This script is provided "as-is" without any guarantee
    of fitness for a particular purpose, accuracy, or reliability.

  • Use at your own risk — The author is not responsible for any
    unintended charges, data loss, account suspension, or system issues
    that may arise from running or modifying this code.

  • May become outdated — Stripe, Anthropic, and other third-party APIs
    change over time. The author makes no commitment to maintain or
    update this code. Always verify against official documentation.

  • Not legal or financial advice — Nothing in this file constitutes
    professional advice of any kind.

  © Jasginder Singh / Payments Deep Dive — shared for learning purposes.
    Feel free to adapt for personal or internal use; please credit
    the source if you redistribute or publish derivatives.

╔══════════════════════════════════════════════╗
║   STRIPE PAYMENT LINK CREATOR  —  OpenAI / ChatGPT Version  ║
╚══════════════════════════════════════════════╝

COST    Not free, but extremely cheap. gpt-4o-mini costs ~$0.002
        per run of this script. New OpenAI accounts often get
        a small free credit to start.

ONE-TIME SETUP
──────────────
  Step 1 — Install:
            pip install openai stripe

  Step 2 — Get an OpenAI key:
            https://platform.openai.com/api-keys  →  Create new secret key
            (starts with  sk-...)

  Step 3 — Get a FREE Stripe TEST key:
            https://dashboard.stripe.com/test/apikeys
            (starts with  rk_test_...)

  Step 4 — Paste both keys below, then run:
            python stripe_agent_openai.py

── DIFFERENCE FROM GROQ VERSION ──────────────────────────────
  Only 4 lines change:
    • pip install openai  (was groq)
    • from openai import OpenAI  (was from groq import Groq)
    • OPENAI_KEY = "sk-..."  (was GROQ_KEY = "gsk_...")
    • model = "gpt-4o-mini"  (was "llama-3.3-70b-versatile")
  Everything else — tools, Stripe code, response handling — is identical.
"""

from openai import OpenAI
import stripe
import json


# ── PASTE YOUR KEYS HERE ────────────────────────────────────────────────────

OPENAI_KEY = "sk-..."       # from platform.openai.com/api-keys
STRIPE_KEY = "rk_test_..."  # from dashboard.stripe.com/test/apikeys


# ── YOUR INSTRUCTION IN PLAIN ENGLISH ───────────────────────────────────────

MY_INSTRUCTION = (
    "Create a product called 'Agent Guidebook' "
    "priced at $17 and give me a payment link."
)


# ── NOTHING TO EDIT BELOW THIS LINE ─────────────────────────────────────────

stripe.api_key = STRIPE_KEY


# ── THE TOOL ─────────────────────────────────────────────────────────────────

def create_stripe_payment_link(product_name: str, price_dollars: float) -> str:
    """Creates a Stripe product and returns a shareable payment URL."""
    print(f"\n  ⚙  Creating '{product_name}' at ${price_dollars:.2f} in Stripe...")

    product = stripe.Product.create(name=product_name)

    price = stripe.Price.create(
        product=product.id,
        unit_amount=int(price_dollars * 100),   # Stripe uses cents
        currency="usd",
    )

    link = stripe.PaymentLink.create(
        line_items=[{"price": price.id, "quantity": 1}]
    )

    return link.url


# ── DESCRIBE THE TOOL TO THE AI ──────────────────────────────────────────────

TOOLS = [{
    "type": "function",
    "function": {
        "name": "create_stripe_payment_link",
        "description": "Creates a product in Stripe and returns a payment link URL",
        "parameters": {
            "type": "object",
            "properties": {
                "product_name":  {"type": "string", "description": "Name of the product"},
                "price_dollars": {"type": "number", "description": "Price in US dollars"},
            },
            "required": ["product_name", "price_dollars"],
        },
    },
}]


# ── SEND TO AI AND RUN THE RESULT ────────────────────────────────────────────

print(f'\n🤖  Instruction → "{MY_INSTRUCTION}"')
print("    Sending to AI (GPT-4o mini via OpenAI)...\n")

client = OpenAI(api_key=OPENAI_KEY)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": MY_INSTRUCTION}],
    tools=TOOLS,
    tool_choice="auto",
)

message = response.choices[0].message

if message.tool_calls:
    tool_call = message.tool_calls[0]
    args      = json.loads(tool_call.function.arguments)
    print(f"  AI called: {tool_call.function.name}({args})")

    url = create_stripe_payment_link(**args)

    print(f"\n✅  Done!  Share this payment link:")
    print(f"    {url}")
else:
    print(f"\n🤖  AI replied: {message.content}")
