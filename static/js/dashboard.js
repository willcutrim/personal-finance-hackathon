(function () {
    "use strict";

    var COLORS = {
        receita: "#22c55e",
        receitaFill: "rgba(34,197,94,0.12)",
        despesa: "#ef4444",
        despesaFill: "rgba(239,68,68,0.10)",
        bar: "#3b82f6",
        donut: [
            "#1e3a8a",
            "#3b82f6",
            "#22c55e",
            "#f59e0b",
            "#ef4444",
            "#a855f7",
            "#06b6d4",
            "#f97316",
        ],
    };

    function readJsonScript(id) {
        var el = document.getElementById(id);
        if (!el) return null;
        try {
            return JSON.parse(el.textContent);
        } catch (e) {
            return null;
        }
    }

    function initChartLinha() {
        var canvas = document.getElementById("chartLinha");
        if (!canvas) return;
        var data = readJsonScript("chartLinhaData");
        if (!data) return;

        new Chart(canvas, {
            type: "line",
            data: {
                labels: data.labels,
                datasets: [
                    {
                        label: "Receitas",
                        data: data.receitas,
                        borderColor: COLORS.receita,
                        backgroundColor: COLORS.receitaFill,
                        borderWidth: 2.5,
                        pointRadius: 4,
                        pointBackgroundColor: COLORS.receita,
                        fill: true,
                        tension: 0.35,
                    },
                    {
                        label: "Despesas",
                        data: data.despesas,
                        borderColor: COLORS.despesa,
                        backgroundColor: COLORS.despesaFill,
                        borderWidth: 2.5,
                        pointRadius: 4,
                        pointBackgroundColor: COLORS.despesa,
                        fill: true,
                        tension: 0.35,
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: { mode: "index", intersect: false },
                plugins: {
                    legend: {
                        display: true,
                        position: "top",
                        labels: {
                            boxWidth: 12,
                            boxHeight: 12,
                            borderRadius: 4,
                            useBorderRadius: true,
                            font: { size: 12, family: "'Plus Jakarta Sans', sans-serif" },
                            color: "#5f6f8f",
                        },
                    },
                    tooltip: {
                        callbacks: {
                            label: function (ctx) {
                                return (
                                    " " +
                                    ctx.dataset.label +
                                    ": R$ " +
                                    ctx.parsed.y.toLocaleString("pt-BR", {
                                        minimumFractionDigits: 2,
                                    })
                                );
                            },
                        },
                    },
                },
                scales: {
                    x: {
                        grid: { color: "rgba(203,213,225,0.5)", lineWidth: 1 },
                        ticks: {
                            font: { size: 11, family: "'Plus Jakarta Sans', sans-serif" },
                            color: "#94a3b8",
                            maxTicksLimit: 10,
                        },
                    },
                    y: {
                        grid: { color: "rgba(203,213,225,0.5)", lineWidth: 1 },
                        ticks: {
                            font: { size: 11, family: "'Plus Jakarta Sans', sans-serif" },
                            color: "#94a3b8",
                            callback: function (v) {
                                if (v >= 1000) return "R$ " + (v / 1000).toFixed(0) + "k";
                                return "R$ " + v;
                            },
                        },
                    },
                },
            },
        });
    }

    function initChartDonut() {
        var canvas = document.getElementById("chartDonut");
        if (!canvas) return;
        var data = readJsonScript("chartDespesasCatData");
        if (!data || !data.labels.length) return;

        new Chart(canvas, {
            type: "doughnut",
            data: {
                labels: data.labels,
                datasets: [
                    {
                        data: data.valores,
                        backgroundColor: COLORS.donut.slice(0, data.labels.length),
                        borderWidth: 0,
                        hoverOffset: 6,
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: "62%",
                plugins: {
                    legend: {
                        display: true,
                        position: "bottom",
                        labels: {
                            boxWidth: 12,
                            boxHeight: 12,
                            borderRadius: 4,
                            useBorderRadius: true,
                            font: { size: 12, family: "'Plus Jakarta Sans', sans-serif" },
                            color: "#5f6f8f",
                            padding: 12,
                        },
                    },
                    tooltip: {
                        callbacks: {
                            label: function (ctx) {
                                return (
                                    " " +
                                    ctx.label +
                                    ": R$ " +
                                    ctx.parsed.toLocaleString("pt-BR", {
                                        minimumFractionDigits: 2,
                                    })
                                );
                            },
                        },
                    },
                },
            },
        });
    }

    function initChartBarra() {
        var canvas = document.getElementById("chartBarra");
        if (!canvas) return;
        var data = readJsonScript("chartReceitasCatData");
        if (!data || !data.labels.length) return;

        new Chart(canvas, {
            type: "bar",
            data: {
                labels: data.labels,
                datasets: [
                    {
                        label: "Receitas",
                        data: data.valores,
                        backgroundColor: COLORS.bar,
                        borderRadius: 6,
                        borderSkipped: false,
                        maxBarThickness: 60,
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function (ctx) {
                                return (
                                    " R$ " +
                                    ctx.parsed.y.toLocaleString("pt-BR", {
                                        minimumFractionDigits: 2,
                                    })
                                );
                            },
                        },
                    },
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: {
                            font: { size: 12, family: "'Plus Jakarta Sans', sans-serif" },
                            color: "#5f6f8f",
                        },
                    },
                    y: {
                        grid: { color: "rgba(203,213,225,0.5)", lineWidth: 1 },
                        ticks: {
                            font: { size: 11, family: "'Plus Jakarta Sans', sans-serif" },
                            color: "#94a3b8",
                            callback: function (v) {
                                if (v >= 1000) return "R$ " + (v / 1000).toFixed(0) + "k";
                                return "R$ " + v;
                            },
                        },
                    },
                },
            },
        });
    }

    document.addEventListener("DOMContentLoaded", function () {
        initChartLinha();
        initChartDonut();
        initChartBarra();
    });
})();
