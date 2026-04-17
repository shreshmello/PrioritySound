const COLORS = {
  emergency: '#f87171',
  high: '#fb923c',
  medium: '#fcd34d',
  low: '#6ee7b7',
};

async function fetchDirection() {
  try {
    const data = await fetch('/direction_data').then(r => r.json());

    const arrow = document.getElementById('ar-arrow');
    const dirText = document.getElementById('ar-direction-text');
    const soundText = document.getElementById('ar-sound-text');
    const label = document.getElementById('ar-label');
    const color = COLORS[data.priority] || COLORS.low;

    arrow.textContent = data.direction === 'left' ? '◀' : data.direction === 'right' ? '▶' : '●';
    arrow.style.color = color;
    arrow.style.textShadow = `0 0 24px ${color}`;
    dirText.textContent = data.direction.toUpperCase();
    dirText.style.color = color;
    soundText.textContent = data.label;
    if (label) label.textContent = data.label;

    ['left', 'center', 'right'].forEach(d => {
      const el = document.getElementById(`ar-${d}`);
      if (el) {
        el.classList.toggle('active', d === data.direction);
      }
    });
  } catch(e) {}
}

setInterval(fetchDirection, 1500);
fetchDirection();