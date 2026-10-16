"""The seo-helper template: the seo-engine skill, and no network in the
sandbox. Every outside read goes through DataForSEO from the Orca server.

    templates = client.beta.agents.environments.templates
    define(templates, {"seo-engine": "<skill id>"})
"""


def define(templates, skills):
    return templates.create(
        name="seo-helper",
        skills=[{"type": "skill_reference", "skill_id": skills["seo-engine"]}],
        network={"access": "disabled"},
    )
