async function fetchDirection() {
    const response = await fetch("/direction_data");
    const data = await response.json();

    const arrow = document.getElementById("arrow");
    const label = document.getElementById("sound-label");
    const ring = document.getElementById("distance-ring");
    const halo = document.getElementById("priority-halo");
    const compassAngle = document.getElementById("compass-angle");

    // Rotate arrow
    arrow.style.transform = `rotate(${data.angle}deg)`;

    // Update text
    label.innerText = `${data.label.toUpperCase()} – ${data.angle}°`;
    compassAngle.innerText = `${data.angle}°`;

    // Scale ring by amplitude
    const size = 150 + (data.amplitude * 200);
    ring.style.width = `${size}px`;
    ring.style.height = `${size}px`;

    // Priority Colors
    const colors = {
        emergency: "#ef4444",
        high: "#f97316",
        medium: "#eab308",
        low: "#ffffff"
    };

    arrow.style.color = colors[data.priority];
    halo.style.boxShadow = `0 0 100px 30px ${colors[data.priority]}`;
}

setInterval(fetchDirection, 2000);
