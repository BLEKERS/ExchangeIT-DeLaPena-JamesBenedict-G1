/* Side-by-side report from capture.mjs metrics. */
import { readFileSync, writeFileSync } from 'node:fs';

const before = JSON.parse(readFileSync('.taste-skill/before/metrics.json', 'utf8'));
const after = JSON.parse(readFileSync('.taste-skill/after/metrics.json', 'utf8'));
const pages = ['dashboard', 'convert', 'history', 'favorites', 'profile', 'login'];
const widths = [1440, 1024, 768, 390];
const fmt = (v) => Array.isArray(v) ? v.join(' / ') : (v === null || v === undefined ? '—' : String(v));

let out = '# ExchangeIt — before / after measurements\n\n';
out += 'Captures: `.taste-skill/before` and `.taste-skill/after`, 6 pages × 4 widths.\n\n';

out += '## Integrity across all pages (higher is worse)\n\n';
out += '| Width | Overflow px (b → a) | Off-screen elements (b → a) | Text overlap pairs (b → a) | Controls under 44px (b → a) |\n';
out += '|---|---|---|---|---|\n';
for (const w of widths) {
  const sum = (data, key) => pages.reduce((n, p) => n + (data[`${p}-${w}`]?.[key] ?? 0), 0);
  const over = (data) => pages.reduce((n, p) => n + Math.max(0, data[`${p}-${w}`]?.overflowPx ?? 0), 0);
  out += `| ${w} | ${over(before)} → ${over(after)} | ${sum(before,'spillElements')} → ${sum(after,'spillElements')} | ${sum(before,'textOverlapPairs')} → ${sum(after,'textOverlapPairs')} | ${sum(before,'tapsUnder44')} → ${sum(after,'tapsUnder44')} |\n`;
}

const rows = [
  ['Nav height', 'navHeight'],
  ['Min control height', 'minTapHeight'],
  ['Heading size', 'headingPx'],
  ['Heading font', 'headingFont'],
];
out += '\n## Shared shell\n\n| Metric | Width | Before | After |\n|---|---|---|---|\n';
for (const w of [1440, 390]) for (const [label, key] of rows) {
  out += `| ${label} | ${w} | ${fmt(before[`dashboard-${w}`]?.[key])} | ${fmt(after[`dashboard-${w}`]?.[key])} |\n`;
}

out += '\n## Dashboard Bento\n\n| Metric | Width | Before | After |\n|---|---|---|---|\n';
for (const w of [1440, 1024, 390]) {
  const b = before[`dashboard-${w}`], a = after[`dashboard-${w}`];
  out += `| Grid columns | ${w} | ${fmt(b?.gridColumns)} | ${fmt(a?.gridColumns)} |\n`;
  out += `| Stat number sizes | ${w} | ${fmt(b?.statFontPx)} | ${fmt(a?.statFontPx)} |\n`;
  out += `| Card heights | ${w} | ${fmt(b?.cardHeights)} | ${fmt(a?.cardHeights)} |\n`;
}

out += '\n## Converter\n\n| Metric | Width | Before | After |\n|---|---|---|---|\n';
for (const w of [1440, 390]) {
  const b = before[`convert-${w}`], a = after[`convert-${w}`];
  out += `| Amount input height | ${w} | ${fmt(b?.amountHeight)}px | ${fmt(a?.amountHeight)}px |\n`;
  out += `| Amount font size | ${w} | ${fmt(b?.amountFontPx)} | ${fmt(a?.amountFontPx)} |\n`;
  out += `| Result font size | ${w} | ${fmt(b?.resultFontPx)} | ${fmt(a?.resultFontPx)} |\n`;
  out += `| Result block width | ${w} | ${fmt(b?.resultWidth)}px | ${fmt(a?.resultWidth)}px |\n`;
  out += `| Page height | ${w} | ${fmt(b?.pageHeight)}px | ${fmt(a?.pageHeight)}px |\n`;
}

writeFileSync('.taste-skill/measurements.md', out);
console.log(out);
