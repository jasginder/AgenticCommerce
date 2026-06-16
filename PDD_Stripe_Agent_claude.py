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
╔═══════════════════════════════════════════════╗
║    STRIPE PAYMENT LINK CREATOR  —  Claude / Anthropic Version ║
╚═══════════════════════════════════════════════╝

COST    Not free, but extremely cheap. Claude Haiku costs ~$0.001
        per run of this script. New Anthropic accounts often get
        a small free credit to start.

ONE-TIME SETUP
──────────────
  Step 1 — Install:
            pip install anthropic stripe

  Step 2 — Get a Claude API key:
            https://console.anthropic.com/settings/keys  →  Create Key
            (starts with  sk-ant-...)

  Step 3 — Get a FREE Stripe TEST key:
            https://dashboard.stripe.com/test/apikeys
            (starts with  rk_test_...)

  Step 4 — Paste both keys below, then run:
            python stripe_agent_claude.py

── DIFFERENCE FROM GROQ VERSION ──────────────────────────────
  Claude uses a different API format in 3 areas:
    1. TOOLS — uses "input_schema" instead of nested "function"/"parameters"
    2. API call — client.messages.create() needs max_tokens
    3. Response — check response.content blocks for type "tool_use"
  The Stripe function itself is completely unchanged.
"""

import anthropic
import stripe


# ── PASTE YOUR KEYS HERE ────────────────────────────────────────────────────

CLAUDE_KEY = "sk-ant-..."   # from console.anthropic.com/settings/keys
STRIPE_KEY = "rk_test_..."  # from dashboard.stripe.com/test/apikeys


# ── YOUR INSTRUCTION IN PLAIN ENGLISH ───────────────────────────────────────

MY_INSTRUCTION = (
    "Create a product called 'Agent Guidebook' "
    "priced at $17 and give me a payment link."
)


# ── NOTHING TO EDIT BELOW THIS LINE ─────────────────────────────────────────

stripe.api_key = STRIPE_KEY


# ── THE TOOL  (Stripe logic — identical to the Groq version) ────────────────

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


# ── DESCRIBE THE TOOL TO CLAUDE (different format from Groq/OpenAI) ──────────
#   Claude uses "input_schema" where Groq/OpenAI use "function"/"parameters"

TOOLS = [{
    "name": "create_stripe_payment_link",
    "description": "Creates a product in Stripe and returns a payment link URL",
    "input_schema": {                               # ← Claude calls this "input_schema"
        "type": "object",
        "properties": {
            "product_name":  {"type": "string", "description": "Name of the product"},
            "price_dollars": {"type": "number", "description": "Price in US dollars"},
        },
        "required": ["product_name", "price_dollars"],
    },
}]


# ── SEND TO AI AND RUN THE RESULT ────────────────────────────────────────────

print(f'\n🤖  Instruction → "{MY_INSTRUCTION}"')
print("    Sending to AI (Claude Haiku via Anthropic)...\n")

client = anthropic.Anthropic(api_key=CLAUDE_KEY)

response = client.messages.create(
    model="claude-haiku-4-5-20251001",           # cheapest Claude model
    max_tokens=1024,                              # ← Claude requires this; Groq/OpenAI don't
    tools=TOOLS,
    messages=[{"role": "user", "content": MY_INSTRUCTION}],
)

# Claude returns a list of content blocks; find the tool_use block
for block in response.content:
    if block.type == "tool_use":                  # ← Claude calls it "tool_use"
        args = block.input                        #   (Groq/OpenAI use message.tool_calls)
        print(f"  AI called: {block.name}({args})")

        url = create_stripe_payment_link(**args)

        print(f"\n✅  Done!  Share this payment link:")
        print(f"    {url}")
        break
