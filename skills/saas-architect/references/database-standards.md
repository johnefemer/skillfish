# Database Standards Reference

Schema conventions, RLS patterns, and migration standards for multi-tenant SaaS.

## Naming Conventions

- Tables: `snake_case`, plural (`users`, `tenant_subscriptions`)
- Primary keys: `id uuid DEFAULT gen_random_uuid()`
- Tenant FK: `tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE`
- Timestamps: `created_at timestamptz DEFAULT now()`, `updated_at timestamptz DEFAULT now()`
- Soft deletes: `deleted_at timestamptz` (never hard-delete tenant data)

## Core Tenant Schema

```sql
CREATE TABLE tenants (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  slug text UNIQUE NOT NULL,
  name text NOT NULL,
  plan text NOT NULL DEFAULT 'free',
  stripe_customer_id text,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE tenant_users (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  user_id uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  role text NOT NULL DEFAULT 'member', -- owner, admin, member
  created_at timestamptz DEFAULT now(),
  UNIQUE(tenant_id, user_id)
);
```

## Row-Level Security

```sql
-- Enable on every tenant-scoped table
ALTER TABLE [table] ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON [table]
  USING (tenant_id = current_setting('app.tenant_id')::uuid);

-- Set at query time (e.g. in middleware)
SELECT set_config('app.tenant_id', $tenantId, true);
```

## Audit Log

```sql
CREATE TABLE audit_log (
  id bigserial PRIMARY KEY,
  tenant_id uuid NOT NULL,
  user_id uuid,
  action text NOT NULL,
  entity_type text NOT NULL,
  entity_id uuid,
  payload jsonb,
  created_at timestamptz DEFAULT now()
);
-- No RLS UPDATE/DELETE policies — append-only
```

## Migration Standards

- Use sequential numbered migrations: `0001_init.sql`, `0002_add_audit_log.sql`
- Never modify a deployed migration — add a new one
- Test migrations on a copy of production data before deploying
- All `ALTER TABLE` statements must be backward-compatible for zero-downtime deploys
