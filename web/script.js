const buttons = document.querySelectorAll(".copy-btn");

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
