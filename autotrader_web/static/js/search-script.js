let ACTIVE_LAYOUT = "VERTICAL";
const TOTAL_PAGES = Math.ceil(TOTAL_SEARCH_RESULTS / 20);
console.log(TOTAL_SEARCH_RESULTS)

function getParameterByName(name, url = window.location.href) {
  name = name.replace(/[\[\]]/g, "\\$&");
  var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
    results = regex.exec(url);
  if (!results) return null;
  if (!results[2]) return "";
  return decodeURIComponent(results[2].replace(/\+/g, " "));
}

function changeLayout(to) {
  if (window.matchMedia("(min-width:768px)").matches) {
    if (to == "grid") {
      ACTIVE_LAYOUT = "GRID";
      document.getElementById("grid-layout").style.display = "block";
      document.getElementById("vertical-layout").style.display = "none";
      document.getElementById("grid-btn").style.backgroundColor = "#c91f3b";
      document.getElementById("grid-btn").style.color = "white";
      document.getElementById("list-btn").style.backgroundColor = "white";
      document.getElementById("list-btn").style.color = "#c91f3b";
    } else {
      ACTIVE_LAYOUT = "VERTICAL";
      document.getElementById("grid-layout").style.display = "none";
      document.getElementById("vertical-layout").style.display = "";
      document.getElementById("list-btn").style.backgroundColor = "#c91f3b";
      document.getElementById("list-btn").style.color = "white";
      document.getElementById("grid-btn").style.backgroundColor = "white";
      document.getElementById("grid-btn").style.color = "#c91f3b";
    }
  } else {
      ACTIVE_LAYOUT = "VERTICAL"
      document.getElementById("grid-layout-mobile").style.display = "none";
      document.getElementById("vertical-layout-mobile").style.display = "";
      document.getElementById("list-btn").style.backgroundColor = "#c91f3b";
      document.getElementById("list-btn").style.color = "white";
      document.getElementById("grid-btn").style.backgroundColor = "white";
      document.getElementById("grid-btn").style.color = "#c91f3b";
  }
}

function filterSBar() {
  const filters_button = document.getElementById("show-all-filters-button");
  if (document.getElementById("s-bar").style.display == "none") {
    document.getElementById("s-bar").style.display = "";
    document.getElementById("full").style.width = "";
    filters_button.style.backgroundColor = "#c91f3b";
    filters_button.style.color = "white";
  } else {
    document.getElementById("s-bar").style.display = "none";
    document.getElementById("full").style.width = "100%";
    filters_button.style.backgroundColor = "white";
    filters_button.style.color = "#c91f3b";
  }
}

function hideFilterOnMob() {
  if (window.matchMedia("(max-width:991px)").matches) {
    if (document.getElementById("s-bar").style.display != "none") {
      filterSBar();
    }
  }
}

if (window.matchMedia("(max-width:991px)").matches) {
  hideFilterOnMob();
} else {
  filterSBar();
}

const onresizeFunction = () => {
  hideFilterOnMob();

  if (window.matchMedia("(min-width:768px)").matches) {
    document.getElementById("layout-btns").style.display = "";
    document.getElementById("grid-layout-mobile").style.display = "none";
    document.getElementById("vertical-layout-mobile").style.display = "none";
    if (ACTIVE_LAYOUT == "GRID") {
      document.getElementById("grid-layout").style.display = "block";
      document.getElementById("vertical-layout").style.display = "none";
    } else {
      document.getElementById("vertical-layout").style.display = "";
      document.getElementById("grid-layout").style.display = "none";
    }
  } else {
    document.getElementById("layout-btns").style.display = "none";
    document.getElementById("grid-layout").style.display = "none";
    document.getElementById("vertical-layout").style.display = "";
    document.getElementById("vertical-layout-mobile").style.display = "";
    document.getElementById("grid-layout-mobile").style.display = "none";
  }
}

onresizeFunction();
window.addEventListener("resize", onresizeFunction);

const filters = ["auctionCompany", "damageType", "model", "make", "locationName", "year", "bodyStyle", "color", "vehicleType", "engineSize", "odometer", "newlyAddedLots", "primaryDamage"]

