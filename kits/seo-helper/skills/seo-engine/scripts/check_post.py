#!/usr/bin/env python3
"""Checks a post and its figures against the seo-engine writing and figure
rules, and prints what fails. Python's standard library only.

    python3 check_post.py outputs/<slug>/post.mdx --digest /workspace/site-digest.md
    python3 check_post.py outputs/<slug>/post.mdx --min-words 1200 --max-words 1800 --keyword "..."
    python3 check_post.py --svg outputs/<slug>/figures/*.svg

Exits 1 when anything fails, 0 when the post or figures are clean. It checks
what a script can: the self-review gate in references/writing.md still needs
a read.
"""

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET

DASHES = {chr(0x2014): "em dash", chr(0x2013): "en dash"}
BANNED_WORDS = (
    "delve tapestry landscape robust seamless cutting-edge groundbreaking transformative unprecedented pivotal "
    "leverage harness unlock unleash navigate foster elevate embark furthermore moreover additionally "
    "consequently notably compelling innovative dynamic utilize comprehensive paramount meticulous game-changer "
    "streamline scalable crucial remarkable profound multifaceted nuanced facilitate endeavor resonate bolster "
    "underscore illuminate empower supercharge skyrocket cultivate"
).split()
BANNED_PHRASES = [
    "shed light on", "here's the thing", "let's dive in", "it's worth noting", "in conclusion",
    "at the end of the day", "in today's world", "when it comes to", "that being said", "a testament to",
    "move the needle", "hits different", "hits home", "hits hard", "the answer?", "the result?", "my take:",
    "hot take:", "the hard part", "the part that catches", "here's the part",
]
BANNED_HEADINGS = re.compile(r"^(introduction|conclusion|in summary|summary)\b", re.IGNORECASE)
TITLE_MAX = 60
META_MAX = 155
SHORT_SENTENCE = 6
LONG_SENTENCE = 30
SVG_MIN_FONT = 14


class Findings(list):
    def add(self, where, message):
        self.append(f"{where}: {message}")


def front_matter(text):
    """(fields, body). Simple 'key: value' lines are enough for title and
    description; anything else in the block is kept as text."""
    match = re.match(r"^---\n(.*?)\n---\n?", text, re.DOTALL)
    if not match:
        return {}, text
    fields = {}
    for line in match.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep and re.fullmatch(r"[A-Za-z_][\w-]*", key.strip()):
            fields[key.strip()] = value.strip().strip("'\"")
    return fields, text[match.end():]


def prose(body):
    """The body as a reader sees its words: no code, JSON-LD, tags, link
    targets or markdown marks."""
    text = re.sub(r"^```.*?^```", " ", body, flags=re.DOTALL | re.MULTILINE)
    text = re.sub(r"<script\b.*?</script>", " ", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"^\s*(import|export)\s.*$", " ", text, flags=re.MULTILINE)
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"`[^`]*`", " code ", text)
    text = re.sub(r"^\s*\|?\s*:?-{3,}.*$", " ", text, flags=re.MULTILINE)
    text = re.sub(r"[*_#>|]", " ", text)
    return text


INLINE_TAGS = re.compile(r"</?(?:code|a|strong|em|span|b|i|abbr|kbd)\b[^>]*>")
STRING = r"""(?P<q>['"`])(?P<v>(?:(?!(?P=q))[^\\]|\\.)*)(?P=q)"""


def unquote(value):
    return value.replace("\\'", "'").replace('\\"', '"').replace("&apos;", "'").replace("&quot;", '"').replace("&amp;", "&")


def tsx_post(path, text):
    """(fields, prose, h1s, h2s, links) for a post written as a React
    component: title and description from the sibling meta.ts, prose from
    the JSX text and the FAQ's question and answer strings."""
    fields = {}
    meta = re.sub(r"[^/]+$", "meta.ts", path)
    try:
        source = open(meta, encoding="utf-8").read()
        for match in re.finditer(rf"\b(?P<k>\w+):\s*\n?\s*{STRING}", source):
            fields.setdefault(match.group("k"), unquote(match.group("v")))
        fields.setdefault("description", fields.get("summary", ""))
    except OSError:
        pass
    body = re.sub(r"^\s*import\s.*$", " ", text, flags=re.MULTILINE)
    body = INLINE_TAGS.sub("", body)
    body = re.sub(r"\{['\"] ['\"]\}", " ", body)
    blocks = [unquote(" ".join(t.split())) for t in re.findall(r">([^<>{}]*[A-Za-z][^<>{}]*)<", body)]
    blocks += [unquote(m.group("v")) for m in re.finditer(rf"\b(?:question|answer):\s*\n?\s*{STRING}", text)]
    clean = lambda h: unquote(" ".join(re.sub(r"<[^>]+>|\{[^}]*\}", " ", h).split()))
    h1 = [clean(h) for h in re.findall(r"<h1\b[^>]*>(.*?)</h1>", text, re.DOTALL)]
    h2 = [clean(h) for h in re.findall(r"<h2\b[^>]*>(.*?)</h2>", text, re.DOTALL)]
    links = re.findall(r"""(?:href|to)=\{?['"](/[^'"#]*)""", text)
    return fields, "\n\n".join(blocks), h1, h2, links


