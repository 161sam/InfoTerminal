// ULTIMATE Theme Debug Script für InfoTerminal
// Copy-paste diesen Code vollständig in die Browser-Konsole

console.log('🔥 ULTIMATE THEME DEBUG - InfoTerminal');
console.log('=====================================');

// 1. Grund-Setup überprüfen
console.log('\n1️⃣ GRUND-SETUP CHECK:');
console.log('- Window object:', typeof window);
console.log('- Document object:', typeof document);
console.log('- Local storage:', typeof localStorage);

// 2. Theme Provider Check
console.log('\n2️⃣ THEME PROVIDER CHECK:');
const root = document.documentElement;
console.log('- HTML root element:', !!root);
console.log('- Current classes:', Array.from(root.classList));
console.log('- data-theme attribute:', root.getAttribute('data-theme'));
console.log('- data-theme-owner:', root.getAttribute('data-theme-owner'));

// 3. LocalStorage Check
console.log('\n3️⃣ LOCALSTORAGE CHECK:');
try {
  const storedTheme = localStorage.getItem('ui.theme');
  console.log('- Stored theme:', storedTheme);
  
  // Test storage
  localStorage.setItem('theme-test', 'working');
  const testValue = localStorage.getItem('theme-test');
  localStorage.removeItem('theme-test');
  console.log('- Storage functional:', testValue === 'working');
} catch (e) {
  console.error('- Storage error:', e);
}

// 4. Theme Toggle Button Check
console.log('\n4️⃣ THEME TOGGLE BUTTON CHECK:');
const possibleSelectors = [
  'button[title*="theme" i]',
  'button[aria-label*="theme" i]',
  'button[class*="theme" i]',
  '[data-testid*="theme"]',
  'button:has(svg + span:contains("Light"))',
  'button:has(svg + span:contains("Dark"))',
  'button:has(svg + span:contains("System"))'
];

let foundButtons = [];
possibleSelectors.forEach((selector, i) => {
  try {
    const buttons = document.querySelectorAll(selector);
    if (buttons.length > 0) {
      foundButtons.push(...Array.from(buttons));
      console.log(`- Selector ${i+1} (${selector}): ${buttons.length} found`);
    }
  } catch (e) {
    // Selector might not be supported
  }
});

// Deduplicate buttons
const uniqueButtons = [...new Set(foundButtons)];
console.log(`- Total unique theme buttons found: ${uniqueButtons.length}`);

uniqueButtons.forEach((btn, i) => {
  console.log(`  Button ${i+1}:`);
  console.log(`    - Text: "${btn.textContent?.trim() || 'No text'}"`);
  console.log(`    - Title: "${btn.getAttribute('title') || 'None'}"`);
  console.log(`    - Aria-label: "${btn.getAttribute('aria-label') || 'None'}"`);
  console.log(`    - Classes: "${btn.className}"`);
  console.log(`    - Disabled: ${btn.disabled}`);
});

// 5. CSS Classes Test
console.log('\n5️⃣ CSS CLASSES TEST:');
const testClasses = ['dark', 'light', 'bg-white', 'bg-gray-900', 'text-gray-900', 'text-white'];
testClasses.forEach(cls => {
  const hasClass = root.classList.contains(cls);
  console.log(`- ${cls}: ${hasClass ? '✅' : '❌'}`);
});

// 6. CSS Variables Check
console.log('\n6️⃣ CSS VARIABLES CHECK:');
const computedStyle = getComputedStyle(root);
const cssVars = [
  '--color-bg-primary',
  '--color-bg-secondary', 
  '--color-text-primary',
  '--color-text-secondary',
  '--tw-bg-opacity'
];

cssVars.forEach(varName => {
  const value = computedStyle.getPropertyValue(varName).trim();
  console.log(`- ${varName}: "${value || 'Not defined'}"`);
});

// 7. System Preference Check
console.log('\n7️⃣ SYSTEM PREFERENCE CHECK:');
try {
  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
  console.log('- System prefers dark:', mediaQuery.matches);
  console.log('- Media query support:', !!mediaQuery.addEventListener);
} catch (e) {
  console.error('- System preference error:', e);
}

