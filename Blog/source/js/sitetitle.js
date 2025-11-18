var OriginTitle = document.title;
var titleTime;

document.addEventListener("visibilitychange", function () {
  clearTimeout(titleTime);

  if (document.hidden) {
    document.title = "真的不再看看嘛～";
    titleTime = setTimeout(function () {
      document.title = OriginTitle;
    }, 2000);
  } else {
    document.title = "欢迎回来！";
    titleTime = setTimeout(function () {
      document.title = OriginTitle;
    }, 1000);
  }
});