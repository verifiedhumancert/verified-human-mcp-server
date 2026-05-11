# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it
privately — **do not open a public GitHub issue**.

**Preferred channel:** [GitHub Private Vulnerability Reporting](https://github.com/verifiedhumancert/verified-human-mcp-server/security/advisories/new)

**Alternative:** email `jj@verifiedhumancert.com` with:

- A description of the issue and its impact.
- Steps to reproduce (proof-of-concept code, request payloads, etc.).
- Affected version(s) and environment.
- Your name and contact for follow-up (optional — anonymous reports are
  accepted).

### What to expect

| Stage              | Target SLA       |
| ------------------ | ---------------- |
| Acknowledgement    | within 3 days    |
| Triage & severity  | within 7 days    |
| Fix or mitigation  | within 30 days   |
| Public disclosure  | coordinated with reporter after a fix is available |

We follow [coordinated disclosure](https://en.wikipedia.org/wiki/Coordinated_disclosure):
please give us a reasonable window to ship a fix before going public.

## Scope

In scope:

- The MCP server code in this repository.
- The HTTP client that talks to the Verified Human Cert API.

Out of scope (report upstream):

- Vulnerabilities in the [Verified Human Cert](https://verifiedhumancert.com) API itself.
- Vulnerabilities in dependencies — please report to the dependency's
  maintainers and let us know so we can pin a fixed version.

## Acknowledgements

We thank all researchers who responsibly disclose security issues. With your
permission, we'll credit you in the release notes for the fix.
