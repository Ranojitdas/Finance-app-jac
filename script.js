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
