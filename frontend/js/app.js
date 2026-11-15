/**
 * Global Malnutrition Pattern Simulator
 * Pure Vanilla JavaScript (Zero build step, Zero dependencies)
 * Reads empirical World Bank / UNICEF data directly from window.RESULTS
 */

(function () {
  'use strict';

  // Cluster Color Palette (High contrast in both Light & Dark modes)
  const PALETTE = [
    '#e11d48', // Cluster 0: Rose (Severe Undernutrition)
    '#0284c7', // Cluster 1: Sky / Cyan (High Overweight & Obesity)
    '#059669', // Cluster 2: Emerald (Moderate Undernutrition / Transitional)
    '#d97706', // Cluster 3: Amber (Double Burden)
    '#7c3aed', // Cluster 4: Violet
    '#db2777', // Cluster 5: Pink
    '#2563eb', // Cluster 6: Blue
    '#65a30d'  // Cluster 7: Lime
  ];

  // Indicator Slider Configurations
  const INDICATOR_CONFIGS = [
    { key: 'stunting', label: 'Child Stunting', min: 0, max: 60, step: 0.5, unit: '%', category: 'Child Undernutrition', defaultVal: 22.5 },
    { key: 'wasting', label: 'Child Wasting', min: 0, max: 25, step: 0.2, unit: '%', category: 'Child Undernutrition', defaultVal: 5.4 },
    { key: 'underweight', label: 'Child Underweight', min: 0, max: 40, step: 0.5, unit: '%', category: 'Child Undernutrition', defaultVal: 12.8 },
    { key: 'undernourishment', label: 'Undernourishment', min: 0, max: 55, step: 0.5, unit: '%', category: 'Child Undernutrition', defaultVal: 11.0 },
    { key: 'anaemia_children', label: 'Child Anaemia', min: 0, max: 85, step: 0.5, unit: '%', category: 'Micronutrient Deficit', defaultVal: 41.5 },
    { key: 'anaemia_women', label: 'Women Anaemia', min: 0, max: 70, step: 0.5, unit: '%', category: 'Micronutrient Deficit', defaultVal: 28.5 },
    { key: 'exclusive_breastfeeding', label: 'Exclusive Breastfeeding', min: 0, max: 90, step: 0.5, unit: '%', category: 'Protective Factor', defaultVal: 45.0 },
    { key: 'child_overweight', label: 'Child Overweight', min: 0, max: 30, step: 0.2, unit: '%', category: 'Overnutrition Burden', defaultVal: 5.8 },
    { key: 'adult_obesity', label: 'Adult Obesity', min: 0, max: 60, step: 0.5, unit: '%', category: 'Overnutrition Burden', defaultVal: 18.5 }
  ];

  // Targeted Strategic Interventions to Achieve the Project Goal
  const TARGETED_INTERVENTIONS = {
    0: {
      title: 'Cluster 0 Strategy: Acute Therapeutic Relief & Child Survival',
      icon: '🚨 🍼',
      badge: 'Acute Child Undernutrition Action',
      badgeColor: '#e11d48',
      actions: [
        'Scale up Ready-to-Use Therapeutic Food (RUTF) community distribution for acute child wasting.',
        'Deploy universal maternal iron-folic acid and infant high-dose Vitamin A supplementation programs.',
        'Invest in localized community WASH (clean water, sanitation) infrastructure to break chronic diarrheal stunting cycles.'
      ]
    },
    1: {
      title: 'Cluster 1 Strategy: Metabolic Morbidity Prevention & Food Systems Regulation',
      icon: '⚡ 🥗',
      badge: 'Overnutrition & NCD Mitigation',
      badgeColor: '#0284c7',
      actions: [
        'Enforce mandatory Front-of-Pack warning labels (black octagons) on ultra-processed high-sugar/sodium foods.',
        'Implement tiered excise taxation on Sugar-Sweetened Beverages (SSBs) to shift population consumption.',
        'Integrate adult primary care routine screening for early metabolic risk (hypertension, HbA1c, cardiovascular).'
      ]
    },
    2: {
      title: 'Cluster 2 Strategy: Dual-Duty Interventions & Nutritional Safety Nets',
      icon: '⚖️ 🌾',
      badge: 'Transitional Vulnerability Action',
      badgeColor: '#059669',
      actions: [
        'Dual-duty food assistance: replace calorie-only grain subsidies with diversified nutrient-dense rations.',
        'Biofortification of national staple grains (iron-pearl millet, zinc-wheat, vitamin-A orange sweet potato).',
        'Mandatory workplace maternity protection and nursing facilities to protect the 6-month exclusive breastfeeding window.'
      ]
    },
    3: {
      title: 'Cluster 3 Strategy: Dual-Burden Coexistence Package (K=4 Solution)',
      icon: '⚖️ 🍎',
      badge: 'Double Burden Action',
      badgeColor: '#d97706',
      actions: [
        'Life-course preventive packages: prevent child stunting without accelerating rapid childhood adiposity.',
        'School nutrition standards prohibiting junk food marketing while supplying fresh whole local foods.',
        'Targeted maternal metabolic monitoring during prenatal care to prevent gestational diabetes and low birth weight.'
      ]
    }
  };

  // Archetype Presets for What-If Policy Simulation
  const TYPOLOGY_PRESETS = {
    sub_saharan: {
      name: 'Severe Undernutrition (e.g. Niger, Chad, South Sudan)',
      values: {
        stunting: 38.5,
        wasting: 8.8,
        underweight: 22.0,
        undernourishment: 24.5,
        anaemia_children: 68.0,
        anaemia_women: 46.0,
        exclusive_breastfeeding: 52.0,
        child_overweight: 3.2,
        adult_obesity: 6.5
      }
    },
    double_burden: {
      name: 'Double Burden (e.g. India, Egypt, Guatemala)',
      values: {
        stunting: 31.5,
        wasting: 3.8,
        underweight: 12.5,
        undernourishment: 11.2,
        anaemia_children: 38.0,
        anaemia_women: 28.5,
        exclusive_breastfeeding: 35.0,
        child_overweight: 9.8,
        adult_obesity: 26.5
      }
    },
    high_obesity: {
      name: 'High Obesity (e.g. USA, UK, Mexico, Chile)',
      values: {
        stunting: 4.8,
        wasting: 1.2,
        underweight: 2.1,
        undernourishment: 3.2,
        anaemia_children: 12.5,
        anaemia_women: 15.0,
        exclusive_breastfeeding: 24.0,
        child_overweight: 12.8,
        adult_obesity: 34.5
      }
    },
    low_burden: {
      name: 'Low Malnutrition (e.g. Japan, Norway, Sweden)',
      values: {
        stunting: 5.5,
        wasting: 1.8,
        underweight: 2.2,
        undernourishment: 3.8,
        anaemia_children: 14.0,
        anaemia_women: 16.0,
        exclusive_breastfeeding: 62.0,
        child_overweight: 4.8,
        adult_obesity: 16.5
      }
    }
  };

  // Application State
  let state = {
    results: null,
    activeDistance: 'euclidean',
    activeK: 3,
    showLoadings: true,
    searchTerm: '',
    selectedRegion: 'all',
    simulatedValues: {},
    simulatedCoords: { x: 0, y: 0 },
    simulatedCluster: 0,
    activeCountryIso: null,
    // Auto transition simulation
    isAutoSimulating: false,
    autoSimTimer: null,
    autoSimStep: 0,
    // K Progression
    isPlayingProgression: false,
    progressionTimer: null
  };

  function getThemeColors() {
    const isDark = document.body.classList.contains('dark-theme');
    return {
      isDark,
      grid: isDark ? '#1e293b' : '#e2e8f0',
      axisText: isDark ? '#94a3b8' : '#64748b',
      labelText: isDark ? '#cbd5e1' : '#334155',
      mainText: isDark ? '#f8fafc' : '#0f172a',
      cardBorder: isDark ? 'rgba(255, 255, 255, 0.08)' : '#e2e8f0',
      zeroAxis: isDark ? '#334155' : '#cbd5e1',
      simStarFill: '#f59e0b'
    };
  }

  document.addEventListener('DOMContentLoaded', initApp);

  function initApp() {
    if (!window.RESULTS) {
      console.error('Fatal: window.RESULTS is undefined. Ensure data/results.js is loaded.');
      showErrorState('Results data not found. Please ensure backend/run_pipeline.py has run.');
      return;
    }

    state.results = window.RESULTS;
    state.activeDistance = state.results.metadata.selected_distance || 'euclidean';
    state.activeK = state.results.metadata.selected_k || 3;

    // Initialize simulated values with dataset mean
    const mean = state.results.scaler ? state.results.scaler.mean : {};
    INDICATOR_CONFIGS.forEach(ind => {
      state.simulatedValues[ind.key] = mean[ind.key] !== undefined ? Math.round(mean[ind.key] * 10) / 10 : ind.defaultVal;
    });

    // Demo banner check
    if (state.results.metadata.is_demo) {
      const banner = document.getElementById('demoBanner');
      if (banner) banner.classList.add('visible');
    }

    populateCountrySelect();
    renderSimulatorSliders();
    setupSimulationControls();
    setupModelSwitchers();
    setupPCAControls();
    setupPipelineDrawer();
    setupThemeToggle();
    setupStepCardInteractions();

    // Initial inference & plot render
    updateSimulator();
    renderPCAExplorer();
  }

  function showErrorState(msg) {
    const main = document.querySelector('main');
    if (main) {
      main.innerHTML = `<div class="glass-card" style="margin: 4rem auto; max-width: 600px; text-align: center; border-color: var(--rose-accent);">
        <h2 style="color: var(--rose-accent); margin-bottom: 1rem;">Data Loading Error</h2>
        <p style="color: var(--text-muted);">${msg}</p>
      </div>`;
    }
  }

  // ============================================================================
  // 1. Country Quick Selector (166 Sovereign Nations)
  // ============================================================================
  function populateCountrySelect() {
    const select = document.getElementById('countrySelect');
    if (!select || !state.results.countries) return;

    // Sort countries alphabetically by name
    const sorted = [...state.results.countries].sort((a, b) => a.country_name.localeCompare(b.country_name));

    select.innerHTML = `<option value="">-- Choose a country to load real empirical data (${sorted.length} sovereign states) --</option>` +
      sorted.map(c => `
        <option value="${c.country_code}">
          ${c.country_name} (${c.country_code}) • ${c.region}
        </option>
      `).join('');

    select.addEventListener('change', e => {
      const iso = e.target.value;
      if (!iso) {
        const badge = document.getElementById('countryLoadedBadge');
        if (badge) badge.textContent = 'Custom Simulation';
        state.activeCountryIso = null;
        return;
      }

      loadCountryData(iso);
    });

    // Populate PCA Region select
    const regionSelect = document.getElementById('pcaRegionSelect');
    if (regionSelect) {
      const regions = [...new Set(state.results.countries.map(c => c.region))].filter(Boolean).sort();
      regionSelect.innerHTML = `<option value="all">All Global Regions (${sorted.length} Nations)</option>` +
        regions.map(r => `<option value="${r}">${r}</option>`).join('');

      regionSelect.addEventListener('change', e => {
        state.selectedRegion = e.target.value;
        renderPCAExplorer();
      });
    }
  }

  function loadCountryData(iso) {
    const country = state.results.countries.find(c => c.country_code === iso);
    if (!country) return;

    state.activeCountryIso = iso;

    // Load indicators into simulated state
    for (const [k, v] of Object.entries(country.indicators)) {
      state.simulatedValues[k] = v;
      const slider = document.getElementById(`slider_${k}`);
      if (slider) slider.value = v;
      const valLabel = document.getElementById(`val_${k}`);
      if (valLabel) {
        const cfg = INDICATOR_CONFIGS.find(c => c.key === k);
        valLabel.textContent = `${v.toFixed(1)}${cfg ? cfg.unit : '%'}`;
      }
    }

    const badge = document.getElementById('countryLoadedBadge');
    if (badge) {
      badge.textContent = `Loaded: ${country.country_name} (${country.country_code})`;
      badge.style.color = 'var(--emerald-accent)';
    }

    // Stop auto-simulate if active
    stopAutoSimulation();

    // Update inference and highlight dot
    updateSimulator();
    renderPCAExplorer();
  }

  // ============================================================================
  // 2. Interactive Indicator Sliders with Live Z-Score Feedback
  // ============================================================================
  function renderSimulatorSliders() {
    const container = document.getElementById('simulatorSlidersContainer');
    if (!container) return;

    const mean = state.results.scaler ? state.results.scaler.mean : {};
    const scale = state.results.scaler ? state.results.scaler.scale : {};

    container.innerHTML = INDICATOR_CONFIGS.map(cfg => {
      const curVal = state.simulatedValues[cfg.key] !== undefined ? state.simulatedValues[cfg.key] : cfg.defaultVal;
      const m = mean[cfg.key] || curVal;
      const s = scale[cfg.key] || 1;
      const z = (curVal - m) / s;

      let zClass = 'neutral';
      let zLabel = `${z >= 0 ? '+' : ''}${z.toFixed(1)}σ`;
      if (z > 0.8) zClass = 'high';
      else if (z < -0.8) zClass = 'low';

      return `
        <div class="sim-slider-group" id="group_${cfg.key}">
          <div class="sim-slider-header" style="display: flex; justify-content: space-between; align-items: baseline;">
            <div>
              <span class="sim-slider-name" style="font-weight: 600;">${cfg.label}</span>
              <span style="font-size: 0.68rem; color: var(--text-dim); margin-left: 4px;">(${cfg.category})</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.4rem;">
              <span class="zscore-pill ${zClass}" id="zscore_${cfg.key}">${zLabel}</span>
              <span class="sim-slider-val" id="val_${cfg.key}">${curVal.toFixed(1)}${cfg.unit}</span>
            </div>
          </div>
          <input 
            type="range" 
            class="sim-slider" 
            id="slider_${cfg.key}" 
            data-key="${cfg.key}" 
            data-unit="${cfg.unit}" 
            min="${cfg.min}" 
            max="${cfg.max}" 
            step="${cfg.step}" 
            value="${curVal}"
          />
        </div>
      `;
    }).join('');

    // Attach real-time input listeners
    container.querySelectorAll('.sim-slider').forEach(slider => {
      slider.addEventListener('input', e => {
        // Stop auto-simulation immediately if user manually interacts with any slider
        stopAutoSimulation();

        const key = slider.getAttribute('data-key');
        const unit = slider.getAttribute('data-unit');
        const val = parseFloat(slider.value);
        state.simulatedValues[key] = val;

        const valLabel = document.getElementById(`val_${key}`);
        if (valLabel) valLabel.textContent = `${val.toFixed(1)}${unit}`;

        // Update live Z-Score badge
        const m = mean[key] || val;
        const s = scale[key] || 1;
        const z = (val - m) / s;
        const zBadge = document.getElementById(`zscore_${key}`);
        if (zBadge) {
          zBadge.textContent = `${z >= 0 ? '+' : ''}${z.toFixed(1)}σ`;
          zBadge.className = `zscore-pill ${z > 0.8 ? 'high' : (z < -0.8 ? 'low' : 'neutral')}`;
        }

        // Custom simulation active
        const badge = document.getElementById('countryLoadedBadge');
        if (badge) {
          badge.textContent = 'Custom Simulation';
          badge.style.color = 'var(--cyan-accent)';
        }
        const select = document.getElementById('countrySelect');
        if (select) select.value = '';
        state.activeCountryIso = null;

        updateSimulator();
      });
    });
  }

  // ============================================================================
  // 3. Preset Buttons, Reset, & Auto-Run Transition Simulation
  // ============================================================================
  function setupSimulationControls() {
    // Presets
    document.querySelectorAll('[data-preset]').forEach(btn => {
      btn.addEventListener('click', () => {
        const pKey = btn.getAttribute('data-preset');
        loadTypologyPreset(pKey);
      });
    });

    // Reset button
    const resetBtn = document.getElementById('simResetBtn');
    if (resetBtn) {
      resetBtn.addEventListener('click', () => {
        loadTypologyPreset('global_mean');
      });
    }

    // Auto-Run Transition Simulation
    const autoSimBtn = document.getElementById('autoSimulateBtn');
    if (autoSimBtn) {
      autoSimBtn.addEventListener('click', () => {
        if (state.isAutoSimulating) {
          stopAutoSimulation();
        } else {
          startAutoSimulation();
        }
      });
    }
  }

  function loadTypologyPreset(presetKey) {
    stopAutoSimulation();
    autoSimProgress.stageIdx = 0;
    autoSimProgress.t = 0;
    autoSimProgress.isFinished = false;
    let vals = {};
    const mean = state.results.scaler ? state.results.scaler.mean : {};

    if (presetKey === 'global_mean') {
      INDICATOR_CONFIGS.forEach(cfg => {
        vals[cfg.key] = mean[cfg.key] !== undefined ? Math.round(mean[cfg.key] * 10) / 10 : cfg.defaultVal;
      });
    } else if (TYPOLOGY_PRESETS[presetKey]) {
      vals = TYPOLOGY_PRESETS[presetKey].values;
    }

    const scale = state.results.scaler ? state.results.scaler.scale : {};

    // Apply values to state and DOM
    for (const [k, v] of Object.entries(vals)) {
      state.simulatedValues[k] = v;
      const slider = document.getElementById(`slider_${k}`);
      const valLabel = document.getElementById(`val_${k}`);
      if (slider) slider.value = v;
      if (valLabel) {
        const cfg = INDICATOR_CONFIGS.find(c => c.key === k);
        valLabel.textContent = `${v.toFixed(1)}${cfg ? cfg.unit : '%'}`;
      }

      const m = mean[k] || v;
      const s = scale[k] || 1;
      const z = (v - m) / s;
      const zBadge = document.getElementById(`zscore_${k}`);
      if (zBadge) {
        zBadge.textContent = `${z >= 0 ? '+' : ''}${z.toFixed(1)}σ`;
        zBadge.className = `zscore-pill ${z > 0.8 ? 'high' : (z < -0.8 ? 'low' : 'neutral')}`;
      }
    }

    const badge = document.getElementById('countryLoadedBadge');
    if (badge) {
      badge.textContent = TYPOLOGY_PRESETS[presetKey] ? TYPOLOGY_PRESETS[presetKey].name : 'Global Mean Baseline';
      badge.style.color = 'var(--indigo-accent)';
    }
    const select = document.getElementById('countrySelect');
    if (select) select.value = '';
    state.activeCountryIso = null;

    updateSimulator();
  }

  // Presentation transition stages metadata
  const TRANSITION_STAGES = [
    { title: 'Stage 1/4: Acute Child Undernutrition', desc: 'Niger / Chad Archetype', values: TYPOLOGY_PRESETS.sub_saharan.values },
    { title: 'Stage 2/4: Double Burden of Malnutrition', desc: 'India / Egypt Archetype', values: TYPOLOGY_PRESETS.double_burden.values },
    { title: 'Stage 3/4: High Overweight & Adult Obesity', desc: 'USA / UK Archetype', values: TYPOLOGY_PRESETS.high_obesity.values },
    { title: 'Stage 4/4: Low Malnutrition / Balance', desc: 'Japan / Norway Archetype', values: TYPOLOGY_PRESETS.low_burden.values }
  ];

  let autoSimProgress = {
    stageIdx: 0,
    t: 0,
    isFinished: false
  };

  // Structured presentation simulation: smoothly travels through 4 stages and automatically finishes
  function startAutoSimulation() {
    state.isAutoSimulating = true;
    const btn = document.getElementById('autoSimulateBtn');
    const icon = document.getElementById('autoSimulateIcon');
    const text = document.getElementById('autoSimulateText');
    if (btn) btn.style.background = 'linear-gradient(135deg, #e11d48, #d97706)';
    if (icon) icon.textContent = '⏸';
    if (text) text.textContent = 'Pause Transition Simulation';

    // If already finished previously, restart from Stage 1
    if (autoSimProgress.isFinished || autoSimProgress.stageIdx >= TRANSITION_STAGES.length - 1) {
      autoSimProgress.stageIdx = 0;
      autoSimProgress.t = 0;
      autoSimProgress.isFinished = false;
    }

    const stepsPerStage = 65; // ~2.9 seconds per transition stage

    state.autoSimTimer = setInterval(() => {
      autoSimProgress.t += 1 / stepsPerStage;

      // Stage transition check
      if (autoSimProgress.t >= 1) {
        autoSimProgress.t = 0;
        autoSimProgress.stageIdx++;

        // Once all 4 stages are completed, finish and auto-stop!
        if (autoSimProgress.stageIdx >= TRANSITION_STAGES.length - 1) {
          const finalStage = TRANSITION_STAGES[TRANSITION_STAGES.length - 1];
          applySimulatedValues(finalStage.values);

          const badge = document.getElementById('countryLoadedBadge');
          if (badge) {
            badge.textContent = `✅ Complete: Demonstrated All 4 Transition Stages!`;
            badge.style.color = 'var(--emerald-accent)';
          }

          stopAutoSimulation(true);
          return;
        }
      }

      const fromVals = TRANSITION_STAGES[autoSimProgress.stageIdx].values;
      const toVals = TRANSITION_STAGES[autoSimProgress.stageIdx + 1].values;
      const mean = state.results.scaler.mean;
      const scale = state.results.scaler.scale;

      // Smooth cosine easing
      const ease = 0.5 - 0.5 * Math.cos(autoSimProgress.t * Math.PI);

      INDICATOR_CONFIGS.forEach(cfg => {
        const k = cfg.key;
        const v = fromVals[k] + (toVals[k] - fromVals[k]) * ease;
        state.simulatedValues[k] = v;

        const slider = document.getElementById(`slider_${k}`);
        if (slider) slider.value = v;
        const valLabel = document.getElementById(`val_${k}`);
        if (valLabel) valLabel.textContent = `${v.toFixed(1)}${cfg.unit}`;

        const z = (v - mean[k]) / scale[k];
        const zBadge = document.getElementById(`zscore_${k}`);
        if (zBadge) {
          zBadge.textContent = `${z >= 0 ? '+' : ''}${z.toFixed(1)}σ`;
          zBadge.className = `zscore-pill ${z > 0.8 ? 'high' : (z < -0.8 ? 'low' : 'neutral')}`;
        }
      });

      const currentStage = TRANSITION_STAGES[autoSimProgress.stageIdx];
      const nextStage = TRANSITION_STAGES[autoSimProgress.stageIdx + 1];
      const overallPct = Math.min(99, Math.round(((autoSimProgress.stageIdx + autoSimProgress.t) / (TRANSITION_STAGES.length - 1)) * 100));

      const badge = document.getElementById('countryLoadedBadge');
      if (badge) {
        badge.textContent = `▶ ${currentStage.title} → ${nextStage.desc} (${overallPct}%)`;
        badge.style.color = 'var(--amber-accent)';
      }

      updateSimulator();
    }, 45);
  }

  function applySimulatedValues(vals) {
    const mean = state.results.scaler ? state.results.scaler.mean : {};
    const scale = state.results.scaler ? state.results.scaler.scale : {};

    for (const [k, v] of Object.entries(vals)) {
      state.simulatedValues[k] = v;
      const slider = document.getElementById(`slider_${k}`);
      if (slider) slider.value = v;
      const valLabel = document.getElementById(`val_${k}`);
      if (valLabel) {
        const cfg = INDICATOR_CONFIGS.find(c => c.key === k);
        valLabel.textContent = `${v.toFixed(1)}${cfg ? cfg.unit : '%'}`;
      }

      const m = mean[k] || v;
      const s = scale[k] || 1;
      const z = (v - m) / s;
      const zBadge = document.getElementById(`zscore_${k}`);
      if (zBadge) {
        zBadge.textContent = `${z >= 0 ? '+' : ''}${z.toFixed(1)}σ`;
        zBadge.className = `zscore-pill ${z > 0.8 ? 'high' : (z < -0.8 ? 'low' : 'neutral')}`;
      }
    }
    updateSimulator();
  }

  function stopAutoSimulation(isComplete = false) {
    if (!state.isAutoSimulating && !isComplete) return;
    state.isAutoSimulating = false;
    clearInterval(state.autoSimTimer);
    state.autoSimTimer = null;
    autoSimProgress.isFinished = isComplete;

    const btn = document.getElementById('autoSimulateBtn');
    const icon = document.getElementById('autoSimulateIcon');
    const text = document.getElementById('autoSimulateText');
    if (btn) btn.style.background = 'linear-gradient(135deg, #4f46e5, #0284c7)';
    if (icon) icon.textContent = isComplete ? '↺' : '▶';
    if (text) {
      if (isComplete) {
        text.textContent = 'Replay Transition Simulation';
      } else if (autoSimProgress.stageIdx > 0 || autoSimProgress.t > 0) {
        text.textContent = 'Resume Transition Simulation';
      } else {
        text.textContent = 'Auto-Run Transition Simulation';
      }
    }
  }

  // ============================================================================
  // 4. Real-Time Model Inference, Centroid Distance, & Goal Interventions
  // ============================================================================
  function updateSimulator() {
    if (!state.results || !state.results.scaler || !state.results.cluster_centers) return;

    const feats = state.results.features;
    const mean = state.results.scaler.mean;
    const scale = state.results.scaler.scale;
    const activeCfg = `${state.activeDistance}_k${state.activeK}`;
    const centers = state.results.cluster_centers[activeCfg];

    if (!centers || centers.length === 0) return;

    // 1. Z-Score Standardization
    const zVec = feats.map(f => {
      const raw = state.simulatedValues[f] !== undefined ? state.simulatedValues[f] : mean[f];
      return (raw - mean[f]) / scale[f];
    });

    // 2. Centroid Distance Minimization: min d(z, c_k)
    const isManhattan = state.activeDistance === 'manhattan';
    const distances = centers.map((cen, cIdx) => {
      let d = 0;
      for (let i = 0; i < feats.length; i++) {
        const diff = Math.abs(zVec[i] - cen[i]);
        d += isManhattan ? diff : diff * diff;
      }
      return {
        cluster_id: cIdx,
        distance: isManhattan ? d : Math.sqrt(d)
      };
    });

    // Closest cluster assignment
    distances.sort((a, b) => a.distance - b.distance);
    const closestCluster = distances[0].cluster_id;
    state.simulatedCluster = closestCluster;

    // 3. 2D PCA Biplot Projection
    const pcaLoadings = state.results.pca.loadings;
    let px = 0, py = 0;
    for (let i = 0; i < feats.length; i++) {
      const f = feats[i];
      if (pcaLoadings[f]) {
        px += zVec[i] * pcaLoadings[f][0];
        py += zVec[i] * pcaLoadings[f][1];
      }
    }
    state.simulatedCoords = { x: px, y: py };

    // 4. Update UI: Model Badge
    const modelBadge = document.getElementById('simActiveModelBadge');
    if (modelBadge) {
      modelBadge.textContent = `${state.activeDistance.toUpperCase()} (K = ${state.activeK})`;
    }

    // 5. Update UI: Predicted Cluster Display
    const clusterOut = document.getElementById('simClusterOutputBox');
    if (clusterOut) {
      const color = PALETTE[closestCluster % PALETTE.length];
      const clName = getClusterDisplayName(closestCluster, state.activeDistance, state.activeK);

      clusterOut.innerHTML = `
        <div style="display: flex; align-items: center; gap: 0.75rem;">
          <span style="width: 16px; height: 16px; border-radius: 50%; background: ${color}; box-shadow: 0 0 12px ${color};"></span>
          <div>
            <div style="font-size: 0.72rem; color: var(--text-dim); text-transform: uppercase; font-weight: 700; letter-spacing: 0.04em;">Predicted Typology</div>
            <div style="font-size: 1.15rem; font-weight: 700; color: var(--text-main); font-family: var(--font-heading);">${clName}</div>
          </div>
        </div>
        <span class="pill-status" style="background: ${color}22; color: ${color}; border: 1px solid ${color}44; font-size: 0.88rem; font-weight: 700; padding: 0.35rem 0.75rem;">
          Cluster ${closestCluster}
        </span>
      `;
    }

    // 6. Update UI: Achieving the Goal (Prescribed Public Health Intervention)
    const goalBox = document.getElementById('goalPrescriptionBox');
    if (goalBox) {
      const strat = TARGETED_INTERVENTIONS[closestCluster] || TARGETED_INTERVENTIONS[0];
      const color = PALETTE[closestCluster % PALETTE.length];

      goalBox.innerHTML = `
        <div class="goal-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
          <div style="display: flex; align-items: center; gap: 0.45rem;">
            <span>${strat.icon}</span>
            <span class="goal-title" style="color: ${color};">${strat.title}</span>
          </div>
          <span class="pill-status" style="font-size: 0.7rem; background: ${color}15; color: ${color}; border: 1px solid ${color}33;">
            ${strat.badge}
          </span>
        </div>
        <ul style="margin: 0; padding-left: 1.25rem; font-size: 0.82rem; color: var(--text-main); line-height: 1.55;">
          ${strat.actions.map(act => `<li style="margin-bottom: 0.25rem;">${act}</li>`).join('')}
        </ul>
      `;
      goalBox.style.borderLeft = `4px solid ${color}`;
    }

    // 7. Update UI: Distance Minimization Bars
    const distContainer = document.getElementById('simDistanceBarsContainer');
    if (distContainer) {
      const maxDist = Math.max(...distances.map(d => d.distance), 1);
      distContainer.innerHTML = distances.map(d => {
        const color = PALETTE[d.cluster_id % PALETTE.length];
        const clName = getClusterDisplayName(d.cluster_id, state.activeDistance, state.activeK);
        const pct = Math.min(100, Math.max(12, (1 - d.distance / (maxDist * 1.25)) * 100));
        const isMin = d.cluster_id === closestCluster;

        return `
          <div class="sim-dist-item" style="margin-bottom: 0.35rem;">
            <div class="sim-dist-meta" style="display: flex; justify-content: space-between; font-size: 0.78rem;">
              <span style="color: ${isMin ? 'var(--text-main)' : 'var(--text-muted)'}; font-weight: ${isMin ? '700' : '500'};">
                ${isMin ? '★ ' : ''}C${d.cluster_id}: ${clName.slice(0, 28)}
              </span>
              <span style="color: ${color}; font-weight: 700;">d = ${d.distance.toFixed(2)}</span>
            </div>
            <div class="bar-track" style="height: 6px; background: var(--slider-track); border-radius: 3px; overflow: hidden; margin-top: 2px;">
              <div class="bar-fill" style="height: 100%; width: ${pct}%; background: ${color}; transition: width 0.15s ease;"></div>
            </div>
          </div>
        `;
      }).join('');
    }

    // 8. Update UI: Nearest Real Sovereign States
    computeClosestRealCountries(zVec);

    // 9. Update Live Simulated Point on PCA Factor Plot
    updateSimulatedPointOnPCA();
  }

  function getClusterDisplayName(clId, distance, k) {
    if (k === 3 && distance === 'euclidean' && state.results.cluster_profiles) {
      const p = state.results.cluster_profiles.find(cp => cp.cluster_id === clId);
      if (p) return p.name;
    }
    if (k === 4 && distance === 'euclidean') {
      const names = ['Severe Undernutrition', 'High Obesity & Overweight', 'Transitional Vulnerability', 'Double Burden of Malnutrition'];
      return names[clId] || `Cluster ${clId} (K=4)`;
    }
    return `Cluster ${clId} (${distance.toUpperCase()} K=${k})`;
  }

  function computeClosestRealCountries(zVec) {
    const listContainer = document.getElementById('simClosestCountriesList');
    if (!listContainer || !state.results.countries) return;

    const feats = state.results.features;
    const mean = state.results.scaler.mean;
    const scale = state.results.scaler.scale;

    const countryDistances = state.results.countries.map(c => {
      let d = 0;
      for (let i = 0; i < feats.length; i++) {
        const val = c.indicators[feats[i]] !== undefined ? c.indicators[feats[i]] : mean[feats[i]];
        const cz = (val - mean[feats[i]]) / scale[feats[i]];
        const diff = zVec[i] - cz;
        d += diff * diff;
      }
      return {
        country: c,
        distance: Math.sqrt(d)
      };
    });

    countryDistances.sort((a, b) => a.distance - b.distance);
    const top3 = countryDistances.slice(0, 3);

    listContainer.innerHTML = top3.map(item => {
      const c = item.country;
      const clId = c[`cluster_${state.activeDistance}_k${state.activeK}`] !== undefined ? 
        c[`cluster_${state.activeDistance}_k${state.activeK}`] : c.cluster;
      const color = PALETTE[clId % PALETTE.length];

      return `
        <div class="nearest-country-chip" onclick="window.appLoadCountry('${c.country_code}')" title="Click to load ${c.country_name} into simulator">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-weight: 700; font-size: 0.84rem; color: var(--text-main);">${c.country_name}</span>
            <span style="font-size: 0.7rem; font-weight: 700; color: ${color};">C${clId}</span>
          </div>
          <div style="font-size: 0.72rem; color: var(--text-dim); display: flex; justify-content: space-between;">
            <span>${c.region.split('&')[0]}</span>
            <span style="font-weight: 600;">dist: ${item.distance.toFixed(2)}</span>
          </div>
        </div>
      `;
    }).join('');
  }

  // Global helper for onclick on nearest chips
  window.appLoadCountry = function(iso) {
    const select = document.getElementById('countrySelect');
    if (select) select.value = iso;
    loadCountryData(iso);
  };

  // ============================================================================
  // 5. Interactive 2D PCA Factor Space Projection & Biplot
  // ============================================================================
  function renderPCAExplorer() {
    const container = document.getElementById('pcaScatterSvg');
    const tooltip = document.getElementById('pcaTooltip');
    if (!container || !tooltip) return;

    const colors = getThemeColors();
    const width = 860;
    const height = 500;
    const margin = { top: 35, right: 35, bottom: 45, left: 55 };

    const countries = state.results.countries;
    const activeCfg = `${state.activeDistance}_k${state.activeK}`;
    const pcaMeta = state.results.pca;

    // Filter by search and region
    const filtered = countries.filter(c => {
      const matchSearch = !state.searchTerm || 
        c.country_name.toLowerCase().includes(state.searchTerm.toLowerCase()) ||
        c.country_code.toLowerCase().includes(state.searchTerm.toLowerCase());
      const matchRegion = state.selectedRegion === 'all' || c.region === state.selectedRegion;
      return matchSearch && matchRegion;
    });

    const xVals = countries.map(c => c.pca_x);
    const yVals = countries.map(c => c.pca_y);
    const xMin = Math.min(...xVals) - 0.6;
    const xMax = Math.max(...xVals) + 0.6;
    const yMin = Math.min(...yVals) - 0.6;
    const yMax = Math.max(...yVals) + 0.6;

    const xScale = x => margin.left + ((x - xMin) / (xMax - xMin)) * (width - margin.left - margin.right);
    const yScale = y => margin.top + (1 - (y - yMin) / (yMax - yMin)) * (height - margin.top - margin.bottom);

    let svg = `<svg class="svg-chart" viewBox="0 0 ${width} ${height}" id="pcaMainSvg">`;
    svg += `<rect width="${width}" height="${height}" fill="transparent"/>`;

    // Center Axes (0,0)
    const xZero = xScale(0);
    const yZero = yScale(0);
    svg += `<line x1="${xScale(xMin)}" y1="${yZero}" x2="${xScale(xMax)}" y2="${yZero}" stroke="${colors.zeroAxis}" stroke-width="1" stroke-dasharray="3,3"/>`;
    svg += `<line x1="${xZero}" y1="${yScale(yMin)}" x2="${xZero}" y2="${yScale(yMax)}" stroke="${colors.zeroAxis}" stroke-width="1" stroke-dasharray="3,3"/>`;

    // Feature Loadings Vectors (Biplot)
    if (state.showLoadings && pcaMeta.loadings) {
      const scaleLoadings = 3.6;
      const arrowStroke = colors.isDark ? 'rgba(251, 191, 36, 0.75)' : 'rgba(217, 119, 6, 0.85)';
      const arrowText = colors.isDark ? '#fde68a' : '#92400e';

      for (const [feat, coords] of Object.entries(pcaMeta.loadings)) {
        const vx = xScale(coords[0] * scaleLoadings);
        const vy = yScale(coords[1] * scaleLoadings);
        svg += `<line x1="${xZero}" y1="${yZero}" x2="${vx}" y2="${vy}" stroke="${arrowStroke}" stroke-width="1.4"/>`;
        svg += `<circle cx="${vx}" cy="${vy}" r="2.5" fill="var(--amber-accent)"/>`;
        svg += `<text x="${vx + 4}" y="${vy + 3}" fill="${arrowText}" font-size="9" font-weight="700">${feat.replace(/_/g, ' ')}</text>`;
      }
    }

    // Country Scatter Dots
    filtered.forEach(c => {
      const cx = xScale(c.pca_x);
      const cy = yScale(c.pca_y);
      const clId = c[`cluster_${activeCfg}`] !== undefined ? c[`cluster_${activeCfg}`] : c.cluster;
      const dotColor = PALETTE[clId % PALETTE.length];
      const isSelected = state.activeCountryIso === c.country_code;

      svg += `<circle 
        cx="${cx}" cy="${cy}" r="${isSelected ? 9 : (c.is_borderline ? 6 : 5)}" 
        fill="${dotColor}" 
        stroke="${isSelected ? '#000000' : (c.is_borderline ? 'var(--amber-accent)' : '#ffffff')}" 
        stroke-width="${isSelected ? 3 : (c.is_borderline ? 2 : 1)}" 
        opacity="${isSelected ? 1.0 : 0.88}"
        class="pca-dot"
        data-iso="${c.country_code}"
        style="cursor: pointer; transition: transform 0.15s ease;"
      />`;
    });

    // Render LIVE SIMULATED NATION Marker (pulsing halo + star marker)
    if (state.simulatedCoords) {
      const simX = xScale(state.simulatedCoords.x);
      const simY = yScale(state.simulatedCoords.y);
      const simClColor = PALETTE[state.simulatedCluster % PALETTE.length];
      const simBoxBg = colors.isDark ? 'rgba(15, 23, 42, 0.95)' : 'rgba(255, 255, 255, 0.98)';
      const simBoxText = colors.isDark ? '#ffffff' : '#0f172a';

      svg += `
        <g id="simulatedPcaGroup" style="cursor: pointer; transition: transform 0.15s ease;">
          <!-- Pulsing Outer Ring -->
          <circle id="simPulseCircle" cx="${simX}" cy="${simY}" r="18" fill="${simClColor}" opacity="0.3" class="sim-point"></circle>
          <circle id="simCoreCircle" cx="${simX}" cy="${simY}" r="9" fill="${simClColor}" stroke="#ffffff" stroke-width="2.5"></circle>
          <circle id="simInnerStar" cx="${simX}" cy="${simY}" r="3" fill="#ffffff"></circle>
          <!-- Callout Label -->
          <rect id="simBoxRect" x="${simX + 12}" y="${simY - 14}" width="138" height="22" rx="4" fill="${simBoxBg}" stroke="${simClColor}" stroke-width="1.4"></rect>
          <text id="simBoxLabel" x="${simX + 18}" y="${simY + 1}" fill="${simBoxText}" font-size="10" font-weight="700">★ SIMULATED NATION</text>
        </g>
      `;
    }

    // Axis Labels
    svg += `<text x="${width / 2}" y="${height - 10}" fill="${colors.axisText}" font-size="11" font-weight="600" text-anchor="middle">Principal Component 1 (${(pcaMeta.variance_explained[0]*100).toFixed(1)}% Variance — Undernutrition vs Overnutrition Axis)</text>`;
    svg += `<text x="${margin.left - 10}" y="${margin.top - 12}" fill="${colors.axisText}" font-size="11" font-weight="600" text-anchor="start">PC2 (${(pcaMeta.variance_explained[1]*100).toFixed(1)}% Variance — Wasting / Stunting)</text>`;

    svg += `</svg>`;
    container.innerHTML = svg;

    attachPCATooltipEvents(container, tooltip, countries, activeCfg);
    renderPCALegend(activeCfg);
  }

  // Lightweight update of simulated star on PCA without full re-render
  function updateSimulatedPointOnPCA() {
    const mainSvg = document.getElementById('pcaMainSvg');
    if (!mainSvg || !state.results || !state.simulatedCoords) return;

    const width = 860;
    const height = 500;
    const margin = { top: 35, right: 35, bottom: 45, left: 55 };

    const countries = state.results.countries;
    const xVals = countries.map(c => c.pca_x);
    const yVals = countries.map(c => c.pca_y);
    const xMin = Math.min(...xVals) - 0.6;
    const xMax = Math.max(...xVals) + 0.6;
    const yMin = Math.min(...yVals) - 0.6;
    const yMax = Math.max(...yVals) + 0.6;

    const xScale = x => margin.left + ((x - xMin) / (xMax - xMin)) * (width - margin.left - margin.right);
    const yScale = y => margin.top + (1 - (y - yMin) / (yMax - yMin)) * (height - margin.top - margin.bottom);

    const simX = xScale(state.simulatedCoords.x);
    const simY = yScale(state.simulatedCoords.y);
    const simClColor = PALETTE[state.simulatedCluster % PALETTE.length];

    const pulse = document.getElementById('simPulseCircle');
    const core = document.getElementById('simCoreCircle');
    const star = document.getElementById('simInnerStar');
    const box = document.getElementById('simBoxRect');
    const label = document.getElementById('simBoxLabel');

    if (pulse && core && star && box && label) {
      pulse.setAttribute('cx', simX);
      pulse.setAttribute('cy', simY);
      pulse.setAttribute('fill', simClColor);

      core.setAttribute('cx', simX);
      core.setAttribute('cy', simY);
      core.setAttribute('fill', simClColor);

      star.setAttribute('cx', simX);
      star.setAttribute('cy', simY);

      box.setAttribute('x', simX + 12);
      box.setAttribute('y', simY - 14);
      box.setAttribute('stroke', simClColor);

      label.setAttribute('x', simX + 18);
      label.setAttribute('y', simY + 1);
    } else {
      renderPCAExplorer();
    }
  }

  function attachPCATooltipEvents(container, tooltip, countries, activeCfg) {
    const dots = container.querySelectorAll('.pca-dot');
    const countryMap = new Map(countries.map(c => [c.country_code, c]));

    dots.forEach(dot => {
      dot.addEventListener('mouseenter', e => {
        const iso = dot.getAttribute('data-iso');
        const c = countryMap.get(iso);
        if (!c) return;

        const clId = c[`cluster_${activeCfg}`] !== undefined ? c[`cluster_${activeCfg}`] : c.cluster;
        const color = PALETTE[clId % PALETTE.length];

        tooltip.innerHTML = `
          <div class="tooltip-title">
            <span>${c.country_name} (${c.country_code})</span>
            <span class="tooltip-badge" style="background: ${color}22; color: ${color}; border: 1px solid ${color}44;">C${clId}</span>
          </div>
          <div class="tooltip-row"><span>Region:</span> <span class="tooltip-val">${c.region}</span></div>
          <div class="tooltip-row"><span>Income:</span> <span class="tooltip-val">${c.income_group || 'N/A'}</span></div>
          <div class="tooltip-row"><span>Silhouette:</span> <span class="tooltip-val">${c.silhouette ? c.silhouette.toFixed(3) : 'N/A'} ${c.is_borderline ? '⚠️ Borderline' : ''}</span></div>
          <div style="border-top: 1px solid rgba(148, 163, 184, 0.2); margin: 6px 0; padding-top: 4px;">
            <div class="tooltip-row"><span>Stunting:</span> <span class="tooltip-val">${c.indicators.stunting || 'N/A'}%</span></div>
            <div class="tooltip-row"><span>Wasting:</span> <span class="tooltip-val">${c.indicators.wasting || 'N/A'}%</span></div>
            <div class="tooltip-row"><span>Adult Obesity:</span> <span class="tooltip-val">${c.indicators.adult_obesity || 'N/A'}%</span></div>
          </div>
          <div style="margin-top: 6px; font-size: 0.72rem; color: var(--indigo-accent); text-align: center; font-weight: 700;">
            Click to load country into simulator &rarr;
          </div>
        `;

        const rect = dot.getBoundingClientRect();
        const containerRect = container.getBoundingClientRect();
        tooltip.style.left = `${rect.left - containerRect.left + 5}px`;
        tooltip.style.top = `${rect.top - containerRect.top - 10}px`;
        tooltip.classList.add('active');

        dot.setAttribute('r', '8');
      });

      dot.addEventListener('mouseleave', () => {
        tooltip.classList.remove('active');
        const iso = dot.getAttribute('data-iso');
        const isSelected = state.activeCountryIso === iso;
        const c = countryMap.get(iso);
        dot.setAttribute('r', isSelected ? '9' : (c && c.is_borderline ? '6' : '5'));
      });

      // Click loads country into simulator
      dot.addEventListener('click', () => {
        const iso = dot.getAttribute('data-iso');
        const select = document.getElementById('countrySelect');
        if (select) select.value = iso;
        loadCountryData(iso);
      });
    });
  }

  function renderPCALegend(activeCfg) {
    const legend = document.getElementById('pcaClusterLegend');
    if (!legend) return;

    const k = state.activeK;
    let html = '';
    for (let i = 0; i < k; i++) {
      const color = PALETTE[i % PALETTE.length];
      const name = getClusterDisplayName(i, state.activeDistance, k);
      html += `
        <div style="display: flex; align-items: center; gap: 0.35rem; font-size: 0.75rem; margin-right: 0.85rem;">
          <span style="width: 10px; height: 10px; border-radius: 50%; background: ${color};"></span>
          <span style="font-weight: 600; color: var(--text-muted);">C${i}: ${name.split('/')[0].slice(0, 22)}</span>
        </div>
      `;
    }
    legend.innerHTML = html;
  }

  function setupPCAControls() {
    // Toggle Loading Vectors
    const toggleBtn = document.getElementById('toggleLoadingsBtn');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', () => {
        state.showLoadings = !state.showLoadings;
        toggleBtn.classList.toggle('active', state.showLoadings);
        renderPCAExplorer();
      });
    }

    // Play K Progression
    const playBtn = document.getElementById('playProgressionBtn');
    if (playBtn) {
      playBtn.addEventListener('click', () => {
        if (state.isPlayingProgression) {
          stopProgression();
        } else {
          startProgression();
        }
      });
    }

    // Search input
    const search = document.getElementById('pcaSearchInput');
    if (search) {
      search.addEventListener('input', e => {
        state.searchTerm = e.target.value.trim();
        renderPCAExplorer();
      });
    }
  }

  function startProgression() {
    state.isPlayingProgression = true;
    const icon = document.getElementById('playProgressionIcon');
    const text = document.getElementById('playProgressionText');
    if (icon) icon.textContent = '⏸';
    if (text) text.textContent = 'Pause Progression';

    state.progressionTimer = setInterval(() => {
      let nextK = state.activeK + 1;
      if (nextK > 8) nextK = 3;
      switchActiveModel(state.activeDistance, nextK);
    }, 1800);
  }

  function stopProgression() {
    state.isPlayingProgression = false;
    clearInterval(state.progressionTimer);
    state.progressionTimer = null;
    const icon = document.getElementById('playProgressionIcon');
    const text = document.getElementById('playProgressionText');
    if (icon) icon.textContent = '▶';
    if (text) text.textContent = 'Play K Progression';
  }

  // ============================================================================
  // 6. Model Quick Switchers (K=3, K=4, K=5, Manhattan)
  // ============================================================================
  function setupModelSwitchers() {
    document.querySelectorAll('[data-model-k]').forEach(btn => {
      btn.addEventListener('click', () => {
        const k = parseInt(btn.getAttribute('data-model-k'), 10);
        const dist = btn.getAttribute('data-model-dist') || 'euclidean';
        switchActiveModel(dist, k);
      });
    });
  }

  function switchActiveModel(dist, k) {
    state.activeDistance = dist;
    state.activeK = k;

    // Update active button state
    document.querySelectorAll('[data-model-k]').forEach(b => {
      const bK = parseInt(b.getAttribute('data-model-k'), 10);
      const bDist = b.getAttribute('data-model-dist') || 'euclidean';
      b.classList.toggle('active', bK === k && bDist === dist);
    });

    updateSimulator();
    renderPCAExplorer();
  }

  // ============================================================================
  // 7. Model Pipeline & Math Explainer Drawer
  // ============================================================================
  function setupPipelineDrawer() {
    const openBtn = document.getElementById('openPipelineDrawerBtn');
    const closeBtn = document.getElementById('pipelineDrawerCloseBtn');
    const drawer = document.getElementById('pipelineDrawer');
    const backdrop = document.getElementById('pipelineDrawerBackdrop');

    function openDrawer() {
      if (drawer) drawer.classList.add('open');
      if (backdrop) backdrop.classList.add('visible');
    }

    function closeDrawer() {
      if (drawer) drawer.classList.remove('open');
      if (backdrop) backdrop.classList.remove('visible');
    }

    if (openBtn) openBtn.addEventListener('click', openDrawer);
    if (closeBtn) closeBtn.addEventListener('click', closeDrawer);
    if (backdrop) backdrop.addEventListener('click', closeDrawer);
  }

  function setupStepCardInteractions() {
    const cardProb = document.getElementById('stepCardProblem');
    const cardProc = document.getElementById('stepCardProcess');
    const cardGoal = document.getElementById('stepCardGoal');

    if (cardProb) {
      cardProb.addEventListener('click', () => {
        const slidersBox = document.getElementById('simulatorSlidersContainer');
        if (slidersBox) {
          slidersBox.style.transition = 'outline 0.3s ease';
          slidersBox.style.outline = '3px solid var(--rose-accent)';
          setTimeout(() => { slidersBox.style.outline = 'none'; }, 900);
        }
      });
    }

    if (cardProc) {
      cardProc.addEventListener('click', () => {
        const openBtn = document.getElementById('openPipelineDrawerBtn');
        if (openBtn) openBtn.click();
      });
    }

    if (cardGoal) {
      cardGoal.addEventListener('click', () => {
        const goalBox = document.getElementById('goalPrescriptionBox');
        if (goalBox) {
          goalBox.style.transition = 'transform 0.3s ease, box-shadow 0.3s ease';
          goalBox.style.transform = 'scale(1.03)';
          goalBox.style.boxShadow = '0 0 20px var(--emerald-accent)';
          setTimeout(() => { 
            goalBox.style.transform = 'scale(1)'; 
            goalBox.style.boxShadow = 'none';
          }, 700);
        }
      });
    }
  }

  // ============================================================================
  // 8. Theme Toggle (Light / Dark)
  // ============================================================================
  function setupThemeToggle() {
    const btn = document.getElementById('themeToggleBtn');
    const icon = document.getElementById('themeToggleIcon');
    const text = document.getElementById('themeToggleText');
    if (!btn) return;

    btn.addEventListener('click', () => {
      const isDark = document.body.classList.toggle('dark-theme');
      if (icon) icon.textContent = isDark ? '☀️' : '🌙';
      if (text) text.textContent = isDark ? 'Light Mode' : 'Dark Mode';

      renderPCAExplorer();
    });
  }

})();
