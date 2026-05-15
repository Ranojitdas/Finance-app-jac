const buttons = document.querySelectorAll(".copy-btn");
const navLinks = document.querySelectorAll(".topbar nav a[href^='#']");
const sections = document.querySelectorAll("main section[id]");
const progressBar = document.querySelector(".scroll-progress");
const counters = document.querySelectorAll("[data-count]");

for (const button of buttons) {
  button.addEventListener("click", async () => {
    const targetId = button.getAttribute("data-copy-target");
    if (!targetId) return;

    const target = document.getElementById(targetId);
    if (!target) return;

    const text = target.textContent || "";

    try {
      await navigator.clipboard.writeText(text.trim());
      const original = button.textContent;
      button.textContent = "Copied";
      setTimeout(() => {
        button.textContent = original || "Copy";
      }, 1200);
    } catch {
      const original = button.textContent;
      button.textContent = "Copy failed";
      setTimeout(() => {
        button.textContent = original || "Copy";
      }, 1200);
    }
  });
}

function updateScrollProgress() {
  if (!progressBar) return;
  const scrollTop = window.scrollY;
  const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
  const ratio = scrollHeight > 0 ? (scrollTop / scrollHeight) * 100 : 0;
  progressBar.style.width = `${Math.min(100, Math.max(0, ratio))}%`;
}

function updateActiveSection() {
  let currentId = "";
  const offset = window.scrollY + 120;

  for (const section of sections) {
    if (section.offsetTop <= offset) {
      currentId = section.id;
    }
  }

  for (const link of navLinks) {
    const href = link.getAttribute("href") || "";
    const isActive = href === `#${currentId}`;
    link.classList.toggle("active", isActive);
  }
}

function animateCounters() {
  for (const counter of counters) {
    const target = Number(counter.getAttribute("data-count") || "0");
    const durationMs = 1000;
    const start = performance.now();

    const tick = (now) => {
      const progress = Math.min((now - start) / durationMs, 1);
      const value = Math.floor(progress * target);
      counter.textContent = String(value);
      if (progress < 1) {
        requestAnimationFrame(tick);
      }
    };

    requestAnimationFrame(tick);
  }
}

window.addEventListener("scroll", () => {
  updateScrollProgress();
  updateActiveSection();
});

updateScrollProgress();
updateActiveSection();
animateCounters();

// Demo results: fetch demo_results.json and render explainability cards
async function loadDemoResults() {
  const container = document.getElementById("results-grid");
  if (!container) return;
  container.innerHTML = "<p class=\"muted\">Loading...</p>";

  try {
    const res = await fetch("./demo_results.json", { cache: "no-store" });
    if (!res.ok) throw new Error("failed to fetch demo results");
    const data = await res.json();
    if (!Array.isArray(data) || data.length === 0) {
      container.innerHTML = "<p class=\"muted\">No demo results available.</p>";
      return;
    }

    container.innerHTML = "";
    for (const item of data) {
      const card = document.createElement("article");
      card.className = "card result-card";

      const label = (item.explainability && item.explainability.label) || item.decision || "Unknown";
      const summary = (item.explainability && item.explainability.summary) || "";

      card.innerHTML = `
        <h3>${item.scenario.replace(/_/g, ' ')}</h3>
        <p><strong>Txn:</strong> ${item.txn_id} — <strong>Decision:</strong> ${item.decision}</p>
        <p><span class="badge">${label}</span> ${summary}</p>
      `;

      container.appendChild(card);
    }
  } catch (e) {
    container.innerHTML = `<p class=\"muted\">Unable to load demo results.</p>`;
    console.error(e);
  }
}

const refreshBtn = document.getElementById("btn-refresh-results");
if (refreshBtn) refreshBtn.addEventListener("click", loadDemoResults);

// Load on page open
window.addEventListener("load", loadDemoResults);
