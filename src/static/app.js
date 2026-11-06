document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("scan-form");
  const urlInput = document.getElementById("url-input");
  const submitBtn = document.getElementById("submit-btn");
  const errorCard = document.getElementById("error-card");
  const errorTitle = document.getElementById("error-title");
  const errorMessage = document.getElementById("error-message");
  const resultsCard = document.getElementById("results-card");

  const verdictBadge = document.getElementById("verdict-badge");
  const scannedUrlElem = document.getElementById("scanned-url");
  const scanTimeElem = document.getElementById("scan-time");
  const countMalicious = document.getElementById("count-malicious");
  const countSuspicious = document.getElementById("count-suspicious");
  const countHarmless = document.getElementById("count-harmless");
  const countUndetected = document.getElementById("count-undetected");
  const detectionList = document.getElementById("detection-list");

  function hideFeedback() {
    errorCard.classList.add("hidden");
    resultsCard.classList.add("hidden");
  }

  function showError(title, message) {
    errorTitle.textContent = title;
    errorMessage.textContent = message;
    errorCard.classList.remove("hidden");
    resultsCard.classList.add("hidden");
  }

  function setLoading(isLoading) {
    if (isLoading) {
      submitBtn.disabled = true;
      submitBtn.classList.add("loading");
    } else {
      submitBtn.disabled = false;
      submitBtn.classList.remove("loading");
    }
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    hideFeedback();

    const rawUrl = urlInput.value.trim();

    if (!rawUrl) {
      showError("Validation Error", "Please provide a valid URL to scan.");
      return;
    }

    if (!/^https?:\/\//i.test(rawUrl)) {
      showError("Protocol Error", "URL must explicitly begin with http:// or https:// (FR-INP-01).");
      return;
    }

    if (rawUrl.length > 2048) {
      showError("Boundary Error", "Target URL exceeds the maximum length of 2048 characters (FR-INP-03).");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch("/scan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: rawUrl }),
      });

      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        let title = "Scan Failed";
        let detail = data.detail || `Server responded with status code ${response.status}.`;

        if (response.status === 422) {
          title = "Invalid URL / Restricted Range (422)";
        } else if (response.status === 429) {
          title = "Upstream Quota Exceeded (429)";
        } else if (response.status === 504) {
          title = "Upstream Timeout (504)";
        } else if (response.status === 502) {
          title = "Threat Service Error (502)";
        }

        showError(title, detail);
        return;
      }

      // Populate verdict and metrics
      scannedUrlElem.textContent = data.url || rawUrl;
      scanTimeElem.textContent = new Date().toLocaleTimeString();

      const malicious = data.malicious_count || 0;
      const suspicious = data.suspicious_count || 0;
      const harmless = data.harmless_count || 0;
      const undetected = data.undetected_count || 0;

      countMalicious.textContent = malicious;
      countSuspicious.textContent = suspicious;
      countHarmless.textContent = harmless;
      countUndetected.textContent = undetected;

      verdictBadge.className = "verdict-badge";
      if (malicious > 0) {
        verdictBadge.textContent = "MALICIOUS";
        verdictBadge.classList.add("verdict-malicious");
      } else if (suspicious > 0) {
        verdictBadge.textContent = "SUSPICIOUS";
        verdictBadge.classList.add("verdict-suspicious");
      } else {
        verdictBadge.textContent = "CLEAN";
        verdictBadge.classList.add("verdict-clean");
      }

      // Populate engine breakdown
      detectionList.innerHTML = "";
      const results = data.engine_results || {};
      const engines = Object.keys(results);

      if (engines.length === 0) {
        const item = document.createElement("li");
        item.className = "detection-item";
        item.textContent = "No specific vendor flags reported.";
        detectionList.appendChild(item);
      } else {
        engines.forEach((name) => {
          const item = document.createElement("li");
          item.className = "detection-item";

          const engineSpan = document.createElement("span");
          engineSpan.className = "detection-engine";
          engineSpan.textContent = name;

          const cat = results[name]?.category || "undetected";
          const catSpan = document.createElement("span");
          catSpan.className = `detection-status ${cat}`;
          catSpan.textContent = cat;

          item.appendChild(engineSpan);
          item.appendChild(catSpan);
          detectionList.appendChild(item);
        });
      }

      resultsCard.classList.remove("hidden");
    } catch (err) {
      showError("Network Error", "Failed to communicate with the scanner API. Please check your network connection.");
    } finally {
      setLoading(false);
    }
  });
});