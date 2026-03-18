
// AR / Sound Localization JS
const canvas = document.getElementById("overlay");
const ctx = canvas.getContext("2d");
const video = document.getElementById("videoFeed");
const toggleButton = document.getElementById("toggleButton");
let audioContext, analyser, dataArray;
let strongestAngle = 90;
let cameraOn = false;
// Toggle Camera
toggleButton.addEventListener("click", () => {
    cameraOn = !cameraOn;
    video.style.display = cameraOn ? "block" : "none";
    if (cameraOn) startCamera();
});
// Start Camera
async function startCamera() {
    if (video.srcObject) return;
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
    } catch (err) {
        console.error("Camera access denied", err);
    }
}
// Start Audio
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
        console.error("Microphone access denied", err);
    }
}
startAudio();
// Scan Direction (mouse-based simulation)
function scanDirection(mouseX) {
    if (!analyser) return;
    analyser.getByteFrequencyData(dataArray);
    const volume = dataArray.reduce((a, b) => a + b) / dataArray.length;
    if (volume > 100) strongestAngle = (mouseX / canvas.width) * 180;
}
canvas.addEventListener("mousemove", e => scanDirection(e.clientX));
// Draw Arrow
function drawArrow() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    let x = strongestAngle < 60 ? canvas.width * 0.2 :
            strongestAngle < 120 ? canvas.width * 0.5 : canvas.width * 0.8;
    ctx.fillStyle = "red";
    ctx.beginPath();
    ctx.moveTo(x, canvas.height/2);
    ctx.lineTo(x, canvas.height/2 - 50);
    ctx.lineTo(x + 20, canvas.height/2 - 30);
    ctx.closePath();
    ctx.fill();
}

// Resize Canvas to Fit Section
function resizeCanvas() {
    const container = document.getElementById("ar-section");
    canvas.width = container.clientWidth;
    canvas.height = container.clientHeight;
}
window.addEventListener("resize", resizeCanvas);
resizeCanvas();
// Animate Loop
function animate() {
    drawArrow();
    requestAnimationFrame(animate);
}
animate();
