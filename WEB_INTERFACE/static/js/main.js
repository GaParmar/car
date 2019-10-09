var thrustGauge;
var steerGuage;

window.onload = () => {
  get_log_path((log_path) => document.getElementById("log_dir_content").value = log_path);
}

document.getElementById("refresh").addEventListener("click", () => {
  get_log_path((log_path) => document.getElementById("log_dir_content").value = log_path);
});

document.getElementById("send").addEventListener("click", () => {
  post_log_path(document.getElementById("log_dir_content").value);
});
