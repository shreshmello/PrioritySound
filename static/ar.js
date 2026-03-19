const canvas = document.getElementById("overlay");
const ctx = canvas.getContext("2d");
const video = document.getElementById("videoFeed");
const toggleButton = document.getElementById("toggleButton");
let audioContext, analyser, dataArray;
let cameraOn = false;
let blob = {
    x: 0,
    y: 0,
    targetX: 0,
    targetY: 0,
    size: 40
};
// Resize canvas to container
function resizeCanvas() {
    const container = document.getElementById("ar-section");
    canvas.width = container.clientWidth;
    canvas.height = container.clientHeight;
}
window.addEventListener("resize", resizeCanvas);
resizeCanvas();
// Start microphone
async function startAudio() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        audioContext = new AudioContext();
        const source = audioContext.createMediaStreamSource(stream);
        analyser = audioContext.createAnalyser();
        analyser.fftSize = 512;
        source.connect(analyser);
        dataArray = new Uint8Array(analyser.frequencyBinCount);
    } catch (err) {
        console.error("Mic error:", err);
    }
}
startAudio();
// Toggle camera
toggleButton.addEventListener("click", async () => {
    cameraOn = !cameraOn;
    video.style.display = cameraOn ? "block" : "none";

    if (cameraOn && !video.srcObject) {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            video.srcObject = stream;
        } catch (err) {
            console.error("Camera error:", err);
        }
    }
});
// Compute sound intensity
function getVolume() {
    if (!analyser) return 0;
    analyser.getByteFrequencyData(dataArray);
    return dataArray.reduce((a, b) => a + b) / dataArray.length;
}
// Update blob position dynamically
function updateBlob() {
    const volume = getVolume();
    if (volume > 40) {
        // Map volume to screen area
        blob.targetX = (Math.sin(Date.now() * 0.002) * 0.4 + 0.5) * canvas.width;
        blob.targetY = (Math.cos(Date.now() * 0.002) * 0.4 + 0.5) * canvas.height;
        blob.size = 30 + volume * 0.3;
    }
    // Smooth movement
    blob.x += (blob.targetX - blob.x) * 0.08;
    blob.y += (blob.targetY - blob.y) * 0.08;
}
// Draw glowing blob
function drawBlob() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const gradient = ctx.createRadialGradient(
        blob.x, blob.y, 0,
        blob.x, blob.y, blob.size
    );

    gradient.addColorStop(0, "rgba(255, 0, 0, 0.9)");
    gradient.addColorStop(1, "rgba(255, 0, 0, 0)");
    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.arc(blob.x, blob.y, blob.size, 0, Math.PI * 2);
    ctx.fill();
}
// Animation loop
function animate() {
    updateBlob();
    drawBlob();
    requestAnimationFrame(animate);
}

animate();
