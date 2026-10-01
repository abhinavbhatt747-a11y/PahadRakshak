const DemoSimulator = {
  async triggerSimulation() {
    const btn = document.getElementById('demo-simulate-btn');
    if (btn) {
      btn.disabled = true;
      btn.innerHTML = `<span class="inline-block animate-spin mr-2">⚡</span> Simulating Emergency...`;
    }

    try {
      const res = await App.fetchAPI('/demo/simulate', { method: 'POST' });
      App.showToast(`⚡ EMERGENCY SIMULATED: #${res.simulated_incident.incident_code} (${res.simulated_incident.risk_level} RISK - ${res.simulated_incident.risk_score}/100)`, 'info');

      // Trigger custom event so page controllers can reload data
      window.dispatchEvent(new CustomEvent('emergency-simulated', { detail: res.simulated_incident }));

    } catch (err) {
      console.error("Simulation failed:", err);
    } finally {
      if (btn) {
        btn.disabled = false;
        btn.innerHTML = `<span class="text-amber-400">⚡</span> Simulate Emergency`;
      }
    }
  }
};
