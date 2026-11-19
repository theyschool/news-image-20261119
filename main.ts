// Entry point: copy the rendered poster to the output directory.
//
// Reads entry.png from this repository and writes it byte for byte to
// <output>/entry.png, where <output> is MAKEFUN_OUTPUT_DIR (default
// /output). Node 22, standard library only.

import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const source = join(here, "entry.png");

if (!existsSync(source)) {
  throw new Error("entry.png is missing: run build_image.py first");
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, join(outDir, "entry.png"));
console.log("wrote", join(outDir, "entry.png"));
