import Document, { Html, Head, Main, NextScript } from "next/document";

const themeInit = `
(function(){
  try{
    var KEY='ui.theme';
    var m = null;
    try { m = localStorage.getItem(KEY); } catch(_) {}
    var sys = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    var dark = m==='dark' || (m==='system' && sys);
    var de = document.documentElement;
    de.classList.toggle('dark', !!dark);
    de.setAttribute('data-theme', dark ? 'dark':'light');
    de.setAttribute('data-theme-owner','tp');
    document.body && document.body.classList.remove('dark');
    if (typeof window!=='undefined') {
      window.__theme = {
        get: function(){ try { return localStorage.getItem(KEY)||'light'; } catch(_) { return 'light'; }},
        set: function(mode){ try{ localStorage.setItem(KEY, mode); }catch(e){}; 
          var s = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
          var d = mode==='dark' || (mode==='system' && s);
          de.classList.toggle('dark', !!d);
          de.setAttribute('data-theme', d ? 'dark':'light');
          de.setAttribute('data-theme-owner','tp');
          document.body && document.body.classList.remove('dark');
        }
      };
    }
  }catch(e){}
})();`;

export default class MyDocument extends Document {
  render() {
    return (
      <Html lang="en">
        <Head>
          <script dangerouslySetInnerHTML={{ __html: themeInit }} />
        </Head>
        <body>
          <Main />
          <NextScript />
        </body>
      </Html>
    );
  }
}
