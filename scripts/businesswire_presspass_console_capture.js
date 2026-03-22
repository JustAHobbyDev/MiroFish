(async () => {
  const clean = (value) => (value || "").replace(/\s+/g, " ").trim();
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
  const normalizeUrl = (href) => {
    if (!href) return "";
    try {
      return new URL(href, window.location.href).toString().split("#")[0];
    } catch (error) {
      return "";
    }
  };

  const requestedCount = Number(window.prompt("Max Business Wire results to capture", "20") || "20");
  const maxResults = Number.isFinite(requestedCount) && requestedCount > 0 ? requestedCount : 20;
  const anchors = Array.from(document.querySelectorAll('a[href*="/news/home/"]')).filter(visible);
  const dedup = new Set();
  const candidates = [];

  for (const anchor of anchors) {
    const url = normalizeUrl(anchor.getAttribute("href"));
    if (!url || dedup.has(url)) {
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

    dedup.add(url);
    candidates.push({
      result_index: candidates.length,
      title,
      url,
      published_label: publishedLabel,
      teaser,
    });
    if (candidates.length >= maxResults) {
      break;
    }
  }

  if (candidates.length === 0) {
    throw new Error("No visible Business Wire article links were found on the current page.");
  }

  const results = [];
  for (const candidate of candidates) {
    try {
      const response = await fetch(candidate.url, {
        credentials: "include",
        redirect: "follow",
      });
      const articleHtml = await response.text();
      results.push({
        ...candidate,
        capture_status: response.ok ? "captured" : "capture_failed",
        article_final_url: response.url || candidate.url,
        article_html: response.ok ? articleHtml : "",
        capture_error: response.ok ? "" : `HTTP ${response.status}`,
      });
    } catch (error) {
      results.push({
        ...candidate,
        capture_status: "capture_failed",
        article_html: "",
        capture_error: error instanceof Error ? error.message : String(error),
      });
    }
  }

  const stamp = new Date().toISOString();
  const payload = {
    capture_meta: {
      provider: "businesswire-presspass-console",
      captured_at: stamp,
      capture_mode: "user_mediated_browser_console",
      source_page: window.location.href,
      source_page_title: document.title,
      notes: [
        "Capture executed inside a real authenticated browser session.",
        "Visible result links were collected from the current PressPass page.",
        "Article HTML was fetched with browser session credentials.",
      ],
    },
    results,
    metrics: {
      visible_result_count: candidates.length,
      captured_article_count: results.filter((item) => item.capture_status === "captured").length,
      capture_failure_count: results.filter((item) => item.capture_status === "capture_failed").length,
    },
  };

  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = `businesswire-presspass-capture-${stamp.replace(/[:.]/g, "-")}.json`;
  anchor.click();
  URL.revokeObjectURL(url);

  console.log("Business Wire capture payload", payload);
  return payload;
})();
