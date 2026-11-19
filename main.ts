// news-image-20261119 entry (Node 22, standard library only).
// The poster is the entry.png beside this file; the program copies it
// to /output/entry.png. The copy is byte for byte, so both graded runs
// write identical bytes, and the file is never re-encoded or resized.
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
// /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, 'entry.png');
// Fail loudly instead of copying nothing: a missing or empty poster
// must never produce a silent zero-byte output.
if (!existsSync(src) || statSync(src).size === 0) {
  throw new Error(`entry.png missing or empty at ${src}`);
}
copyFileSync(src, join(outDir, 'entry.png'));