def sentences(text):
    out = []
    for block in re.split(r"\n\s*\n", text):
        block = " ".join(block.split())
        if not block:
            continue
        for sentence in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])", block):
            words = sentence.split()
            if words:
                out.append((sentence, len(words)))
    return out


def digest_paths(path):
    """Slugs and paths the digest names, for internal links."""
    try:
        text = open(path, encoding="utf-8").read()
    except OSError as error:
        sys.exit(f"cannot read the digest: {error}")
    found = set()
    for match in re.finditer(r"(/[A-Za-z0-9._~/-]+)", text):
        found.add(match.group(1).rstrip("/").split("/")[-1])
    for match in re.finditer(r"slug\W+([A-Za-z0-9-]+)", text, re.IGNORECASE):
        found.add(match.group(1))
    return found


def check_post(path, args, findings, notes):
    try:
        text = open(path, encoding="utf-8").read()
    except OSError as error:
        findings.add(path, f"cannot read: {error}")
        return
    tsx = path.endswith((".tsx", ".jsx"))
    if tsx:
        fields, words_text, h1, h2, links = tsx_post(path, text)
        body = text
        scanned = "\n".join([words_text, fields.get("title", ""), fields.get("description", ""), fields.get("heroAlt", "")])
    else:
        fields, body = front_matter(text)
        words_text = prose(body)
        scanned = text
        fenced, h1, h2 = False, [], []
        for line in body.splitlines():
            if line.startswith("```"):
                fenced = not fenced
            elif not fenced and re.match(r"^# \S", line):
                h1.append(line)
            elif not fenced and re.match(r"^## \S", line):
                h2.append(line[3:].strip())
        links = re.findall(r"\]\((/[^)\s#]*)", body) + re.findall(r'href="(/[^"#]*)"', body)

    for char, name in DASHES.items():
        count = text.count(char)
        if count:
            findings.add(path, f"{count} {name}{'es' if count > 1 else ''}; use a comma, a period or 'to'")

    lowered = scanned.lower()
    for word in (w for w in BANNED_WORDS if w not in args.allow):
        hits = len(re.findall(rf"\b{re.escape(word)}\w*\b", lowered))
        if hits:
            findings.add(path, f"banned word '{word}' x{hits}")
    for phrase in BANNED_PHRASES:
        hits = lowered.count(phrase)
        if hits:
            findings.add(path, f"banned phrase '{phrase}' x{hits}")

    count = len(words_text.split())
    if count < args.min_words or count > args.max_words:
        findings.add(path, f"{count} words; this post's range is {args.min_words} to {args.max_words}")

    # A fragment without a full stop is a heading or a label, not a sentence.
    short = [s for s, n in sentences(words_text) if n < SHORT_SENTENCE and s.rstrip().endswith((".", "!"))]
    if short:
        findings.add(path, f"{len(short)} sentences under {SHORT_SENTENCE} words, first: {short[0][:80]!r}")
    long = [s for s, n in sentences(words_text) if n > LONG_SENTENCE]
    if long:
        notes.append(f"{len(long)} sentences over {LONG_SENTENCE} words; split run-ons, first: {long[0][:80]!r}")

    title = fields.get("title", "")
    if not title:
        findings.add(path, "no title in the front matter")
    elif len(title) > TITLE_MAX:
        findings.add(path, f"title is {len(title)} characters; at most {TITLE_MAX}")
    description = fields.get("description") or fields.get("excerpt") or fields.get("summary") or ""
    if not description:
        findings.add(path, "no description in the front matter")
    elif len(description) > META_MAX:
        findings.add(path, f"description is {len(description)} characters; at most {META_MAX}")
    if args.keyword:
        keyword = args.keyword.lower()
        if keyword not in title.lower():
            findings.add(path, "the primary keyword is not in the title")
        if description and keyword not in " ".join(description.lower().split()[:20]):
            findings.add(path, "the primary keyword is not in the description's first 20 words")

    if len(h1) > 1 or (h1 and title and not args.body_h1):
        findings.add(path, f"{len(h1)} H1 in the body; the title is the one H1 (pass --body-h1 if this layout puts it in the body)")
    if args.body_h1 and len(h1) != 1:
        findings.add(path, f"{len(h1)} H1 in the body; exactly one")
    for heading in h2:
        if BANNED_HEADINGS.match(heading):
            findings.add(path, f"heading '{heading}': use a substantive heading")
    questions = sum(1 for h in h2 if h.endswith("?"))
    if h2 and questions * 2 < len(h2):
        notes.append(f"{questions} of {len(h2)} H2s are questions; phrase most as questions")

    if not args.no_faq:
        if "FAQPage" not in text:
            findings.add(path, "no FAQPage JSON-LD (pass --no-faq if the site's format has none)")
        else:
            for block in re.findall(r"<script[^>]*application/ld\+json[^>]*>(.*?)</script>", text, re.DOTALL | re.IGNORECASE):
                raw = block.strip()
                if tsx or raw.startswith("{`") or raw.startswith("{JSON"):
                    continue  # MDX expressions: checked by the site's build
                try:
                    json.loads(raw)
                except json.JSONDecodeError as error:
                    findings.add(path, f"JSON-LD does not parse: {error}")

    if args.domain:
        links += [re.sub(r"^https?://[^/]+", "", l) for l in re.findall(rf"\]\((https?://(?:www\.)?{re.escape(args.domain)}[^)\s#]*)", body)]
    if len(links) < args.min_links:
        findings.add(path, f"{len(links)} internal links; at least {args.min_links}")
    if args.digest:
        known = digest_paths(args.digest)
        for link in links:
            last = link.rstrip("/").split("/")[-1]
            if last and last not in known:
                findings.add(path, f"internal link {link} is not in the digest")

    images = re.findall(r"!\[([^\]]*)\]\(([^)\s]+)", body) + [(a, s) for s, a in re.findall(r'<img[^>]*src="([^"]+)"[^>]*alt="([^"]*)"', body)]
    for alt, src in images:
        if not alt.strip():
            findings.add(path, f"image {src} has no alt text")

    print(f"{path}: {count} words, title {len(title)} characters, description {len(description)} characters, "
          f"{len(h2)} H2s ({questions} questions), {len(links)} internal links, {len(images)} images")


