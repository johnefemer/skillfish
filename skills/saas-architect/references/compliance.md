# Compliance Reference

Architecture requirements and decision trees for common SaaS compliance frameworks.

## SOC 2 Type II

**When required:** Any B2B customer asking "do you have SOC 2?" during sales — plan for Year 1.

**Architecture requirements:**
- Audit logging on all data mutations (see `database-standards.md`)
- Encryption at rest (Supabase/AWS default) and in transit (TLS 1.2+)
- Access control with role-based permissions
- Vulnerability management (Dependabot, Snyk)
- Incident response runbook

**Tooling:** Vanta or Drata for evidence collection (~$1K–3K/month).

---

## GDPR

**When required:** Any EU customers or processing EU personal data.

**Architecture requirements:**
- Data residency: host in EU region (Supabase EU, AWS eu-west-1)
- Right to erasure: implement `DELETE /users/:id` that anonymizes PII (do not hard-delete — breaks audit logs)
- Data processing agreements (DPAs) with all sub-processors
- Cookie consent for any analytics/tracking

**Anonymization pattern:**
```sql
UPDATE users SET
  email = 'deleted-' || id || '@deleted.invalid',
  name = 'Deleted User',
  deleted_at = now()
WHERE id = $1;
```

---

## HIPAA

**When required:** Any US healthcare data (PHI — Protected Health Information).

**Architecture implications (BREAKING):**
- Supabase, Vercel, Railway are **NOT** HIPAA-eligible — do not use for PHI
- Use AWS with signed BAA (Business Associate Agreement): RDS, S3 (server-side encryption), Cognito
- Audit logs must be tamper-proof (CloudTrail)
- PHI must be encrypted at the field level for highest sensitivity

**Recommendation:** Avoid HIPAA scope for MVP unless healthcare is the core vertical. Plan AWS migration at Series A.

---

## PCI DSS

**When required:** Storing, processing, or transmitting cardholder data.

**Architecture recommendation:** Use Stripe — it scopes you to SAQ-A (minimal compliance). Never store raw card data.

**Required:**
- HTTPS everywhere (TLS 1.2+ minimum)
- No card data in logs
- Stripe.js / Stripe Elements (card data never touches your servers)

---

## Decision Tree

```
Does the product handle:
├── Healthcare data (PHI)?      → HIPAA required → AWS mandatory
├── EU personal data?           → GDPR required → EU region + DPAs
├── Payment card data?          → Use Stripe (SAQ-A) → no card storage
└── Enterprise B2B customers?   → SOC 2 Type II → plan Year 1 audit
```
