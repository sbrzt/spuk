document.addEventListener("DOMContentLoaded", function () {
  const itemsPerPage = 15;
  const items = Array.from(document.querySelectorAll(".entity"));
  console.log(`🔍 Found ${items.length} .entity cards`);
  const totalPages = Math.ceil(items.length / itemsPerPage);
  let currentPage = 1;

  function showPage(page) {
    items.forEach((item, index) => {
      item.style.display = (
        index >= (page - 1) * itemsPerPage && index < page * itemsPerPage
      ) ? "" : "none";
    });
    renderPagination(page);
  }

  function renderPagination(current) {
    const paginationList = document.getElementById("pagination");
    paginationList.innerHTML = "";

    const range = getPageRange(current, totalPages);

    range.forEach(page => {
      if (page === "...") {
        const li = document.createElement("li");
        li.innerHTML = `<span class="pagination-ellipsis">&hellip;</span>`;
        paginationList.appendChild(li);
      } else {
        const li = document.createElement("li");
        li.innerHTML = `<a class="pagination-link ${page === current ? "is-current" : ""}">${page}</a>`;
        paginationList.appendChild(li);
      }
    });

    // Handle previous/next buttons
    document.querySelector(".pagination-previous").onclick = () => {
      if (currentPage > 1) {
        currentPage--;
        showPage(currentPage);
      }
    };

    document.querySelector(".pagination-next").onclick = () => {
      if (currentPage < totalPages) {
        currentPage++;
        showPage(currentPage);
      }
    };

    // Add event listeners
    paginationList.querySelectorAll(".pagination-link").forEach(link => {
      link.addEventListener("click", function () {
        const page = parseInt(this.textContent);
        currentPage = page;
        showPage(currentPage);
      });
    });
  }

  function getPageRange(current, total) {
    const delta = 2;
    const range = [];
    const rangeWithDots = [];
    let l;

    for (let i = 1; i <= total; i++) {
      if (i === 1 || i === total || (i >= current - delta && i <= current + delta)) {
        range.push(i);
      }
    }

    for (let i of range) {
      if (l) {
        if (i - l === 2) {
          rangeWithDots.push(l + 1);
        } else if (i - l !== 1) {
          rangeWithDots.push("...");
        }
      }
      rangeWithDots.push(i);
      l = i;
    }

    return rangeWithDots;
  }

  if (items.length > 0) {
    showPage(currentPage);
  }
});
