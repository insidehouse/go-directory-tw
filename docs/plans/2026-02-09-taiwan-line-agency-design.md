# Taiwan LINE Marketing Agency — System Design

## Problem Statement

Taiwan service businesses (tutoring schools, dental clinics, gyms, salons) rely heavily on LINE for customer communication but use it primitively — broadcast-all with no segmentation, no automation, no tracking. There is no Taiwan-localized all-in-one marketing platform equivalent to GoHighLevel.

**GoHighLevel** is a US-based all-in-one marketing automation platform ($82.7M revenue, 70K customers, 781% 3-year growth) designed for marketing agencies. Its killer feature is white-label SaaS mode — agencies rebrand and resell it to clients for recurring revenue. However, it fundamentally doesn't fit Taiwan due to LINE dominance, local payment gateways, and OMO (online-merge-offline) patterns.

## Market Context

### Why Not GoHighLevel in Taiwan?

| US (HighLevel Strength) | Taiwan (Actual Need) |
|------------------------|---------------------|
| SMS marketing | LINE Official Account push notifications |
| Email-first campaigns | LINE-first, email secondary |
| Stripe / PayPal | ECPay / Newebpay / convenience store payment |
| Phone voice drops | LINE messages / stickers |
| English interface | Traditional Chinese (繁體中文) |
| Online-only funnels | OMO — convenience store pickup & payment |

### Key Taiwan Market Facts

- **LINE penetration**: 94% of population (22M monthly active users)
- **LINE for business**: People exchange LINE accounts instead of business cards
- **E-commerce**: NT$1.2T GMV (2023), 60% mobile, 10-12% annual growth
- **Payment**: ECPay (market leader, 2.88%), Newebpay, convenience store payment/pickup
- **Marketing automation adoption**: Relatively slow compared to global trends

### Taiwan Local Tool Ecosystem

**LINE CRM Specialists:**
- **MAAC (漸強實驗室 Crescendo Lab)** — Taiwan LINE CRM market leader, 400+ brands, NT$2,660/mo+. AI purchase prediction, cart reminders, product recommendations.
- **Lychee ACHO** — LINE OA marketing management, friend segmentation, raffle interactions

**Local CRM Systems:**
- **ORDERLY** — B2C e-commerce CRM, 1-week rapid deployment, free personal version
- **ECFIT** — E-commerce brand CRM, integrates website POS + LINE customer management
- **Vital CRM (叡揚資訊)** — Enterprise-grade, AI Copilot, social media integration
- **鼎新 CRM (Digiwin)** — Manufacturing/distribution/services, deep ERP integration

**International Players in Taiwan:**
- **Salesforce** — Highest market share, local agents for implementation
- **HubSpot** — Tech sector adoption, less localized

## Target Customers

### Tier 1 — High margin, high repeat, low digital capability (best entry point)

- **Tutoring / cram schools (補教業)** — Monthly tuition model, need enrollment automation and parent communication. Natural synergy with go-directory-tw project (60+ Go schools already catalogued).
- **Medical aesthetics / dental / TCM (醫美/牙科/中醫)** — High per-visit value (NT$3,000-50,000+), rely on word-of-mouth and LINE for booking.
- **Gyms / yoga studios (健身房/瑜伽)** — Subscription model, need renewal reminders and class booking automation.

### Tier 2 — Medium margin, needs systematization

- **Restaurants (餐飲業)** — LINE loyalty points, reservations, new menu push notifications
- **Hair salons / beauty (美容美髮)** — Booking system + revisit reminders
- **Real estate agents (房仲)** — Property push notifications, customer segmentation tracking

### Why These Customers?

1. Owners typically don't understand digital marketing — willing to outsource
2. Already using LINE but primitively (broadcast-all, no segmentation)
3. Per-customer value supports NT$15,000-30,000/mo service fees
4. Results are easy to measure (foot traffic, bookings, revenue)

### Positioning Strategy

Don't call yourself "marketing agency" (行銷代理商) — too abstract. Use language customers understand:

> **「我們幫你用 LINE 自動拉回舊客戶，每月多賺 XX 萬」**
> "We help you use LINE to automatically bring back old customers and earn NT$XX more per month"

Positioning options:
- **「LINE 行銷外包」** — Most direct, instantly understood
- **「客戶自動回流系統」** — Emphasizes results
- **「OO 產業專屬行銷系統」** — Vertical positioning (e.g., tutoring-specific)

## Technical Architecture