function applyFilter(remove="") {
  let q = document.getElementById("search").value;
  const query_params = [{ name: "q", value: q }];
  let params = "";

  filters.forEach(f=>{
    document.querySelectorAll(`[name="${f}-finput"]`).forEach(el=>{
      if (el.checked && el.getAttribute("data-value") != remove) {
        query_params.push({
          name:el.getAttribute("name").replace("-finput", ""),
          value:el.getAttribute("data-value")
        })
      }
    })
  })

  if (window.location.href.search("fromYear") !== -1 && remove.search("From Year") === -1) {
    query_params.push({
      name:"fromYear",
      value:getParameterByName("fromYear")
    })
  }

  if (window.location.href.search("toYear") !== -1 && remove.search("To Year") === -1) {
    query_params.push({
      name:"toYear",
      value:getParameterByName("toYear")
    })
  }

  query_params.forEach((param) => {
    params += `${param.name}=${param.value}&`;
  });
  params = params.slice(0, -1);

  window.location = "/search?" + params;
}

function removeFilter(filter) {
    applyFilter(filter);
}

function showLessFilters(filter) {
  let i = 0;
  const filters = document.querySelectorAll(`[name="${filter}-finput-div"]`)
  filters.forEach(el=>{
    i+=1;
    if (i >= 5) {
      el.style.display = "none";
    }
  })
  document.getElementById(filter+"-message").innerText = LANG_SHOW_MORE;
  document.getElementById(filter+"-showbtn").setAttribute("onClick", `showMoreFilters('${filter}')`);
}

function showMoreFilters(filter) {
  const filters = document.querySelectorAll(`[name="${filter}-finput-div"]`)
  filters.forEach(el=>{
    el.style.display = "";
  })
  document.getElementById(filter+"-message").innerText = LANG_SHOW_LESS;
  document.getElementById(filter+"-showbtn").setAttribute("onClick", `showLessFilters('${filter}')`);
}

filters.forEach(filter=>{
  try {
    showLessFilters(filter);
  } catch (err) {}
})

function addQueryToUrl(url, key, value) {
  if (url.search("=") !== -1) {
    url += `&`;
  } else {
    url += `?`
  }

  url += `${key}=${value}`;
  return url;
}

function setPagination() {
  let pages = "";
  console.log(TOTAL_PAGES)
    let url = window.location.href;
    let current_page = 1;
    if (url.search("page") !== -1) {
      current_page = parseInt(getParameterByName("page"));
    }
    if (url.search("page") !== -1) {
      if (url.search("&") !== -1) {
        url = url.replace(`&page=${getParameterByName("page")}`, "")
      } else {
        url = url.replace(`page=${getParameterByName("page")}`, "")
      }
    }

    let back_url = "#"
    let next_url = "#"
    if (current_page+1 <= TOTAL_PAGES) {
      next_url = addQueryToUrl(url, "page", (current_page+1).toString());
    }
    if (current_page-1 >= 1) {
      back_url = addQueryToUrl(url, "page", (current_page-1).toString());
    }

    for(let i=current_page-3;i<=current_page+3;i++) {
      if (i >= 1 && i <= TOTAL_PAGES) {
        pages += `
        <li class="page-item ${current_page == i ? "active" : null}">
        <a class="page-link" href="${addQueryToUrl(url, "page", i)}">${i}</a>
        </li>
        `
      }
    }

    document.querySelector(".search-pagination-main").innerHTML = `
              <li class="page-item">
                <a class="page-link" href="${back_url}"
                  ><i class="fa fa-angle-left"></i
                ></a>
              </li>
              ${pages}
              <li class="page-item">
                <a class="page-link" href="${next_url}"
                  ><i class="fa fa-angle-right"></i
                ></a>
              </li>
    `
}

setPagination();

function filterSlider(todo) {
  const slider = document.querySelector(".filter-slider-child");
  if (todo == "right") {
    slider.scrollTo(slider.scrollLeft + 50, 0)
  } else {
    slider.scrollTo(slider.scrollLeft - 50, 0)
  }
}

function applyTopFilter(name) {
    url = window.location.href.split("?")[0] + "?"
    let filters = window.location.href.split("&")
    filters.forEach(fil=>{
        if (fil.search("\\?") !== -1) {
            url += fil.split("?")[1].split("=")[0] + "=" + fil.split("?")[1].split("=")[1]
        } else {
            url += fil.split("=")[0] + "=" + fil.split("=")[1]
        }
    })
    console.log(filters)
    if (!filters.includes("buyItNow=1")) {
        url += "&buyItNow=1"
    }
    window.location = url
}
