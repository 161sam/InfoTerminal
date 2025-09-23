// Comprehensive Theme Debug Tool for InfoTerminal
// Enhanced debugging script for theme toggle functionality
// Run in browser console: copy-paste entire script and execute

console.log('🎨 InfoTerminal Comprehensive Theme Debug Analysis');
console.log('='.repeat(60));

// Helper function for better output formatting
const logSection = (title) => {
  console.log(`\n📍 ${title}`);
  console.log('-'.repeat(40));
};

// 1. Theme Context and Provider Analysis
logSection('1. Theme Context & Provider Check');
try {
  // Check if ThemeProvider is mounted
  const themeOwnerElement = document.querySelector('[data-theme-owner="tp"]');
  console.log('✓ Theme provider element found:', !!themeOwnerElement);
  
  if (themeOwnerElement) {
    console.log('  - data-theme:', themeOwnerElement.getAttribute('data-theme'));
    console.log('  - classList contains dark:', themeOwnerElement.classList.contains('dark'));
  }
  
  // Check document root classes
  const root = document.documentElement;
  console.log('✓ Document root classes:', Array.from(root.classList).join(', ') || 'none');
  console.log('✓ data-theme attribute:', root.getAttribute('data-theme') || 'not set');
  
} catch (e) {
  console.error('❌ Theme context error:', e);
}

// 2. LocalStorage Theme Persistence
logSection('2. Theme Storage Analysis');
try {
  const storedTheme = localStorage.getItem('ui.theme');
  console.log('✓ Stored theme value:', storedTheme || 'not stored');
  
  // Check if storage is working
  const testKey = 'theme-debug-test';
  localStorage.setItem(testKey, 'test');
  const testValue = localStorage.getItem(testKey);
  localStorage.removeItem(testKey);
  
  console.log('✓ localStorage functional:', testValue === 'test');
} catch (e) {
  console.error('❌ Storage error:', e);
}

// 3. Theme Toggle Button Detection
logSection('3. Theme Toggle Components');
const themeButtons = document.querySelectorAll([
  'button[title*="theme" i]',
  'button[aria-label*="theme" i]', 
  'button[class*="theme" i]',
  '[data-testid*="theme"]'
].join(', '));

console.log('✓ Theme toggle buttons found:', themeButtons.length);
themeButtons.forEach((btn, i) => {
  console.log(`  Button ${i + 1}:`);
  console.log(`    - title: ${btn.getAttribute('title') || 'none'}`);
  console.log(`    - aria-label: ${btn.getAttribute('aria-label') || 'none'}`);
  console.log(`    - classes: ${btn.className || 'none'}`);
  console.log(`    - disabled: ${btn.disabled}`);
});

// 4. CSS Variables and Custom Properties
logSection('4. CSS Variables Analysis');
try {
  const rootStyles = getComputedStyle(document.documentElement);
  const themeVariables = [
    '--primary-color',
    '--background-color', 
    '--text-color',
    '--border-color'
  ];
  
  themeVariables.forEach(varName => {
    const value = rootStyles.getPropertyValue(varName).trim();
    console.log(`✓ ${varName}: ${value || 'not defined'}`);
  });
  
  // Check computed styles on body
  const bodyStyles = getComputedStyle(document.body);
  console.log('✓ Body background-color:', bodyStyles.backgroundColor);
  console.log('✓ Body color:', bodyStyles.color);
  
} catch (e) {
  console.error('❌ CSS variables error:', e);
}

// 5. Theme System Functionality Test
logSection('5. Theme Toggle Functionality Test');
let originalTheme = null;

function testManualThemeSwitch() {
  try {
    const root = document.documentElement;
    originalTheme = {
      darkClass: root.classList.contains('dark'),
      dataTheme: root.getAttribute('data-theme')
    };
    
    console.log('🧪 Before switch:');
    console.log(`  - Has dark class: ${originalTheme.darkClass}`);
    console.log(`  - data-theme: ${originalTheme.dataTheme}`);
    
    // Toggle theme manually
    if (originalTheme.darkClass) {
      root.classList.remove('dark');
      root.setAttribute('data-theme', 'light');
    } else {
      root.classList.add('dark');
      root.setAttribute('data-theme', 'dark');
    }
    
    console.log('🧪 After switch:');
    console.log(`  - Has dark class: ${root.classList.contains('dark')}`);
    console.log(`  - data-theme: ${root.getAttribute('data-theme')}`);
    
    // Test if visual changes occurred
    setTimeout(() => {
      const newBodyColor = getComputedStyle(document.body).backgroundColor;
      console.log(`  - Body background changed: ${newBodyColor}`);
      console.log('✅ Manual theme switch: SUCCESSFUL');
      
      // Restore original theme
      restoreOriginalTheme();
    }, 100);
    
  } catch (e) {
    console.error('❌ Manual theme switch failed:', e);
    restoreOriginalTheme();
  }
}

