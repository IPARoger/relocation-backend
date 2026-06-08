# LOCAL_CONFIG_PLAN_v1

## Purpose

Define local configuration before Supabase schema work begins.

This file prevents secrets, provider choices, and environment assumptions from being scattered across prototypes.

## Files

### .env.example

Committed template.

May contain non-secret defaults.

Must not contain private API keys, service-role keys, passwords, or billing secrets.

### .env.local

Local-only real secrets.

Must remain ignored by Git.

Never paste into chat.

## Required Environment Variables

SUPABASE_URL

Public Supabase project URL.

Example:

https://dpmtmmryvlftfahipowa.supabase.co

SUPABASE_ANON_KEY

Public anon/publishable Supabase key.

Safe for browser use, but still should not be casually pasted into public places.

GEOAPIFY_API_KEY

Geoapify key for city search/autocomplete.

Must not be committed.

CITY_PROVIDER

Default:

geoapify

DEFAULT_LANGUAGE

Default:

en

Used for city display language and search preference.

DEFAULT_COUNTRY_DISPLAY

Default:

en

TIMEZONE_PROVIDER

Default:

iana

TIMEZONE_LOOKUP_MODE

Default:

offline_timezonefinder_plus_zoneinfo

## Timezone Doctrine

Birth time conversion must not use current UTC offsets.

Correct flow:

birth place coordinates
→ IANA timezone ID lookup
→ historical timezone rules for birth date/time
→ UTC datetime

Timezone boundary lookup and historical offset calculation are separate responsibilities.

## City Search Doctrine

Live provider results are lookup inputs, not product truth.

Provider result
→ normalization layer
→ canonical place record
→ app usage

The app must store country, admin region, coordinates, timezone ID, provider IDs, and multilingual names where available.

## Secret Handling

Never commit:

- Supabase service_role key
- database password
- JWT secret
- Geoapify API key
- billing details
- SMTP credentials

