document.addEventListener("DOMContentLoaded", function () {
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
                    title: { display: true, text: title.split("\n") },
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
        ctx.setAttribute("aria-label", `${title.replace("\n", " ")}: ` + data.map(([label, value]) => `${label} ${value}`).join(", "));


        const downloadLink = document.getElementById(`download-${id}`);
        if (downloadLink) {
            downloadLink.addEventListener("click", function () {
                const url = ctx.toDataURL("image/png");
                downloadLink.href = url;
            });
        }
        
    });
});
