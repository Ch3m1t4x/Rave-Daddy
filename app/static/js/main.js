// Ojos que siguen el ratón
(function(){
    const head = document.getElementById('botHead');
    const left = document.getElementById('pupilLeft');
    const right = document.getElementById('pupilRight');
  
    // límites del movimiento del pupil dentro del ojo
    const maxOffset = 10; // px desde el centro
  
    function movePupils(e){
      const rect = head.getBoundingClientRect();
      const cx = rect.left + rect.width / 2;
      const cy = rect.top + rect.height / 2;
  
      const dx = e.clientX - cx;
      const dy = e.clientY - cy;
  
      // normalizamos
      const angle = Math.atan2(dy, dx);
      const dist = Math.min(Math.hypot(dx, dy) / 80, 1); // suavizado
      const ox = Math.cos(angle) * maxOffset * dist;
      const oy = Math.sin(angle) * maxOffset * dist;
  
      left.style.transform = `translate(${ox}px, ${oy}px)`;
      right.style.transform = `translate(${ox}px, ${oy}px)`;
    }
  
    window.addEventListener('mousemove', movePupils, { passive: true });
  })();
  
  // Toggle “Rave mode” para intensificar el glow
  (function(){
    const toggle = document.getElementById('raveToggle');
    function setRave(on){
      document.body.style.filter = on
        ? 'saturate(1.15) brightness(1.05)'
        : 'saturate(1) brightness(1)';
      document.documentElement.style.setProperty('--ring-size', on ? '18px' : '14px');
    }
    setRave(toggle.checked);
    toggle.addEventListener('change', () => setRave(toggle.checked));
  })();
  