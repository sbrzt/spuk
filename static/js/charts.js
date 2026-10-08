document.addEventListener("DOMContentLoaded", function () {
    // One entry per [[index.charts]] block in config.toml, in page order.
    (window.INDEX_CHARTS || []).forEach(({ title, type, data }, index) => {
        const id = `chart-${index}`;
        const ctx = document.getElementById(id);
        if (!ctx) return;

        const labels = data.map(item => item[0]);
        const values = data.map(item => item[1]);

        new Chart(ctx, {
            type: type,
            data: {
                labels: labels,
                datasets: [{
                    label: "Occurrences",
                    data: values,
                    backgroundColor: window.THEME_CHART_COLOR || "rgba(54, 162, 235, 0.7)"
                }]
            },
            plugins: [ChartDataLabels],
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false },
                    title: { display: true, text: title },
                    datalabels: {
                        color: 'black',
                        anchor: 'end',
                        align: 'start',
                    }
                },
                scales: {
                    x: { ticks: { autoSkip: false }, grid: { display: false } },
                    y: { display: false }
                }
            }
        });

        ctx.style.backgroundColor = 'rgba(255,255,255)';
        // Text alternative: a canvas is opaque to screen readers.
        ctx.setAttribute("aria-label", `${title}: ` + data.map(([label, value]) => `${label} ${value}`).join(", "));


        const downloadLink = document.getElementById(`download-${id}`);
        if (downloadLink) {
            // href is set on click, before the browser follows the link.
            downloadLink.addEventListener("click", function () {
                const url = ctx.toDataURL("image/png");
                downloadLink.href = url;
            });
        }
        
    });
});
