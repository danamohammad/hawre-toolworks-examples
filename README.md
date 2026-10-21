# Hawre Toolworks examples

Deterministic API utilities running on local hardware, without an LLM dependency. Purchases belong on OKX.AI using the listed service IDs. No revenue or earnings guarantee.

Public catalog: https://a2mcp-tools.danamohammadkhidhir.workers.dev/tools.json

Five flagship examples are described in `verified-offerings.json`, with a sample request and locally computed result for each. The original category listings were verified approved on 21 October 2026. Current availability must be checked again before publishing a promotion.

An unpaid POST to the published endpoint returns HTTP 402 with the payment requirements; it does not deliver the paid result or charge the caller. The result files here are local demonstrations, not receipts. No script in this folder signs or executes a payment. Use the official OKX workflow for actual purchases.

The public catalog also contains newly deployed APIs that are not yet submitted or approved; those must not be advertised as approved marketplace services. No operations dashboard, account inventories, wallet records, credentials, customer data or private material belongs in a public repository.

Approved marketplace pages verified publicly on 21 October 2026:

- [Developer checks](https://www.okx.ai/agents/13990)
- [Dataset utilities](https://www.okx.ai/agents/13989)
- [Market metrics](https://www.okx.ai/agents/13986)

Each example includes its JSON input schema. Run `python3 probe.py` for unpaid availability checks. The example requests are synthetic and the results were computed locally.
