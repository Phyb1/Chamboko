(() => {
  const csrf = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
  const trackUrl = '/track/';

  document.addEventListener('click', (event) => {
    const el = event.target.closest('[data-track-type]');
    if (!el) return;
    const payload = new URLSearchParams({
      event_type: el.dataset.trackType || 'other',
      label: el.dataset.trackLabel || '',
      page: window.location.pathname,
      target: el.getAttribute('href') || '',
      service_id: el.dataset.serviceId || '',
      branch_id: el.dataset.branchId || ''
    });
    fetch(trackUrl, {
      method: 'POST',
      credentials: 'same-origin',
      headers: {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8', 'X-CSRFToken': csrf || ''},
      body: payload,
      keepalive: true
    }).catch(() => {});
  });

  const sections = [...document.querySelectorAll('[data-section]')];
  const markers = [...document.querySelectorAll('[data-progress]')];
  if ('IntersectionObserver' in window && sections.length && markers.length) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        markers.forEach(marker => marker.classList.toggle(
          'is-active', marker.dataset.progress === entry.target.dataset.section
        ));
      });
    }, {rootMargin: '-35% 0px -55% 0px', threshold: 0});
    sections.forEach(section => observer.observe(section));
  }

  document.querySelectorAll('.reveal').forEach(el => {
    if (!('IntersectionObserver' in window)) {
      el.classList.add('is-visible');
      return;
    }
    const observer = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting) {
        el.classList.add('is-visible');
        observer.disconnect();
      }
    }, {threshold: 0.12});
    observer.observe(el);
  });
})();