def check_svg(path, findings):
    try:
        text = open(path, encoding="utf-8").read()
        root = ET.fromstring(text)
    except (OSError, ET.ParseError) as error:
        findings.add(path, f"not well-formed: {error}")
        return
    if not root.tag.endswith("svg"):
        findings.add(path, "the root element is not <svg>")
    if "viewBox" not in root.attrib:
        findings.add(path, "no viewBox")
    for char, name in DASHES.items():
        if char in text:
            findings.add(path, f"has an {name}")
    for element in root.iter():
        tag = element.tag.split("}")[-1]
        if tag in ("script", "foreignObject", "image"):
            findings.add(path, f"<{tag}> is not allowed")
        for key, value in element.attrib.items():
            name = key.split("}")[-1]
            if name.lower().startswith("on"):
                findings.add(path, f"event attribute {name} is not allowed")
            if name == "href" and not value.startswith("#"):
                findings.add(path, f"external reference {value}")
        size = element.attrib.get("font-size") or ""
        style = re.search(r"font-size:\s*([\d.]+)", element.attrib.get("style", ""))
        number = re.match(r"([\d.]+)", size) or style
        if tag in ("text", "tspan", "g") and number and float(number.group(1)) < SVG_MIN_FONT:
            findings.add(path, f"<{tag}> font-size {number.group(1)} is under {SVG_MIN_FONT}")
    if re.search(r"@import|url\((?!#)", text):
        findings.add(path, "imports or references something outside the file")
    print(f"{path}: checked")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("post", nargs="?", help="the post file")
    parser.add_argument("--svg", nargs="+", default=[], help="figure files to check")
    parser.add_argument("--digest", help="the site digest, to check internal links")
    parser.add_argument("--keyword", help="the primary keyword")
    parser.add_argument("--domain", help="the site's domain, so absolute links to it count as internal")
    parser.add_argument("--min-words", type=int, default=2500)
    parser.add_argument("--max-words", type=int, default=3000)
    parser.add_argument("--min-links", type=int, default=3)
    parser.add_argument("--no-faq", action="store_true", help="the post has no FAQ (a one-off, or a format without it)")
    parser.add_argument("--allow", nargs="+", default=[], help="banned words the site uses as names, from the brief (for example harness)")
    parser.add_argument("--body-h1", action="store_true", help="the layout puts the H1 in the body, not the front matter")
    args = parser.parse_args()
    if not args.post and not args.svg:
        parser.error("give a post, --svg files, or both")
    findings, notes = Findings(), []
    if args.post:
        check_post(args.post, args, findings, notes)
    for svg in args.svg:
        check_svg(svg, findings)
    for note in notes:
        print(f"NOTE {note}")
    for finding in findings:
        print(f"FAIL {finding}")
    print(f"{len(findings)} findings")
    sys.exit(1 if findings else 0)


if __name__ == "__main__":
    main()
