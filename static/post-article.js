var apikey = "ef429efba9bfcdc3708191d5c354509d";
function readURL(e) {
  if (e.files && e.files[0]) {
    var n = new FileReader();
    (n.onload = function (e) {
      $("#imageResult").attr("src", e.target.result);
    }),
      n.readAsDataURL(e.files[0]);
  }
}
$(function () {
  $("#upload").on("change", function () {
    readURL(input), uploadimage("upload");
  });
});
var input = document.getElementById("upload"),
  infoArea = document.getElementById("upload-label"),
  urllink = document.getElementById("urllink");
function showFileName(e) {
  var n = e.srcElement.files[0].name;
  infoArea.textContent = "File name: " + n;
}
function uploadimage(e) {
  var n = document.getElementById(e),
    a = new FormData();
  a.append("image", n.files[0]);
  var o = {
    url: "https://api.imgbb.com/1/upload?key=" + apikey,
    method: "POST",
    timeout: 0,
    processData: !1,
    mimeType: "multipart/form-data",
    contentType: !1,
    data: a,
  };
  $.ajax(o).done(function (e) {
    console.log(e);
    var n = JSON.parse(e);
    console.log(n.data.url), (urllink.innerHTML = n.data.url);
  });
}
input.addEventListener("change", showFileName),
  $(document)
    .on("dragstart dragenter dragover", function (e) {
      $("#image-drag-drop").removeClass("d-none"), (dropZoneVisible = !0);
    })
    .on("drop dragleave dragend", function (e) {
      (dropZoneTimer = setTimeout(function () {
        dropZoneVisible || $("#image-drag-drop").addClass("d-none");
      }, 50)),
        clearTimeout(dropZoneTimer);
    });
const scriptURL = "",
  form = document.forms["application-form"];
let res;
function successs() {
  $("#success").removeClass("d-none"),
    $("#wait").addClass("d-none"),
    200 !== res.status &&
      ($("#success").addClass("d-none"), $("#fail").removeClass("d-none"));
}
form.addEventListener("submit", (e) => {
  e.preventDefault(),
    $("#submit-btn").addClass("d-none"),
    document.getElementById("wait").classList.remove("d-none"),
    fetch("", { method: "POST", body: new FormData(form) })
      .then((e) => {
        (res = e), console.log("Success!", e);
      })
      .catch((e) => {
        console.error("Error!", e.message),
          $("#fail").removeClass("d-none"),
          $("#success").addClass("d-none");
      }),
    setTimeout(successs, 5e3);
});
