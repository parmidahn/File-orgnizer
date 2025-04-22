function organize() {
  const src = document.getElementById("src").value;
  const dst = document.getElementById("dst").value;
  const button = document.getElementById("orgBtn");
  const loading = document.getElementById("loading");
  const status = document.getElementById("status");

  if (!src || !dst) {
    status.innerText = "Please enter both paths!";
    return;
  }

  button.disabled = true;
  loading.style.display = "block";
  status.innerText = "";

  fetch("/organize", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ src, dst })
  })
  .then(response => response.json())
  .then(data => {
    status.innerText = data.message;
  })
  .catch(error => {
    status.innerText = "Error: " + error;
  })
  .finally(() => {
    loading.style.display = "none";
    button.disabled = false;
  });
}
