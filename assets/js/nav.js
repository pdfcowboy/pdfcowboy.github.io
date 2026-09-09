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
      href:   'tools/edit/',
      tools:  [
        { label: 'Merge',               href: 'tools/edit/#merge'     },
        { label: 'Split',               href: 'tools/edit/#split'     },
        { label: 'Rearrange',           href: 'tools/edit/#rearrange' },
        { label: 'Rotate',              href: 'tools/edit/#rotate'    },
        { label: 'Crop',                href: 'tools/edit/#crop'      },
        { label: 'Resize',              href: 'tools/edit/#resize'    },
        { label: 'Blank page inserter', href: 'tools/edit/#blank'     },
      ]
    },
    {
      label: 'Content',
      href:  'tools/content/',
      tools: [
        { label: 'Text & Drawing',  href: 'tools/content/' },
        { label: 'Annotate',        href: 'tools/content/' },
        { label: 'Stamp',           href: 'tools/content/' },
        { label: 'Watermark',       href: 'tools/content/' },
        { label: 'Page numbers',    href: 'tools/content/' },
      ]
    },
    {
      label: 'Measure',
      href:  'tools/measure/',
      tools: [
        { label: 'Measure areas',   href: 'tools/measure/' },
        { label: 'Measure lengths', href: 'tools/measure/' },
        { label: 'Add dimensions',  href: 'tools/measure/' },
        { label: 'Markup plans',    href: 'tools/measure/' },
      ]
    },
    {
      label: 'Sign',
      href:  'tools/sign/',
      tools: [
        { label: 'Sign a PDF', href: 'tools/sign/' },
      ]
    },
    {
      label: 'Utilities',
      href:  'tools/utilities/',
      tools: [
        { label: 'Protect',   href: 'tools/utilities/#protect'  },
        { label: 'Unlock',    href: 'tools/utilities/#unlock'   },
        { label: 'Compress',  href: 'tools/utilities/#compress' },
        { label: 'Repair',    href: 'tools/utilities/#repair'   },
      ]
    },
    {
      label: 'Convert',
      href:  'tools/convert/',
      tools: [
        { label: 'PDF to Image', href: 'tools/convert/' },
        { label: 'Image to PDF', href: 'tools/convert/' },
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
