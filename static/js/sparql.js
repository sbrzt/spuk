document.addEventListener("DOMContentLoaded", () => {
  const querySelector = document.getElementById("query-selector");
  const queryTextarea = document.getElementById("sparql-query");
  const runButton = document.getElementById("run-query");
  const resultsContainer = document.getElementById("query-results");

  querySelector.addEventListener("change", () => {
    const selectedIndex = querySelector.value;
    if (selectedIndex !== "") {
      queryTextarea.value = predefinedQueries[selectedIndex].query;
    }
  });

  runButton.addEventListener("click", () => {
    const query = queryTextarea.value.trim();
    if (!query) return alert("Query is empty");

    const endpointUrl = document.querySelector("code").textContent;
    const url = endpointUrl + "?query=" + encodeURIComponent(query);

    fetch(url, {
      headers: { Accept: "application/sparql-results+json" }
    })
    .then(response => response.json())
    .then(data => renderResults(data))
    .catch(err => {
      console.error("SPARQL query failed", err);
      resultsContainer.innerHTML = `<div class="notification is-danger">Query failed. Check console for details.</div>`;
    });
  });

  function renderResults(data) {
    if (!data.results || !data.results.bindings.length) {
      resultsContainer.innerHTML = "<p>No results found.</p>";
      return;
    }

    const vars = data.head.vars;
    const rows = data.results.bindings;

    const table = document.createElement("table");
    table.classList.add("table", "is-fullwidth", "is-striped");

    const thead = table.createTHead();
    const headRow = thead.insertRow();
    vars.forEach(v => {
      const th = document.createElement("th");
      th.textContent = v;
      headRow.appendChild(th);
    });

    const tbody = table.createTBody();
    rows.forEach(binding => {
      const row = tbody.insertRow();
      vars.forEach(v => {
        const cell = row.insertCell();
        cell.textContent = binding[v]?.value || "";
      });
    });

    resultsContainer.innerHTML = "";
    resultsContainer.appendChild(table);
  }
});
