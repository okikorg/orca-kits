/**
 * Prints the bodies a kit's TypeScript definitions send, as JSON, without
 * calling the API: each define() gets a stand-in whose create() returns its
 * argument. check.py compares this with the Python definitions.
 *
 *   node --experimental-strip-types scripts/define.ts kits/<slug>
 */
import { existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const folder = resolve(process.argv[2] ?? '');
const record = { create: (body: unknown) => body };
// A template names a kit skill by folder name; the stand-in id says which.
const skills = new Proxy({}, { get: (_, name) => `kit_skill:${String(name)}` });

const bodies: Record<string, unknown> = {};
for (const kind of ['agent', 'template']) {
  const file = resolve(folder, `${kind}.ts`);
  if (!existsSync(file)) continue;
  const module = await import(pathToFileURL(file).href);
  bodies[kind] = kind === 'agent' ? module.define(record) : module.define(record, skills);
}
console.log(JSON.stringify(bodies));
