/**
 * The seo-helper template: the seo-engine skill, and no network in the
 * sandbox. Every outside read goes through DataForSEO from the Orca server.
 *
 *   define(client.beta.agents.environments.templates, { 'seo-engine': '<skill id>' })
 */
import type { TemplateCreateParams } from 'openai/resources/beta/agents/environments/templates';

export function define<T>(
  templates: { create(body: TemplateCreateParams): T },
  skills: Record<string, string>,
): T {
  return templates.create({
    name: 'seo-helper',
    skills: [{ type: 'skill_reference', skill_id: skills['seo-engine'] }],
    network: { access: 'disabled' },
  });
}