### Phase A: Tool Integrator (Months 1-3, fast start)

```
Customer Touchpoints          Integration Layer              Backend
─────────────────            ─────────────────             ────────
LINE Official Account  ──→  MAAC (Crescendo Lab)  ──→  Google Sheets / Notion
Landing Page           ──→  Make.com (automation)  ──→  (customer data aggregation)
Forms                  ──→  n8n / Zapier          ──→  LINE push triggers
Email                  ──→  電子豹 / Mailchimp
Payment                ──→  ECPay
```

- **Pros**: Start serving clients in 1-2 weeks
- **Cons**: Manual setup per client, tool fragmentation, hard to scale
- **Best for**: Validating market demand, first 5-10 clients

### Phase B: Platform Builder (Months 4-12, long-term moat)

```
Your Platform (Next.js / Astro)
├── Dashboard (Client Portal)
│   ├── LINE OA management (LINE Messaging API)
│   ├── Customer lists & segmentation
│   ├── Automation workflow builder
│   └── Analytics reports
├── Integration Layer
│   ├── LINE Messaging API (direct integration)
│   ├── ECPay API
│   ├── Google Calendar API
│   └── GA4 API
└── Infrastructure
    ├── Supabase (DB + Auth)
    ├── Vercel (deployment)
    └── Resend / 電子豹 (Email)
```

- **Pros**: White-label resale, scalable, deep moat
- **Cons**: 3-6 months development, high initial investment
- **Best for**: After validating market demand

### Recommended Approach: A → B Progressive

| Timeline | Phase | Focus |
|----------|-------|-------|
| Month 1-3 | Phase A: manual integration | Serve 5-10 clients. Validate: will clients actually pay? Which features get used most? |
| Month 4-6 | Hybrid: productize top features | Self-build the most-used features (usually LINE automation). Productize manual processes one by one. |
| Month 7+ | Phase B: full platform | Complete platform build. Start white-labeling to other small agencies. |

## Business Model

### Revenue Streams (4 layers)

#### Layer 1: Setup Fee (one-time)

- **Price**: NT$30,000-80,000 per client
- **Includes**: LINE OA setup, automation flows, landing page, segmentation strategy
- **Delivery**: 1-2 weeks

#### Layer 2: Monthly Fee (MRR — core revenue)

| Plan | Monthly Fee | Includes |
|------|------------|---------|
| Basic (基礎版) | NT$8,000 | LINE auto-reply + monthly report |
| Pro (進階版) | NT$18,000 | + Segmented push + booking system |
| Premium (專業版) | NT$30,000 | + Landing page + ad management |

**Cost structure (Pro plan example):**
- Tool costs: NT$4,000-6,000/mo
- Labor allocation: NT$3,000-5,000/mo (assuming 10 concurrent clients)
- **Gross margin: ~50-65%**

#### Layer 3: Performance Revenue Share (advanced)

- 5-10% of incremental revenue generated through your system
- Example: Tutoring school enrolls 10 extra students/mo x NT$5,000 = NT$50,000 → your share: NT$2,500-5,000
- Requires clear tracking mechanism (UTM, dedicated LINE OA, promo codes)

#### Layer 4: White-label SaaS (ultimate goal, after Phase B)

- White-label your platform to other small agencies
- Monthly fee: NT$5,000-10,000/agency
- 50 agencies x NT$8,000 = **NT$400,000/mo MRR**
- This is what HighLevel does — Taiwan edition

### Scaling Path

```
Stage 1 (Month 1-6): Solo operation
  5 clients x NT$18,000 = NT$90,000/mo
  + Setup fees NT$50,000 x 5 = NT$250,000 (one-time)
  Goal: Validate PMF, solo operation

Stage 2 (Month 7-12): Small team
  20 clients x NT$18,000 = NT$360,000/mo
  Hire 1 support/setup person
  Start building automation platform (reduce manual work)

Stage 3 (Year 2+): Platform
  50+ direct clients + white-label to 10+ small agencies
  MRR target: NT$1,000,000+/mo
  Transition: no longer an agency — now a SaaS company
```

### Key KPIs

| Metric | Target |
|--------|--------|
| Monthly churn rate | < 5% |
| Customer lifetime (LTV) | > 12 months |
| Customer acquisition cost (CAC) | < 1 month fee |
| Gross margin | > 50% |

### Path to Passive Income

