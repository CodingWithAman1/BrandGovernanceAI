/**
 * BrandGuard AI — Cyber Effects Engine
 * 1. Interactive Dual Cyber Cursor (Dot + Lagging Magnetic Glow Ring + Ripple)
 * 2. Ambient Constellation Particle Canvas
 * 3. Dynamic Interactive Toasts & Audio-Visual Feedback
 */

(function () {
  'use strict';

  // =========================================================================
  // 1. DUAL CYBER CURSOR ENGINE
  // =========================================================================
  function initCyberCursor() {
    // Only initialize on desktop / pointer-fine devices
    if (!window.matchMedia('(pointer: fine)').matches) return;

    const dot = document.getElementById('cursor-dot');
    const ring = document.getElementById('cursor-ring');
    if (!dot || !ring) return;

    let mouseX = -100;
    let mouseY = -100;
    let ringX = -100;
    let ringY = -100;
    let isVisible = false;
    let isClicking = false;
    let isHovering = false;

    // Linear interpolation helper
    const lerp = (start, end, factor) => start + (end - start) * factor;

    // Track mouse movement
    window.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;

      if (!isVisible) {
        isVisible = true;
        dot.style.opacity = '1';
        ring.style.opacity = '1';
        ringX = mouseX;
        ringY = mouseY;
      }

      // Dot moves instantaneously
      dot.style.transform = `translate3d(${mouseX}px, ${mouseY}px, 0)`;
    });

    // Detect mouse leaving window
    document.addEventListener('mouseleave', () => {
      isVisible = false;
      dot.style.opacity = '0';
      ring.style.opacity = '0';
    });

    document.addEventListener('mouseenter', () => {
      isVisible = true;
      dot.style.opacity = '1';
      ring.style.opacity = '1';
    });

    // Click feedback
    window.addEventListener('mousedown', (e) => {
      isClicking = true;
      ring.classList.add('cursor-clicking');
      createClickRipple(e.clientX, e.clientY);
    });

    window.addEventListener('mouseup', () => {
      isClicking = false;
      ring.classList.remove('cursor-clicking');
    });

    // Hover detection over interactive elements
    const interactiveSelectors = [
      'a',
      'button',
      'input',
      'textarea',
      'select',
      '.btn',
      '.btn-sample-chip',
      '.dropzone-container',
      '.nav-link-custom',
      '.bg-card-hover',
      '.dropdown-item',
      '.badge[role="button"]',
      '[data-cursor-hover]'
    ].join(',');

    document.addEventListener('mouseover', (e) => {
      if (e.target.closest(interactiveSelectors)) {
        isHovering = true;
        ring.classList.add('cursor-hovering');
        dot.classList.add('dot-hovering');
      }
    });

    document.addEventListener('mouseout', (e) => {
      if (e.target.closest(interactiveSelectors)) {
        isHovering = false;
        ring.classList.remove('cursor-hovering');
        dot.classList.remove('dot-hovering');
      }
    });

    // Click ripple particle wave
    function createClickRipple(x, y) {
      const ripple = document.createElement('div');
      ripple.className = 'cursor-click-ripple';
      ripple.style.left = `${x}px`;
      ripple.style.top = `${y}px`;
      document.body.appendChild(ripple);

      ripple.addEventListener('animationend', () => {
        ripple.remove();
      });
    }

    // High performance RAF loop for smooth ring trailing (lerp)
    function renderCursor() {
      if (isVisible) {
        ringX = lerp(ringX, mouseX, 0.18);
        ringY = lerp(ringY, mouseY, 0.18);
        ring.style.transform = `translate3d(${ringX}px, ${ringY}px, 0)`;
      }
      requestAnimationFrame(renderCursor);
    }
    requestAnimationFrame(renderCursor);
  }

  // =========================================================================
  // 2. AMBIENT CONSTELLATION PARTICLE CANVAS
  // =========================================================================
  function initAmbientParticles() {
    const canvas = document.getElementById('ambient-particles');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    // Responsive particle count (fewer on small screens)
    const particleCount = width < 768 ? 22 : 42;
    const particles = [];
    const colors = [
      'rgba(56, 189, 248, ',  // Electric Cyan
      'rgba(99, 102, 241, ',  // Indigo
      'rgba(168, 85, 247, ',  // Violet
      'rgba(14, 165, 233, '   // Sky Blue
    ];

    class Particle {
      constructor() {
        this.reset(true);
      }

      reset(init = false) {
        this.x = Math.random() * width;
        this.y = init ? Math.random() * height : height + 10;
        this.vx = (Math.random() - 0.5) * 0.45;
        this.vy = -(Math.random() * 0.35 + 0.15); // drift gently upward
        this.baseRadius = Math.random() * 1.8 + 0.8;
        this.radius = this.baseRadius;
        this.colorPrefix = colors[Math.floor(Math.random() * colors.length)];
        this.alpha = Math.random() * 0.45 + 0.2;
        this.pulseSpeed = Math.random() * 0.02 + 0.01;
        this.pulseAngle = Math.random() * Math.PI * 2;
      }

      update() {
        this.x += this.vx;
        this.y += this.vy;

        // Subtle pulsing size/alpha
        this.pulseAngle += this.pulseSpeed;
        this.currentAlpha = this.alpha + Math.sin(this.pulseAngle) * 0.12;
        this.currentAlpha = Math.max(0.1, Math.min(0.7, this.currentAlpha));

        // Wrap around boundaries
        if (this.x < -20) this.x = width + 20;
        if (this.x > width + 20) this.x = -20;
        if (this.y < -20) {
          this.y = height + 20;
          this.x = Math.random() * width;
        }
      }

      draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = `${this.colorPrefix}${this.currentAlpha})`;
        ctx.shadowBlur = 10;
        ctx.shadowColor = `${this.colorPrefix}0.6)`;
        ctx.fill();
        ctx.shadowBlur = 0; // reset
      }
    }

    // Initialize particles
    for (let i = 0; i < particleCount; i++) {
      particles.push(new Particle());
    }

    // Connect nearby particles with subtle glowing lines
    function drawConnections() {
      const maxDist = 110;
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < maxDist) {
            const lineAlpha = (1 - dist / maxDist) * 0.12;
            ctx.beginPath();
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.strokeStyle = `rgba(147, 197, 253, ${lineAlpha})`;
            ctx.lineWidth = 0.8;
            ctx.stroke();
          }
        }
      }
    }

    let animationFrameId;
    function animate() {
      if (document.hidden) {
        animationFrameId = requestAnimationFrame(animate);
        return;
      }

      ctx.clearRect(0, 0, width, height);

      particles.forEach((p) => {
        p.update();
        p.draw();
      });

      drawConnections();

      animationFrameId = requestAnimationFrame(animate);
    }

    animate();

    // Debounced window resize
    let resizeTimer;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
      }, 200);
    });
  }

  // =========================================================================
  // 3. TOAST NOTIFICATION UTILITY
  // =========================================================================
  window.showToast = function (message, type = 'info', duration = 3200) {
    let container = document.getElementById('bg-toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'bg-toast-container';
      container.className = 'bg-toast-container';
      document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `bg-toast-item bg-toast-${type}`;

    let icon = 'bi-info-circle';
    if (type === 'success') icon = 'bi-check2-circle';
    if (type === 'warning') icon = 'bi-exclamation-triangle';
    if (type === 'error') icon = 'bi-x-circle';

    toast.innerHTML = `
      <div class="toast-icon"><i class="bi ${icon}"></i></div>
      <div class="toast-body">${message}</div>
      <button class="toast-close" type="button"><i class="bi bi-x"></i></button>
    `;

    container.appendChild(toast);

    const closeBtn = toast.querySelector('.toast-close');
    closeBtn.addEventListener('click', () => {
      toast.classList.add('toast-leave');
      setTimeout(() => toast.remove(), 300);
    });

    setTimeout(() => {
      if (toast.parentNode) {
        toast.classList.add('toast-leave');
        setTimeout(() => toast.remove(), 300);
      }
    }, duration);
  };

  // Clipboard copy helper
  window.copyToClipboard = function (text, label = 'Copied to clipboard!') {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(() => {
        window.showToast(label, 'success');
      }).catch(() => {
        fallbackCopy(text, label);
      });
    } else {
      fallbackCopy(text, label);
    }
  };

  function fallbackCopy(text, label) {
    const el = document.createElement('textarea');
    el.value = text;
    el.setAttribute('readonly', '');
    el.style.position = 'absolute';
    el.style.left = '-9999px';
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
    window.showToast(label, 'success');
  }

  // Initialize once DOM is ready
  document.addEventListener('DOMContentLoaded', () => {
    initCyberCursor();
    initAmbientParticles();
  });

})();
