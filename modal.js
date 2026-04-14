// Modal Component - Reusable across all pages
class Modal {
    constructor() {
        this.createModalStyles();
        this.createModalHTML();
    }

    createModalStyles() {
        if (document.getElementById('modalStyles')) return;
        const style = document.createElement('style');
        style.id = 'modalStyles';
        style.textContent = `
            .modal-overlay {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.5);
                display: none;
                z-index: 10000;
                align-items: center;
                justify-content: center;
            }
            .modal-overlay.active {
                display: flex;
                animation: fadeIn 0.3s ease-out;
            }
            .modal-content {
                background: white;
                border-radius: 12px;
                padding: 30px;
                max-width: 500px;
                width: 90%;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
                animation: slideUp 0.3s ease-out;
            }
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            @keyframes slideUp {
                from {
                    transform: translateY(30px);
                    opacity: 0;
                }
                to {
                    transform: translateY(0);
                    opacity: 1;
                }
            }
            .modal-header {
                font-size: 24px;
                font-weight: 600;
                color: #1f3a5f;
                margin-bottom: 15px;
            }
            .modal-body {
                color: #666;
                line-height: 1.6;
                margin-bottom: 25px;
                font-size: 15px;
            }
            .modal-footer {
                display: flex;
                gap: 12px;
                justify-content: flex-end;
            }
            .modal-btn {
                padding: 10px 24px;
                border: none;
                border-radius: 6px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s;
            }
            .modal-btn-primary {
                background: #2c5fb8;
                color: white;
            }
            .modal-btn-primary:hover {
                background: #1f3a5f;
            }
            .modal-btn-secondary {
                background: #e0e0e0;
                color: #1f3a5f;
            }
            .modal-btn-secondary:hover {
                background: #d0d0d0;
            }
            .loading-spinner {
                border: 4px solid #e0e0e0;
                border-top: 4px solid #2c5fb8;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 20px auto;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        `;
        document.head.appendChild(style);
    }

    createModalHTML() {
        if (document.getElementById('modal')) return;
        const overlay = document.createElement('div');
        overlay.id = 'modal';
        overlay.className = 'modal-overlay';
        overlay.innerHTML = `
            <div class="modal-content">
                <div class="modal-header" id="modalHeader"></div>
                <div class="modal-body" id="modalBody"></div>
                <div class="modal-footer" id="modalFooter"></div>
            </div>
        `;
        document.body.appendChild(overlay);
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) this.close();
        });
    }

    alert(title, message) {
        return new Promise((resolve) => {
            document.getElementById('modalHeader').textContent = title;
            document.getElementById('modalBody').textContent = message;
            document.getElementById('modalFooter').innerHTML = `
                <button class="modal-btn modal-btn-primary" onclick="modal.close(); resolve();">OK</button>
            `;
            document.getElementById('modal').classList.add('active');
        });
    }

    confirm(title, message) {
        return new Promise((resolve) => {
            document.getElementById('modalHeader').textContent = title;
            document.getElementById('modalBody').textContent = message;
            document.getElementById('modalFooter').innerHTML = `
                <button class="modal-btn modal-btn-secondary" onclick="modal.close(); resolve(false);">Cancel</button>
                <button class="modal-btn modal-btn-primary" onclick="modal.close(); resolve(true);">Confirm</button>
            `;
            document.getElementById('modal').classList.add('active');
        });
    }

    loading(title = 'Loading...') {
        document.getElementById('modalHeader').textContent = title;
        document.getElementById('modalBody').innerHTML = '<div class="loading-spinner"></div>';
        document.getElementById('modalFooter').innerHTML = '';
        document.getElementById('modal').classList.add('active');
    }

    close() {
        document.getElementById('modal').classList.remove('active');
    }
}

const modal = new Modal();
