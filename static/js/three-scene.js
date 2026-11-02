/**
 * BrandGuard AI — Interactive 3D WebGL Holographic Engine (Three.js)
 * Features:
 * 1. Interactive 3D Holographic Governance Core (Wireframe Icosahedron + Inner Shield + Gyro Rings)
 * 2. Real-Time Mouse Parallax & Inertial Drag-to-Spin Physics
 * 3. Dynamic Orbiting Satellite Nodes with Pulsing Glow
 * 4. Ambient 3D Star/Dust Particle Constellation with Depth of Field
 * 5. Floating Mini 3D Core HUD Widget with Interactive Mode Switching
 */

(function () {
  'use strict';

  // Check if Three.js is available
  if (typeof THREE === 'undefined') {
    console.warn('[BrandGuard 3D] Three.js not loaded. Skipping 3D initialization.');
    return;
  }

  // =========================================================================
  // 1. MAIN 3D HOLOGRAPHIC SCENE BUILDER
  // =========================================================================
  function initHero3DScene(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return null;

    const width = container.clientWidth || 400;
    const height = container.clientHeight || 340;

    // 1. Scene, Camera, Renderer
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    camera.position.z = 8.5;

    const renderer = new THREE.WebGLRenderer({
      alpha: true,
      antialias: true,
      powerPreference: 'high-performance'
    });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.outputEncoding = THREE.sRGBEncoding;

    // Clear previous canvas if any
    container.innerHTML = '';
    container.appendChild(renderer.domElement);

    // 2. Lights
    const ambientLight = new THREE.AmbientLight(0x0f172a, 2.5);
    scene.add(ambientLight);

    const cyanLight = new THREE.PointLight(0x38bdf8, 4, 25);
    cyanLight.position.set(5, 4, 5);
    scene.add(cyanLight);

    const indigoLight = new THREE.PointLight(0x6366f1, 3.5, 25);
    indigoLight.position.set(-5, -4, -4);
    scene.add(indigoLight);

    const emeraldLight = new THREE.PointLight(0x10b981, 2.5, 20);
    emeraldLight.position.set(0, 6, -3);
    scene.add(emeraldLight);

    // 3. Holographic Core Group
    const coreGroup = new THREE.Group();
    scene.add(coreGroup);

    // --- Inner Faceted Core (Glowing Polyhedron) ---
    const innerGeom = new THREE.IcosahedronGeometry(1.6, 0);
    const innerMat = new THREE.MeshPhysicalMaterial({
      color: 0x0f172a,
      emissive: 0x1e293b,
      roughness: 0.2,
      metalness: 0.8,
      clearcoat: 1.0,
      clearcoatRoughness: 0.1,
      wireframe: false,
      transparent: true,
      opacity: 0.85
    });
    const innerCore = new THREE.Mesh(innerGeom, innerMat);
    coreGroup.add(innerCore);

    // --- Outer Wireframe Cage (Electric Cyan) ---
    const wireGeom = new THREE.IcosahedronGeometry(1.95, 1);
    const wireMat = new THREE.MeshBasicMaterial({
      color: 0x38bdf8,
      wireframe: true,
      transparent: true,
      opacity: 0.65
    });
    const wireCore = new THREE.Mesh(wireGeom, wireMat);
    coreGroup.add(wireCore);

    // --- Core Vertices Glow Spheres ---
    const vertexGroup = new THREE.Group();
    const posAttr = wireGeom.attributes.position;
    const vertexSpheres = [];
    const vDotGeom = new THREE.SphereGeometry(0.045, 8, 8);
    const vDotMat = new THREE.MeshBasicMaterial({ color: 0x67e8f9 });

    for (let i = 0; i < posAttr.count; i += 3) {
      const vDot = new THREE.Mesh(vDotGeom, vDotMat);
      vDot.position.set(posAttr.getX(i), posAttr.getY(i), posAttr.getZ(i));
      vertexGroup.add(vDot);
      vertexSpheres.push(vDot);
    }
    coreGroup.add(vertexGroup);

    // --- Gyroscopic Orbital Rings ---
    // Ring 1: Primary Equatorial Ring
    const ring1Geom = new THREE.TorusGeometry(2.7, 0.025, 16, 100);
    const ring1Mat = new THREE.MeshBasicMaterial({
      color: 0x38bdf8,
      transparent: true,
      opacity: 0.75
    });
    const ring1 = new THREE.Mesh(ring1Geom, ring1Mat);
    ring1.rotation.x = Math.PI / 3;
    ring1.rotation.y = Math.PI / 6;
    coreGroup.add(ring1);

    // Ring 2: Polar Gyro Ring (Indigo / Violet)
    const ring2Geom = new THREE.TorusGeometry(3.1, 0.02, 16, 100);
    const ring2Mat = new THREE.MeshBasicMaterial({
      color: 0x818cf8,
      transparent: true,
      opacity: 0.65
    });
    const ring2 = new THREE.Mesh(ring2Geom, ring2Mat);
    ring2.rotation.x = -Math.PI / 4;
    ring2.rotation.z = Math.PI / 5;
    coreGroup.add(ring2);

    // Ring 3: Outer Precision Horizon Ring (Dotted/Dashed effect)
    const ring3Geom = new THREE.TorusGeometry(3.5, 0.015, 12, 80);
    const ring3Mat = new THREE.MeshBasicMaterial({
      color: 0x34d399,
      transparent: true,
      opacity: 0.45
    });
    const ring3 = new THREE.Mesh(ring3Geom, ring3Mat);
    ring3.rotation.y = Math.PI / 2.5;
    coreGroup.add(ring3);

    // --- Orbiting Satellite Compliance Nodes ---
    const satelliteGroup = new THREE.Group();
    coreGroup.add(satelliteGroup);

    const satellites = [
      { radius: 2.7, speed: 1.2, offset: 0, color: 0x38bdf8, size: 0.09, label: 'FTC' },
      { radius: 2.7, speed: 1.2, offset: Math.PI, color: 0x06b6d4, size: 0.08, label: 'WCAG' },
      { radius: 3.1, speed: -0.9, offset: Math.PI / 2, color: 0xa855f7, size: 0.09, label: 'TONE' },
      { radius: 3.5, speed: 0.7, offset: Math.PI / 3, color: 0x10b981, size: 0.08, label: 'SEC' }
    ];

    const satMeshes = satellites.map(s => {
      const g = new THREE.SphereGeometry(s.size, 12, 12);
      const m = new THREE.MeshBasicMaterial({ color: s.color });
      const mesh = new THREE.Mesh(g, m);
      satelliteGroup.add(mesh);
      return { config: s, mesh };
    });

    // --- 3D Floating Particle Constellation ---
    const particlesCount = 140;
    const particleGeometry = new THREE.BufferGeometry();
    const particlePositions = new Float32Array(particlesCount * 3);
    const particleColors = new Float32Array(particlesCount * 3);

    const palette = [
      new THREE.Color(0x38bdf8), // Cyan
      new THREE.Color(0x6366f1), // Indigo
      new THREE.Color(0xa855f7), // Purple
      new THREE.Color(0x10b981)  // Emerald
    ];

    for (let i = 0; i < particlesCount; i++) {
      const pIndex = i * 3;
      // Distribute randomly in a 3D sphere volume
      const r = 2.5 + Math.random() * 5.0;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(Math.random() * 2 - 1);

      particlePositions[pIndex] = r * Math.sin(phi) * Math.cos(theta);
      particlePositions[pIndex + 1] = r * Math.sin(phi) * Math.sin(theta);
      particlePositions[pIndex + 2] = r * Math.cos(phi);

      const col = palette[Math.floor(Math.random() * palette.length)];
      particleColors[pIndex] = col.r;
      particleColors[pIndex + 1] = col.g;
      particleColors[pIndex + 2] = col.b;
    }

    particleGeometry.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
    particleGeometry.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));

    const particleMaterial = new THREE.PointsMaterial({
      size: 0.07,
      vertexColors: true,
      transparent: true,
      opacity: 0.75,
      blending: THREE.AdditiveBlending
    });

    const particleSystem = new THREE.Points(particleGeometry, particleMaterial);
    scene.add(particleSystem);

    // =========================================================================
    // 4. INTERACTION & MOUSE PARALLAX / DRAG PHYSICS
    // =========================================================================
    let targetRotationX = 0;
    let targetRotationY = 0;
    let mouseX = 0;
    let mouseY = 0;
    let isDragging = false;
    let previousMousePosition = { x: 0, y: 0 };
    let dragVelocity = { x: 0, y: 0 };

    // Mouse movement parallax (passive non-blocking)
    window.addEventListener('mousemove', (e) => {
      const normX = (e.clientX / window.innerWidth) * 2 - 1;
      const normY = (e.clientY / window.innerHeight) * 2 - 1;
      mouseX = normX * 0.45;
      mouseY = normY * 0.35;
    }, { passive: true });

    // Drag to spin on the container
    container.style.cursor = 'grab';

    container.addEventListener('mousedown', (e) => {
      isDragging = true;
      container.style.cursor = 'grabbing';
      previousMousePosition = { x: e.clientX, y: e.clientY };
    });

    window.addEventListener('mouseup', () => {
      if (isDragging) {
        isDragging = false;
        container.style.cursor = 'grab';
      }
    });

    window.addEventListener('mousemove', (e) => {
      if (!isDragging) return;
      const deltaX = e.clientX - previousMousePosition.x;
      const deltaY = e.clientY - previousMousePosition.y;

      dragVelocity.x = deltaX * 0.005;
      dragVelocity.y = deltaY * 0.005;

      coreGroup.rotation.y += dragVelocity.x;
      coreGroup.rotation.x += dragVelocity.y;

      previousMousePosition = { x: e.clientX, y: e.clientY };
    });

    // Touch support for mobile devices
    container.addEventListener('touchstart', (e) => {
      if (e.touches.length === 1) {
        isDragging = true;
        previousMousePosition = { x: e.touches[0].clientX, y: e.touches[0].clientY };
      }
    }, { passive: true });

    window.addEventListener('touchend', () => { isDragging = false; });

    window.addEventListener('touchmove', (e) => {
      if (!isDragging || e.touches.length !== 1) return;
      const deltaX = e.touches[0].clientX - previousMousePosition.x;
      const deltaY = e.touches[0].clientY - previousMousePosition.y;
      coreGroup.rotation.y += deltaX * 0.006;
      coreGroup.rotation.x += deltaY * 0.006;
      previousMousePosition = { x: e.touches[0].clientX, y: e.touches[0].clientY };
    }, { passive: true });

    // Handle container resize
    const resizeObserver = new ResizeObserver(() => {
      const newWidth = container.clientWidth;
      const newHeight = container.clientHeight;
      if (newWidth && newHeight) {
        camera.aspect = newWidth / newHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(newWidth, newHeight);
      }
    });
    resizeObserver.observe(container);

    // =========================================================================
    // 5. ANIMATION LOOP (60 FPS WITH DAMPING & LEVITATION)
    // =========================================================================
    let clock = new THREE.Clock();
    let animId;

    function animate() {
      animId = requestAnimationFrame(animate);

      if (document.hidden) return;

      const elapsedTime = clock.getElapsedTime();

      // Autonomous Gyroscopic Rotation
      if (!isDragging) {
        // Natural rotation
        coreGroup.rotation.y += 0.004;
        coreGroup.rotation.x += 0.002;

        // Apply mouse parallax smoothly with damping
        targetRotationY = mouseX * 0.8;
        targetRotationX = mouseY * 0.6;
        coreGroup.rotation.y += (targetRotationY - coreGroup.rotation.y) * 0.02;
        coreGroup.rotation.x += (targetRotationX - coreGroup.rotation.x) * 0.02;

        // Apply residual drag inertia
        dragVelocity.x *= 0.95;
        dragVelocity.y *= 0.95;
        coreGroup.rotation.y += dragVelocity.x;
        coreGroup.rotation.x += dragVelocity.y;
      }

      // Floating / Levitation sine wave
      coreGroup.position.y = Math.sin(elapsedTime * 1.5) * 0.18;

      // Independent Orbital Ring Rotations
      ring1.rotation.z += 0.012;
      ring2.rotation.y -= 0.015;
      ring3.rotation.x += 0.008;

      // Inner Core Pulse
      const scalePulse = 1.0 + Math.sin(elapsedTime * 2.5) * 0.035;
      innerCore.scale.set(scalePulse, scalePulse, scalePulse);

      // Rotate Satellites on Ring Trajectories
      satMeshes.forEach(sat => {
        const angle = elapsedTime * sat.config.speed + sat.config.offset;
        sat.mesh.position.x = Math.cos(angle) * sat.config.radius;
        sat.mesh.position.z = Math.sin(angle) * sat.config.radius;
        sat.mesh.position.y = Math.sin(angle * 1.5) * 0.4;
      });

      // Slowly rotate the particle constellation field in reverse
      particleSystem.rotation.y = -elapsedTime * 0.02;
      particleSystem.rotation.x = Math.sin(elapsedTime * 0.015) * 0.05;

      // Pulse light intensity subtly
      cyanLight.intensity = 3.5 + Math.sin(elapsedTime * 3) * 0.8;

      renderer.render(scene, camera);
    }

    animate();

    return {
      destroy: () => {
        cancelAnimationFrame(animId);
        resizeObserver.disconnect();
        renderer.dispose();
      },
      setTheme: (theme) => {
        if (theme === 'admin') {
          wireMat.color.setHex(0xef4444);
          ring1Mat.color.setHex(0xf87171);
          cyanLight.color.setHex(0xef4444);
        } else if (theme === 'reviewer') {
          wireMat.color.setHex(0xf59e0b);
          ring1Mat.color.setHex(0xfbbf24);
          cyanLight.color.setHex(0xf59e0b);
        } else {
          wireMat.color.setHex(0x38bdf8);
          ring1Mat.color.setHex(0x38bdf8);
          cyanLight.color.setHex(0x38bdf8);
        }
      }
    };
  }

  // =========================================================================
  // 6. MINI 3D CORE FLOATING HUD WIDGET (BOTTOM CORNER)
  // =========================================================================
  function initMiniFloatingCore() {
    // Only on desktop
    if (!window.matchMedia('(min-width: 992px)').matches) return;

    let miniContainer = document.getElementById('brandguard-mini-3d-hud');
    if (!miniContainer) {
      miniContainer = document.createElement('div');
      miniContainer.id = 'brandguard-mini-3d-hud';
      miniContainer.className = 'mini-3d-hud-container';
      miniContainer.innerHTML = `
        <div class="mini-3d-hud-card" title="BrandGuard 3D Holographic Core (Interactive)">
          <div class="mini-3d-canvas-wrap" id="mini3DCanvas"></div>
          <div class="mini-3d-hud-label">
            <span class="pulse-dot pulse-dot-cyan me-1"></span>
            <span class="hud-tag">3D CORE</span>
          </div>
          <div class="mini-3d-hud-stats">
            <span class="hud-stat-item">60 FPS</span> &bull;
            <span class="hud-stat-item text-cyan">GYRO: ON</span>
          </div>
        </div>
      `;
      document.body.appendChild(miniContainer);
    }

    const canvasWrap = document.getElementById('mini3DCanvas');
    if (!canvasWrap) return;

    // Small WebGL scene (80x80)
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
    camera.position.z = 4.8;

    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(76, 76);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    canvasWrap.appendChild(renderer.domElement);

    // Small Icosahedron + Ring
    const geom = new THREE.IcosahedronGeometry(1.0, 1);
    const mat = new THREE.MeshBasicMaterial({ color: 0x38bdf8, wireframe: true, transparent: true, opacity: 0.85 });
    const mesh = new THREE.Mesh(geom, mat);
    scene.add(mesh);

    const ringGeom = new THREE.TorusGeometry(1.5, 0.025, 8, 48);
    const ringMat = new THREE.MeshBasicMaterial({ color: 0x818cf8, transparent: true, opacity: 0.6 });
    const ring = new THREE.Mesh(ringGeom, ringMat);
    ring.rotation.x = Math.PI / 3;
    scene.add(ring);

    // Mini animation
    function miniAnimate() {
      requestAnimationFrame(miniAnimate);
      if (document.hidden) return;
      mesh.rotation.y += 0.015;
      mesh.rotation.x += 0.008;
      ring.rotation.z -= 0.02;
      renderer.render(scene, camera);
    }
    miniAnimate();

    // Click on mini core triggers a cool 3D burst toast / status inspection
    miniContainer.addEventListener('click', () => {
      mesh.scale.set(1.3, 1.3, 1.3);
      setTimeout(() => mesh.scale.set(1.0, 1.0, 1.0), 300);
      if (window.showToast) {
        window.showToast('🛡️ 3D Neural Governance Core Active & Synchronized', 'info');
      }
    });
  }

  // =========================================================================
  // 7. AUTO-INITIALIZE ON DOM READY
  // =========================================================================
  document.addEventListener('DOMContentLoaded', () => {
    // Check for hero 3D container
    const heroTarget = document.getElementById('brandguard-hero-3d');
    if (heroTarget) {
      window.brandGuardHero3D = initHero3DScene('brandguard-hero-3d');
    }

    // Initialize floating corner HUD
    initMiniFloatingCore();
  });

})();
