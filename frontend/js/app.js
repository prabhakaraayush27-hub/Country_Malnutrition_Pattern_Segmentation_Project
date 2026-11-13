/**
 * Country Malnutrition Pattern Segmentation Dashboard
 * Pure Vanilla JavaScript (No frameworks, No build step)
 * Reads data directly from window.RESULTS
 */

(function () {
  'use strict';

  // Cluster Color Palette
  const PALETTE = [
    '#f43f5e', // Cluster 0: Rose / Red
    '#06b6d4', // Cluster 1: Cyan
    '#10b981', // Cluster 2: Emerald
    '#f59e0b', // Cluster 3: Amber
    '#a855f7', // Cluster 4: Purple
    '#ec4899', // Cluster 5: Pink
    '#3b82f6', // Cluster 6: Blue
    '#84cc16'  // Cluster 7: Lime
  ];

  // Indicator Slider Configurations for Live Simulator
  const INDICATOR_CONFIGS = [
    { key: 'stunting', label: 'Child Stunting', min: 0, max: 60, step: 0.5, unit: '%', category: 'undernutrition' },
    { key: 'wasting', label: 'Child Wasting', min: 0, max: 25, step: 0.2, unit: '%', category: 'undernutrition' },
    { key: 'underweight', label: 'Child Underweight', min: 0, max: 40, step: 0.5, unit: '%', category: 'undernutrition' },
    { key: 'undernourishment', label: 'Undernourishment', min: 0, max: 55, step: 0.5, unit: '%', category: 'undernutrition' },
    { key: 'anaemia_children', label: 'Child Anaemia', min: 0, max: 85, step: 0.5, unit: '%', category: 'undernutrition' },
    { key: 'anaemia_women', label: 'Women Anaemia', min: 0, max: 70, step: 0.5, unit: '%', category: 'undernutrition' },
    { key: 'exclusive_breastfeeding', label: 'Exclusive Breastfeeding', min: 0, max: 90, step: 0.5, unit: '%', category: 'protective' },
    { key: 'child_overweight', label: 'Child Overweight', min: 0, max: 30, step: 0.2, unit: '%', category: 'overnutrition' },
    { key: 'adult_obesity', label: 'Adult Obesity', min: 0, max: 60, step: 0.5, unit: '%', category: 'overnutrition' }
  ];

  // Archetype Presets for What-If Simulation
  const TYPOLOGY_PRESETS = {
    sub_saharan: {
      name: 'High Undernutrition (Sub-Saharan)',
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
      name: 'Double Burden (Transitional)',
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
      name: 'High Overweight & Obesity',
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
      name: 'Lower Malnutrition Burden',
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
    progressionTimer: null,
    isPlayingProgression: false,
    activeCountryIso: null
  };

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
      state.simulatedValues[ind.key] = mean[ind.key] !== undefined ? Math.round(mean[ind.key] * 10) / 10 : 15;
    });

    // Check demo data banner
    if (state.results.metadata.is_demo) {
      const banner = document.getElementById('demoBanner');
      if (banner) banner.classList.add('visible');
    }

    renderKPIs();
    renderPreprocessingAudit();
    renderIndicatorTable();
    renderCorrelationHeatmap();
    renderModelSelectionCharts();
    renderModelTable();
    renderPCAExplorer();
    renderHierarchicalSection();
    renderClusterProfiles();
    renderSimulator();
    renderBorderlineTable();
    renderReproduceSection();

    setupEventListeners();
    setupDrawer();
    setupPlayProgression();
    setupTableModelSwitching();
    setupScrollReveal();
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
  // 1. KPI Cards with Counter Animation
  // ============================================================================
  function animateValue(id, start, end, duration, decimals = 0, prefix = '', suffix = '') {
    const obj = document.getElementById(id);
    if (!obj) return;
    let startTimestamp = null;
    const step = (timestamp) => {
      if (!startTimestamp) startTimestamp = timestamp;
      const progress = Math.min((timestamp - startTimestamp) / duration, 1);
      const ease = 1 - Math.pow(1 - progress, 3); // cubic ease-out
      const current = start + ease * (end - start);
      obj.textContent = prefix + current.toFixed(decimals) + suffix;
      if (progress < 1) {
        window.requestAnimationFrame(step);
      } else {
        obj.textContent = prefix + end.toFixed(decimals) + suffix;
      }
    };
    window.requestAnimationFrame(step);
  }

  function renderKPIs() {
    const m = state.results.metadata;
    const setVal = (id, val) => {
      const el = document.getElementById(id);
      if (el) el.textContent = val;
    };

    animateValue('kpiCountries', 0, m.total_countries_analyzed, 1200, 0);
    setVal('kpiCountriesSub', `of ${m.total_countries_raw} sovereign states`);

    animateValue('kpiIndicators', 0, m.total_indicators_used, 800, 0);
    setVal('kpiIndicatorsSub', 'retained (low missingness)');

    setVal('kpiK', `K = ${m.selected_k}`);
    setVal('kpiKSub', `${m.selected_distance.toUpperCase()} distance`);

    animateValue('kpiSilhouette', 0, m.selected_silhouette, 1400, 4);
    setVal('kpiSilhouetteSub', 'Euclidean common ruler');

    animateValue('kpiDB', 0, m.selected_davies_bouldin, 1400, 4);
    setVal('kpiDBSub', 'Separation ratio (lower=better)');

    animateValue('kpiStability', 0, m.selected_stability_ari, 1400, 4);
    setVal('kpiStabilitySub', `±${m.selected_stability_std.toFixed(3)} ARI (20 boots)`);
  }

  // ============================================================================
  // 2. Preprocessing Audit Stepper
  // ============================================================================
  function renderPreprocessingAudit() {
    const audit = state.results.preprocessing_audit;
    const container = document.getElementById('preprocessingAuditContainer');
    if (!container) return;

    const steps = [
      {
        num: '01',
        title: 'Indicator Missingness Audit',
        desc: `Audited 10 candidate World Bank indicators. Dropped indicators missing > 40% of countries: [${audit.dropped_indicators.join(', ') || 'None'}]. Retained ${audit.kept_indicators.length} indicators with high global reporting coverage.`,
        badge: `${audit.kept_indicators.length} Kept / ${audit.dropped_indicators.length} Dropped`
      },
      {
        num: '02',
        title: 'Country Completeness Pruning',
        desc: `Excluded ${audit.dropped_countries.length} countries (primarily non-reporting microstates and high-income nations without UNICEF anthropometric surveys) that missed > 50% of kept indicators. Retained 166 sovereign states.`,
        badge: `${audit.dropped_countries.length} Excluded`
      },
      {
        num: '03',
        title: 'Multicollinearity & Redundancy Check',
        desc: `Computed pairwise Pearson correlation matrix across all 9 indicators. Filter threshold |r| > 0.92. Maximum observed correlation was r = 0.88 (Stunting vs Underweight). All 9 indicators retained as distinct dimensions.`,
        badge: '0 Collinear Dropped'
      },
      {
        num: '04',
        title: 'Hierarchical Median Imputation',
        desc: `Remaining missing values imputed using regional median (e.g. Sub-Saharan Africa, Latin America), falling back to global median. Preserves geographical heterogeneity without distorting variances.`,
        badge: 'Regional Median Imputed'
      },
      {
        num: '05',
        title: 'Winsorization Outlier Control',
        desc: `Heavy-tailed health indicators clipped at the 1st and 99th percentiles to prevent extreme national outliers from exerting excessive leverage on distance calculations.`,
        badge: '1st & 99th Percentile'
      },
      {
        num: '06',
        title: 'Categorical Profiling Isolation',
        desc: `World Bank Income Group ordinal-encoded (1-4) and Region kept strictly as profiling labels. Critical methodological control: EXCLUDED from feature vector to prevent circular reasoning.`,
        badge: 'Strictly Isolated'
      },
      {
        num: '07',
        title: 'StandardScaler (Z-Score Normalization)',
        desc: `Transformed all 9 health indicators to zero mean (μ = 0) and unit variance (σ = 1). Ensures equal weighting between infant percentages and adult population rates.`,
        badge: 'Zero Mean / Unit Var'
      }
    ];

    container.innerHTML = steps.map(s => `
      <div class="glass-card step-card">
        <div class="step-num">${s.num}</div>
        <div class="step-content">
          <div style="display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.35rem;">
            <h3 style="font-size: 1.1rem; color: #ffffff;">${s.title}</h3>
            <span class="pill-status pill-info">${s.badge}</span>
          </div>
          <p style="font-size: 0.88rem; color: var(--text-muted); line-height: 1.6;">${s.desc}</p>
        </div>
      </div>
    `).join('');
  }

  // ============================================================================
  // 3. Indicator Table
  // ============================================================================
  function renderIndicatorTable() {
    const tbody = document.querySelector('#indicatorTable tbody');
    if (!tbody) return;

    const meta = state.results.indicator_metadata;
    const audit = state.results.preprocessing_audit;
    const feats = state.results.features;

    tbody.innerHTML = feats.map(f => {
      const m = meta[f] || {};
      const missInfo = audit.indicator_missingness && audit.indicator_missingness[f];
      const coverage = missInfo ? (100 - missInfo.missing_pct).toFixed(1) : 'N/A';
      const catClass = m.type === 'undernutrition' ? 'pill-warning' : (m.type === 'overnutrition' ? 'pill-danger' : 'pill-success');
      
      return `
        <tr>
          <td><strong>${m.name || f}</strong></td>
          <td><code>${f}</code><br><small style="color: var(--text-dim);">${m.code || ''}</small></td>
          <td><span class="pill-status ${catClass}">${m.type || 'health'}</span></td>
          <td>${coverage}%</td>
          <td>${m.description || 'Health and nutrition metric'}</td>
        </tr>
      `;
    }).join('');
  }

  // ============================================================================
  // 4. Correlation Heatmap SVG
  // ============================================================================
  function renderCorrelationHeatmap() {
    const container = document.getElementById('correlationHeatmapSvg');
    if (!container) return;

    const feats = state.results.features;
    const corr = state.results.preprocessing_audit.correlation_matrix;
    const n = feats.length;

    const width = 640;
    const height = 560;
    const margin = { top: 70, right: 30, bottom: 90, left: 140 };
    const cellSize = Math.min((width - margin.left - margin.right) / n, (height - margin.top - margin.bottom) / n);

    let svg = `<svg class="svg-chart" viewBox="0 0 ${width} ${height}">`;
    svg += `<rect width="${width}" height="${height}" fill="transparent"/>`;

    // Cells
    for (let i = 0; i < n; i++) {
      const f1 = feats[i];
      // Y label
      svg += `<text x="${margin.left - 10}" y="${margin.top + i * cellSize + cellSize / 2 + 4}" fill="#94a3b8" font-size="11" text-anchor="end">${f1.replace(/_/g, ' ')}</text>`;
      // X label
      svg += `<text x="${margin.left + i * cellSize + cellSize / 2}" y="${margin.top - 12}" fill="#94a3b8" font-size="10" text-anchor="start" transform="rotate(-35, ${margin.left + i * cellSize + cellSize / 2}, ${margin.top - 12})">${f1.replace(/_/g, ' ')}</text>`;

      for (let j = 0; j < n; j++) {
        const f2 = feats[j];
        const val = corr[f1] ? corr[f1][f2] : 0;
        
        let fillColor = '#1e293b';
        if (val > 0) {
          const t = Math.min(1, val);
          fillColor = interpolateColor('#1e293b', '#f43f5e', t);
        } else {
          const t = Math.min(1, Math.abs(val));
          fillColor = interpolateColor('#1e293b', '#06b6d4', t);
        }

        const x = margin.left + j * cellSize;
        const y = margin.top + i * cellSize;

        svg += `<rect x="${x}" y="${y}" width="${cellSize - 2}" height="${cellSize - 2}" rx="3" fill="${fillColor}" stroke="rgba(255,255,255,0.06)" stroke-width="1">
          <title>${f1} vs ${f2}: r = ${val.toFixed(2)}</title>
        </rect>`;
        svg += `<text x="${x + cellSize / 2 - 1}" y="${y + cellSize / 2 + 4}" fill="${Math.abs(val) > 0.45 ? '#ffffff' : '#94a3b8'}" font-size="9.5" font-weight="${Math.abs(val) > 0.6 ? '700' : '400'}" text-anchor="middle">${val.toFixed(2)}</text>`;
      }
    }

    svg += `</svg>`;
    container.innerHTML = svg;
  }

  function interpolateColor(color1, color2, factor) {
    const c1 = hexToRgb(color1);
    const c2 = hexToRgb(color2);
    const r = Math.round(c1.r + factor * (c2.r - c1.r));
    const g = Math.round(c1.g + factor * (c2.g - c1.g));
    const b = Math.round(c1.b + factor * (c2.b - c1.b));
    return `rgb(${r}, ${g}, ${b})`;
  }

  function hexToRgb(hex) {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
      r: parseInt(result[1], 16),
      g: parseInt(result[2], 16),
      b: parseInt(result[3], 16)
    } : { r: 30, g: 41, b: 59 };
  }

  // ============================================================================
  // 5. Model Selection Charts (WCSS Elbow, Silhouette, DB, Stability)
  // ============================================================================
  function renderModelSelectionCharts() {
    renderElbowChart();
    renderValidationChart();
    renderStabilityChart();
  }

  function renderElbowChart() {
    const container = document.getElementById('elbowChartSvg');
    if (!container) return;

    const data = state.results.model_comparison;
    const eucData = data.filter(d => d.distance === 'euclidean').sort((a, b) => a.k - b.k);

    const width = 560;
    const height = 300;
    const margin = { top: 30, right: 30, bottom: 40, left: 60 };

    const minK = 3, maxK = 8;
    const maxWCSS = Math.max(...eucData.map(d => d.wcss));
    const minWCSS = Math.min(...eucData.map(d => d.wcss));

    const xScale = k => margin.left + ((k - minK) / (maxK - minK)) * (width - margin.left - margin.right);
    const yScale = v => margin.top + (1 - (v - minWCSS * 0.9) / (maxWCSS - minWCSS * 0.9)) * (height - margin.top - margin.bottom);

    let svg = `<svg class="svg-chart" viewBox="0 0 ${width} ${height}">`;
    svg += `<rect width="${width}" height="${height}" fill="transparent"/>`;

    // Grid lines
    for (let k = minK; k <= maxK; k++) {
      const x = xScale(k);
      svg += `<line x1="${x}" y1="${margin.top}" x2="${x}" y2="${height - margin.bottom}" stroke="#1e293b" stroke-width="1"/>`;
      svg += `<text x="${x}" y="${height - margin.bottom + 18}" fill="#94a3b8" font-size="11" text-anchor="middle">K=${k}</text>`;
    }

    // Euclidean line
    const eucPoints = eucData.map(d => `${xScale(d.k)},${yScale(d.wcss)}`).join(' ');
    svg += `<polyline fill="none" stroke="var(--cyan-accent)" stroke-width="2.5" points="${eucPoints}"/>`;

    // Elbow vertical marker (Kneedle K=6)
    const elbowK = state.results.metadata.kneedle_elbows.euclidean || 6;
    const elbowX = xScale(elbowK);
    svg += `<line x1="${elbowX}" y1="${margin.top}" x2="${elbowX}" y2="${height - margin.bottom}" stroke="var(--amber-accent)" stroke-width="1.8" stroke-dasharray="4,4"/>`;
    svg += `<text x="${elbowX}" y="${margin.top + 14}" fill="var(--amber-accent)" font-size="10" font-weight="700" text-anchor="middle">Elbow K=${elbowK}</text>`;

    // Points
    eucData.forEach(d => {
      const x = xScale(d.k);
      const y = yScale(d.wcss);
      const isSelected = d.config_id === state.results.metadata.selected_config_id;
      svg += `<circle cx="${x}" cy="${y}" r="${isSelected ? 6 : 4}" fill="${isSelected ? 'var(--amber-accent)' : 'var(--cyan-accent)'}" stroke="#ffffff" stroke-width="1.5">
        <title>K=${d.k}: WCSS = ${d.wcss.toFixed(1)}</title>
      </circle>`;
    });

    // Y Axis label
    svg += `<text x="${margin.left - 10}" y="${margin.top - 8}" fill="#94a3b8" font-size="10" text-anchor="start">Inertia (WCSS)</text>`;
    svg += `</svg>`;
    container.innerHTML = svg;
  }

  function renderValidationChart() {
    const container = document.getElementById('validationChartSvg');
    if (!container) return;

    const data = state.results.model_comparison;
    const eucData = data.filter(d => d.distance === 'euclidean').sort((a, b) => a.k - b.k);
    const manData = data.filter(d => d.distance === 'manhattan').sort((a, b) => a.k - b.k);

    const width = 560;
    const height = 300;
    const margin = { top: 30, right: 30, bottom: 40, left: 60 };

    const minK = 3, maxK = 8;
    const minSil = 0.10, maxSil = 0.32;

    const xScale = k => margin.left + ((k - minK) / (maxK - minK)) * (width - margin.left - margin.right);
    const yScale = s => margin.top + (1 - (s - minSil) / (maxSil - minSil)) * (height - margin.top - margin.bottom);

    let svg = `<svg class="svg-chart" viewBox="0 0 ${width} ${height}">`;
    svg += `<rect width="${width}" height="${height}" fill="transparent"/>`;

    // Grid lines
    for (let k = minK; k <= maxK; k++) {
      const x = xScale(k);
      svg += `<line x1="${x}" y1="${margin.top}" x2="${x}" y2="${height - margin.bottom}" stroke="#1e293b" stroke-width="1"/>`;
      svg += `<text x="${x}" y="${height - margin.bottom + 18}" fill="#94a3b8" font-size="11" text-anchor="middle">K=${k}</text>`;
    }

    // Lines
    const eucPoints = eucData.map(d => `${xScale(d.k)},${yScale(d.silhouette_euclidean)}`).join(' ');
    const manPoints = manData.map(d => `${xScale(d.k)},${yScale(d.silhouette_euclidean)}`).join(' ');

    svg += `<polyline fill="none" stroke="var(--cyan-accent)" stroke-width="2.2" points="${eucPoints}"/>`;
    svg += `<polyline fill="none" stroke="var(--rose-accent)" stroke-width="2" stroke-dasharray="4,4" points="${manPoints}"/>`;

    // Points
    eucData.forEach(d => {
      const x = xScale(d.k);
      const y = yScale(d.silhouette_euclidean);
      const isSelected = d.config_id === state.results.metadata.selected_config_id;
      svg += `<circle cx="${x}" cy="${y}" r="${isSelected ? 7 : 4}" fill="${isSelected ? 'var(--amber-accent)' : 'var(--cyan-accent)'}" stroke="#ffffff" stroke-width="1.5">
        <title>Euclidean K=${d.k}: Silhouette = ${d.silhouette_euclidean.toFixed(4)}</title>
      </circle>`;
    });

    manData.forEach(d => {
      const x = xScale(d.k);
      const y = yScale(d.silhouette_euclidean);
      svg += `<rect x="${x-3.5}" y="${y-3.5}" width="7" height="7" fill="var(--rose-accent)" stroke="#ffffff" stroke-width="1">
        <title>Manhattan K=${d.k}: Silhouette = ${d.silhouette_euclidean.toFixed(4)}</title>
      </rect>`;
    });

    // Legend
    svg += `<circle cx="${width - 170}" cy="${margin.top + 5}" r="4" fill="var(--cyan-accent)"/>`;
    svg += `<text x="${width - 155}" y="${margin.top + 9}" fill="#cbd5e1" font-size="10">Euclidean KMeans</text>`;
    svg += `<rect x="${width - 174}" y="${margin.top + 18}" width="7" height="7" fill="var(--rose-accent)"/>`;
    svg += `<text x="${width - 155}" y="${margin.top + 25}" fill="#cbd5e1" font-size="10">Manhattan KMedians</text>`;

    svg += `<text x="${margin.left - 10}" y="${margin.top - 8}" fill="#94a3b8" font-size="10" text-anchor="start">Silhouette (Euclidean Ruler)</text>`;
    svg += `</svg>`;
    container.innerHTML = svg;
  }

  function renderStabilityChart() {
    const container = document.getElementById('stabilityChartSvg');
    if (!container) return;

    const data = state.results.model_comparison;
    const eucData = data.filter(d => d.distance === 'euclidean').sort((a, b) => a.k - b.k);

    const width = 560;
    const height = 260;
    const margin = { top: 30, right: 30, bottom: 40, left: 60 };

    const minK = 3, maxK = 8;
    const xScale = k => margin.left + ((k - minK) / (maxK - minK)) * (width - margin.left - margin.right);
    const yScale = v => margin.top + (1 - (v - 0.3) / (1.0 - 0.3)) * (height - margin.top - margin.bottom);

    let svg = `<svg class="svg-chart" viewBox="0 0 ${width} ${height}">`;
    svg += `<rect width="${width}" height="${height}" fill="transparent"/>`;

    // Threshold line at 0.70 (Robust Stability)
    const y70 = yScale(0.70);
    svg += `<line x1="${margin.left}" y1="${y70}" x2="${width - margin.right}" y2="${y70}" stroke="var(--emerald-accent)" stroke-dasharray="3,3" stroke-width="1"/>`;
    svg += `<text x="${width - margin.right}" y="${y70 - 6}" fill="var(--emerald-accent)" font-size="9.5" text-anchor="end">High Stability (>0.70 ARI)</text>`;

    eucData.forEach(d => {
      const x = xScale(d.k);
      const y = yScale(d.stability_mean_ari);
      const yTop = yScale(d.stability_mean_ari + d.stability_std_ari);
      const yBot = yScale(d.stability_mean_ari - d.stability_std_ari);
      const isSelected = d.config_id === state.results.metadata.selected_config_id;

      // Error bar
      svg += `<line x1="${x}" y1="${yTop}" x2="${x}" y2="${yBot}" stroke="#64748b" stroke-width="1.5"/>`;
      svg += `<line x1="${x - 4}" y1="${yTop}" x2="${x + 4}" y2="${yTop}" stroke="#64748b" stroke-width="1.5"/>`;
      svg += `<line x1="${x - 4}" y1="${yBot}" x2="${x + 4}" y2="${yBot}" stroke="#64748b" stroke-width="1.5"/>`;

      // Point
      svg += `<circle cx="${x}" cy="${y}" r="${isSelected ? 7 : 5}" fill="${isSelected ? 'var(--amber-accent)' : 'var(--indigo-accent)'}" stroke="#ffffff" stroke-width="1.5">
        <title>K=${d.k}: ARI = ${d.stability_mean_ari.toFixed(3)} ± ${d.stability_std_ari.toFixed(3)}</title>
      </circle>`;
      svg += `<text x="${x}" y="${y - 12}" fill="${isSelected ? 'var(--amber-accent)' : '#cbd5e1'}" font-size="10" font-weight="${isSelected ? '700' : '500'}" text-anchor="middle">${d.stability_mean_ari.toFixed(2)}</text>`;
      svg += `<text x="${x}" y="${height - margin.bottom + 18}" fill="#94a3b8" font-size="11" text-anchor="middle">K=${d.k}</text>`;
    });

    svg += `<text x="${margin.left - 10}" y="${margin.top - 8}" fill="#94a3b8" font-size="10" text-anchor="start">Bootstrap Stability (Mean ARI)</text>`;
    svg += `</svg>`;
    container.innerHTML = svg;
  }

  // ============================================================================
  // 6. Full Model Configurations Table with Click-to-Activate
  // ============================================================================
  function renderModelTable() {
    const tbody = document.querySelector('#modelComparisonTable tbody');
    if (!tbody) return;

    const data = [...state.results.model_comparison].sort((a, b) => (a.composite_rank || 99) - (b.composite_rank || 99));
    const activeCfg = `${state.activeDistance}_k${state.activeK}`;

    tbody.innerHTML = data.map(d => {
      const isSelected = d.config_id === activeCfg;
      const isOptimal = d.config_id === state.results.metadata.selected_config_id;
      return `
        <tr class="${isSelected ? 'selected-row' : ''}" data-config="${d.config_id}" data-dist="${d.distance}" data-k="${d.k}" style="cursor: pointer;" title="Click to activate ${d.config_id} across dashboard">
          <td>
            <strong>${d.config_id}</strong>
            ${isOptimal ? '<span class="pill-status pill-success" style="margin-left: 6px;">OPTIMAL</span>' : ''}
            ${isSelected && !isOptimal ? '<span class="pill-status pill-info" style="margin-left: 6px;">ACTIVE</span>' : ''}
          </td>
          <td>${d.distance.toUpperCase()}</td>
          <td><strong>${d.k}</strong></td>
          <td>${d.silhouette_euclidean.toFixed(4)}</td>
          <td>${d.davies_bouldin_euclidean.toFixed(4)}</td>
          <td>${d.stability_mean_ari.toFixed(4)} <small style="color: var(--text-dim);">±${d.stability_std_ari.toFixed(3)}</small></td>
          <td>${d.min_cluster_size} ${d.min_cluster_size < 5 ? '<span class="pill-status pill-warning"><5</span>' : ''}</td>
          <td>${d.borderline_count}</td>
          <td>${d.composite_rank ? `<strong>#${d.composite_rank.toFixed(0)}</strong>` : 'N/A'}</td>
        </tr>
      `;
    }).join('');
  }

  function setupTableModelSwitching() {
    const table = document.getElementById('modelComparisonTable');
    if (!table) return;

    table.addEventListener('click', e => {
      const row = e.target.closest('tr[data-config]');
      if (!row) return;

      const dist = row.getAttribute('data-dist');
      const k = parseInt(row.getAttribute('data-k'), 10);

      switchActiveModel(dist, k);
    });
  }

  function switchActiveModel(dist, k) {
    state.activeDistance = dist;
    state.activeK = k;

    // Update Distance Buttons
    document.querySelectorAll('[data-dist]').forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('data-dist') === dist);
    });

    // Update K Buttons
    document.querySelectorAll('[data-k]').forEach(btn => {
      btn.classList.toggle('active', parseInt(btn.getAttribute('data-k'), 10) === k);
    });

    // Update Model Table Selection Highlights
    renderModelTable();

    // Re-render PCA Explorer
    renderPCAExplorer();

    // Update Simulator outputs
    updateSimulator();
  }

  // ============================================================================
  // 7. Interactive 2D PCA Explorer (with Live Pulsing Simulated Marker)
  // ============================================================================
  function renderPCAExplorer() {
    const container = document.getElementById('pcaScatterSvg');
    const tooltip = document.getElementById('pcaTooltip');
    if (!container || !tooltip) return;

    const width = 860;
    const height = 540;
    const margin = { top: 40, right: 40, bottom: 50, left: 60 };

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
    svg += `<line x1="${xScale(xMin)}" y1="${yZero}" x2="${xScale(xMax)}" y2="${yZero}" stroke="#334155" stroke-width="1" stroke-dasharray="3,3"/>`;
    svg += `<line x1="${xZero}" y1="${yScale(yMin)}" x2="${xZero}" y2="${yScale(yMax)}" stroke="#334155" stroke-width="1" stroke-dasharray="3,3"/>`;

    // Feature Loadings Vectors (Biplot)
    if (state.showLoadings && pcaMeta.loadings) {
      const scaleLoadings = 3.8;
      for (const [feat, coords] of Object.entries(pcaMeta.loadings)) {
        const vx = xScale(coords[0] * scaleLoadings);
        const vy = yScale(coords[1] * scaleLoadings);
        svg += `<line x1="${xZero}" y1="${yZero}" x2="${vx}" y2="${vy}" stroke="rgba(251, 191, 36, 0.6)" stroke-width="1.4"/>`;
        svg += `<circle cx="${vx}" cy="${vy}" r="2.5" fill="var(--amber-accent)"/>`;
        svg += `<text x="${vx + 4}" y="${vy + 3}" fill="#fde68a" font-size="9" font-weight="600">${feat.replace(/_/g, ' ')}</text>`;
      }
    }

    // Country Scatter Dots
    filtered.forEach(c => {
      const cx = xScale(c.pca_x);
      const cy = yScale(c.pca_y);
      const clId = c[`cluster_${activeCfg}`] !== undefined ? c[`cluster_${activeCfg}`] : c.cluster;
      const dotColor = PALETTE[clId % PALETTE.length];
      const isBorderline = c.is_borderline;

      svg += `<circle 
        cx="${cx}" cy="${cy}" r="${isBorderline ? 6 : 5}" 
        fill="${dotColor}" 
        stroke="${isBorderline ? '#fbbf24' : '#ffffff'}" 
        stroke-width="${isBorderline ? 2 : 0.8}" 
        opacity="0.88"
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

      svg += `
        <g id="simulatedPcaGroup" style="cursor: pointer;">
          <!-- Pulsing Outer Ring -->
          <circle cx="${simX}" cy="${simY}" r="16" fill="${simClColor}" opacity="0.3" class="sim-point"></circle>
          <circle cx="${simX}" cy="${simY}" r="9" fill="${simClColor}" stroke="#ffffff" stroke-width="2.5"></circle>
          <circle cx="${simX}" cy="${simY}" r="3" fill="#ffffff"></circle>
          <!-- Callout Label -->
          <rect x="${simX + 12}" y="${simY - 14}" width="130" height="22" rx="4" fill="rgba(15, 23, 42, 0.9)" stroke="${simClColor}" stroke-width="1.2"></rect>
          <text x="${simX + 18}" y="${simY + 1}" fill="#ffffff" font-size="10" font-weight="700">★ SIMULATED NATION</text>
        </g>
      `;
    }

    // Axis Labels
    svg += `<text x="${width / 2}" y="${height - 12}" fill="#94a3b8" font-size="12" font-weight="600" text-anchor="middle">Principal Component 1 (${(pcaMeta.variance_explained[0]*100).toFixed(1)}% Variance Explained - Undernutrition Axis)</text>`;
    svg += `<text x="${margin.left - 12}" y="${margin.top - 14}" fill="#94a3b8" font-size="11" font-weight="600" text-anchor="start">PC2 (${(pcaMeta.variance_explained[1]*100).toFixed(1)}% Variance)</text>`;

    svg += `</svg>`;
    container.innerHTML = svg;

    // Attach scatter hover & click handlers
    attachPCATooltipEvents(container, tooltip, countries, activeCfg);
    renderPCALegend(activeCfg);
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
          <div class="tooltip-row"><span>Silhouette:</span> <span class="tooltip-val">${c.silhouette.toFixed(3)} ${c.is_borderline ? '⚠️ Borderline' : ''}</span></div>
          <div style="border-top: 1px solid rgba(255,255,255,0.1); margin: 6px 0; padding-top: 4px;">
            <div class="tooltip-row"><span>Stunting:</span> <span class="tooltip-val">${c.indicators.stunting || 'N/A'}%</span></div>
            <div class="tooltip-row"><span>Wasting:</span> <span class="tooltip-val">${c.indicators.wasting || 'N/A'}%</span></div>
            <div class="tooltip-row"><span>Child Overweight:</span> <span class="tooltip-val">${c.indicators.child_overweight || 'N/A'}%</span></div>
            <div class="tooltip-row"><span>Adult Obesity:</span> <span class="tooltip-val">${c.indicators.adult_obesity || 'N/A'}%</span></div>
            <div class="tooltip-row"><span>GDP per cap:</span> <span class="tooltip-val">${c.gdp_per_capita ? '$' + Math.round(c.gdp_per_capita).toLocaleString() : 'N/A'}</span></div>
          </div>
          <div style="margin-top: 6px; font-size: 0.72rem; color: var(--amber-accent); text-align: center;">Click dot to inspect full profile &rarr;</div>
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
        const c = countryMap.get(iso);
        dot.setAttribute('r', c && c.is_borderline ? '6' : '5');
      });

      dot.addEventListener('click', () => {
        const iso = dot.getAttribute('data-iso');
        openCountryDrawer(iso);
      });
    });

    // Simulated marker click
    const simGroup = container.querySelector('#simulatedPcaGroup');
    if (simGroup) {
      simGroup.addEventListener('click', () => {
        const simSec = document.getElementById('simulator');
        if (simSec) simSec.scrollIntoView({ behavior: 'smooth' });
      });
    }
  }

  function renderPCALegend(activeCfg) {
    const legendContainer = document.getElementById('pcaClusterLegend');
    if (!legendContainer) return;

    let itemsHtml = '';
    for (let cl = 0; cl < state.activeK; cl++) {
      const color = PALETTE[cl % PALETTE.length];
      itemsHtml += `
        <div style="display: flex; align-items: center; gap: 0.5rem; font-size: 0.82rem; margin-right: 1.25rem; margin-bottom: 0.35rem;">
          <span style="width: 10px; height: 10px; border-radius: 50%; background: ${color}; display: inline-block;"></span>
          <span style="color: #e2e8f0; font-weight: 600;">Cluster ${cl}</span>
        </div>
      `;
    }
    // Add simulated marker badge to legend
    itemsHtml += `
      <div style="display: flex; align-items: center; gap: 0.5rem; font-size: 0.82rem; margin-bottom: 0.35rem;">
        <span style="width: 12px; height: 12px; border-radius: 50%; background: var(--amber-accent); border: 2px solid #ffffff; display: inline-block;"></span>
        <span style="color: var(--amber-accent); font-weight: 700;">★ Simulated Nation</span>
      </div>
    `;
    legendContainer.innerHTML = itemsHtml;
  }

  // ============================================================================
  // 8. "Play Progression" Animation Engine (K = 3 to 8)
  // ============================================================================
  function setupPlayProgression() {
    const btn = document.getElementById('playProgressionBtn');
    const icon = document.getElementById('playProgressionIcon');
    const text = document.getElementById('playProgressionText');
    if (!btn) return;

    btn.addEventListener('click', () => {
      if (state.isPlayingProgression) {
        // Stop playback
        stopPlayProgression();
      } else {
        // Start playback
        startPlayProgression();
      }
    });

    function startPlayProgression() {
      state.isPlayingProgression = true;
      btn.classList.add('active');
      if (icon) icon.textContent = '⏸';
      if (text) text.textContent = 'Pause Progression';

      state.progressionTimer = setInterval(() => {
        let nextK = state.activeK + 1;
        if (nextK > 8) nextK = 3;
        switchActiveModel(state.activeDistance, nextK);
      }, 1600);
    }

    function stopPlayProgression() {
      state.isPlayingProgression = false;
      clearInterval(state.progressionTimer);
      state.progressionTimer = null;
      btn.classList.remove('active');
      if (icon) icon.textContent = '▶';
      if (text) text.textContent = 'Play Progression (K=3 to 8)';
    }
  }

  // ============================================================================
  // 9. LIVE COUNTRY NUTRITION PROFILE SIMULATOR
  // ============================================================================
  function renderSimulator() {
    const container = document.getElementById('simulatorSlidersContainer');
    if (!container) return;

    container.innerHTML = INDICATOR_CONFIGS.map(cfg => {
      const curVal = state.simulatedValues[cfg.key] !== undefined ? state.simulatedValues[cfg.key] : 15;
      return `
        <div class="sim-slider-group">
          <div class="sim-slider-header">
            <span class="sim-slider-name">${cfg.label}</span>
            <span class="sim-slider-val" id="val_${cfg.key}">${curVal.toFixed(1)}${cfg.unit}</span>
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

    // Attach slider change listeners
    container.querySelectorAll('.sim-slider').forEach(slider => {
      slider.addEventListener('input', e => {
        const key = slider.getAttribute('data-key');
        const unit = slider.getAttribute('data-unit');
        const val = parseFloat(slider.value);
        state.simulatedValues[key] = val;

        const valLabel = document.getElementById(`val_${key}`);
        if (valLabel) valLabel.textContent = `${val.toFixed(1)}${unit}`;

        updateSimulator();
      });
    });

    // Preset buttons
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

    // Jump to PCA button
    const jumpBtn = document.getElementById('simJumpToPcaBtn');
    if (jumpBtn) {
      jumpBtn.addEventListener('click', () => {
        const pcaSec = document.getElementById('pca-explorer');
        if (pcaSec) {
          pcaSec.scrollIntoView({ behavior: 'smooth' });
          // Highlight simulated marker
          setTimeout(() => {
            const marker = document.querySelector('#simulatedPcaGroup');
            if (marker) {
              marker.style.transition = 'transform 0.4s ease';
              marker.style.transform = 'scale(1.4)';
              setTimeout(() => { marker.style.transform = 'scale(1)'; }, 500);
            }
          }, 600);
        }
      });
    }

    // Run initial computation
    updateSimulator();
  }

  function loadTypologyPreset(presetKey) {
    let vals = {};
    if (presetKey === 'global_mean') {
      const mean = state.results.scaler ? state.results.scaler.mean : {};
      INDICATOR_CONFIGS.forEach(cfg => {
        vals[cfg.key] = mean[cfg.key] !== undefined ? Math.round(mean[cfg.key] * 10) / 10 : 15;
      });
    } else if (TYPOLOGY_PRESETS[presetKey]) {
      vals = TYPOLOGY_PRESETS[presetKey].values;
    }

    // Update state and UI sliders
    for (const [k, v] of Object.entries(vals)) {
      state.simulatedValues[k] = v;
      const slider = document.getElementById(`slider_${k}`);
      const valLabel = document.getElementById(`val_${k}`);
      if (slider) slider.value = v;
      if (valLabel) {
        const cfg = INDICATOR_CONFIGS.find(c => c.key === k);
        valLabel.textContent = `${v.toFixed(1)}${cfg ? cfg.unit : '%'}`;
      }
    }

    updateSimulator();
  }

  function updateSimulator() {
    if (!state.results || !state.results.scaler || !state.results.cluster_centers) return;

    const feats = state.results.features;
    const mean = state.results.scaler.mean;
    const scale = state.results.scaler.scale;
    const activeCfg = `${state.activeDistance}_k${state.activeK}`;
    const centers = state.results.cluster_centers[activeCfg];

    if (!centers || centers.length === 0) return;

    // 1. Compute Standardized Z-Scores
    const zVec = feats.map(f => {
      const raw = state.simulatedValues[f] !== undefined ? state.simulatedValues[f] : mean[f];
      return (raw - mean[f]) / scale[f];
    });

    // 2. Compute Distances to All Cluster Centroids in Active Model
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

    // Find closest cluster
    distances.sort((a, b) => a.distance - b.distance);
    const closestCluster = distances[0].cluster_id;
    state.simulatedCluster = closestCluster;

    // 3. Project to 2D PCA Space
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

    // 4. Update UI Outputs
    // Active Model Badge
    const modelBadge = document.getElementById('simActiveModelBadge');
    if (modelBadge) {
      modelBadge.textContent = `${state.activeDistance.toUpperCase()} (K = ${state.activeK})`;
    }

    // Cluster Prediction Box
    const clusterOut = document.getElementById('simClusterOutputBox');
    if (clusterOut) {
      const color = PALETTE[closestCluster % PALETTE.length];
      const clName = getClusterDisplayName(closestCluster, state.activeDistance, state.activeK);

      clusterOut.innerHTML = `
        <div style="display: flex; align-items: center; gap: 0.75rem;">
          <span style="width: 14px; height: 14px; border-radius: 50%; background: ${color}; box-shadow: 0 0 10px ${color};"></span>
          <div>
            <div style="font-size: 0.72rem; color: var(--text-dim); text-transform: uppercase;">Predicted Typology</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #ffffff;">${clName}</div>
          </div>
        </div>
        <span class="pill-status" style="background: ${color}22; color: ${color}; border: 1px solid ${color}44; font-size: 0.85rem; font-weight: 700;">
          Cluster ${closestCluster}
        </span>
      `;
    }

    // Distance Bars
    const distContainer = document.getElementById('simDistanceBarsContainer');
    if (distContainer) {
      const maxDist = Math.max(...distances.map(d => d.distance), 1);
      distContainer.innerHTML = distances.map(d => {
        const color = PALETTE[d.cluster_id % PALETTE.length];
        const clName = getClusterDisplayName(d.cluster_id, state.activeDistance, state.activeK);
        const pct = Math.min(100, Math.max(12, (1 - d.distance / (maxDist * 1.2)) * 100));
        const isMin = d.cluster_id === closestCluster;

        return `
          <div class="sim-dist-item">
            <div class="sim-dist-meta">
              <span style="color: ${isMin ? '#ffffff' : 'var(--text-muted)'}; font-weight: ${isMin ? '700' : '500'};">
                ${isMin ? '★ ' : ''}C${d.cluster_id}: ${clName.slice(0, 24)}
              </span>
              <span style="color: ${color}; font-weight: 700;">d = ${d.distance.toFixed(2)}</span>
            </div>
            <div class="bar-track">
              <div class="bar-fill" style="width: ${pct}%; background: ${color};"></div>
            </div>
          </div>
        `;
      }).join('');
    }

    // 5. Compute Closest Real Countries in 9D Space
    computeClosestRealCountries(zVec);

    // 6. Update PCA Explorer Scatter Map with Live Simulated Point
    renderPCAExplorer();
  }

  function getClusterDisplayName(clId, distance, k) {
    if (k === 3 && distance === 'euclidean' && state.results.cluster_profiles) {
      const p = state.results.cluster_profiles.find(cp => cp.cluster_id === clId);
      if (p) return p.name;
    }
    // Dynamic fallback name based on cluster profile means if available
    return `Cluster ${clId} Partition (${distance.toUpperCase()})`;
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
        const f = feats[i];
        const cz = (c.indicators[f] - mean[f]) / scale[f];
        const diff = zVec[i] - cz;
        d += diff * diff;
      }
      return {
        country: c,
        dist: Math.sqrt(d)
      };
    });

    countryDistances.sort((a, b) => a.dist - b.dist);
    const top3 = countryDistances.slice(0, 3);

    listContainer.innerHTML = top3.map((item, idx) => {
      const c = item.country;
      const clColor = PALETTE[c.cluster % PALETTE.length];
      return `
        <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(255,255,255,0.03); padding: 0.4rem 0.6rem; border-radius: var(--radius-sm); border: 1px solid var(--border-card);">
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span style="font-size: 0.75rem; color: var(--amber-accent); font-weight: 700;">#${idx + 1}</span>
            <span class="country-pill" data-drawer-iso="${c.country_code}" style="cursor: pointer;">
              ${c.country_name} (${c.country_code})
            </span>
            <span style="font-size: 0.72rem; color: var(--text-dim);">${c.region}</span>
          </div>
          <span style="font-size: 0.75rem; color: var(--text-muted); font-family: var(--font-heading); font-weight: 600;">
            dist: ${item.dist.toFixed(2)}
          </span>
        </div>
      `;
    }).join('');

    // Attach drawer clicks to the closest countries pills
    listContainer.querySelectorAll('[data-drawer-iso]').forEach(pill => {
      pill.addEventListener('click', () => {
        const iso = pill.getAttribute('data-drawer-iso');
        openCountryDrawer(iso);
      });
    });
  }

  // ============================================================================
  // 10. Interactive Country Detail Inspector Drawer
  // ============================================================================
  function setupDrawer() {
    const backdrop = document.getElementById('drawerBackdrop');
    const closeBtn = document.getElementById('drawerCloseBtn');

    if (backdrop) backdrop.addEventListener('click', closeCountryDrawer);
    if (closeBtn) closeBtn.addEventListener('click', closeCountryDrawer);

    // Escape key to close
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape') closeCountryDrawer();
    });
  }

  function openCountryDrawer(iso) {
    if (!state.results || !state.results.countries) return;

    const c = state.results.countries.find(item => item.country_code === iso);
    if (!c) return;

    state.activeCountryIso = iso;

    const drawer = document.getElementById('countryDrawer');
    const backdrop = document.getElementById('drawerBackdrop');
    const content = document.getElementById('drawerContent');

    if (!drawer || !backdrop || !content) return;

    const activeCfg = `${state.activeDistance}_k${state.activeK}`;
    const clId = c[`cluster_${activeCfg}`] !== undefined ? c[`cluster_${activeCfg}`] : c.cluster;
    const clColor = PALETTE[clId % PALETTE.length];
    const clName = c.cluster_name || `Cluster ${clId}`;

    const mean = state.results.scaler.mean;

    // Build Indicators Comparison List
    const indicatorBarsHtml = INDICATOR_CONFIGS.map(cfg => {
      const val = c.indicators[cfg.key];
      const gMean = mean[cfg.key];
      const maxVal = cfg.max;
      const pct = Math.min(100, Math.max(6, (val / maxVal) * 100));
      const meanPct = Math.min(100, Math.max(6, (gMean / maxVal) * 100));

      const isHigher = val > gMean;
      const diffStr = (val - gMean).toFixed(1);

      return `
        <div style="margin-bottom: 0.85rem;">
          <div style="display: flex; justify-content: space-between; font-size: 0.82rem; margin-bottom: 0.25rem;">
            <span style="color: #cbd5e1; font-weight: 500;">${cfg.label}</span>
            <span>
              <strong style="color: #ffffff;">${val !== undefined ? val.toFixed(1) + cfg.unit : 'N/A'}</strong>
              <small style="color: ${isHigher ? 'var(--rose-accent)' : 'var(--cyan-accent)'}; margin-left: 4px;">
                (${isHigher ? '+' : ''}${diffStr}${cfg.unit} vs global)
              </small>
            </span>
          </div>
          <div class="bar-track" style="position: relative; height: 8px;">
            <div class="bar-fill" style="width: ${pct}%; background: ${clColor};"></div>
            <!-- Global Average Marker -->
            <div style="position: absolute; left: ${meanPct}%; top: -2px; width: 2px; height: 12px; background: #ffffff; box-shadow: 0 0 4px #ffffff;" title="Global Average: ${gMean.toFixed(1)}${cfg.unit}"></div>
          </div>
        </div>
      `;
    }).join('');

    content.innerHTML = `
      <div style="margin-bottom: 1.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
          <div>
            <div style="font-size: 0.8rem; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.05em;">Sovereign State Audit</div>
            <h2 style="font-size: 1.6rem; color: #ffffff; font-family: var(--font-heading); margin-top: 0.2rem;">${c.country_name}</h2>
          </div>
          <span style="font-size: 1.1rem; padding: 0.2rem 0.6rem; border-radius: 6px; background: rgba(255,255,255,0.08); font-weight: 700;">${c.country_code}</span>
        </div>

        <div style="display: flex; align-items: center; gap: 0.6rem; flex-wrap: wrap; margin-top: 0.5rem;">
          <span class="pill-status" style="background: ${clColor}22; color: ${clColor}; border: 1px solid ${clColor}44; font-weight: 700;">
            C${clId}: ${clName}
          </span>
          <span class="pill-status pill-info">${c.region}</span>
          <span class="pill-status pill-warning">${c.income_group || 'Income N/A'}</span>
        </div>
      </div>

      <!-- Quick Metrics Grid -->
      <div class="drawer-metric-grid">
        <div class="drawer-metric-box">
          <div class="drawer-metric-label">GDP Per Capita</div>
          <div class="drawer-metric-val">${c.gdp_per_capita ? '$' + Math.round(c.gdp_per_capita).toLocaleString() : 'N/A'}</div>
        </div>
        <div class="drawer-metric-box">
          <div class="drawer-metric-label">Silhouette Score</div>
          <div class="drawer-metric-val" style="color: ${c.is_borderline ? 'var(--amber-accent)' : 'var(--emerald-accent)'};">
            ${c.silhouette.toFixed(3)}
          </div>
        </div>
        <div class="drawer-metric-box">
          <div class="drawer-metric-label">PCA Coordinate 1</div>
          <div class="drawer-metric-val">${c.pca_x.toFixed(2)}</div>
        </div>
        <div class="drawer-metric-box">
          <div class="drawer-metric-label">PCA Coordinate 2</div>
          <div class="drawer-metric-val">${c.pca_y.toFixed(2)}</div>
        </div>
      </div>

      ${c.is_borderline ? `
        <div style="background: rgba(251, 191, 36, 0.1); border-left: 3px solid var(--amber-accent); padding: 0.75rem 1rem; border-radius: 4px; margin-bottom: 1.5rem; font-size: 0.82rem; color: #fde68a;">
          ⚠️ <strong>Borderline Nation:</strong> Low silhouette score indicates this country lies on the transition boundary between malnutrition macro-clusters.
        </div>
      ` : ''}

      <!-- Transfer to Simulator Action CTA -->
      <div style="margin-bottom: 1.5rem;">
        <button id="drawerLoadSimulatorBtn" class="btn-action" style="width: 100%; justify-content: center; padding: 0.75rem; background: rgba(6, 182, 212, 0.15); border-color: rgba(6, 182, 212, 0.4); color: var(--cyan-accent); font-size: 0.9rem;">
          ⚡ Load ${c.country_name}'s Indicators into Simulator
        </button>
      </div>

      <!-- Indicator Breakdown vs Global Mean -->
      <div>
        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.75rem;">
          <h4 style="font-size: 0.95rem; color: #ffffff;">9 Health Indicators vs. Global Baseline</h4>
          <span style="font-size: 0.72rem; color: var(--text-dim);">White tick = Global Mean</span>
        </div>
        <div>
          ${indicatorBarsHtml}
        </div>
      </div>
    `;

    // Hook up Load into Simulator button
    const loadBtn = document.getElementById('drawerLoadSimulatorBtn');
    if (loadBtn) {
      loadBtn.addEventListener('click', () => {
        // Copy real indicators into simulated values
        for (const [k, v] of Object.entries(c.indicators)) {
          state.simulatedValues[k] = v;
          const slider = document.getElementById(`slider_${k}`);
          const valLabel = document.getElementById(`val_${k}`);
          if (slider) slider.value = v;
          if (valLabel) {
            const cfg = INDICATOR_CONFIGS.find(cfg => cfg.key === k);
            valLabel.textContent = `${v.toFixed(1)}${cfg ? cfg.unit : '%'}`;
          }
        }

        updateSimulator();
        closeCountryDrawer();

        const simSec = document.getElementById('simulator');
        if (simSec) simSec.scrollIntoView({ behavior: 'smooth' });
      });
    }

    // Open drawer & backdrop
    backdrop.classList.add('active');
    drawer.classList.add('active');
  }

  function closeCountryDrawer() {
    const drawer = document.getElementById('countryDrawer');
    const backdrop = document.getElementById('drawerBackdrop');
    if (drawer) drawer.classList.remove('active');
    if (backdrop) backdrop.classList.remove('active');
    state.activeCountryIso = null;
  }

  // ============================================================================
  // 11. Hierarchical Clustering Section & Dendrogram
  // ============================================================================
  function renderHierarchicalSection() {
    renderDendrogram();
    renderHierarchicalTable();
  }

  function renderDendrogram() {
    const container = document.getElementById('dendrogramSvg');
    if (!container) return;

    const ddata = state.results.dendrogram_data;
    if (!ddata || !ddata.icoord) {
      container.innerHTML = '<p style="color: var(--text-muted); text-align: center;">Dendrogram data not available.</p>';
      return;
    }

    const width = 860;
    const height = 360;
    const margin = { top: 30, right: 30, bottom: 40, left: 60 };

    const allX = ddata.icoord.flat();
    const allY = ddata.dcoord.flat();
    const xMin = Math.min(...allX);
    const xMax = Math.max(...allX);
    const yMax = Math.max(...allY) * 1.05;

    const xScale = x => margin.left + ((x - xMin) / (xMax - xMin)) * (width - margin.left - margin.right);
    const yScale = y => height - margin.bottom - (y / yMax) * (height - margin.top - margin.bottom);

    let svg = `<svg class="svg-chart" viewBox="0 0 ${width} ${height}">`;
    svg += `<rect width="${width}" height="${height}" fill="transparent"/>`;

    // Horizontal Cut Height Line
    const cutY = yScale(ddata.cut_height);
    svg += `<line x1="${margin.left}" y1="${cutY}" x2="${width - margin.right}" y2="${cutY}" stroke="var(--rose-accent)" stroke-width="2" stroke-dasharray="5,4"/>`;
    svg += `<text x="${width - margin.right}" y="${cutY - 6}" fill="var(--rose-accent)" font-size="10.5" font-weight="700" text-anchor="end">Cut Height = ${ddata.cut_height.toFixed(2)} (K=${state.results.metadata.selected_k})</text>`;

    // Dendrogram tree links
    for (let i = 0; i < ddata.icoord.length; i++) {
      const xs = ddata.icoord[i];
      const ys = ddata.dcoord[i];
      const cCode = ddata.color_list[i] || '#64748b';
      
      const pts = `${xScale(xs[0])},${yScale(ys[0])} ${xScale(xs[1])},${yScale(ys[1])} ${xScale(xs[2])},${yScale(ys[2])} ${xScale(xs[3])},${yScale(ys[3])}`;
      svg += `<polyline fill="none" stroke="${cCode === 'C0' ? '#64748b' : (cCode === 'C1' ? 'var(--cyan-accent)' : (cCode === 'C2' ? 'var(--rose-accent)' : 'var(--emerald-accent)'))}" stroke-width="1.3" points="${pts}"/>`;
    }

    svg += `<text x="${margin.left - 10}" y="${margin.top - 8}" fill="#94a3b8" font-size="10" text-anchor="start">Linkage Merge Distance</text>`;
    svg += `</svg>`;
    container.innerHTML = svg;
  }

  function renderHierarchicalTable() {
    const tbody = document.querySelector('#hierarchicalTable tbody');
    if (!tbody) return;

    const data = state.results.hierarchical_comparison || [];
    tbody.innerHTML = data.map(d => `
      <tr>
        <td><strong>${d.name}</strong></td>
        <td>${d.linkage.toUpperCase()}</td>
        <td><code>${d.metric}</code></td>
        <td><strong>${d.cophenetic_correlation.toFixed(4)}</strong></td>
        <td>${d.silhouette.toFixed(4)}</td>
        <td>${d.davies_bouldin.toFixed(4)}</td>
        <td>${d.ari_vs_kmeans.toFixed(4)}</td>
        <td>${d.cut_height.toFixed(2)}</td>
      </tr>
    `).join('');
  }

  // ============================================================================
  // 12. Cluster Profile Cards & Heatmap (with Drawer Hooks)
  // ============================================================================
  function renderClusterProfiles() {
    const grid = document.getElementById('clusterProfilesGrid');
    if (!grid) return;

    const profiles = state.results.cluster_profiles;

    grid.innerHTML = profiles.map(p => {
      const color = PALETTE[p.cluster_id % PALETTE.length];
      
      // Typical countries pills (clickable to open drawer)
      const typicalPills = p.typical_countries.map(tc => `
        <span class="country-pill" data-drawer-iso="${tc.country_code}" title="Click to view ${tc.country_name} in detail inspector">
          ${tc.country_name} (${tc.country_code})
        </span>
      `).join('');

      // Top regions
      const regionEntries = Object.entries(p.region_mix).sort((a,b) => b[1]-a[1]).slice(0, 3);
      const regionStr = regionEntries.map(([r, c]) => `${r} (${c})`).join(', ');

      // Income mix
      const incomeEntries = Object.entries(p.income_mix).sort((a,b) => b[1]-a[1]).slice(0, 2);
      const incomeStr = incomeEntries.map(([inc, c]) => `${inc} (${c})`).join(', ');

      // Key indicators
      const barList = [
        { name: 'Child Stunting', val: p.raw_means.stunting, z: p.z_means.stunting, max: 45, unit: '%' },
        { name: 'Child Wasting', val: p.raw_means.wasting, z: p.z_means.wasting, max: 15, unit: '%' },
        { name: 'Child Anaemia', val: p.raw_means.anaemia_children, z: p.z_means.anaemia_children, max: 70, unit: '%' },
        { name: 'Adult Obesity', val: p.raw_means.adult_obesity, z: p.z_means.adult_obesity, max: 40, unit: '%' },
        { name: 'Child Overweight', val: p.raw_means.child_overweight, z: p.z_means.child_overweight, max: 15, unit: '%' },
      ];

      const barsHtml = barList.map(b => {
        const pct = Math.min(100, Math.max(8, (b.val / b.max) * 100));
        const barColor = b.z > 0.5 ? 'var(--rose-accent)' : (b.z < -0.5 ? 'var(--cyan-accent)' : 'var(--indigo-accent)');
        return `
          <div class="indicator-bar-item">
            <div class="bar-meta">
              <span class="bar-name">${b.name}</span>
              <span class="bar-value">${b.val !== undefined ? b.val.toFixed(1) + b.unit : 'N/A'} <small style="color: #64748b;">(Z: ${b.z > 0 ? '+' : ''}${b.z.toFixed(2)})</small></span>
            </div>
            <div class="bar-track">
              <div class="bar-fill" style="width: ${pct}%; background: ${barColor};"></div>
            </div>
          </div>
        `;
      }).join('');

      return `
        <div class="glass-card cluster-card" style="border-top-color: ${color};">
          <div>
            <div class="cluster-card-header">
              <div class="cluster-title-wrap">
                <h3>${p.name}</h3>
                <div class="cluster-size-tag">${p.size} countries (${p.percentage}% of analyzed cohort)</div>
              </div>
              <span class="cluster-badge" style="background: ${color}22; color: ${color}; border: 1px solid ${color}44;">C${p.cluster_id}</span>
            </div>
            <p class="cluster-narrative">${p.narrative}</p>
            <div class="indicator-bars-list">
              ${barsHtml}
            </div>
          </div>
          <div>
            <div style="font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-dim); margin-bottom: 0.25rem;">Context Metrics</div>
            <div style="font-size: 0.85rem; color: #cbd5e1; margin-bottom: 0.2rem;"><strong>Median GDP:</strong> ${p.median_gdp_per_capita ? '$' + p.median_gdp_per_capita.toLocaleString() : 'N/A'}</div>
            <div style="font-size: 0.82rem; color: var(--text-muted); margin-bottom: 0.2rem;"><strong>Dominant Regions:</strong> ${regionStr}</div>
            <div style="font-size: 0.82rem; color: var(--text-muted); margin-bottom: 0.6rem;"><strong>Income Groups:</strong> ${incomeStr}</div>
            <div style="font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-dim);">Representative Nations (Centroid Neighbors)</div>
            <div class="typical-countries-pills">
              ${typicalPills}
            </div>
          </div>
        </div>
      `;
    }).join('');

    // Attach click listeners to typical country pills
    grid.querySelectorAll('[data-drawer-iso]').forEach(pill => {
      pill.addEventListener('click', e => {
        e.stopPropagation();
        const iso = pill.getAttribute('data-drawer-iso');
        openCountryDrawer(iso);
      });
    });

    renderZScoreHeatmap();
  }

  function renderZScoreHeatmap() {
    const container = document.getElementById('profileHeatmapSvg');
    if (!container) return;

    const profiles = state.results.cluster_profiles;
    const feats = state.results.features;
    const nC = profiles.length;
    const nF = feats.length;

    const width = 860;
    const height = 260;
    const margin = { top: 50, right: 30, bottom: 40, left: 160 };

    const cellW = (width - margin.left - margin.right) / nF;
    const cellH = (height - margin.top - margin.bottom) / nC;

    let svg = `<svg class="svg-chart" viewBox="0 0 ${width} ${height}">`;
    svg += `<rect width="${width}" height="${height}" fill="transparent"/>`;

    // Header labels (features)
    for (let j = 0; j < nF; j++) {
      const f = feats[j];
      svg += `<text x="${margin.left + j * cellW + cellW / 2}" y="${margin.top - 12}" fill="#94a3b8" font-size="10" font-weight="600" text-anchor="middle">${f.replace(/_/g, ' ')}</text>`;
    }

    // Rows (Clusters)
    for (let i = 0; i < nC; i++) {
      const p = profiles[i];
      svg += `<text x="${margin.left - 12}" y="${margin.top + i * cellH + cellH / 2 + 4}" fill="#f8fafc" font-size="11" font-weight="700" text-anchor="end">C${p.cluster_id}: ${p.name.slice(0, 18)}</text>`;

      for (let j = 0; j < nF; j++) {
        const f = feats[j];
        const z = p.z_means[f] !== undefined ? p.z_means[f] : 0;
        
        let fillColor = '#1e293b';
        if (z > 0) {
          const t = Math.min(1, z / 1.5);
          fillColor = interpolateColor('#1e293b', '#f43f5e', t);
        } else {
          const t = Math.min(1, Math.abs(z) / 1.5);
          fillColor = interpolateColor('#1e293b', '#06b6d4', t);
        }

        const x = margin.left + j * cellW;
        const y = margin.top + i * cellH;

        svg += `<rect x="${x}" y="${y}" width="${cellW - 2}" height="${cellH - 2}" rx="4" fill="${fillColor}" stroke="rgba(255,255,255,0.06)" stroke-width="1">
          <title>${p.name} - ${f}: Z = ${z > 0 ? '+' : ''}${z.toFixed(2)}</title>
        </rect>`;
        svg += `<text x="${x + cellW / 2}" y="${y + cellH / 2 + 4}" fill="${Math.abs(z) > 0.6 ? '#ffffff' : '#cbd5e1'}" font-size="10.5" font-weight="700" text-anchor="middle">${z > 0 ? '+' : ''}${z.toFixed(2)}</text>`;
      }
    }

    svg += `</svg>`;
    container.innerHTML = svg;
  }

  // ============================================================================
  // 13. Borderline Countries Table (with Click-to-Drawer)
  // ============================================================================
  function renderBorderlineTable() {
    const tbody = document.querySelector('#borderlineTable tbody');
    if (!tbody) return;

    const countries = state.results.countries;
    const borderlines = countries.filter(c => c.is_borderline).sort((a, b) => a.silhouette - b.silhouette);

    tbody.innerHTML = borderlines.map(c => `
      <tr data-drawer-iso="${c.country_code}" style="cursor: pointer;" title="Click to inspect ${c.country_name} in detail drawer">
        <td><strong>${c.country_name}</strong> (${c.country_code})</td>
        <td>${c.region}</td>
        <td>${c.income_group || 'N/A'}</td>
        <td><span class="pill-status" style="background: rgba(251, 191, 36, 0.15); color: #fbbf24; border: 1px solid rgba(251, 191, 36, 0.3);">C${c.cluster}: ${c.cluster_name}</span></td>
        <td><strong style="color: ${c.silhouette < 0 ? 'var(--rose-accent)' : 'var(--amber-accent)'};">${c.silhouette.toFixed(4)}</strong></td>
        <td>${c.indicators.stunting || 'N/A'}%</td>
        <td>${c.indicators.wasting || 'N/A'}%</td>
        <td>${c.indicators.adult_obesity || 'N/A'}%</td>
      </tr>
    `).join('');

    tbody.querySelectorAll('tr[data-drawer-iso]').forEach(row => {
      row.addEventListener('click', () => {
        const iso = row.getAttribute('data-drawer-iso');
        openCountryDrawer(iso);
      });
    });
  }

  // ============================================================================
  // 14. Reproduce CLI Commands
  // ============================================================================
  function renderReproduceSection() {
    const box = document.getElementById('reproduceCodeBox');
    if (!box) return;

    box.innerHTML = `<code># 1. Clone repository & install dependencies
git clone &lt;repo_url&gt;
cd "Clustering project"
python -m pip install -r backend/requirements.txt

# 2. Download fresh real World Bank health indicators
python backend/fetch_data.py

# 3. Execute 7-step preprocessing, clustering sweep, validation, & export
python backend/run_pipeline.py

# 4. Open static dashboard locally (zero build tools or web servers required!)
# Simply double-click frontend/index.html in your web browser.</code>`;
  }

  // ============================================================================
  // 15. Event Listeners & Interactive Controls
  // ============================================================================
  function setupEventListeners() {
    // Distance toggle buttons
    const distBtns = document.querySelectorAll('[data-dist]');
    distBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const dist = btn.getAttribute('data-dist');
        switchActiveModel(dist, state.activeK);
      });
    });

    // K selection buttons
    const kBtns = document.querySelectorAll('[data-k]');
    kBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const k = parseInt(btn.getAttribute('data-k'), 10);
        switchActiveModel(state.activeDistance, k);
      });
    });

    // Loadings biplot toggle
    const loadingsBtn = document.getElementById('toggleLoadingsBtn');
    if (loadingsBtn) {
      loadingsBtn.addEventListener('click', () => {
        state.showLoadings = !state.showLoadings;
        loadingsBtn.classList.toggle('active', state.showLoadings);
        renderPCAExplorer();
      });
    }

    // Country search input
    const searchInput = document.getElementById('pcaSearchInput');
    if (searchInput) {
      searchInput.addEventListener('input', e => {
        state.searchTerm = e.target.value.trim();
        renderPCAExplorer();
      });
    }

    // Region filter select
    const regionSelect = document.getElementById('pcaRegionSelect');
    if (regionSelect) {
      const regions = Array.from(new Set(state.results.countries.map(c => c.region))).filter(Boolean).sort();
      regionSelect.innerHTML = `<option value="all">All Global Regions (${state.results.countries.length})</option>` +
        regions.map(r => `<option value="${r}">${r}</option>`).join('');

      regionSelect.addEventListener('change', e => {
        state.selectedRegion = e.target.value;
        renderPCAExplorer();
      });
    }
  }

  // ============================================================================
  // 16. Smooth Scroll-Reveal
  // ============================================================================
  function setupScrollReveal() {
    const reveals = document.querySelectorAll('.reveal-on-scroll');
    if (!('IntersectionObserver' in window)) {
      reveals.forEach(el => el.classList.add('is-revealed'));
      return;
    }

    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-revealed');
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

    reveals.forEach(el => observer.observe(el));
  }

})();
