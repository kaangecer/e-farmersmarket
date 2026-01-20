document.addEventListener("DOMContentLoaded", () => {
  const el = document.getElementById("homeMap");
  if (!el) return;

  // Deutschland als Startpunkt
  const map = L.map("homeMap").setView([52.5200, 13.4050], 10);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 12,
    attribution: "&copy; OpenStreetMap"
  }).addTo(map);

  // Testmarker
  L.marker([52.52, 13.405]).addTo(map).bindPopup("Demo: Berlin");
});
