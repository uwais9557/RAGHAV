/* ============================================================
   TALENT FINDER - Main JavaScript
   Animations, interactions, dark mode, upload handling
   ============================================================ */

// ── Document Ready ──────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initNavbar();
  initUploadZone();
  initAnimations();
  initCounters();
  initParticles();
  initProgressBars();
  initCharts();
});

// ── Theme (Dark/Light Mode) ─────────────────────────────────────────────────
function initTheme() {
  const stored = localStorage.getItem('tf_theme') || 'dark';
  applyTheme(stored);

  document.querySelectorAll('.theme-toggle').forEach(btn => {
    btn.addEventListener('click', () => {
      const current = document.body.classList.contains('light-mode') ? 'light' : 'dark';
      const next = current === 'dark' ? 'light' : 'dark';
      applyTheme(next);
      localStorage.setItem('tf_theme', next);
    });
  });
}

function applyTheme(theme) {
  if (theme === 'light') {
    document.body.classList.add('light-mode');
    document.querySelectorAll('.theme-toggle i').forEach(i => {
      i.className = 'fas fa-moon';
    });
  } else {
    document.body.classList.remove('light-mode');
    document.querySelectorAll('.theme-toggle i').forEach(i => {
      i.className = 'fas fa-sun';
    });
  }
}

// ── Navbar ──────────────────────────────────────────────────────────────────
function initNavbar() {
  const navbar = document.querySelector('.navbar-custom');
  if (!navbar) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      navbar.style.background = 'rgba(13, 14, 26, 0.95)';
      navbar.style.boxShadow = '0 4px 30px rgba(0,0,0,0.3)';
    } else {
      navbar.style.background = 'rgba(13, 14, 26, 0.8)';
      navbar.style.boxShadow = 'none';
    }
  });

  // Active link detection
  const links = document.querySelectorAll('.navbar-nav .nav-link');
  const current = window.location.pathname;
  links.forEach(link => {
    if (link.getAttribute('href') === current) {
      link.classList.add('active');
    }
  });
}

// ── Upload Zone ─────────────────────────────────────────────────────────────
function initUploadZone() {
  const zone = document.getElementById('uploadZone');
  const fileInput = document.getElementById('resumeFile');
  const fileNameDisplay = document.getElementById('fileNameDisplay');
  const uploadForm = document.getElementById('uploadForm');

  if (!zone || !fileInput) return;

  // Click to browse
  zone.addEventListener('click', () => fileInput.click());

  // Drag & Drop
  zone.addEventListener('dragover', e => {
    e.preventDefault();
    zone.classList.add('drag-over');
  });

  zone.addEventListener('dragleave', () => zone.classList.remove('drag-over'));

  zone.addEventListener('drop', e => {
    e.preventDefault();
    zone.classList.remove('drag-over');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      fileInput.files = files;
      handleFileSelect(files[0]);
    }
  });

  // File selection
  fileInput.addEventListener('change', e => {
    if (e.target.files.length > 0) {
      handleFileSelect(e.target.files[0]);
    }
  });

  // Form submit with loading
  if (uploadForm) {
    uploadForm.addEventListener('submit', e => {
      if (!fileInput.files.length) {
        e.preventDefault();
        showToast('Please select a resume file first!', 'warning');
        return;
      }
      showLoadingOverlay();
    });
  }
}

function handleFileSelect(file) {
  const allowed = ['pdf', 'docx', 'doc', 'txt', 'png', 'jpg', 'jpeg'];
  const ext = file.name.split('.').pop().toLowerCase();

  if (!allowed.includes(ext)) {
    showToast(`Unsupported format: .${ext}. Please use PDF, DOCX, TXT, or Image files.`, 'danger');
    return;
  }

  if (file.size > 10 * 1024 * 1024) {
    showToast('File too large! Maximum size is 10MB.', 'danger');
    return;
  }

  // Update UI
  const zone = document.getElementById('uploadZone');
  const display = document.getElementById('fileNameDisplay');

  if (display) {
    display.innerHTML = `
      <div class="d-flex align-items-center gap-2 justify-content-center mt-3">
        <i class="fas fa-file-${getFileIcon(ext)} text-gradient" style="font-size:1.5rem;"></i>
        <div>
          <div style="font-weight:600; color: var(--text);">${file.name}</div>
          <div style="font-size:0.8rem; color: var(--text-muted);">${formatFileSize(file.size)}</div>
        </div>
        <i class="fas fa-check-circle text-accent" style="font-size:1.2rem;"></i>
      </div>`;
  }

  if (zone) {
    zone.style.borderColor = 'var(--accent)';
    zone.style.background = 'rgba(67,233,123,0.05)';
  }

  showToast(`✅ File selected: ${file.name}`, 'success');
}

