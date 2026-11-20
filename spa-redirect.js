// GitHub Pages SPA redirect, receiving side (paired with public/404.html).
// 404.html turns /path into /?/path; this restores the original URL before the
// app loads. A separate file, not an inline <script>, so CSP script-src 'self'
// covers it without a content hash (BLG-FE-325: the production build minifies
// index.html, so a hash computed from the source never matched the built page).
// Loaded with defer, before the app's own deferred bundle, so it still runs first
// (deferred scripts run in document order) without blocking the first paint.
(function(l) {
  if (l.search[1] === '/' ) {
    var decoded = l.search.slice(1).split('&').map(function(s) { 
      return s.replace(/~and~/g, '&')
    }).join('?');
    window.history.replaceState(null, null,
        l.pathname.slice(0, -1) + decoded + l.hash
    );
  }
}(window.location))
