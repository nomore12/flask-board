let area = document.getElementById("content");

document
  .getElementById("not_allow_submit")
  .addEventListener("enter", function (e) {
    if (e.keyCode === 13 && e.target !== area) {
      e.preventDefault();
    }
  });

// window.addEventListener("enter", function (e) {
//   if (e.keyCode === 13 && target !== area) {
//     e.preventDefault();
//   }
// });