function getFileIcon(ext) {
  const icons = { pdf: 'pdf', docx: 'word', doc: 'word', txt: 'alt', png: 'image', jpg: 'image', jpeg: 'image' };
  return icons[ext] || 'alt';
}

function formatFileSize(bytes) {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

// ── Loading Overlay ──────────────────────────────────────────────────────────
function showLoadingOverlay() {
  let overlay = document.getElementById('loadingOverlay');
  if (!overlay) {
    overlay = document.createElement('div');
    overlay.id = 'loadingOverlay';
    overlay.innerHTML = `
      <div class="loader-ring"></div>
      <div class="loader-text text-gradient">Analyzing Your Resume...</div>
      <div class="loader-steps" id="loaderSteps">
        <div>⚡ Extracting text from document...</div>
      </div>`;
    document.body.appendChild(overlay);
  }

  overlay.style.display = 'flex';
  document.body.style.overflow = 'hidden';

  // Simulated steps
  const steps = [
    '⚡ Extracting text from document...',
    '🔍 Detecting skills & technologies...',
    '🧠 Running AI analysis...',
    '📊 Calculating ATS score...',
    '🎯 Matching with job opportunities...',
    '✅ Finalizing recommendations...',
  ];

  let i = 0;
  const stepsEl = overlay.querySelector('#loaderSteps');
  const interval = setInterval(() => {
    if (i < steps.length && stepsEl) {
      stepsEl.innerHTML += `<div style="opacity:0;animation:fadeIn 0.4s ease forwards">${steps[i]}</div>`;
      i++;
    } else {
      clearInterval(interval);
    }
  }, 1200);
}

// ── Animations (Intersection Observer) ─────────────────────────────────────
function initAnimations() {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.animation = 'slideUp 0.6s ease forwards';
        entry.target.style.opacity = '1';
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

  document.querySelectorAll('.animate-on-scroll').forEach(el => {
    el.style.opacity = '0';
    observer.observe(el);
  });
}

// ── Counter Animation ────────────────────────────────────────────────────────
function initCounters() {
  const counters = document.querySelectorAll('[data-count]');
  if (!counters.length) return;

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  counters.forEach(counter => observer.observe(counter));
}

function animateCounter(el) {
  const target = parseInt(el.getAttribute('data-count'));
  const duration = 1500;
  const start = performance.now();

  function update(time) {
    const elapsed = time - start;
    const progress = Math.min(elapsed / duration, 1);
    const value = Math.round(progress * target * (2 - progress)); // ease out
    el.textContent = value.toLocaleString() + (el.getAttribute('data-suffix') || '');
    if (progress < 1) requestAnimationFrame(update);
  }
  requestAnimationFrame(update);
}

// ── Progress Bars ────────────────────────────────────────────────────────────
function initProgressBars() {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const fill = entry.target.querySelector('.progress-fill');
        const width = entry.target.getAttribute('data-width');
        if (fill && width) {
          setTimeout(() => { fill.style.width = width + '%'; }, 100);
        }
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.3 });

  document.querySelectorAll('.progress-bar-custom').forEach(bar => observer.observe(bar));
}

