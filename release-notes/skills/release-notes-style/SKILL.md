---
name: release-notes-style
description: The house format and voice for release notes. Use whenever you are asked to turn merged pull requests, commits or a changelog into notes for users.
---

# Release notes style

Write for someone who uses the product and has never seen the repository.

Sections, in this order, and no others: Added, Fixed, Changed. Omit a section
with no entries rather than printing it empty.

Added is something that was not there before. Fixed is behaviour that was wrong
and is now right. Changed is behaviour that already existed and now works
differently, including anything faster, cheaper or smaller.

Every entry is one line, starts with a past-tense verb, and names the thing a
user can see. Never a file, a package, a service or an internal component.

An entry a user cannot notice does not appear at all: dependency bumps,
refactors, test changes and build work are dropped, never summarised.

Numbers come from the input and are exact. Never invent a count, a percentage
or a duration. When the input gives a before and an after, print both.

No adjectives of praise. Not "significantly faster", but "starts in 0.3 ms,
was 1.1 ms". No em dashes anywhere.
