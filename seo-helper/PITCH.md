Your blog, researched, written, illustrated and delivered as a draft pull request, on a schedule you set.

seo-helper is a two agent pod that runs the whole loop unattended. It picks a keyword from the topic lanes you define, reads the live top three results to find what they miss, writes the piece in your voice and your repo's post format, has a second agent draw the figures, and opens a draft PR carrying the post, the images and any registry or sitemap updates already in place. Then it emails you the link.

You review and merge. It never merges, because merging is publishing and that decision stays with you.

WHAT GETS COPIED

- seo-writer, the lead: keyword gates, competitor pass, drafting, delivery
- seo-media: authors SVG hero cards and in-body diagrams on your palette, never stock imagery
- seo-engine: the method. Five keyword gates, anti-slop writing rules, a self review checklist, the media contract and the run protocol
- seo-pod: the shared space the two agents hand files through
- A daily scheduled run, yours to retime or leave paused until you are ready

SETTING IT UP

- Connect GitHub to seo-writer. This is the one hard requirement, and a run stops cleanly without it rather than writing something it cannot deliver.
- Write your site prompt: your domain, your repo as owner/name, and three to five topic lanes tied to what you sell. Save it under Prompts and attach it to the scheduled run.
- Optionally connect DataForSEO for real search volumes. Without it the agent works from live search evidence instead and labels every figure as an estimate.
- Point the schedule at a time you will actually read drafts.

THE ONE THING TO GET RIGHT

Everything the agent knows about your site comes from the prompt in front of it. Nothing carries over between sessions, and that is deliberate: it is what lets one pod serve several sites without them bleeding into each other. Save your site prompt under Prompts, attach it to the run, and every run starts complete. Leave it out and the run stops and asks rather than guessing at a repo.

Three things only you can supply: the domain, the repo, and the lanes. The lanes are editorial intent and the one thing no agent can work out for itself. Everything else it discovers from your repo, your content path, post format, registry files, asset conventions and default branch, or falls back to a documented default.

WHAT A HEALTHY RUN LEAVES

- One draft PR labelled seo-draft on branch seo/<slug>
- One email with the link
- One line in the status file

A blocked run leaves a SKIPPED line naming exactly what was missing, and opens nothing. An unattended agent that guesses its own target writes the wrong article to the wrong repo.

Runs in your workspace, on your credits. Every agent, skill and prompt is yours to edit.
