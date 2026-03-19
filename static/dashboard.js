document.getElementById("simulate-form")?.addEventListener("submit", async (e) => {
  e.preventDefault();
  const form = e.target;
  const data = new FormData(form);
  const res = await fetch("/simulate_alert", { method: "POST", body: data });
  const json = await res.json();
  addAlertToFeed(json.alert);
  showPopup(json.alert);
  form.reset();
});

function addAlertToFeed(alert){
  const feed = document.getElementById("alerts-feed");
  const div = document.createElement("div");
  div.classList.add("alert-card");
  div.style.borderLeft = "5px solid "+alert.color;
  div.innerHTML = `
    <span class="alert-time">${alert.time}</span>
    <span class="alert-sound">${alert.sound}</span>
    <span class="alert-priority ${alert.priority}">${alert.priority.toUpperCase()}</span>
  `;
  feed.prepend(div);
  if(feed.children.length > 20) feed.removeChild(feed.lastChild);
}

function showPopup(alert){
  const popup = document.createElement("div");
  popup.classList.add("popup-notification");
  popup.style.borderLeft = "5px solid "+alert.color;
  popup.innerHTML = `<strong>${alert.sound}</strong> detected! Priority: ${alert.priority.toUpperCase()}`;
  document.body.appendChild(popup);
  setTimeout(()=>popup.remove(),4000);
}
