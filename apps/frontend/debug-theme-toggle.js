// Theme Toggle Debug Script - Diagnose warum Dark/Light Mode nicht funktioniert
// In Browser Console kopieren und ausführen

console.log('🔍 InfoTerminal Theme Toggle Diagnose gestartet...');

// 1. Aktuelle Theme-Zustand prüfen
const checkCurrentState = () => {
  console.log('\n1. 🎯 Aktueller Theme-Zustand:');
  
  const root = document.documentElement;
  console.log('   HTML classList:', root.classList.toString());
  console.log('   data-theme:', root.getAttribute('data-theme'));
  console.log('   data-theme-owner:', root.getAttribute('data-theme-owner'));
  
  // LocalStorage prüfen
  try {
    const storedTheme = localStorage.getItem('ui.theme');
    console.log('   localStorage ui.theme:', storedTheme);
  } catch (e) {
    console.log('   localStorage Fehler:', e.message);
  }
  
  // System Dark Mode prüfen
  const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  console.log('   System prefers dark:', systemPrefersDark);
};

// 2. Theme Toggle Buttons finden
const findToggleButtons = () => {
  console.log('\n2. 🔘 Theme Toggle Buttons suchen:');
  
  // Nach verschiedenen Selektoren suchen
  const selectors = [
    'button[title*="theme"]',
    'button[aria-label*="theme"]',
    'button[aria-label*="Theme"]',
    'button[title*="Theme"]',
    '[data-theme-toggle]',
    '.theme-toggle'
  ];
  
  let foundButtons = [];
  
  selectors.forEach(selector => {
    const buttons = document.querySelectorAll(selector);
    if (buttons.length > 0) {
      console.log(`   ✅ Gefunden mit "${selector}":`, buttons.length);
      foundButtons.push(...buttons);
    }
  });
  
  // Alle Buttons mit "theme" im Text suchen
  const allButtons = document.querySelectorAll('button');
  allButtons.forEach((btn, idx) => {
    const text = btn.textContent?.toLowerCase() || '';
    const title = btn.getAttribute('title')?.toLowerCase() || '';
    const ariaLabel = btn.getAttribute('aria-label')?.toLowerCase() || '';
    
    if (text.includes('theme') || title.includes('theme') || ariaLabel.includes('theme') ||
        text.includes('dark') || text.includes('light') || title.includes('dark') || title.includes('light')) {
      console.log(`   🎯 Button ${idx}: "${text}" title="${title}" aria-label="${ariaLabel}"`);
      foundButtons.push(btn);
    }
  });
  
  return [...new Set(foundButtons)]; // Duplikate entfernen
};

// 3. Manual Theme Toggle Test
const testManualToggle = () => {
  console.log('\n3. 🧪 Manueller Theme Toggle Test:');
  
  const root = document.documentElement;
  const currentHasDark = root.classList.contains('dark');
  
  console.log('   Vor Toggle - dark class:', currentHasDark);
  
  if (currentHasDark) {
    root.classList.remove('dark');
    root.setAttribute('data-theme', 'light');
    console.log('   ➡️ Umgeschaltet auf LIGHT');
  } else {
    root.classList.add('dark');
    root.setAttribute('data-theme', 'dark');
    console.log('   ➡️ Umgeschaltet auf DARK');
  }
  
  // Nach 2 Sekunden Ergebnis prüfen
  setTimeout(() => {
    const newHasDark = document.documentElement.classList.contains('dark');
    console.log('   Nach Toggle - dark class:', newHasDark);
    console.log('   Toggle erfolgreich:', newHasDark !== currentHasDark);
    
    // CSS-Style-Änderungen prüfen
    const body = document.body;
    const computedStyle = window.getComputedStyle(body);
    console.log('   Body background-color:', computedStyle.backgroundColor);
    console.log('   Body color:', computedStyle.color);
  }, 100);
};

