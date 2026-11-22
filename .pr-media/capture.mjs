// Screenshot README sections 5 and 6 as GitHub renders them.
//   PW_HOME=<dir with node_modules/playwright> node .pr-media/capture.mjs <ref> <outDir>
// Each shot runs from the section heading to the end of the section's first table.
import { createRequire } from 'node:module';
import { mkdirSync } from 'node:fs';

const require = createRequire(process.env.PW_HOME ? `${process.env.PW_HOME}/` : import.meta.url);
const { chromium } = require('playwright');

const [ref = 'main', out = '.pr-media/before'] = process.argv.slice(2);
const url = `https://github.com/prajwxlk/native-benchmark/blob/${ref}/README.md?plain=0`;
const sections = [
  ['section-5', '5. The write side'],
  ['section-6', '6. One hint for reading and writing'],
];

mkdirSync(out, { recursive: true });
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 800 }, colorScheme: 'light' });
await page.goto(url, { waitUntil: 'networkidle' });
await page.waitForSelector('article.markdown-body h2');

for (const [name, heading] of sections) {
  const box = await page.evaluate((heading) => {
    const h = [...document.querySelectorAll('article.markdown-body h2')].find((e) => e.textContent.trim().startsWith(heading));
    let block = h.closest('.markdown-heading') || h;
    const top = block.getBoundingClientRect().top + scrollY;
    let el = block.nextElementSibling;
    while (el && !(el.matches('table') || el.querySelector('table'))) el = el.nextElementSibling;
    const r = el.getBoundingClientRect();
    const body = document.querySelector('article.markdown-body').getBoundingClientRect();
    return { x: body.left - 8, y: top - 8, width: body.width + 16, height: r.bottom + scrollY - top + 16 };
  }, heading);
  // Let lazy images in the region load before the shot.
  await page.evaluate((y) => scrollTo(0, y), box.y);
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(500);
  await page.screenshot({ path: `${out}/${name}.png`, clip: box, fullPage: true });
  console.log(`${out}/${name}.png`, Math.round(box.height));
}
await browser.close();
