// MeowVersionSwitcher
(function () {
  try {
    var path = window.location.pathname;
    var m = path.match(/^(.*?)\/(latest|\d+\.\d+\.\d+(?:[-+][^\/]*)?)\//);
    if (!m) {
      return;
    }

    var base = m[1];
    var current = m[2];
    var rest = path.substring(m[0].length);
    if (!rest) {
      rest = 'index.html';
    }

    fetch(base + '/versions.json', { cache: 'no-cache' })
      .then(function (r) { return r.ok ? r.json() : []; })
      .then(function (list) {
        if (!Array.isArray(list)) {
          list = [];
        }

        var options = ['latest'].concat(
          list.filter(function (v) { return v !== 'latest'; })
        );

        var select = document.createElement('select');
        options.forEach(function (v) {
          var o = document.createElement('option');
          o.value = v;
          o.textContent = v === 'latest' ? 'latest (最新)' : v;
          if (v === current) {
            o.selected = true;
          }
          select.appendChild(o);
        });

        select.addEventListener('change', function () {
          window.location.href = base + '/' + select.value + '/' + rest;
        });

        var wrap = document.createElement('div');
        wrap.style.cssText = 'position:fixed;top:8px;right:16px;z-index:9999;background:#fff;border:1px solid #c8c8c8;border-radius:4px;padding:2px 6px;box-shadow:0 1px 3px rgba(0,0,0,.12);';
        wrap.appendChild(select);
        document.body.appendChild(wrap);
      })
      .catch(function () {});
  } catch (e) {
    /* ignore */
  }
})();