// 4. Button Click Simulation
const simulateButtonClick = (buttons) => {
  if (buttons.length === 0) {
    console.log('\n4. ❌ Keine Theme Toggle Buttons gefunden!');
    return;
  }
  
  console.log('\n4. 🖱️ Simuliere Button Click:');
  
  const button = buttons[0];
  console.log('   Klicke Button:', button.outerHTML.substring(0, 100) + '...');
  
  const beforeClick = document.documentElement.classList.contains('dark');
  console.log('   Vor Klick - dark mode:', beforeClick);
  
  // Event Listener prüfen
  const events = button.getEventListeners ? button.getEventListeners() : 'Nicht verfügbar';
  console.log('   Event Listeners:', events);
  
  // Button klicken
  button.click();
  
  setTimeout(() => {
    const afterClick = document.documentElement.classList.contains('dark');
    console.log('   Nach Klick - dark mode:', afterClick);
    console.log('   Klick hat Effekt:', beforeClick !== afterClick);
  }, 500);
};

// 5. CSS Rules prüfen
const checkCSSRules = () => {
  console.log('\n5. 🎨 CSS Dark Mode Rules prüfen:');
  
  let darkRules = 0;
  let lightRules = 0;
  
  try {
    Array.from(document.styleSheets).forEach(sheet => {
      try {
        Array.from(sheet.cssRules || []).forEach(rule => {
          if (rule.selectorText) {
            if (rule.selectorText.includes('.dark')) {
              darkRules++;
            }
            if (rule.selectorText.includes(':root') || rule.selectorText.includes('html')) {
              lightRules++;
            }
          }
        });
      } catch (e) {
        // CORS blocked stylesheets
      }
    });
    
    console.log(`   ✅ Dark Mode CSS Rules gefunden: ${darkRules}`);
    console.log(`   ✅ Root/HTML CSS Rules gefunden: ${lightRules}`);
  } catch (e) {
    console.log('   ❌ CSS Inspektion fehlgeschlagen:', e.message);
  }
};

// 6. React DevTools prüfen
const checkReactState = () => {
  console.log('\n6. ⚛️ React State prüfen:');
  
  // Versuche React DevTools zu finden
  if (window.__REACT_DEVTOOLS_GLOBAL_HOOK__) {
    console.log('   ✅ React DevTools verfügbar');
  } else {
    console.log('   ❌ React DevTools nicht verfügbar');
  }
  
  // React Root finden
  const reactRoot = document.querySelector('#__next') || document.querySelector('[data-reactroot]');
  if (reactRoot) {
    console.log('   ✅ React Root gefunden');
  } else {
    console.log('   ❌ React Root nicht gefunden');
  }
};

// Vollständige Diagnose ausführen
const runCompleteDiagnosis = () => {
  checkCurrentState();
  const buttons = findToggleButtons();
  checkCSSRules();
  checkReactState();
  
  console.log('\n⏳ Starte Tests in 2 Sekunden...');
  
  setTimeout(() => {
    testManualToggle();
  }, 2000);
  
  setTimeout(() => {
    simulateButtonClick(buttons);
  }, 4000);
  
  console.log('\n📋 Diagnose wird in 6 Sekunden abgeschlossen...');
  
  setTimeout(() => {
    console.log('\n✅ Diagnose abgeschlossen!');
    console.log('\n💡 Nächste Schritte:');
    console.log('1. Wenn manueller Toggle funktioniert, aber Button nicht -> Event Handler Problem');
    console.log('2. Wenn gar nichts funktioniert -> CSS/Tailwind Problem');
    console.log('3. Wenn Button klick registriert wird, aber Theme nicht ändert -> ThemeProvider Problem');
    
    // Zusätzliche Empfehlungen
    console.log('\n🔧 Debugging-Befehle:');
    console.log('- window.debugTheme.manualToggle() // Manuell umschalten');
    console.log('- window.debugTheme.currentState() // Aktueller Zustand');
    console.log('- window.debugTheme.findButtons() // Buttons finden');
  }, 6000);
};

// Funktionen für manuelles Debugging verfügbar machen
window.debugTheme = {
  currentState: checkCurrentState,
  findButtons: findToggleButtons,
  manualToggle: testManualToggle,
  checkCSS: checkCSSRules,
  runDiagnosis: runCompleteDiagnosis
};

// Auto-Start
runCompleteDiagnosis();
