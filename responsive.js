// Responsive Design & Device Detection

class ResponsiveUtils {
    static isMobile() {
        return window.innerWidth <= 768;
    }

    static isTablet() {
        return window.innerWidth > 768 && window.innerWidth <= 1024;
    }

    static isDesktop() {
        return window.innerWidth > 1024;
    }

    static onResize(callback) {
        let resizeTimer;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(callback, 250);
        });
    }

    static adjustLayoutForMobile() {
        if (this.isMobile()) {
            document.querySelectorAll('.grid-section, .features-grid, .stats-grid').forEach(grid => {
                grid.style.gridTemplateColumns = '1fr';
            });
        }
    }
}

// Tooltip Helper
class Tooltip {
    static add(element, text, position = 'top') {
        element.setAttribute('data-tooltip', text);
        element.setAttribute('data-tooltip-position', position);
        element.style.cursor = 'help';
        element.style.position = 'relative';

        element.addEventListener('mouseenter', () => this.show(element));
        element.addEventListener('mouseleave', () => this.hide(element));
    }

    static show(element) {
        const text = element.getAttribute('data-tooltip');
        const position = element.getAttribute('data-tooltip-position');

        let tooltip = element.querySelector('.tooltip');
        if (!tooltip) {
            tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.style.cssText = `
                position: absolute;
                background: #1f3a5f;
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
                font-size: 13px;
                white-space: nowrap;
                z-index: 1000;
                pointer-events: none;
                opacity: 0;
                transition: opacity 0.2s;
            `;
            tooltip.textContent = text;
            element.appendChild(tooltip);
        }

        const rect = element.getBoundingClientRect();
        if (position === 'top') {
            tooltip.style.bottom = '100%';
            tooltip.style.left = '50%';
            tooltip.style.transform = 'translateX(-50%)';
            tooltip.style.marginBottom = '8px';
        } else if (position === 'bottom') {
            tooltip.style.top = '100%';
            tooltip.style.left = '50%';
            tooltip.style.transform = 'translateX(-50%)';
            tooltip.style.marginTop = '8px';
        }

        setTimeout(() => { tooltip.style.opacity = '1'; }, 10);
    }

    static hide(element) {
        const tooltip = element.querySelector('.tooltip');
        if (tooltip) tooltip.style.opacity = '0';
    }
}

// Initialize responsive utilities on load
document.addEventListener('DOMContentLoaded', () => {
    ResponsiveUtils.adjustLayoutForMobile();
    ResponsiveUtils.onResize(() => {
        ResponsiveUtils.adjustLayoutForMobile();
    });
});
