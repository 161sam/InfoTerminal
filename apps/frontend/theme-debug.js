// Simple theme toggle fix - Add this to browser console
console.log("🔧 Theme Toggle Fix - Testing...");

// 1. Find theme toggle button
const themeButton = document.querySelector(
  'button[title*="theme" i], button[aria-label*="theme" i]',
);
console.log("Theme button found:", !!themeButton);

// 2. Manual theme switch test
function forceThemeSwitch() {
  const root = document.documentElement;
  const isDark = root.classList.contains("dark");

  console.log("Before toggle - isDark:", isDark);

  if (isDark) {
    root.classList.remove("dark");
    root.setAttribute("data-theme", "light");
    localStorage.setItem("ui.theme", "light");
  } else {
    root.classList.add("dark");
    root.setAttribute("data-theme", "dark");
    localStorage.setItem("ui.theme", "dark");
  }

  console.log("After toggle - isDark:", root.classList.contains("dark"));
  console.log("✅ Theme toggle working manually");
  return !isDark;
}

// 3. Test the theme switching
console.log("Testing theme switch...");
const newTheme = forceThemeSwitch();
setTimeout(() => forceThemeSwitch(), 2000); // Switch back after 2s

console.log("🔧 Theme debug complete. If you see visual changes, theme system works.");
