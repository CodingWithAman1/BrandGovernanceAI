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
  },
  ai_pitch: {
    title: "Autonomous AI Enterprise Product Launch",
    content: "In today's fast-paced digital landscape, our game-changer platform is a testament to technological leadership. We delve into massive datasets to deliver 100% foolproof autonomous brand clearance as the #1 AI engine in the world. Obviously, this miraculous architecture never fails to crush the competition."
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

// =============================================================================
// STUDIO AI CO-PILOT ACTIONS
// =============================================================================

function studioAiHarmonize() {
  const contentEl = document.getElementById('inputContent');
  if (!contentEl || !contentEl.value.trim()) {
    if (window.showToast) window.showToast('Please enter draft text first.', 'warning');
    return;
  }

  const origText = contentEl.value.trim();
  if (window.showToast) window.showToast('Consulting BrandGuard AI Neural Engine...', 'info');

  fetch('/api/v1/ai/harmonize', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ content: origText, voice: 'ENTERPRISE_CONSULTATIVE' })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success && data.harmonized_text) {
      contentEl.value = data.harmonized_text;
      contentEl.style.transition = 'all 0.5s ease';
      contentEl.style.backgroundColor = 'rgba(14, 165, 233, 0.15)';
      setTimeout(() => { contentEl.style.backgroundColor = ''; }, 800);
      
      if (typeof updateCharCount === 'function') updateCharCount();
      if (window.showToast) {
        window.showToast('✨ AI Deep Harmonize complete! Cliches neutralized & tone elevated.', 'success');
      }
    } else {
      if (window.showToast) window.showToast(data.message || 'Harmonization failed.', 'error');
    }
  })
  .catch(err => {
    console.error('AI Harmonize error:', err);
    if (window.showToast) window.showToast('AI service error. Please try again.', 'error');
  });
}

function studioAiSafeHarbor() {
  const contentEl = document.getElementById('inputContent');
  if (!contentEl || !contentEl.value.trim()) {
    if (window.showToast) window.showToast('Please enter draft text first.', 'warning');
    return;
  }

  const origText = contentEl.value.trim();
  if (window.showToast) window.showToast('Generating FTC & SEC Safe Harbor...', 'info');

  fetch('/api/v1/ai/safe-harbor', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ content: origText })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success && data.disclaimer) {
      contentEl.value = `${origText}\n\n---\n**COMPLIANCE DISCLAIMER:**\n${data.disclaimer}`;
      if (typeof updateCharCount === 'function') updateCharCount();
      if (window.showToast) {
        window.showToast('🛡️ FTC Section 5 & SEC Safe Harbor appended!', 'success');
      }
    }
  })
  .catch(err => {
    console.error('Safe Harbor error:', err);
    if (window.showToast) window.showToast('Failed to append disclaimer.', 'error');
  });
}
