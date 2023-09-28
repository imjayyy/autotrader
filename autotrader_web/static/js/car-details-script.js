function changeActiveThumbnail(id) {
  id = parseInt(id);
  const imgs = document.getElementsByName("carimage-items");
  const img_thumbnails = document.getElementsByName("carimage-item-thumbnails");

  img_thumbnails.forEach((img) => {
    img.style.filter = "opacity(50%)";
  });
  img_thumbnails[id].style.filter = "";

  if (imgs[id].classList.contains("active")) {
    return true;
  }

  imgs.forEach((img) => {
    if (img.classList.contains("active")) {
      img.classList.remove("active");
    }
  });

  imgs[id].classList.add("active");
}

const items = document.getElementsByName("carimage-items");
items.forEach((item) => {
  const options = {
    attributes: true,
  };

  function callback(mutationList, observer) {
    mutationList.forEach(function (mutation) {
      if (
        mutation.type === "attributes" &&
        mutation.attributeName === "class"
      ) {
        if (item.classList.contains("active")) {
          changeActiveThumbnail(item.getAttribute("data-img-id"));
        }
      }
    });
  }

  const observer = new MutationObserver(callback);
  observer.observe(item, options);
});

changeActiveThumbnail("0");
