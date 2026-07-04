# ADR 0001: Build An Original Generator, Not A Clone Library

## Status

Accepted

## Context

DIY foil board builders often start by tracing an existing successful board. That is practical but not a good open-source foundation. The project should be useful, legal, and ethically clean.

## Decision

Foil Board Toolkit will generate original parameterised board designs. Public board dimensions and photographs may inform ranges and relationships, but the repo will not store copied commercial geometry or produce named-board replicas.

## Consequences

- The first data model must distinguish reference observations from generated geometry.
- Source attribution matters.
- We need tests and visual outputs that prove generated boards are coherent without relying on a clone target.
- Marketing should say "inspired by public design trends", not "clone this board".

