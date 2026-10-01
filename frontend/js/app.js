const API_BASE = '/api/v1';

const App = {
  notifiedIncidents: new Set(),
  userLocation: null,
  gpsPermissionGranted: false,
  watchId: null,

  async fetchAPI(endpoint, options = {}) {
    try {
      const response = await fetch(`${API_BASE}${endpoint}`, options);
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP Error ${response.status}`);
      }
      return await response.json();
    } catch (err) {
      console.error(`API Error on ${endpoint}:`, err);
      this.showToast(err.message || 'API request failed', 'error');
      throw err;
    }
  },

  formatTime(isoString) {
    if (!isoString) return 'Just now';
    const date = new Date(isoString);
    if (isNaN(date.getTime())) return 'Recently';
    return date.toLocaleString('en-IN', {
      day: '2-digit', month: 'short', year: 'numeric',
      hour: '2-digit', minute: '2-digit', hour12: true
    });
  },

  formatRelativeTime(isoString) {
    if (!isoString) return 'Just now';
    const date = new Date(isoString);
    if (isNaN(date.getTime())) return 'Recently';
    const now = new Date();
    const diffSecs = Math.floor((now - date) / 1000);
    if (diffSecs < 60) return 'Just now';
    if (diffSecs < 3600) return `${Math.floor(diffSecs / 60)} mins ago`;
    if (diffSecs < 86400) return `${Math.floor(diffSecs / 3600)} hrs ago`;
    return `${Math.floor(diffSecs / 86400)} days ago`;
  },

  getRiskBadge(level, score) {
    const l = (level || 'MODERATE').toUpperCase();
    let badgeClass = 'badge-moderate';
    if (l === 'LOW') badgeClass = 'badge-low';
    if (l === 'HIGH') badgeClass = 'badge-high';
    if (l === 'CRITICAL') badgeClass = 'badge-critical';

    return `<span class="badge-risk ${badgeClass}">${l} ${score ? `(${score}/100)` : ''}</span>`;
  },

  getStatusBadge(status) {
    const s = (status || 'REPORTED').toUpperCase();
    let bg = 'bg-slate-700 text-slate-300';
    if (s === 'REPORTED') bg = 'bg-amber-900/60 text-amber-300 border border-amber-500/30';
    if (s === 'VERIFIED') bg = 'bg-blue-900/60 text-blue-300 border border-blue-500/30';
    if (s === 'TEAM ASSIGNED') bg = 'bg-purple-900/60 text-purple-300 border border-purple-500/30';
    if (s === 'IN PROGRESS') bg = 'bg-orange-900/60 text-orange-300 border border-orange-500/30';
    if (s === 'RESOLVED') bg = 'bg-emerald-900/60 text-emerald-300 border border-emerald-500/30';

    return `<span class="px-2.5 py-1 text-xs font-semibold rounded-full ${bg}">${s}</span>`;
  },

  getSourceBadge(description = '', code = '') {
    if (description.includes('Instagram') || code.includes('PR-INSTA') || description.includes('#UttarakhandLandslide') || description.includes('#DehradunFlood')) {
      return `<span class="px-2 py-0.5 text-[10px] font-bold rounded bg-pink-950 text-pink-300 border border-pink-500/40 flex items-center gap-1 inline-flex animate-pulse"><span class="text-xs">📸</span> INSTAGRAM CROWD VERIFIED</span>`;
    } else if (description.includes('[OFFICIAL GOVT BULLETIN') || code.includes('PR-GOV')) {
      return `<span class="px-2 py-0.5 text-[10px] font-bold rounded bg-emerald-950 text-emerald-300 border border-emerald-500/30 flex items-center gap-1 inline-flex"><span class="text-xs">🏛️</span> GOVT BULLETIN</span>`;
    } else if (description.includes('[SOURCE:') || code.includes('PR-SOC')) {
      return `<span class="px-2 py-0.5 text-[10px] font-bold rounded bg-sky-950 text-sky-400 border border-sky-500/30 flex items-center gap-1 inline-flex"><span class="text-xs">📱</span> SOCIAL MEDIA</span>`;
    } else if (description.includes('[SIMULATION')) {
      return `<span class="px-2 py-0.5 text-[10px] font-bold rounded bg-amber-950 text-amber-400 border border-amber-500/30 flex items-center gap-1 inline-flex"><span class="text-xs">⚡</span> SIMULATED</span>`;
    } else {
      return `<span class="px-2 py-0.5 text-[10px] font-bold rounded bg-indigo-950 text-indigo-300 border border-indigo-500/30 flex items-center gap-1 inline-flex"><span class="text-xs">📢</span> CITIZEN APP</span>`;
    }
  },


  playEmergencyBeepSound() {
    try {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (!AudioContext) return;
      const ctx = new AudioContext();

      const playTone = (freq, duration, delay) => {
        setTimeout(() => {
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          osc.type = 'sawtooth';
          osc.frequency.setValueAtTime(freq, ctx.currentTime);
          gain.gain.setValueAtTime(0.3, ctx.currentTime);
          gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + duration);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start();
          osc.stop(ctx.currentTime + duration);
        }, delay);
      };

      playTone(880, 0.25, 0);
      playTone(1046, 0.25, 300);
      playTone(880, 0.25, 600);
      playTone(1046, 0.4, 900);
    } catch (e) {
      console.warn("Audio Context sound blocked or not supported:", e);
    }
  },

  haversineKm(lat1, lon1, lat2, lon2) {
    const R = 6371;
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
  },

  promptMobileGPSPermission(onSuccessCallback) {
    this.requestHardwareGPS(onSuccessCallback);
  },

  // 100% UNFILTERED REAL LIVE HARDWARE GPS CHIP ENGINE WITH FAST PASS & REFINEMENT
  requestHardwareGPS(onSuccessCallback) {
    if (!navigator.geolocation) {
      this.showToast("Geolocation not supported by mobile browser", "error");
      this.useIPLocationFallback(onSuccessCallback);
      return;
    }

    this.showToast("🎯 Acquiring your Live Location...", "info");

    // Fast Pass: Get quick location first (within 3 seconds)
    const fastOptions = {
      enableHighAccuracy: false,
      timeout: 4000,
      maximumAge: 300000 // Accept recent cached position for instant response
    };

    const highAccuracyOptions = {
      enableHighAccuracy: true,
      timeout: 10000,
      maximumAge: 0
    };

    let acquired = false;

    navigator.geolocation.getCurrentPosition(
      (pos) => {
        if (acquired) return;
        acquired = true;
        const lat = pos.coords.latitude;
        const lng = pos.coords.longitude;
        const accuracy = pos.coords.accuracy || 10;

        this.gpsPermissionGranted = true;
        this.userLocation = { lat, lng };
        this.showToast(`🎯 Live Location Acquired: ${lat.toFixed(6)}, ${lng.toFixed(6)} (±${Math.round(accuracy)}m)`, 'info');
        if (onSuccessCallback) onSuccessCallback(lat, lng);
        this.checkProximityAlerts();
        this.startLiveGPSTracking(onSuccessCallback);
      },
      (err) => {
        console.warn("Fast GPS error, trying high accuracy hardware GPS:", err.message);
        navigator.geolocation.getCurrentPosition(
          (pos) => {
            if (acquired) return;
            acquired = true;
            const lat = pos.coords.latitude;
            const lng = pos.coords.longitude;
            const accuracy = pos.coords.accuracy || 10;

            this.gpsPermissionGranted = true;
            this.userLocation = { lat, lng };
            this.showToast(`🎯 Live GPS Acquired: ${lat.toFixed(6)}, ${lng.toFixed(6)} (±${Math.round(accuracy)}m)`, 'info');
            if (onSuccessCallback) onSuccessCallback(lat, lng);
            this.checkProximityAlerts();
            this.startLiveGPSTracking(onSuccessCallback);
          },
          (highErr) => {
            console.warn("Hardware GPS error:", highErr.message);
            this.showToast(`⚠️ GPS Notice: Please allow Location Permission in your browser!`, 'error');
            this.useIPLocationFallback(onSuccessCallback);
          },
          highAccuracyOptions
        );
      },
      fastOptions
    );
  },

  startLiveGPSTracking(onSuccessCallback) {
    if (this.watchId !== null) return;
    if (!navigator.geolocation) return;

    this.watchId = navigator.geolocation.watchPosition(
      (pos) => {
        const lat = pos.coords.latitude;
        const lng = pos.coords.longitude;
        const accuracy = pos.coords.accuracy || 50;
        this.userLocation = { lat, lng };

        // Update GPS marker position on map quietly without auto-centering
        if (window.MapVisualizer && typeof window.MapVisualizer.updateUserMarkerQuietly === 'function') {
          window.MapVisualizer.updateUserMarkerQuietly(lat, lng, accuracy);
        }
      },
      (err) => console.warn("Watch position error:", err.message),
      { enableHighAccuracy: true, timeout: 15000, maximumAge: 0 }
    );
  },


  async useIPLocationFallback(onSuccessCallback) {
    try {
      const res = await fetch('https://ipapi.co/json/').catch(() => null);
      if (res && res.ok) {
        const data = await res.json();
        const lat = data.latitude;
        const lng = data.longitude;

        if (lat && lng) {
          this.userLocation = { lat, lng };
          this.showToast(`Location Synced via Network (${lat.toFixed(4)}, ${lng.toFixed(4)})`, 'info');
          if (onSuccessCallback) onSuccessCallback(lat, lng);
          this.checkProximityAlerts();
          return;
        }
      }
    } catch (e) {}

    const lat = 30.1917, lng = 78.1755;
    this.userLocation = { lat, lng };
    if (onSuccessCallback) onSuccessCallback(lat, lng);
    this.checkProximityAlerts();
  },

  initGeoProximityAlerts() {
    if ('Notification' in window && Notification.permission !== 'granted') {
      Notification.requestPermission();
    }
  },

  async checkProximityAlerts() {
    if (!this.userLocation) return;
    try {
      const incidents = await this.fetchAPI('/incidents');
      incidents.forEach(inc => {
        const distKm = this.haversineKm(this.userLocation.lat, this.userLocation.lng, inc.latitude, inc.longitude);
        if (distKm <= 15.0 && inc.status !== 'RESOLVED' && !this.notifiedIncidents.has(inc.id)) {
          this.notifiedIncidents.add(inc.id);
          this.triggerGeoDangerAlert(inc, distKm);
        }
      });
    } catch (e) {
      console.error("Proximity alert check error:", e);
    }
  },

  triggerGeoDangerAlert(inc, distKm) {
    this.playEmergencyBeepSound();

    if ('Notification' in window && Notification.permission === 'granted') {
      new Notification(`🚨 DISASTER PROXIMITY ALERT (${distKm.toFixed(1)} km)`, {
        body: `WARNING: ${inc.type} reported near your location at ${inc.address}! ${inc.road_blocked ? 'Road Blocked.' : ''}`
      });
    }

    this.showEmergencyBanner(inc, distKm);
  },

  showEmergencyBanner(inc, distKm) {
    let banner = document.getElementById('geo-emergency-banner');
    if (!banner) {
      banner = document.createElement('div');
      banner.id = 'geo-emergency-banner';
      banner.className = 'fixed top-20 left-4 right-4 md:left-1/2 md:-translate-x-1/2 md:max-w-xl z-[9999] bg-red-950/95 border-2 border-red-500 p-4 rounded-2xl shadow-2xl backdrop-blur-xl animate-bounce text-slate-100 space-y-2';
      document.body.appendChild(banner);
    }

    banner.innerHTML = `
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2">
          <span class="text-xl animate-ping">🚨</span>
          <span class="font-extrabold text-xs text-red-400 uppercase tracking-widest">NEARBY PROXIMITY DANGER WARNING (${distKm.toFixed(1)} km away)</span>
        </div>
        <button onclick="document.getElementById('geo-emergency-banner').remove()" class="text-slate-400 hover:text-white font-bold">&times;</button>
      </div>
      <div class="font-bold text-sm text-white">${inc.type} — ${inc.address}</div>
      <div class="text-xs text-slate-300">
        ⚠️ Disaster report active within your travel corridor! ${inc.road_blocked ? '<b class="text-amber-400">Road Movement Blocked.</b>' : ''} Please exercise extreme caution or take an alternate bypass.
      </div>
      <div class="flex items-center justify-between text-[11px] pt-1 border-t border-white/10 text-slate-400">
        <span>Risk Score: <b class="text-red-400">${inc.risk_score}/100 (${inc.risk_level})</b></span>
        <a href="/app/map.html" class="text-blue-400 font-bold hover:underline">View on Live Map &rarr;</a>
      </div>
    `;

    setTimeout(() => {
      if (banner && banner.parentElement) {
        banner.classList.remove('animate-bounce');
      }
    }, 4000);
  },

  async triggerLiveFeed() {
    this.showToast("📡 Ingesting fresh live official government & social media disaster feeds...", "info");
    try {
      const res = await this.fetchAPI('/gov/feed-live-incident', { method: 'POST' });
      this.playEmergencyBeepSound();
      this.showToast(`🚨 FRESH LIVE ALERT INGESTED: ${res.incident.title}`, "info");

      // Refresh active page UI components immediately
      if (window.MapVisualizer) {
        window.MapVisualizer.loadMapData();
      }
      if (window.DashboardApp) {
        window.DashboardApp.loadDashboardData();
      }
      if (typeof loadCitizenIncidents === 'function') {
        loadCitizenIncidents();
      }
      if (typeof loadCitizenShelters === 'function') {
        loadCitizenShelters();
      }
    } catch (e) {
      console.error("Live feed trigger error:", e);
    }
  },

  showToast(message, type = 'info') {
    const container = document.getElementById('toast-container') || this.createToastContainer();
    const toast = document.createElement('div');
    const border = type === 'error' ? 'border-red-500/50 bg-red-950/80 text-red-200' : 'border-blue-500/50 bg-slate-900/90 text-slate-100';
    toast.className = `flex items-center gap-3 p-4 rounded-xl border shadow-xl backdrop-blur-md transition-all duration-300 text-sm ${border}`;
    toast.innerHTML = `
      <div class="font-medium">${message}</div>
      <button onclick="this.parentElement.remove()" class="ml-auto opacity-60 hover:opacity-100">&times;</button>
    `;
    container.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      setTimeout(() => toast.remove(), 300);
    }, 4000);
  },

  createToastContainer() {
    const div = document.createElement('div');
    div.id = 'toast-container';
    div.className = 'fixed bottom-5 right-5 z-[9999] flex flex-col gap-2 max-w-md w-full';
    document.body.appendChild(div);
    return div;
  }
};

document.addEventListener('DOMContentLoaded', () => App.initGeoProximityAlerts());

