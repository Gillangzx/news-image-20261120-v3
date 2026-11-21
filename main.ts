// main.ts — entry runner for "Friday 20 November 2026".
//
// The entry image is already finished: it was drawn once, by hand, in
// render.py and committed to this repository as entry.png. This program
// does not draw anything. Its only job is to hand that exact committed
// file to the grader, in the output directory, and then prove the copy
// is a real, non-empty PNG. That way the grader always sees the bytes
// that were reviewed — byte-identical on every run, with no network
// and no rendering at grade time.

import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// The first eight bytes of every PNG file.
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

const IMAGE_NAME = "entry.png";

// The grader sets this; /output is the documented fallback.
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR || "/output";

function errorText(error) {
  return error instanceof Error ? error.message : String(error);
}

// The directory this script lives in. Node re-parses this file as ESM,
// so import.meta.url is the reliable source; __dirname covers the case
// where the loader keeps it CommonJS instead.
function scriptDir() {
  if (typeof __dirname === "string" && __dirname.length > 0) {
    return __dirname;
  }
  try {
    return dirname(fileURLToPath(import.meta.url));
  } catch {
    return process.cwd();
  }
}

// Where the committed image may be found, in order.
function candidatePaths() {
  return [
    join(scriptDir(), IMAGE_NAME),
    join(process.cwd(), IMAGE_NAME),
    join("/bot", IMAGE_NAME),
  ];
}

function findImage() {
  for (const candidate of candidatePaths()) {
    if (existsSync(candidate)) {
      return candidate;
    }
  }
  throw new Error(
    "entry.png not found next to main.ts, in the working directory, or in /bot"
  );
}

// Fail unless the file at path is a non-empty PNG.
function verifyPng(path) {
  const size = statSync(path).size;
  if (size === 0) {
    throw new Error(`${path} is empty`);
  }
  const head = readFileSync(path).subarray(0, PNG_MAGIC.length);
  if (!head.equals(PNG_MAGIC)) {
    throw new Error(`${path} does not start with the PNG magic bytes`);
  }
  return size;
}

function run() {
  const source = findImage();
  const target = join(OUTPUT_DIR, IMAGE_NAME);
  mkdirSync(OUTPUT_DIR, { recursive: true });

  // First attempt: a plain filesystem copy.
  try {
    copyFileSync(source, target);
    const size = verifyPng(target);
    console.log(`entry.png: copied ${size} bytes from ${source} to ${target}`);
    return;
  } catch (firstError) {
    console.error(`direct copy failed (${errorText(firstError)}); retrying once via read/write`);
  }

  // Second and last attempt: read the bytes and write them out by hand.
  const bytes = readFileSync(source);
  writeFileSync(target, bytes);
  const size = verifyPng(target);
  console.log(`entry.png: copied ${size} bytes from ${source} to ${target} (read/write retry)`);
}

try {
  run();
} catch (error) {
  console.error(`error: ${errorText(error)}`);
  process.exit(1);
}
