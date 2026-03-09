---
layout: post
title: Engineering Guidelines Site
tags:
  - engineering
  - best-practices
  - architecture
  - testing
  - devops
  - sdlc
---

I've put together a reference site for engineering best practices, available at [guidelines.ryanharrison.co.uk](https://guidelines.ryanharrison.co.uk). The goal is a single place to find guidelines and conventions covering the full stack - from core principles through to deployment.

Rather than being prescriptive about specific tools, most sections aim to explain the reasoning behind a recommendation so you can apply it to your own context.

## What's Covered

**Principles and practices** - [Core engineering principles](https://guidelines.ryanharrison.co.uk/principles) covers the fundamentals: SOLID, DRY, KISS, YAGNI, clean code, and when to apply them. There's also a [code review guide](https://guidelines.ryanharrison.co.uk/sdlc/code-review) and sections on [technical debt](https://guidelines.ryanharrison.co.uk/sdlc/technical-debt), [pull requests](https://guidelines.ryanharrison.co.uk/sdlc/pull-requests), and [git workflow](https://guidelines.ryanharrison.co.uk/sdlc/git/git-workflow).

**Architecture** - Patterns for [microservices](https://guidelines.ryanharrison.co.uk/architecture/microservices), [event-driven systems](https://guidelines.ryanharrison.co.uk/architecture/event-driven-architecture), and [multi-tenancy](https://guidelines.ryanharrison.co.uk/architecture/multi-tenancy).

**API design** - [REST fundamentals](https://guidelines.ryanharrison.co.uk/api/rest/rest-fundamentals) and patterns, [GraphQL](https://guidelines.ryanharrison.co.uk/api/graphql), and [OpenAPI contract-first development](https://guidelines.ryanharrison.co.uk/api/contracts/openapi-specifications).

**Testing** - The [testing strategy](https://guidelines.ryanharrison.co.uk/testing/testing-strategy) page covers the overall approach. From there, individual pages go into unit, integration, contract, end-to-end, mutation, and chaos testing.

**Security and observability** - [Security overview](https://guidelines.ryanharrison.co.uk/security/security-overview) covering authentication, authorisation, input validation, and data protection. [Observability](https://guidelines.ryanharrison.co.uk/observability/observability-overview) covers structured logging, metrics, tracing, and alerting.

**Languages and frameworks** - Guidelines for Java, Kotlin, TypeScript, and Swift, with framework-specific sections for Spring Boot, React, Angular, React Native, Android, and iOS.

**Infrastructure** - Docker, Kubernetes, Terraform, and a fairly detailed AWS section covering compute, networking, storage, EKS, and more.