1. **Templatize** — One standard flow template per industry (tutoring template, medical aesthetics template...). New clients: 80% template, 20% custom.
2. **Self-service** — Clients can edit push content and schedules themselves. You handle strategy only.
3. **Auto-reporting** — GA4 + Looker Studio auto-generated reports, no manual work.
4. **Platform** — Clients sign up and configure themselves. You collect platform fees.

## Synergy with go-directory-tw

The existing Go directory project provides a natural client pipeline for the tutoring/academy vertical:

- **60+ Go schools** already catalogued with contact info
- Built-in trust and relationships with school owners
- Can offer "upgrade to marketing system" as a natural upsell
- Dog-food your own tools on the directory itself (LINE integration for school inquiries)
- The directory becomes a lead generation channel for the agency business

## Key Decisions (Resolved)

### 1. Vertical Market Strategy: Go Schools → Tutoring (Beachhead)

**Decision**: Start with Go schools from go-directory-tw, then expand to broader tutoring market.

- **Phase 1**: 5-10 Go schools (warm leads, existing relationships from directory)
- **Phase 2**: Use Go school case studies to sell to math/English/music cram schools
- **Phase 3**: Position as 「補教業專屬 LINE 行銷系統」

**Rationale**: Go schools alone are too small (~100-200 in Taiwan) but serve as perfect proof-of-concept. The broader tutoring market has 18,000+ registered cram schools.

### 2. LINE CRM: Progressive Build vs Buy (C → A → B)

| Stage | Tool | Trigger to Upgrade |
|-------|------|--------------------|
| First 3 clients | LINE OA built-in + Make.com | Need more professional features |
| 4-15 clients | MAAC (漸強實驗室) NT$2,660+/mo | Margin pressure from MAAC costs |
| 15+ clients | Self-built platform (LINE Messaging API) | Scale demands full control |

### 3. Solo Founder Capacity

| Metric | Value |
|--------|-------|
| Time per client per month | 5-8 hours |
| Available service hours | ~110 hrs/mo |
| Max clients (Phase A, manual) | ~13 |
| Max clients (templatized) | ~22 |
| Solo revenue ceiling | NT$270,000/mo (15 clients x NT$18K) |
| First hire trigger | 15+ clients |

### 4. Legal/Tax Structure: Progressive Registration

| Stage | Revenue | Structure | Tax |
|-------|---------|-----------|-----|
| POC | < NT$50K/mo | Unregistered freelancer | Personal income tax only |
| Growing | NT$50K-200K/mo | 個人工作室/行號 | 1% business tax (小規模營業人) |
| Established | > NT$200K/mo | 有限公司 | 5% business tax + 20% corporate tax |

**Setup costs**: 行號 NT$5,000-10,000 / 有限公司 NT$8,000-14,000
**Key note**: 行號 cannot be converted to 有限公司 — must establish new entity.

### 5. Pricing Validation Strategy: Gradual Price Escalation

| Phase | Pricing | Purpose |
|-------|---------|---------|
| Client 1-2 | Free (3-month POC) | Get testimonials + ROI data |
| Client 3-5 | NT$8,000/mo | Validate willingness to pay |
| Client 6+ | NT$15,000-18,000/mo | Full pricing with case study proof |

**ROI anchor for tutoring**: System must deliver 5+ new students/mo (NT$25,000+ incremental revenue) to justify NT$18,000/mo fee. Below that, clients won't see enough value.

**Alternative pricing models if monthly fee resistance**:
- Low base + performance: NT$5,000/mo + NT$500-1,000 per new student
- Quarterly discount: NT$45,000/quarter (=NT$15,000/mo)
- Annual contract: NT$150,000/year (=NT$12,500/mo)

## Overarching Pattern

Every dimension follows the same progressive principle:

```
Vertical:    Go schools → Tutoring → Service businesses
Technology:  LINE OA + Make.com → MAAC → Self-built platform
Legal:       Freelancer → 行號 → 有限公司
Pricing:     Free POC → NT$8K → NT$18K
Capacity:    Solo (15 clients) → Small team (20+) → Platform (50+)
```

**Always validate before upgrading. Never over-invest before PMF.**

## References

- GoHighLevel: https://www.gohighlevel.com/ ($82.7M revenue, 70K customers)
- MAAC (Crescendo Lab): https://www.cresclab.com/en/product/maac
- LINE Messaging API: https://developers.line.biz/en/services/messaging-api/
- ECPay: https://www.ecpay.com.tw/
- Taiwan CRM landscape: ORDERLY, ECFIT, Vital CRM, Digiwin
