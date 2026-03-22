#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import readline from "node:readline/promises";
import { stdin as input, stdout as output } from "node:process";

let chromium;
try {
  ({ chromium } = await import("playwright"));
} catch (error) {
  console.error(
    "Playwright is not installed. Add it with `npm install --save-dev playwright` before running this script.",
  );
  process.exit(1);
}

function parseArgs(argv) {
  const args = {
    headless: false,
    outDir: "research/archive/raw/company_release/businesswire_presspass",
    provider: "businesswire-presspass-playwright",
    maxResults: 25,
    articleTimeoutMs: 30000,
  };

  for (let index = 0; index < argv.length; index += 1) {
    const value = argv[index];
    if (!value.startsWith("--")) {
      continue;
    }
    const key = value.slice(2);
    if (key === "headless") {
      args.headless = true;
      continue;
    }
    const next = argv[index + 1];
    if (next == null || next.startsWith("--")) {
      throw new Error(`Missing value for --${key}`);
    }
    args[key] = next;
    index += 1;
  }

  if (!args.url) {
    throw new Error("Missing required --url");
  }

  args.maxResults = Number(args.maxResults) || 25;
  args.articleTimeoutMs = Number(args.articleTimeoutMs) || 30000;
  return args;
}

function slugify(value) {
  return String(value)
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 80);
}

const args = parseArgs(process.argv.slice(2));
const browser = await chromium.launch({
  headless: args.headless,
  chromiumSandbox: false,
  args: ["--disable-setuid-sandbox"],
});
const context = await browser.newContext({ viewport: { width: 1600, height: 1200 } });
const page = await context.newPage();

await page.goto(args.url, { waitUntil: "domcontentloaded" });

const rl = readline.createInterface({ input, output });
output.write(
  [
    "",
    `Opened ${args.url}`,
    "Prepare the Business Wire PressPass page manually in the browser:",
    "- log in",
    "- run the advanced search you want",
    "- apply filters",
    "- make the result list you want visible",
    "- then press Enter here to capture the visible article results",
    "",
  ].join("\n"),
);
await rl.question("> ");
await rl.close();

const searchCapture = await page.evaluate(
  ({ explicitSelector, maxResults }) => {
    const visible = (element) => {
      const style = window.getComputedStyle(element);
      const rect = element.getBoundingClientRect();
      return (
        style.visibility !== "hidden" &&
        style.display !== "none" &&
        rect.width > 0 &&
        rect.height > 0
      );
    };

    const clean = (value) => (value || "").replace(/\s+/g, " ").trim();

    const articleHref = (href) => {
      if (!href) return "";
      try {
        return new URL(href, window.location.href).toString().split("#")[0];
      } catch (error) {
        return "";
      }
    };

    const anchors = Array.from(
      explicitSelector
        ? document.querySelectorAll(explicitSelector)
        : document.querySelectorAll('a[href*="/news/home/"]'),
    ).filter((anchor) => visible(anchor));

    const dedup = new Set();
    const results = [];
    for (const anchor of anchors) {
      const href = articleHref(anchor.getAttribute("href"));
      if (!href || !href.includes("/news/home/") || dedup.has(href)) {
        continue;
      }

      const title = clean(anchor.textContent);
      if (title.length < 20) {
        continue;
      }

      const container = anchor.closest("article, li, section, div") || anchor.parentElement || anchor;
      const timeNode = container.querySelector("time");
      const publishedLabel =
        clean(timeNode?.getAttribute("datetime")) ||
        clean(timeNode?.textContent) ||
        "";

      const teaserCandidates = Array.from(container.querySelectorAll("p, span, div"))
        .map((node) => clean(node.textContent))
        .filter((text) => text && text !== title && text.length >= 20);
      const teaser = teaserCandidates.find((text) => text !== publishedLabel) || "";

      dedup.add(href);
      results.push({
        result_index: results.length,
        title,
        url: href,
        published_label: publishedLabel,
        teaser,
      });
      if (results.length >= maxResults) {
        break;
      }
    }

    return {
      source_page_title: document.title,
      source_page_url: window.location.href,
      results,
    };
  },
  {
    explicitSelector: args.resultLinkSelector || null,
    maxResults: args.maxResults,
  },
);

if (searchCapture.results.length === 0) {
  await browser.close();
  console.error("No visible Business Wire article results found to capture.");
  process.exit(2);
}

const stamp = new Date().toISOString().replace(/[:.]/g, "-");
const baseDir = path.resolve(args.outDir, stamp);
const articlesDir = path.join(baseDir, "articles");
await fs.mkdir(articlesDir, { recursive: true });

const capturedResults = [];
for (const result of searchCapture.results) {
  const articlePage = await context.newPage();
  const fileStem = `${String(result.result_index).padStart(3, "0")}_${slugify(result.title || "businesswire-article")}`;
  try {
    await articlePage.goto(result.url, {
      waitUntil: "domcontentloaded",
      timeout: args.articleTimeoutMs,
    });
    if (args.articleWaitSelector) {
      await articlePage.waitForSelector(args.articleWaitSelector, {
        timeout: args.articleTimeoutMs,
      });
    }
    await articlePage.waitForLoadState("networkidle", { timeout: 5000 }).catch(() => {});
    const html = await articlePage.content();
    const articlePath = path.join("articles", `${fileStem}.html`);
    await fs.writeFile(path.join(baseDir, articlePath), html, "utf8");
    capturedResults.push({
      ...result,
      capture_status: "captured",
      article_path: articlePath,
      article_final_url: articlePage.url(),
      article_page_title: await articlePage.title(),
    });
  } catch (error) {
    capturedResults.push({
      ...result,
      capture_status: "capture_failed",
      capture_error: error instanceof Error ? error.message : String(error),
    });
  } finally {
    await articlePage.close();
  }
}

await browser.close();

const payload = {
  capture_meta: {
    provider: args.provider,
    captured_at: new Date().toISOString(),
    capture_mode: "user_mediated_playwright",
    source_page: args.url,
    result_link_selector: args.resultLinkSelector || null,
    article_wait_selector: args.articleWaitSelector || null,
    max_results_requested: args.maxResults,
    source_page_title: searchCapture.source_page_title,
    source_page_final_url: searchCapture.source_page_url,
    notes: [
      "Search/login/filtering were performed manually in a browser session.",
      "Only visible Business Wire results were captured.",
      "Article HTML was collected from the authenticated browser context.",
    ],
  },
  results: capturedResults,
  metrics: {
    visible_result_count: searchCapture.results.length,
    captured_article_count: capturedResults.filter((item) => item.capture_status === "captured").length,
    capture_failure_count: capturedResults.filter((item) => item.capture_status === "capture_failed").length,
  },
};

const summaryPath = path.join(baseDir, "capture-summary.json");
await fs.writeFile(summaryPath, JSON.stringify(payload, null, 2) + "\n", "utf8");

output.write(
  [
    "",
    `Captured ${payload.metrics.captured_article_count}/${searchCapture.results.length} Business Wire article pages.`,
    `Artifacts written to: ${baseDir}`,
    "Next step:",
    `bash ./scripts/backend-uv.sh run python scripts/build_businesswire_company_release_browser_capture.py ${summaryPath} --output-json research/archive/raw/company_release/businesswire_presspass_raw_v1.json`,
    "",
  ].join("\n"),
);
