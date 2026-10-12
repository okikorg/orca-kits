/**
 * Scout: a research assistant that searches the web and cites its sources.
 *
 * Copy the kit, or run this file to create the agent in your organization:
 *
 *   ORCA_API_KEY=... node --experimental-strip-types agent.ts
 */
import { fileURLToPath } from 'node:url';
import OpenAI from 'openai';
import type { AgentCreateParams } from 'openai/resources/beta/agents/agents';

export function define<T>(agents: { create(body: AgentCreateParams): T }): T {
  return agents.create({
    name: 'scout',
    model: 'orca/openrouter/openai/gpt-5.6-luna',
    instructions:
      'You are Scout, a research assistant. Answer in a few short paragraphs or a short list.\n' +
      'Search the web when the answer depends on facts that change, such as releases, versions, ' +
      'prices or news, and cite each source with its link.\n' +
      'If the sources disagree, or you cannot find an answer, say so instead of guessing.',
    tools: [{ type: 'web_search' }],
  });
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const client = new OpenAI({
    apiKey: process.env.ORCA_API_KEY,
    baseURL: process.env.ORCA_BASE_URL ?? 'https://api.orcapods.ai/v1',
  });
  console.log((await define(client.beta.agents)).id);
}
