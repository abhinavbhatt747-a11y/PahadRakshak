const AuthManager = {
  STORAGE_KEY: 'pahadrakshak_authority_session',

  isLoggedIn() {
    return this.isAuthority();
  },

  isAuthority() {
    const session = this.getSession();
    return session && session.verified === true && session.role === 'AUTHORITY';
  },

  getSession() {
    try {
      const data = sessionStorage.getItem(this.STORAGE_KEY) || localStorage.getItem(this.STORAGE_KEY);
      return data ? JSON.parse(data) : null;
    } catch (e) {
      return null;
    }
  },

  getOfficerProfile() {
    const session = this.getSession();
    if (!session) return { officer_name: 'Guest Officer', department: 'UKSDMA Control' };
    return session;
  },

  async loginOfficer(officerId, passkey) {
    if (!officerId || !passkey) {
      throw new Error("Please enter both Officer ID and Access Passkey.");
    }

    try {
      const res = await fetch('/api/v1/auth/verify-officer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ officer_id: officerId, passkey: passkey })
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || "Verification failed. Check your Officer ID and PIN.");
      }

      const data = await res.json();
      sessionStorage.setItem(this.STORAGE_KEY, JSON.stringify(data));
      localStorage.setItem(this.STORAGE_KEY, JSON.stringify(data));
      return data;
    } catch (err) {
      console.error("Officer Verification Error:", err);
      throw err;
    }
  },

  logoutOfficer() {
    sessionStorage.removeItem(this.STORAGE_KEY);
    localStorage.removeItem(this.STORAGE_KEY);
    window.location.href = '/app/index.html';
  },

  requireAuthority() {
    if (!this.isAuthority()) {
      alert("🔒 Access Restricted: This portal is reserved for Authorized Disaster Officials & First Responders. Please enter your Officer ID on the main page.");
      window.location.href = '/app/index.html?modal=authority';
      return false;
    }
    return true;
  }
};
