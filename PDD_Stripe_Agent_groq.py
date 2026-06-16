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
║     STRIPE PAYMENT LINK CREATOR  —  Groq Version Demo       ║
╚══════════════════════════════════════════════╝

Created by Jasginder Singh for learning purpose.

WHAT THIS DOES
  You type a plain-English instruction.
  An AI (free Llama model via Groq) reads it, creates your Stripe
  product, and hands back a payment link — all automatically.

ONE-TIME SETUP  (~5 minutes total)
─────────────────────────────────
  Step 1 — Install (paste in Terminal / Command Prompt):
            pip install groq stripe

  Step 2 — Get a FREE Groq key (no payment or credit card entry needed):
            https://console.groq.com  (you can sign in with Google Acc → API Keys → Create)

  Step 3 — Get a FREE Stripe TEST key:
            https://dashboard.stripe.com/test/apikeys
            Copy the one that starts with  rk_test_

  Step 4 — Paste both keys below, then run:
            python stripe_agent.py
"""

from groq import Groq
import stripe
import json


# ── PASTE YOUR KEYS HERE ────────────────────────────────────────────────────

GROQ_KEY   = "gsk_xxxxxxxx"      # from console.groq.com  (starts with gsk_)
STRIPE_KEY = "rk_test_xxxxxx"  # from dashboard.stripe.com/test/apikeys


# ── YOUR INSTRUCTION IN PLAIN ENGLISH ───────────────────────────────────────
#   Change this to whatever product you want to create.

MY_INSTRUCTION = (
    "Create a product called 'Agent Guidebook' "
    "priced at $17 and give me a payment link."
)



# ── NOTHING TO EDIT BELOW THIS LINE ─────────────────────────────────────────

stripe.api_key = STRIPE_KEY


# ── THE TOOL ─────────────────────────────────────────────────────────────────
# This is the one action our agent knows how to perform.
# The AI reads the description and decides when to call this.

def create_stripe_payment_link(product_name: str, price_dollars: float) -> str:
    """Creates a Stripe product and returns a shareable payment URL."""
    print(f"\n  ⚙  Creating '{product_name}' at ${price_dollars:.2f} in Stripe...")

    product = stripe.Product.create(name=product_name)

    price = stripe.Price.create(
        product=product.id,
        unit_amount=int(price_dollars * 100),  # Stripe uses cents
        currency="usd",
    )

    link = stripe.PaymentLink.create(
        line_items=[{"price": price.id, "quantity": 1}]
    )

    return link.url   # e.g. https://buy.stripe.com/test/xxxx


# ── DESCRIBE THE TOOL TO THE AI (required for Groq / OpenAI format) ─────────
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
print("    Sending to AI (Llama via Groq)...\n")

client = Groq(api_key=GROQ_KEY)

# Step 1: AI reads the instruction and decides to call our tool
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",   # free, fast, great at tool use
    messages=[{"role": "user", "content": MY_INSTRUCTION}],
    tools=TOOLS,
    tool_choice="auto",                 # let AI decide when to use the tool
)

# Step 2: Execute what the AI decided to call
message = response.choices[0].message

if message.tool_calls:
    tool_call = message.tool_calls[0]
    args      = json.loads(tool_call.function.arguments)
    print(f"  AI called: {tool_call.function.name}({args})")

    url = create_stripe_payment_link(**args)

    print(f"\n✅  Done!  Share this payment link:")
    print(f"    {url}")

else:
    # AI replied with text instead of a tool call (shouldn't happen, but just in case)
    print(f"\n🤖  AI replied: {message.content}")