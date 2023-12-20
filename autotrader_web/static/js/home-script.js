function homePageSearch() {
  query_params = [];
  params_string = "q=&";
  all_filters = ["make", "model", "fromYear", "toYear", "locationName"];
  all_filters.forEach((filter) => {
    document.getElementsByName(filter).forEach((el) => {
      if (el.selected && el.getAttribute("data-filter-name") != "") {
        query_params.push({
          filterType: filter,
          filterName: el.getAttribute("data-filter-name"),
        });
      }
    });
  });
  query_params.forEach((param) => {
    params_string += `${param.filterType}=${param.filterName}&`;
  });
  params_string = params_string.slice(0, -1);
  window.location = 'autotrader.az/' + "search?" + params_string;
}

function setup() {
    try {
          console.log("called");

  document.querySelector("#bid").addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
      updatePrice();
    }
  });
  document
    .querySelector("#lotid")
    .addEventListener("keypress", function (event) {
      if (event.key === "Enter") {
        updatePrice();
      }
    });
    } catch (err) {

    }
}

window.onload = setup;

function showLessFilters(name) {
  let i = 0;
  document.getElementById(name + "-showmore").innerText = LANG_SHOW_MORE;
  document
    .getElementById(name + "-showmore")
    .setAttribute("onClick", `showMoreFilters('${name}')`);

  document.getElementsByName(name).forEach((el) => {
    if (i >= 24) {
      el.style.display = "none";
    }
    i += 1;
  });
}

function showMoreFilters(name) {
  document.getElementById(name + "-showmore").innerText = LANG_SHOW_LESS;
  document
    .getElementById(name + "-showmore")
    .setAttribute("onClick", `showLessFilters('${name}')`);

  document.getElementsByName(name).forEach((el) => {
    el.style.display = "";
  });
}

function showMoreFiltersMob(name) {
  document.getElementById("homefilter-" + name + "-showmore").innerText =
    LANG_SHOW_LESS;
  document
    .getElementById("homefilter-" + name + "-showmore")
    .setAttribute("onClick", `showLessFiltersMob('${name}')`);
  document.getElementById("homefilter-" + name + "-parent").style.overflowY =
    "scroll";
}

function showLessFiltersMob(name) {
  document.getElementById("homefilter-" + name + "-parent").scrollTo(0, 0);
  document.getElementById("homefilter-" + name + "-showmore").innerText =
    LANG_SHOW_MORE;
  document
    .getElementById("homefilter-" + name + "-showmore")
    .setAttribute("onClick", `showMoreFiltersMob('${name}')`);
  document.getElementById("homefilter-" + name + "-parent").style.overflowY =
    "hidden";
}

function windowResizeFunction() {
  /**/
  let arr = ["vehicleType", "bodyStyle", "primaryDamage", "make"];

  if (window.matchMedia("(max-width: 575px)").matches) {
    arr.forEach((name) => {
      console.log("IF");

      //document.getElementsByName("homefilter-" + name).forEach((el) => {
      //  el.style.display = "";
      //});

      //document.getElementById("homefilter-" + name + "-parent").style.height =
      //  "200px";
     // document.getElementById(
      //  "homefilter-" + name + "-parent"
      //).style.overflowY = "hidden";
      //document
      //  .getElementById("homefilter-" + name + "-showmore")
       // .setAttribute("onClick", `showMoreFiltersMob("${name}")`);
    });

    showLessFilters("homefilter-bodyStyle");
    showLessFilters("homefilter-primaryDamage");
    showLessFilters("homefilter-vehicleType");
    showLessFilters("homefilter-make");
  } else {
    arr.forEach((name) => {
        try {
              document.getElementById("homefilter-" + name + "-parent").style.height =
        "";
      document.getElementById(
        "homefilter-" + name + "-parent"
      ).style.overflowY = "";
      document
        .getElementById("homefilter-" + name + "-showmore")
        .setAttribute("onClick", `showMoreFilters("${name}")`);
        } catch (err) {

        }
    });

    showLessFilters("homefilter-bodyStyle");
    showLessFilters("homefilter-primaryDamage");
    showLessFilters("homefilter-vehicleType");
    showLessFilters("homefilter-make");
  }
}

window.addEventListener("resize", windowResizeFunction);
windowResizeFunction();

document.getElementById("engine-type").addEventListener("change", () => {
    if (document.getElementById("engine-type").value == "5") {
        document.getElementById("engine-capacity").value = 0
        document.getElementById("engine-capacity").disabled = true
    } else {
        document.getElementById("engine-capacity").disabled = false
    }
})

