/**
 * BrandGuard AI — Cyber Effects Engine
 * 1. Hardware-Accelerated Native Cursor (Zero-Latency)
 * 2. High-Performance Ambient Constellation Canvas
 * 3. Throttled 3D Card Parallax Tilt & Telemetry
 */

(function () {
  'use strict';

  // =========================================================================
  // 1. CURSOR ENGINE (NATIVE HARDWARE ACCELERATED — ZERO LAG)
  // =========================================================================
  function initCyberCursor() {
    // Rely exclusively on native OS hardware cursor for instantaneous 0ms response.
    // Clean up any legacy custom cursor DOM nodes if present.
    const dot = document.getElementById('cursor-dot');
    const ring = document.getElementById('cursor-ring');
    if (dot) dot.remove();
    if (ring) ring.remove();
  }

  // =========================================================================
  // 2. AMBIENT CONSTELLATION PARTICLE CANVAS (LIGHTWEIGHT 60FPS)
  // =========================================================================
  function initAmbientParticles() {
    const canvas = document.getElementById('ambient-particles');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    // Optimized particle count for 120fps buttery performance
    const particleCount = width < 768 ? 16 : 24;
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
        this.vx = (Math.random() - 0.5) * 0.35;
        this.vy = -(Math.random() * 0.25 + 0.1);
        this.baseRadius = Math.random() * 1.6 + 0.8;
        this.radius = this.baseRadius;
        this.colorPrefix = colors[Math.floor(Math.random() * colors.length)];
        this.alpha = Math.random() * 0.4 + 0.2;
        this.pulseSpeed = Math.random() * 0.02 + 0.01;
        this.pulseAngle = Math.random() * Math.PI * 2;
      }

      update() {
        this.x += this.vx;
        this.y += this.vy;

        this.pulseAngle += this.pulseSpeed;
        this.currentAlpha = this.alpha + Math.sin(this.pulseAngle) * 0.1;
        this.currentAlpha = Math.max(0.1, Math.min(0.6, this.currentAlpha));

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
        ctx.fill();
      }
    }

    for (let i = 0; i < particleCount; i++) {
      particles.push(new Particle());
    }

    // Connect nearby particles with subtle lines
    function drawConnections() {
      const maxDist = 95;
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < maxDist) {
            const lineAlpha = (1 - dist / maxDist) * 0.1;
            ctx.beginPath();
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.strokeStyle = `rgba(147, 197, 253, ${lineAlpha})`;
            ctx.lineWidth = 0.7;
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

  // =========================================================================
  // 4. BRANDGUARD AI CO-PILOT DRAWER CONTROLLER
  // =========================================================================
  function initAiCopilotDrawer() {
    const trigger = document.getElementById('aiCopilotTrigger');
    const drawer = document.getElementById('aiCopilotDrawer');
    const closeBtn = document.getElementById('closeAiDrawer');
    const chatForm = document.getElementById('aiChatForm');
    const chatInput = document.getElementById('aiChatInput');
    const thread = document.getElementById('aiChatThread');

    if (!trigger || !drawer) return;

    // Toggle drawer open/close
    trigger.addEventListener('click', () => {
      drawer.classList.toggle('open');
      if (drawer.classList.contains('open')) {
        if (chatInput) setTimeout(() => chatInput.focus(), 300);
        updateAiDrawerStatus();
      }
    });

    function updateAiDrawerStatus() {
      fetch('/api/v1/ai/status')
        .then(res => res.json())
        .then(data => {
          const statusEl = document.getElementById('aiDrawerStatus');
          if (statusEl) {
            if (data.is_cloud_active) {
              statusEl.innerHTML = `<span class="pulse-dot pulse-dot-green"></span> <strong class="text-info">${data.active_engine}</strong>`;
            } else {
              statusEl.innerHTML = `<span class="pulse-dot pulse-dot-green"></span> ${data.active_engine}`;
            }
          }
        })
        .catch(() => {});
    }

    if (closeBtn) {
      closeBtn.addEventListener('click', () => drawer.classList.remove('open'));
    }

    // Close on Escape
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && drawer.classList.contains('open')) {
        drawer.classList.remove('open');
      }
    });

    // Global helper for quick action chips
    window.askAiPrompt = function (promptText) {
      if (!drawer.classList.contains('open')) {
        drawer.classList.add('open');
      }
      if (chatInput) {
        chatInput.value = promptText;
        submitAiChat(promptText);
      }
    };

    if (chatForm && chatInput && thread) {
      chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const msg = chatInput.value.trim();
        if (!msg) return;
        submitAiChat(msg);
      });
    }

    function submitAiChat(messageText) {
      if (!thread || !chatInput) return;

      // Append user bubble
      appendMsg('user', messageText);
      chatInput.value = '';

      // Append loading indicator
      const loadingId = 'ai-loading-' + Date.now();
      const loadingEl = document.createElement('div');
      loadingEl.className = 'ai-chat-msg bot';
      loadingEl.id = loadingId;
      loadingEl.innerHTML = `
        <div class="ai-msg-bubble text-cyan">
          <span class="spinner-border spinner-border-sm me-2" role="status"></span>
          Consulting BrandGuard AI Neural Engine...
        </div>
      `;
      thread.appendChild(loadingEl);
      thread.scrollTop = thread.scrollHeight;

      // Extract context from page if available (e.g. active text in studio or review)
      let pageContext = '';
      const studioInput = document.getElementById('inputContent');
      const diffUpdated = document.querySelector('.diff-updated');
      if (studioInput && studioInput.value) {
        pageContext = studioInput.value;
      } else if (diffUpdated && diffUpdated.innerText) {
        pageContext = diffUpdated.innerText;
      }

      // Send to backend API
      fetch('/api/v1/ai/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: messageText, context: pageContext })
      })
      .then(res => res.json())
      .then(data => {
        const loading = document.getElementById(loadingId);
        if (loading) loading.remove();

        const reply = data.reply || 'Analysis complete. Adhere to brand guidelines.';
        appendMsg('bot', reply, data.source);
      })
      .catch(err => {
        const loading = document.getElementById(loadingId);
        if (loading) loading.remove();
        appendMsg('bot', 'AI Engine connection error. Please try again.');
      });
    }

    function appendMsg(sender, text, source) {
      if (!thread) return;
      const el = document.createElement('div');
      el.className = `ai-chat-msg ${sender}`;

      // Convert basic markdown-style formatting (*bold*, code, bullets)
      let formatted = text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/`([^`]+)`/g, '<code class="text-cyan px-1 bg-dark rounded">$1</code>')
        .replace(/\n\n/g, '<br/><br/>')
        .replace(/\n•/g, '<br/>&bull;')
        .replace(/\n/g, '<br/>');

      let actionButtons = '';
      let sourceBadge = '';

      if (sender === 'bot') {
        if (source) {
          const isGemini = source.includes('Gemini');
          sourceBadge = `
            <div class="d-flex align-items-center justify-content-between mb-2 pb-1 border-bottom border-secondary border-opacity-15">
              <span class="badge ${isGemini ? 'bg-primary' : 'bg-dark'} border ${isGemini ? 'border-primary' : 'border-secondary'} text-cyan px-2 py-1" style="font-size: 0.68rem; font-weight: 600;">
                <i class="bi ${isGemini ? 'bi-stars' : 'bi-cpu'} me-1"></i>${source}
              </span>
            </div>
          `;
        }

        const cleanCopyText = text.replace(/'/g, "\\'").replace(/"/g, '&quot;');
        actionButtons = `
          <div class="mt-2 pt-2 border-top border-secondary border-opacity-25 d-flex gap-2">
            <button type="button" class="btn btn-xs btn-outline-info rounded-pill py-0 px-2" style="font-size: 0.7rem;" onclick="copyToClipboard('${cleanCopyText}', 'Response copied!')">
              <i class="bi bi-clipboard me-1"></i> Copy
            </button>
            ${document.getElementById('inputContent') ? `
              <button type="button" class="btn btn-xs btn-gradient-primary rounded-pill py-0 px-2" style="font-size: 0.7rem;" onclick="insertAiTextToStudio('${cleanCopyText}')">
                <i class="bi bi-arrow-down-left-square me-1"></i> Use in Studio
              </button>
            ` : ''}
          </div>
        `;
      }

      el.innerHTML = `
        <div class="ai-msg-bubble">
          ${sourceBadge}
          ${formatted}
          ${actionButtons}
        </div>
      `;
      thread.appendChild(el);
      thread.scrollTop = thread.scrollHeight;
    }

    window.insertAiTextToStudio = function (text) {
      const editor = document.getElementById('inputContent');
      if (editor) {
        editor.value = text;
        if (window.updateCharCount) window.updateCharCount();
        window.showToast('AI response loaded into Studio editor!', 'success');
      }
    };
  }

  // =========================================================================
  // 5. 3D INTERACTIVE CARD PARALLAX TILT ENGINE (THROTTLED WITH RAF)
  // =========================================================================
  function init3DCardTilt() {
    if (!window.matchMedia('(pointer: fine)').matches) return;

    const tiltCards = document.querySelectorAll(
      '.bg-card, .portal-card-client, .portal-card-reviewer, .portal-card-admin, .stat-card, .dropzone-container, .card-3d-tilt, .dashboard-stat-card'
    );

    tiltCards.forEach((card) => {
      card.classList.add('perspective-card');

      let bounds = null;
      let rafId = null;

      card.addEventListener('mouseenter', () => {
        bounds = card.getBoundingClientRect();
        card.style.transition = 'transform 0.1s ease-out';
      }, { passive: true });

      card.addEventListener('mousemove', (e) => {
        if (!bounds) bounds = card.getBoundingClientRect();
        if (rafId) return; // Throttle to display refresh rate

        rafId = requestAnimationFrame(() => {
          rafId = null;
          const mouseX = e.clientX - bounds.left;
          const mouseY = e.clientY - bounds.top;

          const xPct = mouseX / bounds.width - 0.5;
          const yPct = mouseY / bounds.height - 0.5;

          const tiltX = -yPct * 8;
          const tiltY = xPct * 10;

          card.style.transform = `perspective(1000px) rotateX(${tiltX.toFixed(1)}deg) rotateY(${tiltY.toFixed(1)}deg) translateZ(4px) scale3d(1.01, 1.01, 1.01)`;
          card.style.setProperty('--sheen-x', `${mouseX}px`);
          card.style.setProperty('--sheen-y', `${mouseY}px`);
        });
      }, { passive: true });

      card.addEventListener('mouseleave', () => {
        if (rafId) {
          cancelAnimationFrame(rafId);
          rafId = null;
        }
        bounds = null;
        card.style.transition = 'transform 0.45s cubic-bezier(0.23, 1, 0.32, 1)';
        card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateZ(0px) scale3d(1, 1, 1)';
      }, { passive: true });
    });
  }

  // =========================================================================
  // 6. DYNAMIC AUDIO EQUALIZER FREQUENCY BARS
  // =========================================================================
  function initEqualizerWaves() {
    const bars = document.querySelectorAll('.eq-bar');
    if (!bars.length) return;

    setInterval(() => {
      bars.forEach((bar) => {
        const h = Math.floor(Math.random() * 75) + 25;
        bar.style.height = `${h}%`;
      });
    }, 250);
  }

  // Initialize once DOM is ready
  document.addEventListener('DOMContentLoaded', () => {
    initAmbientParticles();
    initAiCopilotDrawer();
    init3DCardTilt();
    initEqualizerWaves();
  });

})();
