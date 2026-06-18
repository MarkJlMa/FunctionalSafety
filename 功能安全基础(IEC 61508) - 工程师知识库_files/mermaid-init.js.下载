// Initialize Mermaid with theme-aware configuration
document$.subscribe(() => {
  const palette = __md_get("__palette");
  const isDark = palette?.color?.scheme === "slate";

  mermaid.initialize({
    startOnLoad: true,
    theme: isDark ? "dark" : "default",
    securityLevel: "loose",
  });
});