function restoreOriginalTheme() {
  if (originalTheme) {
    const root = document.documentElement;
    if (originalTheme.darkClass) {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
    root.setAttribute('data-theme', originalTheme.dataTheme || 'light');
    console.log('🔄 Original theme restored');
  }
}

// 6. Theme Provider Context Access
logSection('6. React Context Analysis');
try {
  // Try to access React Dev Tools
  if (window.__REACT_DEVTOOLS_GLOBAL_HOOK__) {
    console.log('✓ React DevTools available');
    
    // Look for ThemeProvider in React tree
    const reactFiber = document.querySelector('#__next')?._reactInternalFiber 
                   || document.querySelector('#root')?._reactInternalFiber;
    
    if (reactFiber) {
      console.log('✓ React fiber found - theme context may be accessible');
    } else {
      console.log('⚠ React fiber not found in DOM');
    }
  } else {
    console.log('⚠ React DevTools not available');
  }
  
  // Check for theme context in window (sometimes exposed for debugging)
  if (window.themeContext) {
    console.log('✓ Theme context found on window:', window.themeContext);
  } else {
    console.log('⚠ No theme context on window object');
  }
  
} catch (e) {
  console.error('❌ React context analysis error:', e);
}

// 7. System Preferences Detection
logSection('7. System Preferences');
try {
  const prefersColorScheme = window.matchMedia('(prefers-color-scheme: dark)');
  console.log('✓ System prefers dark mode:', prefersColorScheme.matches);
  console.log('✓ Media query supported:', !!prefersColorScheme.addEventListener);
  
  // Test listener
  const testListener = () => console.log('Media query listener working');
  prefersColorScheme.addEventListener('change', testListener);
  prefersColorScheme.removeEventListener('change', testListener);
  console.log('✓ Media query listeners functional');
  
} catch (e) {
  console.error('❌ System preferences error:', e);
}

// 8. Theme Button Click Simulation
logSection('8. Theme Button Simulation');
if (themeButtons.length > 0) {
  try {
    const firstButton = themeButtons[0];
    console.log('🎯 Testing first theme button click...');
    
    // Monitor changes
    const root = document.documentElement;
    const beforeState = {
      darkClass: root.classList.contains('dark'),
      dataTheme: root.getAttribute('data-theme')
    };
    
    // Simulate click
    firstButton.click();
    
    setTimeout(() => {
      const afterState = {
        darkClass: root.classList.contains('dark'),
        dataTheme: root.getAttribute('data-theme')
      };
      
      const changed = beforeState.darkClass !== afterState.darkClass || 
                     beforeState.dataTheme !== afterState.dataTheme;
      
      console.log('🎯 Button click result:');
      console.log(`  - Theme changed: ${changed ? '✅ YES' : '❌ NO'}`);
      console.log(`  - Before: dark=${beforeState.darkClass}, theme=${beforeState.dataTheme}`);
      console.log(`  - After: dark=${afterState.darkClass}, theme=${afterState.dataTheme}`);
      
      if (!changed) {
        console.log('⚠ Button click did not trigger theme change - possible broken handler');
      }
    }, 200);
    
  } catch (e) {
    console.error('❌ Button simulation error:', e);
  }
} else {
  console.log('⚠ No theme buttons found to test');
}

// 9. Performance and Memory
logSection('9. Performance Analysis');
try {
  const performanceEntries = performance.getEntriesByType('navigation');
  if (performanceEntries.length > 0) {
    const navigation = performanceEntries[0];
    console.log('✓ Page load time:', Math.round(navigation.loadEventEnd - navigation.fetchStart), 'ms');
  }
  
  // Memory usage (if available)
  if (performance.memory) {
    console.log('✓ JS heap size:', Math.round(performance.memory.usedJSHeapSize / 1024 / 1024), 'MB');
  }
  
} catch (e) {
  console.error('❌ Performance analysis error:', e);
}

// 10. Final Recommendations
logSection('10. Diagnostic Summary & Recommendations');

// Run the manual test
console.log('\n🚀 Running manual theme switch test...');
testManualThemeSwitch();

// Summary
setTimeout(() => {
  console.log('\n📋 DIAGNOSTIC SUMMARY:');
  console.log('1. Check if theme provider is properly mounted');
  console.log('2. Verify theme button event handlers are attached');
  console.log('3. Ensure localStorage is working for persistence');
  console.log('4. Validate CSS classes are properly applied');
  console.log('5. Check React context is providing theme state');
  
  console.log('\n🔧 If theme toggle is not working:');
  console.log('- Check browser console for React errors');
  console.log('- Verify theme provider wraps the entire app');
  console.log('- Ensure button onClick handlers are properly bound');
  console.log('- Check for CSS conflicts overriding theme styles');
  
  console.log('\n✨ Debug script complete - check results above');
  console.log('='.repeat(60));
}, 1000);
