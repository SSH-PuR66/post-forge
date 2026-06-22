---
title: "PostForge: I Built a Social Media Scheduler with AI Generation and Stripe Billing in Pure Python"
published: false
description: "A FastAPI + SQLite social media automation tool — schedule posts across platforms, track analytics, and generate content with AI. All from one codebase."
tags: python, fastapi, ai, automation
cover_image: ""
canonical_url:
---

Content creators have two problems: coming up with posts and remembering to publish them. PostForge solves both — it generates social media posts with AI and schedules them across platforms with analytics tracking.

But what I'm actually proud of is the architecture. The entire backend is 4 Python files. No bloated framework, no monolith. Just FastAPI doing what it does best.

---

## How it works

```
User pastes content (article, notes, ideas)
        ↓
AI generates platform-specific posts
  → Twitter thread (280-char chunks)
  → LinkedIn article summary
  → Instagram caption
        ↓
User reviews, edits, schedules
        ↓
Scheduler publishes at optimal times
        ↓
Analytics tracks engagement
```

### The AI generation

The user pastes at least 100 characters of content — a blog post draft, meeting notes, whatever. The AI service generates formatted posts for each platform, respecting character limits and platform conventions.

```python
@app.post("/api/generate")
async def generate(body: GenerateRequest):
    if len(body.content.strip()) < 100:
        raise HTTPException(400, "Paste at least 100 characters.")
    return await generate_posts(body.content)
```

The 100-character minimum exists because AI needs context. Feed it two sentences and you get generic slop. Feed it a paragraph and you get platform-specific content.

### Rate limiting by tier

Free users get 3 AI generations per day. The limit is tracked by IP:

```python
if not is_pro:
    ip = request.headers.get("x-forwarded-for", request.client.host).split(",")[0]
    today = date.today().isoformat()
    if db.free_uses_today(ip, today) >= FREE_DAILY_LIMIT:
        raise HTTPException(402, "Free limit reached. Upgrade to Pro.")
    db.increment_usage(ip, today)
```

Pro users (via Stripe subscription) get unlimited. The auth check uses a Bearer token from the `Authorization` header.

---

## Stripe billing

The checkout flow is 3 endpoints:

1. **`POST /api/checkout`** — creates a Stripe Checkout Session, returns the URL
2. **`GET /api/activate?session_id=...`** — validates payment, generates an API token
3. Token is stored client-side and sent as `Authorization: Bearer <token>` on every request

```python
@app.post("/api/checkout")
async def checkout():
    session = stripe.checkout.Session.create(
        mode="subscription",
        line_items=[{"price": os.environ["STRIPE_PRICE_ID"], "quantity": 1}],
        success_url=f"{APP_URL}/?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=APP_URL,
    )
    return {"url": session.url}
```

No webhook needed for the basic flow — the activation endpoint pulls the session status directly from Stripe. For production, you'd add a webhook for subscription lifecycle events.

---

## The database

SQLite with four tables:

- `posts` — scheduled/published content with platform, status, and timestamps
- `analytics` — engagement metrics per post (likes, shares, comments)
- `accounts` — platform connections
- `schedule_log` — execution history

No ORM. The `db.py` module uses raw SQL via `sqlite3`. For 4 tables, an ORM is overhead without benefit.

---

## Platform adapters

Each platform has an adapter module that handles the API specifics:

```
platforms/
├── twitter.py    # Twitter/X API v2
├── linkedin.py   # LinkedIn API
└── instagram.py  # Instagram Graph API
```

The scheduler calls the appropriate adapter based on the post's target platform. Each adapter handles authentication, rate limiting, and error formatting specific to its platform.

This is the extensibility story: want to add TikTok? Write a new adapter file, register it in the scheduler, done. The core scheduling logic doesn't change.

---

## Analytics export

```bash
# JSON for automation
GET /api/analytics?format=json

# CSV for spreadsheets
GET /api/analytics?format=csv

# Markdown for reports
GET /api/analytics?format=markdown
```

Three formats because different consumers need different things. Your Zapier automation wants JSON. Your marketing team wants CSV. Your weekly report wants Markdown.

---

## What I'd improve

- **Webhook for Stripe lifecycle** — handle cancellations, failed payments, plan changes
- **OAuth for platforms** — currently requires API keys, should use OAuth flows
- **Batch scheduling from CSV** — import a content calendar in one shot
- **Preview rendering** — show what the post will look like on each platform before publishing

---

## What this project shows

1. **Practical AI integration** — not a chatbot, a tool that generates real deliverables
2. **Multi-platform thinking** — one backend serving multiple frontends (Twitter, LinkedIn, Instagram)
3. **Billing architecture** — Stripe Checkout, token-based auth, tier enforcement
4. **Clean separation** — `main.py` (routes), `ai.py` (generation), `db.py` (persistence), platform adapters

---

*Source: [github.com/SSH-PuR66/post-forge](https://github.com/SSH-PuR66/post-forge)*
