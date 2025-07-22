document.addEventListener("DOMContentLoaded", function () {
    const chartsToRender = [
        {
            id: "topEntitiesChart",
            data: window.topEntitiesData,
            title: "Top Entities"
        },
        {
            id: "topPropertiesChart",
            data: window.topPropertiesData,
            title: "Top Properties"
        },
        {
            id: "topClassesChart",
            data: window.topClassesData,
            title: "Top Classes"
        },
        {
            id: "topModelsChart",
            data: window.topModelsData,
            title: "Top Models"
        }
    ];

    chartsToRender.forEach(({ id, data, title }) => {
        if (!data || data.length === 0) return;

        const ctx = document.getElementById(id);
        if (!ctx) return;

        const labels = data.map(item => item[0]);
        const values = data.map(item => item[1]);

        new Chart(ctx, {
            type: "bar",
            data: {
                labels: labels,
                datasets: [{
                label: "Occurrences",
                data: values,
                backgroundColor: "rgba(54, 162, 235, 0.7)"
                }]
            },
            options: {
                responsive: true,
                plugins: {
                legend: { display: false },
                title: { display: true, text: title }
                },
                scales: {
                x: { ticks: { autoSkip: false } }
                }
            }
        });
    });
});
