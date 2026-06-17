import os
import secrets
from datetime import date

import stripe
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import db
from ai import generate_posts

load_dotenv()
stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
APP_URL = os.environ.get("APP_URL", "http://localhost:8000")
FREE_DAILY_LIMIT = int(os.environ.get("FREE_DAILY_LIMIT", 3))

app = FastAPI(title="PostForge")
db.init_db()


class GenerateRequest(BaseModel):
    content: str


@app.get("/")
async def home():
    return FileResponse("static/index.html")


@app.post("/api/generate")
async def generate(
    body: GenerateRequest,
    request: Request,
    authorization: str | None = Header(default=None),
):
    if len(body.content.strip()) < 100:
        raise HTTPException(400, "Paste at least 100 characters of content.")

    is_pro = False
    if authorization and authorization.startswith("Bearer "):
        is_pro = db.token_is_active(authorization.removeprefix("Bearer "))

    if not is_pro:
        ip = request.headers.get("x-forwarded-for", request.client.host).split(",")[0]
        today = date.today().isoformat()
        if db.free_uses_today(ip, today) >= FREE_DAILY_LIMIT:
            raise HTTPException(
                402, "Free limit reached (3/day). Upgrade to Pro for unlimited."
            )
        db.increment_usage(ip, today)

    try:
        return await generate_posts(body.content)
    except Exception:
        raise HTTPException(502, "Generation failed, please retry.")


@app.post("/api/checkout")
async def checkout():
    session = stripe.checkout.Session.create(
        mode="subscription",
        line_items=[{"price": os.environ["STRIPE_PRICE_ID"], "quantity": 1}],
        success_url=f"{APP_URL}/?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=APP_URL,
    )
    return {"url": session.url}


@app.get("/api/activate")
async def activate(session_id: str):
    session = stripe.checkout.Session.retrieve(session_id)
    if session.payment_status != "paid":
        raise HTTPException(403, "Payment not completed.")
    token = secrets.token_urlsafe(32)
    db.create_token(token, session.customer)
    return {"token": token}


@app.post("/api/stripe/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig = request.headers.get("stripe-signature", "")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig, os.environ["STRIPE_WEBHOOK_SECRET"]
        )
    except Exception:
        raise HTTPException(400, "Invalid signature")

    if event["type"] in ("customer.subscription.deleted", "invoice.payment_failed"):
        db.deactivate_customer(event["data"]["object"]["customer"])
    return {"ok": True}


app.mount("/static", StaticFiles(directory="static"), name="static")
