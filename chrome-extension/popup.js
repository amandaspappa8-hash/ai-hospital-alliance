function open(path) {
  chrome.tabs.create({ url: `http://localhost:5173${path}` })
}

document.getElementById("searchInput").addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    const q = e.target.value.trim()
    if (q) chrome.tabs.create({ url: `http://localhost:5173/patients?search=${encodeURIComponent(q)}` })
  }
})

// Check API status
fetch("http://127.0.0.1:8000/")
  .then(r => r.json())
  .then(() => {
    document.querySelector(".status").innerHTML = '<div class="dot"></div> System Online — API Connected'
  })
  .catch(() => {
    document.querySelector(".status").style.color = "#f87171"
    document.querySelector(".status").style.background = "rgba(239,68,68,0.1)"
    document.querySelector(".dot").style.background = "#f87171"
    document.querySelector(".status").innerHTML = '<div class="dot" style="background:#f87171"></div> API Offline'
  })