// ── Particle Background ──────────────────────────────────────────────────────
function initParticles() {
  const canvas = document.getElementById('particleCanvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  let particles = [];
  const count = window.innerWidth < 768 ? 30 : 60;

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }

  class Particle {
    constructor() { this.reset(); }
    reset() {
      this.x = Math.random() * canvas.width;
      this.y = Math.random() * canvas.height;
      this.size = Math.random() * 2 + 0.5;
      this.speedX = (Math.random() - 0.5) * 0.3;
      this.speedY = (Math.random() - 0.5) * 0.3;
      this.opacity = Math.random() * 0.5 + 0.1;
      this.color = Math.random() > 0.5 ? '108, 99, 255' : '255, 101, 132';
    }
    update() {
      this.x += this.speedX;
      this.y += this.speedY;
      if (this.x < 0 || this.x > canvas.width || this.y < 0 || this.y > canvas.height) {
        this.reset();
      }
    }
    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${this.color}, ${this.opacity})`;
      ctx.fill();
    }
  }

  resize();
  window.addEventListener('resize', resize);
  for (let i = 0; i < count; i++) particles.push(new Particle());

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach(p => { p.update(); p.draw(); });

    // Draw connections
    particles.forEach((p1, i) => {
      particles.slice(i + 1).forEach(p2 => {
        const dist = Math.hypot(p1.x - p2.x, p1.y - p2.y);
        if (dist < 120) {
          ctx.beginPath();
          ctx.strokeStyle = `rgba(108, 99, 255, ${0.1 * (1 - dist/120)})`;
          ctx.lineWidth = 0.5;
          ctx.moveTo(p1.x, p1.y);
          ctx.lineTo(p2.x, p2.y);
          ctx.stroke();
        }
      });
    });

    requestAnimationFrame(animate);
  }
  animate();
}

// ── Charts ───────────────────────────────────────────────────────────────────
function initCharts() {
  initSkillsChart();
  initScoreGauge();
}

function initSkillsChart() {
  const canvas = document.getElementById('skillsChart');
  if (!canvas || typeof Chart === 'undefined') return;

  const rawData = canvas.getAttribute('data-skills');
  if (!rawData) return;

  try {
    const data = JSON.parse(rawData);
    const labels = Object.keys(data).map(k => k.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase()));
    const values = Object.values(data);

    new Chart(canvas, {
      type: 'doughnut',
      data: {
        labels,
        datasets: [{
          data: values,
          backgroundColor: [
            'rgba(108,99,255,0.8)',
            'rgba(255,101,132,0.8)',
            'rgba(67,233,123,0.8)',
            'rgba(56,249,215,0.8)',
            'rgba(255,165,0,0.8)',
            'rgba(135,206,235,0.8)',
            'rgba(255,215,0,0.8)',
          ],
          borderColor: 'transparent',
          borderWidth: 0,
          hoverOffset: 8,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        cutout: '70%',
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              color: getComputedStyle(document.documentElement).getPropertyValue('--text') || '#E8E9F3',
              padding: 15,
              font: { size: 11, family: 'Inter' },
              boxWidth: 12,
              boxHeight: 12,
            },
          },
          tooltip: {
            backgroundColor: 'rgba(21,22,39,0.95)',
            titleColor: '#E8E9F3',
            bodyColor: '#7B7FA8',
            borderColor: 'rgba(108,99,255,0.3)',
            borderWidth: 1,
            padding: 12,
          },
        },
      },
    });
  } catch(e) {
    console.warn('Skills chart init failed', e);
  }
}

function initScoreGauge() {
  const canvas = document.getElementById('scoreGauge');
  if (!canvas || typeof Chart === 'undefined') return;

  const score = parseInt(canvas.getAttribute('data-score') || 0);
  const color = score >= 70 ? '#43E97B' : score >= 40 ? '#FFD700' : '#FF6584';

  new Chart(canvas, {
    type: 'doughnut',
    data: {
      datasets: [{
        data: [score, 100 - score],
        backgroundColor: [color, 'rgba(255,255,255,0.05)'],
        borderColor: 'transparent',
        borderWidth: 0,
      }],
    },
    options: {
      responsive: true,
      cutout: '78%',
      rotation: -90,
      circumference: 180,
      plugins: { legend: { display: false }, tooltip: { enabled: false } },
    },
  });
}

// ── Toast Notifications ───────────────────────────────────────────────────────
function showToast(message, type = 'info') {
  const colors = {
    success: { bg: 'rgba(67,233,123,0.15)', border: 'rgba(67,233,123,0.4)', icon: 'fa-check-circle', color: '#43E97B' },
    danger:  { bg: 'rgba(255,101,132,0.15)', border: 'rgba(255,101,132,0.4)', icon: 'fa-times-circle', color: '#FF6584' },
    warning: { bg: 'rgba(255,165,0,0.15)', border: 'rgba(255,165,0,0.4)', icon: 'fa-exclamation-circle', color: 'orange' },
    info:    { bg: 'rgba(108,99,255,0.15)', border: 'rgba(108,99,255,0.4)', icon: 'fa-info-circle', color: '#8B84FF' },
  };
  const c = colors[type] || colors.info;

  let container = document.getElementById('toastContainer');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toastContainer';
    container.style.cssText = 'position:fixed;top:80px;right:20px;z-index:9998;display:flex;flex-direction:column;gap:10px;';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.style.cssText = `
    background: ${c.bg};
    border: 1px solid ${c.border};
    border-radius: 12px;
    padding: 0.85rem 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-size: 0.9rem;
    max-width: 360px;
    backdrop-filter: blur(10px);
    animation: slideDown 0.3s ease forwards;
    font-family: Inter, sans-serif;
    color: var(--text, #E8E9F3);
  `;
  toast.innerHTML = `<i class="fas ${c.icon}" style="color:${c.color}"></i><span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.animation = 'slideUp 0.3s ease reverse forwards';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

// ── Job Search (AJAX) ────────────────────────────────────────────────────────
function initJobSearch() {
  const searchInput = document.getElementById('jobSearchInput');
  if (!searchInput) return;

  let debounceTimer;
  searchInput.addEventListener('input', () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      const query = searchInput.value.trim();
      if (query.length > 1) {
        fetch(`/api/jobs/search/?q=${encodeURIComponent(query)}`)
          .then(r => r.json())
          .then(data => {
            console.log('Search results:', data.jobs);
          });
      }
    }, 300);
  });
}

// ── Expose globally ──────────────────────────────────────────────────────────
window.showToast = showToast;
window.showLoadingOverlay = showLoadingOverlay;
