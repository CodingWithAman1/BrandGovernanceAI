// Sample Presets for Studio Testing
const SAMPLE_PRESETS = {
  hyperbolic: {
    title: "Q4 Cloud Launch Campaign",
    content: "In today's fast-paced world, our revolutionary, #1 AI platform in the world guarantees 100% perfect marketing results with zero risk. While competitors struggle, our game-changer tool helps you crush the competition. Obviously, any company using Inkloom Classic should upgrade immediately. A rich tapestry of enterprise tools delves into your data."
  },
  compliant: {
    title: "Enterprise Trust & Architecture Whitepaper",
    content: "Inkloom Enterprise Cloud serves over 50,000 active enterprise organizations globally across 85 countries. Our independently audited SOC 2 Type II certified infrastructure provides enterprise-grade reliability backed by our 99.95% verified availability SLA."
  },
  jargon: {
    title: "Customer Success Story Draft",
    content: "It is a testament to our team that we unpack deep customer insights and crush the competition. Why settle for inferior Slack-killer tools when you can have our unrivaled platform that never fails?"
  }
};

function loadPreset(key) {
  if (SAMPLE_PRESETS[key]) {
    const titleEl = document.getElementById('inputTitle');
    const contentEl = document.getElementById('inputContent');
    if (titleEl && contentEl) {
      titleEl.value = SAMPLE_PRESETS[key].title;
      contentEl.value = SAMPLE_PRESETS[key].content;
      if (typeof updateCharCount === 'function') {
        updateCharCount();
      }
      if (window.showToast) {
        window.showToast(`Loaded preset: "${SAMPLE_PRESETS[key].title}"`, 'info');
      }
    }
  }
}

// 1-Click Fix Handler with Smooth Dark-Mode Visual Feedback
function applyOneClickFix(flagId) {
  const btn = document.getElementById(`fix-btn-${flagId}`);
  if (!btn) return;
  
  btn.innerHTML = `<span class="spinner-border spinner-border-sm" role="status"></span> Applying...`;
  btn.disabled = true;

  fetch(`/scanner/apply-fix/${flagId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Requested-With': 'XMLHttpRequest'
    }
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      btn.className = "badge badge-success-glow px-3 py-2 fs-6 rounded-pill text-decoration-none";
      btn.innerHTML = `<i class="bi bi-check2-all me-1"></i> Remediated`;

      // Update text in working container with sleek dark-mode green glow pulse
      const diffUpdatedContainer = document.getElementById('diffUpdatedText');
      if (diffUpdatedContainer && data.new_content) {
        diffUpdatedContainer.innerText = data.new_content;
        diffUpdatedContainer.style.transition = 'all 0.4s ease';
        diffUpdatedContainer.style.backgroundColor = 'rgba(16, 185, 129, 0.25)';
        diffUpdatedContainer.style.boxShadow = '0 0 25px rgba(16, 185, 129, 0.45)';
        
        setTimeout(() => {
          diffUpdatedContainer.style.backgroundColor = 'rgba(16, 185, 129, 0.08)';
          diffUpdatedContainer.style.boxShadow = 'none';
        }, 800);
      }

      // Update overall score counter
      const scoreBadge = document.getElementById('brandScoreValue');
      if (scoreBadge && data.new_score) {
        scoreBadge.innerText = data.new_score;
      }

      // Animate the Radial SVG Progress Bar
      const circleProgress = document.getElementById('radialProgressBar');
      if (circleProgress && data.new_score) {
        const perimeter = 339.29;
        const newOffset = perimeter - (perimeter * data.new_score / 100);
        circleProgress.style.strokeDashoffset = newOffset;
        
        if (data.new_score >= 80) {
          circleProgress.classList.remove('score-low', 'score-med');
          circleProgress.classList.add('score-high');
        } else if (data.new_score >= 50) {
          circleProgress.classList.remove('score-low', 'score-high');
          circleProgress.classList.add('score-med');
        }
      }

      // Update flag status indicator
      const statusIndicator = document.getElementById(`flag-status-${flagId}`);
      if (statusIndicator) {
        statusIndicator.className = "small fw-bold text-success";
        statusIndicator.innerHTML = `&bull; ACCEPTED`;
      }

      // Mark card as accepted
      const flagCard = document.getElementById(`flag-card-${flagId}`);
      if (flagCard) {
        flagCard.classList.remove('border-danger', 'border-warning');
        flagCard.classList.add('border-success');
      }

      // Sleek toast feedback
      if (window.showToast) {
        window.showToast(`1-Click Fix Applied! New Brand Health: ${data.new_score}%`, 'success');
      }
    } else {
      btn.innerHTML = `Error`;
      if (window.showToast) {
        window.showToast(data.message || 'Could not apply fix.', 'error');
      } else {
        alert(data.message || 'Could not apply fix.');
      }
    }
  })
  .catch(err => {
    btn.innerHTML = `Retry`;
    btn.disabled = false;
    console.error('Error applying fix:', err);
    if (window.showToast) {
      window.showToast('Failed to apply fix. Network error.', 'error');
    }
  });
}

// Helper: Copy Suggested Text Snippet
function copySuggestedText(text) {
  if (window.copyToClipboard) {
    window.copyToClipboard(text, 'Tone correction copied to clipboard!');
  } else {
    navigator.clipboard.writeText(text);
  }
}

// Helper: Copy Current Remediated Copy
function copyRemediatedCopy() {
  const container = document.getElementById('diffUpdatedText');
  if (container) {
    const text = container.innerText || container.textContent;
    if (window.copyToClipboard) {
      window.copyToClipboard(text.trim(), 'Remediated copy copied to clipboard!');
    }
  }
}

// Helper: Download Remediated Copy as Text File
function downloadCleanCopy(title = 'Remediated_Copy') {
  const container = document.getElementById('diffUpdatedText');
  if (!container) return;
  const text = (container.innerText || container.textContent).trim();
  const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  const safeTitle = title.replace(/[^a-zA-Z0-9_-]/g, '_');
  a.download = `${safeTitle}_BrandGuard_Clean.txt`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  if (window.showToast) {
    window.showToast('Clean copy downloaded as .txt', 'success');
  }
}
