(function () {
    function getListContainerFromEvent(event) {
        if (!event || !event.detail) return null;

        const sourceElement = event.detail.elt;
        if (sourceElement && typeof sourceElement.closest === "function") {
            const containerFromSource = sourceElement.closest(".list-content");
            if (containerFromSource) return containerFromSource;
        }

        const targetElement = event.detail.target;
        if (targetElement && typeof targetElement.closest === "function") {
            const containerFromTarget = targetElement.closest(".list-content");
            if (containerFromTarget) return containerFromTarget;
        }

        if (targetElement && targetElement.classList && targetElement.classList.contains("list-content")) {
            return targetElement;
        }

        return null;
    }

    function setupHtmxListLoading() {
        if (!document.body) return;

        document.body.addEventListener("htmx:beforeRequest", function (event) {
            const container = getListContainerFromEvent(event);
            if (container) {
                container.classList.add("is-loading");
            }
        });

        function clearLoading(event) {
            const container = getListContainerFromEvent(event);
            if (container) {
                container.classList.remove("is-loading");
            }
        }

        document.body.addEventListener("htmx:afterRequest", clearLoading);
        document.body.addEventListener("htmx:responseError", clearLoading);
        document.body.addEventListener("htmx:sendError", clearLoading);
    }

    function setDynamicTitles() {
        const source = document.getElementById("pageTitleSource");
        const topbar = document.getElementById("topbarPageTitle");
        const header = document.getElementById("pageHeaderTitle");
        const subtitleSource = document.getElementById("pageSubtitleSource");
        const subtitle = document.getElementById("pageHeaderSubtitle");

        if (source) {
            const text = source.textContent.trim();
            if (text && topbar) topbar.textContent = text;
            if (text && header) header.textContent = text;
        }

        if (subtitleSource && subtitle) {
            const sub = subtitleSource.textContent.trim();
            subtitle.textContent = sub || "Acompanhe os dados financeiros em tempo real.";
        }
    }

    function drawLineChart(canvasId) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;
        const ctx = canvas.getContext("2d");
        const dataReceitas = [18, 20, 22, 24, 21, 26, 28, 31, 29, 34, 33, 36];
        const dataDespesas = [13, 14, 15, 17, 16, 18, 19, 21, 20, 23, 22, 24];

        const width = canvas.width;
        const height = canvas.height;
        ctx.clearRect(0, 0, width, height);

        ctx.strokeStyle = "#e2e8f0";
        ctx.lineWidth = 1;
        for (let y = 20; y < height - 20; y += 45) {
            ctx.beginPath();
            ctx.moveTo(24, y);
            ctx.lineTo(width - 20, y);
            ctx.stroke();
        }

        function drawSeries(series, color) {
            const max = 40;
            const stepX = (width - 52) / (series.length - 1);
            ctx.beginPath();
            ctx.lineWidth = 3;
            ctx.strokeStyle = color;

            series.forEach(function (value, index) {
                const x = 24 + stepX * index;
                const y = height - 24 - (value / max) * (height - 52);
                if (index === 0) ctx.moveTo(x, y);
                else ctx.lineTo(x, y);
            });

            ctx.stroke();
        }

        drawSeries(dataReceitas, "#1d4ed8");
        drawSeries(dataDespesas, "#ef4444");
    }

    function drawBarChart(canvasId) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;
        const ctx = canvas.getContext("2d");
        const values = [8, 9, 7, 10, 11, 9, 12, 10, 13, 14, 12, 15];
        const width = canvas.width;
        const height = canvas.height;
        const max = 16;

        ctx.clearRect(0, 0, width, height);
        const barWidth = (width - 60) / values.length;

        values.forEach(function (value, index) {
            const x = 28 + index * barWidth;
            const h = ((height - 50) * value) / max;
            const y = height - 24 - h;
            ctx.fillStyle = "#3b82f6";
            ctx.fillRect(x, y, barWidth - 8, h);
        });
    }

    function drawDonutChart(canvasId) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;
        const ctx = canvas.getContext("2d");
        const values = [34, 26, 21, 19];
        const colors = ["#ef4444", "#f59e0b", "#3b82f6", "#10b981"];
        const total = values.reduce(function (a, b) {
            return a + b;
        }, 0);

        const cx = canvas.width / 2;
        const cy = canvas.height / 2;
        const radius = Math.min(cx, cy) - 12;
        const inner = radius * 0.62;

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        let start = -Math.PI / 2;
        values.forEach(function (value, index) {
            const angle = (value / total) * Math.PI * 2;
            ctx.beginPath();
            ctx.moveTo(cx, cy);
            ctx.fillStyle = colors[index];
            ctx.arc(cx, cy, radius, start, start + angle);
            ctx.closePath();
            ctx.fill();
            start += angle;
        });

        ctx.beginPath();
        ctx.fillStyle = "#fff";
        ctx.arc(cx, cy, inner, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = "#0f172a";
        ctx.font = "600 14px 'Plus Jakarta Sans'";
        ctx.textAlign = "center";
        ctx.fillText("Categorias", cx, cy - 2);
        ctx.fillStyle = "#64748b";
        ctx.font = "500 12px 'Plus Jakarta Sans'";
        ctx.fillText("Despesas", cx, cy + 16);
    }

    function initCharts() {
        drawLineChart("lineChartReceitasDespesas");
        drawBarChart("barChartEvolucao");
        drawDonutChart("donutChartCategorias");
    }

    document.addEventListener("DOMContentLoaded", function () {
        setDynamicTitles();
        initCharts();
        setupHtmxListLoading();
    });
})();
