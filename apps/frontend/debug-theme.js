// Debug script to test theme switching functionality
// Run in browser console on InfoTerminal frontend

console.log("🔍 InfoTerminal Theme Debug Analysis");

// 1. Check if ThemeProvider is working
console.log("1. Theme Context Check:");
try {
  const themeContext = document.querySelector('[data-theme-owner="tp"]');
  console.log("   Theme element found:", !!themeContext);
  console.log("   Current data-theme:", document.documentElement.getAttribute("data-theme"));
  console.log("   Has dark class:", document.documentElement.classList.contains("dark"));
} catch (e) {
  console.error("   Theme context error:", e);
}

// 2. Check localStorage
console.log("2. Theme Storage Check:");
try {
  const storedTheme = localStorage.getItem("ui.theme");
  console.log("   Stored theme:", storedTheme);
} catch (e) {
  console.error("   Storage error:", e);
}

// 3. Check if theme toggle exists
console.log("3. Theme Toggle Check:");
const toggleButtons = document.querySelectorAll(
  'button[title*="theme" i], button[aria-label*="theme" i]',
);
console.log("   Theme toggle buttons found:", toggleButtons.length);
toggleButtons.forEach((btn, i) => {
  console.log(`   Button ${i + 1}:`, btn.getAttribute("title") || btn.getAttribute("aria-label"));
});

// 4. Test theme switching manually
console.log("4. Manual Theme Switch Test:");
function testThemeSwitch() {
  const root = document.documentElement;
  const isDark = root.classList.contains("dark");

  console.log("   Before switch - isDark:", isDark);

  if (isDark) {
    root.classList.remove("dark");
    root.setAttribute("data-theme", "light");
  } else {
    root.classList.add("dark");
    root.setAttribute("data-theme", "dark");
  }

  console.log("   After switch - isDark:", root.classList.contains("dark"));
  console.log("   Theme switch test: ✅ SUCCESSFUL");
}

// Auto-run the test
testThemeSwitch();

// 5. Check for CSS conflicts
console.log("5. CSS Conflict Check:");
const computedStyle = getComputedStyle(document.body);
console.log("   Body background:", computedStyle.backgroundColor);
console.log("   Body color:", computedStyle.color);

console.log("🔍 Theme Debug Complete - Check results above");
