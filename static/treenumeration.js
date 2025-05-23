var readerfiles,
  drop,
  fileCount,
  fileinput,
  backdrop,
  notify,
  list,
  listwait,
  image_preview,
  dt_allowed = !1,
  listsync = !1;
function init_elements() {
  (drop = document),
    (fileCount = document.getElementById("filecount")),
    (fileinput = document.getElementById("form-files")),
    (backdrop = document.getElementById("backdrop")),
    (list = document.getElementById("list")),
    (notify = document.getElementById("notify")),
    (image_preview = document.getElementById("image_preview")),
    previewClose();
}
function init_fileinput() {
  addEventHandler(fileinput, "change", function (e) {
    return cancelDefault(e), listsync || addFiles(fileinput.files), !1;
  });
}
function init_datatransfer() {
  (dt_allowed = !0),
    (readerfiles = new DataTransfer()),
    addEventHandler(drop, "dragover", function (e) {
      return cancelDefault(e), backdrop.classList.add("visible"), !1;
    }),
    addEventHandler(drop, "dragleave", function (e) {
      return cancelDefault(e), backdrop.classList.remove("visible"), !1;
    }),
    addEventHandler(drop, "dragenter", cancelDefault),
    addEventHandler(drop, "drop", function (e) {
      cancelDefault(e),
        backdrop.classList.remove("visible"),
        addFiles(e.dataTransfer.files);
    });
}
function cancelDefault(e) {
  return (e = e || window.event) && e.preventDefault && e.preventDefault(), !1;
}
function addEventHandler(e, t, i) {
  e.addEventListener
    ? e.addEventListener(t, i, !1)
    : e.attachEvent
    ? e.attachEvent("on" + t, i)
    : (e["on" + t] = i);
}
function clearFiles() {
  (fileinput.value = ""),
    dt_allowed && (readerfiles = new DataTransfer()),
    previewClose(),
    notify_msg("Files removed."),
    listFiles();
}
function addFiles(e) {
  files_text = "Files add:</br>";
  for (var t = 0, i = e.length; t < i; t++)
    (files_text += " " + e[t].name + "</br>"),
      dt_allowed && readerfiles.items.add(e[t]);
  notify_msg(files_text), listFiles();
}
function remFile(e) {
  dt_allowed &&
    (previewClose(),
    (e = parseInt(e)) < 0 ||
      readerfiles.files.length - 1 < e ||
      (notify_msg("File removed:</br>" + readerfiles.files[e].name),
      readerfiles.items.remove(e),
      listFiles()));
}
function listFiles(e = !0) {
  if (e || listwait)
    return (
      listwait && clearTimeout(listwait),
      void (listwait = setTimeout(function () {
        (listwait = null), listFiles(!1);
      }, 200))
    );
  var t = dt_allowed ? readerfiles : fileinput;
  (listsync = !0),
    (fileCount.innerHTML = t.files.length + " files: "),
    (list.innerHTML = "");
  for (var i = 0, n = t.files.length; i < n; i++) {
    var l = document.createElement("button");
    l.setAttribute("type", "button"),
      l.setAttribute("class", "close"),
      l.setAttribute("aria-label", "Close"),
      l.setAttribute("onclick", "remFile(" + i + ")");
    var r = document.createElement("span");
    r.setAttribute("aria-hidden", "true"),
      (r.textContent = "×"),
      l.appendChild(r),
      list.appendChild(l);
    var a = document.createElement("a");
    (a.innerHTML = t.files[i].name + " size " + t.files[i].size + "B"),
      a.setAttribute("href", "#"),
      a.setAttribute("onclick", "previewFile(" + i + ")"),
      list.appendChild(a),
      list.appendChild(document.createElement("br"));
  }
  dt_allowed && (fileinput.files = readerfiles.files), (listsync = !1);
}
function previewClose() {
  image_preview.parentElement.classList.add("invisible");
}
function previewFile(e) {
  if ((previewClose(), !dt_allowed)) return;
  if ((e = parseInt(e)) < 0 || readerfiles.files.length - 1 < e) return;
  const t = new FileReader();
  ["png", "svg", "gif", "jpg", "jpeg", "tiff"].includes(
    readerfiles.files[e].name.split(".", -1).pop().toLowerCase()
  ) &&
    (t.addEventListener(
      "load",
      function () {
        previewFileReader(t.result);
      },
      !1
    ),
    t.readAsDataURL(readerfiles.files[e]));
}
function previewFileReader(e) {
  (image_preview.src = e),
    image_preview.parentElement.classList.remove("invisible");
}
function notify_msg(e) {
  (notify.innerHTML = e), notify.parentElement.classList.remove("invisible");
}
addEventHandler(window, "load", function () {
  init_elements(),
    init_fileinput(),
    window.FileReader && window.DataTransfer
      ? init_datatransfer()
      : notify_msg(
          "Your browser does not support the HTML5 FileReader.<br/> Drag and drop is disabled."
        ),
    listFiles();
});