// 8. Manual Theme Switch Test
console.log('\n8️⃣ MANUAL THEME SWITCH TEST:');
window.testThemeSwitch = function() {
  const root = document.documentElement;
  const currentlyDark = root.classList.contains('dark');
  
  console.log(`Before: dark=${currentlyDark}`);
  
  if (currentlyDark) {
    root.classList.remove('dark');
    root.setAttribute('data-theme', 'light');
    localStorage.setItem('ui.theme', 'light');
  } else {
    root.classList.add('dark');
    root.setAttribute('data-theme', 'dark');
    localStorage.setItem('ui.theme', 'dark');
  }
  
  const afterDark = root.classList.contains('dark');
  console.log(`After: dark=${afterDark}`);
  console.log(`Switch successful: ${currentlyDark !== afterDark ? '✅' : '❌'}`);
  
  // Test visual change
  setTimeout(() => {
    const bodyBg = getComputedStyle(document.body).backgroundColor;
    console.log(`Body background: ${bodyBg}`);
  }, 100);
  
  return !currentlyDark;
};

console.log('- Manual test function created: window.testThemeSwitch()');

// 9. Button Click Test
console.log('\n9️⃣ BUTTON CLICK TEST:');
if (uniqueButtons.length > 0) {
  const firstButton = uniqueButtons[0];
  console.log('- Testing first button click...');
  
  const beforeState = {
    dark: root.classList.contains('dark'),
    theme: root.getAttribute('data-theme')
  };
  
  // Simulate click
  firstButton.click();
  
  setTimeout(() => {
    const afterState = {
      dark: root.classList.contains('dark'),
      theme: root.getAttribute('data-theme')
    };
    
    const changed = beforeState.dark !== afterState.dark || beforeState.theme !== afterState.theme;
    console.log(`- Before: dark=${beforeState.dark}, theme=${beforeState.theme}`);
    console.log(`- After: dark=${afterState.dark}, theme=${afterState.theme}`);
    console.log(`- Button click effective: ${changed ? '✅' : '❌'}`);
    
    if (!changed) {
      console.log('🚨 BUTTON CLICK HAD NO EFFECT!');
      console.log('Checking for JavaScript errors...');
      
      // Try to access React events
      if (firstButton._reactInternalFiber || firstButton._reactInternalInstance) {
        console.log('- React fiber found on button');
      } else {
        console.log('- No React fiber found - event handler might not be attached');
      }
    }
  }, 200);
} else {
  console.log('❌ No theme buttons found to test');
}

// 10. Final Summary
setTimeout(() => {
  console.log('\n🔟 FINAL SUMMARY:');
  console.log('================================');
  
  const issues = [];
  
  if (uniqueButtons.length === 0) {
    issues.push('❌ No theme toggle buttons found');
  }
  
  if (!localStorage.getItem('ui.theme')) {
    issues.push('❌ No theme stored in localStorage');
  }
  
  if (!root.getAttribute('data-theme-owner')) {
    issues.push('❌ Theme provider not active (no data-theme-owner)');
  }
  
  const hasCorrectClasses = root.classList.contains('dark') || root.classList.contains('light');
  if (!hasCorrectClasses && !root.classList.contains('dark')) {
    // Default should be light mode
    console.log('ℹ️ No explicit theme classes, assuming light mode default');
  }
  
  if (issues.length === 0) {
    console.log('✅ All basic theme system components appear to be present');
    console.log('🧪 Try running: window.testThemeSwitch()');
  } else {
    console.log('🚨 IDENTIFIED ISSUES:');
    issues.forEach(issue => console.log(issue));
  }
  
  console.log('\n📋 QUICK TESTS:');
  console.log('- Run: window.testThemeSwitch() // Manual theme toggle');
  console.log('- Check: Elements with bg-white/bg-gray-900 classes');
  console.log('- Look for: Console errors when clicking theme button');
  
}, 500);

console.log('\n🎯 Theme debug script loaded! Check output above and try window.testThemeSwitch()');
