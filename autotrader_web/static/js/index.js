document.addEventListener("DOMContentLoaded", function () {
  if (window.innerWidth < 992) {
    document
      .querySelectorAll(".navbar .dropdown")
      .forEach(function (everydropdown) {
        everydropdown.addEventListener("hidden.bs.dropdown", function () {
          this.querySelectorAll(".submenu").forEach(function (everysubmenu) {
            everysubmenu.style.display = "none";
          });
        });
      });
    document.querySelectorAll(".dropdown-menu a").forEach(function (element) {
      element.addEventListener("click", function (e) {
        let nextEl = this.nextElementSibling;
        if (nextEl && nextEl.classList.contains("submenu")) {
          e.preventDefault();
          if (nextEl.style.display == "block") {
            nextEl.style.display = "none";
          } else {
            nextEl.style.display = "block";
          }
        }
      });
    });
  }
});

document
  .getElementById("search")
  .addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
      event.preventDefault();
      document.getElementById("search-btn").click();
    }
  });

function searchFunction() {
  let q = document.getElementById("search").value;
  window.location = "/search?q=" + q;
}

function getParameterByName(name, url = window.location.href) {
  name = name.replace(/[\[\]]/g, "\\$&");
  var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
    results = regex.exec(url);
  if (!results) return null;
  if (!results[2]) return "";
  return decodeURIComponent(results[2].replace(/\+/g, " "));
}

if (
  getParameterByName("q") != "" &&
  getParameterByName("q") != null &&
  getParameterByName("q") != undefined
) {
  document.getElementById("search").value = getParameterByName("q");
}

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

let valid_languages = ["ENG", "RUS", "AZE"];
console.log(getCookie("lang"))
if (
  getCookie("lang") == undefined ||
  !valid_languages.includes(getCookie("lang"))
) {
  console.log("HAHAHH")
  document.cookie = "lang=; Max-Age=-99999999;path=/;";
  document.cookie = "lang=ENG;path=/;";
}
document.getElementById("active_lang").innerText = getCookie("lang");

function changeLang(lang) {
  document.cookie = "lang=; Max-Age=-99999999;path=/;";
  document.cookie = "lang=" + lang + ";path=/;";
  window.location.reload();
}

const auction_calculate = (lot_id, bid, to_country) => {
  return fetch(`/calculator?lot_id=${lot_id}&bid=${bid}&to_country=${to_country}`)
  .then(res=>res.json())
  .then(data=>data)
  .catch(err=>{
    console.log(err)
  })
}

const car_details_calculate = async (lot_id) => {
  const response_elements = [
    "auction-fee",
    "shipping-fee",
    "service-fee",
    "final-price",
    "car-bid",
    "documentation_fee",
    "transfer_fee",
    "insurance_fee",
    "customs-fee"
  ]
  const bid = document.getElementById("bid").value
  const to_country = document.getElementById("to_country").value
  const response = await auction_calculate(lot_id, bid, to_country);
  console.log(response)
  response_elements.forEach(id=>{
    try {
      const el = document.getElementById(id);
      const prop = el.getAttribute("data-response-prop")
      if (Object.keys(response).includes(prop)) {
        let value = response[prop];
        if (value == null) {
          value = "0"
        }
        el.innerText = value + " " + response.currency;
        console.log(prop, response[prop])
      }
    } catch (err) {
      console.log(err)
    }
  })
}

const home_calculate = async () => {
  const response_elements = [
    "auction-fee",
    "shipping-fee",
    "service-fee",
    "final-price",
    "car-bid",
    "cost_of_delivery_to_baku",
    "from_port",
    "from_country",
    "auction_company",
    "transfer_fee",
    "documentation_fee",
    "insurance_fee",
  ]
  const bid = document.getElementById("bid").value
  const lot_id = document.getElementById("lot_id_home_calculator").value
  const to_country = document.getElementById("to_country").value
  const response = await auction_calculate(lot_id, bid, to_country);
  console.log(response)
  response_elements.forEach(id=>{
    try {
      const el = document.getElementById(id);
      const prop = el.getAttribute("data-response-prop")
      if (Object.keys(response).includes(prop)) {
        if (isNaN(response[prop])) {
          el.innerText = response[prop];
        } else {
          el.innerText = response[prop] + " " + response.currency;
        }
      }
    } catch (err) {
      console.log(err)
    }
  })
}