#!/usr/bin/env node

import * as fs from "fs";
import * as path from "path";
import * as readline from "readline";

// ANSI Colors
const ANSI_COLORS = {
  black: "\x1b[30m",
  red: "\x1b[31m",
  green: "\x1b[32m",
  yellow: "\x1b[33m",
  blue: "\x1b[34m",
  magenta: "\x1b[35m",
  cyan: "\x1b[36m",
  white: "\x1b[37m",
  reset: "\x1b[0m"
};

// Function to detect repeating bytes
function highlightRepeats(chunk: Uint8Array, minRepeat: number = 2): (string | null)[] {
  const colors = Array(chunk.length).fill(null);
  let i = 0;

  while (i < chunk.length - 1) {
    let repeatLen = 1;
    while (i + repeatLen < chunk.length && chunk[i] === chunk[i + repeatLen]) {
      repeatLen++;
    }

    if (repeatLen >= minRepeat) {
      for (let j = 0; j < repeatLen; j++) colors[i + j] = "pattern";
      i += repeatLen;
    } else {
      i++;
    }
  }
  return colors;
}

// Function to display hex content
async function hexView(
  filePath: string,
  bytesPerLine = 16,
  start = 0,
  length?: number,
  colors = {
    nonprint: "red",
    repeat: "yellow",
    null: "cyan",
    pattern: "magenta",
    search: "green"
  }
) {
  const stats = fs.statSync(filePath);
  const fileSize = stats.size;
  const fileBuffer = fs.readFileSync(filePath);

  const startOffset = Math.min(start, fileSize);
  const endOffset = length ? Math.min(fileSize, startOffset + length) : fileSize;

  let previousChunk: Uint8Array | null = null;

  for (let offset = startOffset; offset < endOffset; offset += bytesPerLine) {
    const chunk = fileBuffer.slice(offset, offset + bytesPerLine);
    const repeatColors = highlightRepeats(chunk);
    const hexParts: string[] = [];
    const asciiParts: string[] = [];

    for (let i = 0; i < chunk.length; i++) {
      const byte = chunk[i];
      let hexStr = byte.toString(16).padStart(2, "0").toUpperCase();
      let asciiStr = (byte >= 32 && byte <= 126) ? String.fromCharCode(byte) : ".";

      // Color highlights
      if (byte === 0x00) hexStr = `${ANSI_COLORS[colors.null]}${hexStr}${ANSI_COLORS.reset}`;
      if (repeatColors[i]) asciiStr = `${ANSI_COLORS[colors.pattern]}${asciiStr}${ANSI_COLORS.reset}`;

      hexParts.push(hexStr);
      asciiParts.push(asciiStr);
    }

    const hexLine = hexParts.join(" ");
    const asciiLine = asciiParts.join("");

    console.log(`${offset.toString(16).padStart(8, "0")}  ${hexLine}  ${asciiLine}`);
    previousChunk = chunk;
  }
}

// Main entry point
async function main() {
  const args = process.argv.slice(2);
  const filePath = args[0];
  if (!filePath || !fs.existsSync(filePath)) {
    console.error("Error: File not found or invalid.");
    process.exit(1);
  }

  await hexView(filePath, 16, 0, undefined);
}

main();