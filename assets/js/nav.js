/* ═══════════════════════════════════════════════════════════════
   PDF Cowboy — Shared Navigation
   Edit this file to update the header across ALL pages at once.
   Each page just needs:
     <header class="site-header" id="site-header"></header>
     <script src="../assets/js/nav.js"></script>
   (use src="assets/js/nav.js" on the root index.html)
═══════════════════════════════════════════════════════════════ */

(function() {

  /* ── Nav definition ─────────────────────────────────────────
     To add/remove/rename a tile or tool, edit this array only.
  ─────────────────────────────────────────────────────────────*/
  const NAV = [
    {
      label:  'Edit',
      href:   'edit/',
      tools:  [
        { label: 'Merge',               href: 'edit/#merge'     },
        { label: 'Split',               href: 'edit/#split'     },
        { label: 'Rearrange',           href: 'edit/#rearrange' },
        { label: 'Rotate',              href: 'edit/#rotate'    },
        { label: 'Crop',                href: 'edit/#crop'      },
        { label: 'Resize',              href: 'edit/#resize'    },
        { label: 'Blank page inserter', href: 'edit/#blank'     },
      ]
    },
    {
      label: 'Content',
      href:  'content/',
      tools: [
        { label: 'Text & Drawing',  href: 'content/' },
        { label: 'Annotate',        href: 'content/' },
        { label: 'Stamp',           href: 'content/' },
        { label: 'Watermark',       href: 'content/' },
        { label: 'Page numbers',    href: 'content/' },
      ]
    },
    {
      label: 'Measure',
      href:  'measure/',
      tools: [
        { label: 'Measure areas',   href: 'measure/' },
        { label: 'Measure lengths', href: 'measure/' },
        { label: 'Add dimensions',  href: 'measure/' },
        { label: 'Markup plans',    href: 'measure/' },
      ]
    },
    {
      label: 'Sign',
      href:  'sign/',
      tools: [
        { label: 'Sign a PDF', href: 'sign/' },
      ]
    },
    {
      label: 'Utilities',
      href:  'utilities/',
      tools: [
        { label: 'Protect',   href: 'utilities/' },
        { label: 'Unlock',    href: 'utilities/' },
        { label: 'Compress',  href: 'utilities/' },
        { label: 'Repair',    href: 'utilities/' },
      ]
    },
    {
      label: 'Convert',
      href:  'convert/',
      tools: [
        { label: 'PDF to Image', href: 'convert/' },
        { label: 'Image to PDF', href: 'convert/' },
      ]
    },
  ];

  /* ── Use absolute paths — works from any page ── */


  /* ── Build HTML ─────────────────────────────────────────────*/
  const tilesHTML = NAV.map(tile => `
    <div class="site-tile">
      <a class="site-tile-name" href="/${tile.href}">PDF <span>${tile.label}</span></a>
      <ul class="site-tile-tools">
        ${tile.tools.map(t => `
          <li><a href="/${t.href}">${t.label}</a></li>
        `).join('')}
      </ul>
    </div>
  `).join('');

  const html = `
    <a class="site-logo" href="/"><em>PDF</em> Cowboy</a>
    <nav class="site-nav">${tilesHTML}</nav>
  `;

  /* ── Inject ─────────────────────────────────────────────────*/
  const el = document.getElementById('site-header');
  if (el) {
    el.innerHTML = html;
  } else {
    // Fallback: create header if placeholder not found
    const header = document.createElement('header');
    header.className = 'site-header';
    header.id = 'site-header';
    header.innerHTML = html;
    document.body.insertBefore(header, document.body.firstChild);
  }

})();
