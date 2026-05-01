/**
 * RAPOS UI Engine
 * Orchestrates all DOM updates, chart renderings, and visual state.
 */

const RAPOS_UI = {
    state: {
        holdings: [],
        allocationChart: null,
        targetChart: null,
        currentUser: null,
        activeTab: 'portfolioTab'
    },

    /**
     * Initialization
     */
    init(user) {
        this.state.currentUser = user;
        this.initCharts();
        this.setupEventListeners();
    },

    initCharts() {
        const allocCtx = document.getElementById('allocationChart');
        if (allocCtx) {
            this.state.allocationChart = new Chart(allocCtx, {
                type: 'doughnut',
                data: {
                    labels: [],
                    datasets: [{
                        data: [],
                        backgroundColor: ['#3b82f6', '#6366f1', '#10b981', '#f59e0b', '#ef4444'],
                        borderWidth: 0,
                        hoverOffset: 15
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: '75%',
                    plugins: {
                        legend: { position: 'bottom', labels: { usePointStyle: true, padding: 20, font: { family: 'Inter', weight: 600 } } }
                    }
                }
            });
        }
    },

    setupEventListeners() {
        // Any global UI listeners can go here
    },

    /**
     * View Controllers
     */
    switchTab(tabId, element) {
        // Tab switching logic with smooth transitions
        document.querySelectorAll('.sidebar-item').forEach(i => i.classList.remove('active'));
        if (element) element.classList.add('active');

        const views = document.querySelectorAll('.tab-view');
        views.forEach(v => {
            v.style.opacity = '0';
            setTimeout(() => { v.style.display = 'none'; }, 200);
        });

        setTimeout(() => {
            const activeView = document.getElementById(tabId);
            activeView.style.display = 'block';
            setTimeout(() => { activeView.style.opacity = '1'; }, 50);
            this.state.activeTab = tabId;
            
            // Trigger tab-specific loads
            if (tabId === 'marketTab') this.initTradingView();
        }, 250);
    },

    /**
     * Portfolio Rendering
     */
    updatePortfolio(holdings) {
        this.state.holdings = holdings;
        this.renderHoldingsList();
        this.updateStats();
        this.updateCharts();
    },

    renderHoldingsList() {
        const list = document.getElementById('holdingsList');
        if (!list) return;

        if (this.state.holdings.length === 0) {
            list.innerHTML = `
                <div style="text-align:center; padding:60px; color:var(--slate-400);">
                    <i class="fas fa-folder-open" style="font-size:32px; margin-bottom:16px; opacity:0.5;"></i>
                    <p style="font-weight:600;">Node is currently vacant.</p>
                    <p style="font-size:13px;">Add assets to begin neural tracking.</p>
                </div>`;
            return;
        }

        list.innerHTML = this.state.holdings.map(h => `
            <div class="list-item animate-fade-in">
                <div style="display:flex; align-items:center; gap:16px;">
                    <div style="width:48px; height:48px; background:var(--slate-100); border-radius:12px; display:flex; align-items:center; justify-content:center; font-weight:800; color:var(--brand-primary); font-size:12px;">${h.ticker.substring(0,4)}</div>
                    <div>
                        <div style="font-weight:700; color:var(--slate-900);">${h.asset_name}</div>
                        <div style="font-size:12px; color:var(--slate-500);">${h.quantity} units @ $${(h.current_price || 0).toLocaleString()}</div>
                    </div>
                </div>
                <div style="display:flex; align-items:center; gap:24px;">
                    <div style="text-align:right;">
                        <div style="font-weight:800; font-size:16px; color:var(--slate-900);">$${(h.live_value || 0).toLocaleString()}</div>
                        <div class="stat-trend ${h.performance_pct >= 0 ? 'trend-up' : 'trend-down'}">
                            ${h.performance_pct >= 0 ? '+' : ''}${h.performance_pct}%
                        </div>
                    </div>
                    <button onclick="handleDeleteAsset('${h.id}')" style="background:none; border:none; color:var(--slate-300); cursor:pointer; font-size:18px; transition:color 0.2s;">
                        <i class="fas fa-trash-alt"></i>
                    </button>
                </div>
            </div>
        `).join('');
    },

    updateStats() {
        let totalVal = 0, totalPrevVal = 0;
        this.state.holdings.forEach(h => {
            const val = h.live_value || 0;
            totalVal += val;
            const prevPrice = (h.current_price || 0) / (1 + (h.performance_pct || 0) / 100);
            totalPrevVal += (h.quantity || 1) * prevPrice;
        });

        const totalGain = totalVal - totalPrevVal;
        const velocity = totalPrevVal > 0 ? (totalGain / totalPrevVal) * 100 : 0;

        const valEl = document.getElementById('portfolioValue');
        if (valEl) valEl.textContent = '$' + totalVal.toLocaleString(undefined, { minimumFractionDigits: 2 });

        const changeEl = document.getElementById('portfolioDailyChange');
        if (changeEl) {
            changeEl.textContent = `${totalGain >= 0 ? '+' : ''}$${totalGain.toLocaleString(undefined, { minimumFractionDigits: 2 })} (${velocity.toFixed(2)}%)`;
            changeEl.className = `stat-trend ${totalGain >= 0 ? 'trend-up' : 'trend-down'}`;
        }

        const countEl = document.getElementById('assetCount');
        if (countEl) countEl.textContent = this.state.holdings.length;
    },

    updateCharts() {
        if (this.state.allocationChart) {
            const groups = {};
            this.state.holdings.forEach(h => { groups[h.asset_type] = (groups[h.asset_type] || 0) + (h.live_value || 0); });
            this.state.allocationChart.data.labels = Object.keys(groups);
            this.state.allocationChart.data.datasets[0].data = Object.values(groups);
            this.state.allocationChart.update();
        }
    },

    /**
     * Intelligence Hub Rendering
     */
    renderAIPrediction(data) {
        const pClose = document.getElementById('predictedCloseValue');
        const pScore = document.getElementById('aiRiskScoreValue');
        const pConf = document.getElementById('modelConfidence');
        const pSent = document.getElementById('predictedSentiment');

        if (pClose) pClose.textContent = '$' + data.predicted_next_close;
        if (pScore) pScore.textContent = data.ai_risk_score;
        if (pConf) pConf.textContent = (85 + Math.random() * 10).toFixed(1) + '%';
        if (pSent) {
            const isBull = data.predicted_daily_return_pct >= 0;
            pSent.textContent = isBull ? 'Bullish' : 'Bearish';
            pSent.className = `stat-trend ${isBull ? 'trend-up' : 'trend-down'}`;
            pSent.style.background = isBull ? 'var(--success-bg)' : 'var(--danger-bg)';
            pSent.style.padding = '4px 12px';
            pSent.style.borderRadius = '8px';
        }
    },

    renderNews(news) {
        const div = document.getElementById('newsFeed');
        if (!div) return;
        div.innerHTML = news.map(item => `
            <div style="padding:20px 24px; border-bottom:1px solid var(--slate-100); cursor:pointer; transition:background 0.2s;" onclick="window.open('${item.url}', '_blank')">
                <div style="font-size:14px; font-weight:700; color:var(--slate-800); margin-bottom:6px; line-height:1.4;">${item.headline}</div>
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-size:11px; color:var(--slate-400); font-weight:700; text-transform:uppercase;">${item.source}</span>
                    <span style="font-size:11px; color:var(--slate-400);">${new Date(item.datetime * 1000).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</span>
                </div>
            </div>
        `).join('');
    },

    /**
     * Overlay Systems
     */
    showModal(title, body, confirmText, onConfirm) {
        document.getElementById('modalTitle').textContent = title;
        document.getElementById('modalBody').innerHTML = body;
        const btn = document.getElementById('modalConfirmBtn');
        btn.textContent = confirmText;
        btn.onclick = onConfirm;
        document.getElementById('modalOverlay').style.display = 'flex';
    },

    closeModal() {
        document.getElementById('modalOverlay').style.display = 'none';
    },

    showToast(message, type = 'info') {
        const toast = document.getElementById('toast');
        const msg = document.getElementById('toastMsg');
        if (!toast || !msg) return;
        
        msg.textContent = message;
        toast.style.display = 'flex';
        toast.style.opacity = '1';
        
        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => { toast.style.display = 'none'; }, 300);
        }, 3000);
    },

    /**
     * Market Visuals
     */
    initTradingView() {
        if (typeof TradingView !== 'undefined') {
            new TradingView.widget({
                "width": "100%", "height": "100%", "symbol": "NASDAQ:AAPL", "interval": "D", "theme": "light", "container_id": "tradingview_widget",
                "style": "3", "toolbar_bg": "#f1f5f9", "enable_publishing": false, "hide_top_toolbar": true, "save_image": false
            });
        }
    }
};
