const video = document.getElementById("camera");
const canvas = document.getElementById("overlay");
const ctx = canvas.getContext("2d");

let audioContext;
let analyser;
let dataArray;

let currentAngle = 90;
let maxVolume = 0;
let strongestAngle = 90;
let pulseSize = 0;
let pulseDirection = 1;

/* CAMERA */

async function startCamera() {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;
}
startCamera();

/* AUDIO ANALYSIS */

async function startAudioAnalysis() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    audioContext = new AudioContext();
    const source = audioContext.createMediaStreamSource(stream);

    analyser = audioContext.createAnalyser();
    analyser.fftSize = 512;

    source.connect(analyser);
    dataArray = new Uint8Array(analyser.frequencyBinCount);
}
startAudioAnalysis();

function getVolumeLevel() {
    if (!analyser) return 0;

    analyser.getByteFrequencyData(dataArray);

    let sum = 0;
    for (let i = 0; i < dataArray.length; i++) {
        sum += dataArray[i];
    }

    return sum / dataArray.length;
}

/* ORIENTATION TRACKING */

window.addEventListener("mousemove", (e) => {
    currentAngle = (e.clientX / window.innerWidth) * 180;
});

/*  FETCH BACKEND */

async function fetchPrediction() {
    const response = await fetch("/latest_prediction");
    return await response.json();
}

/* DIRECTION SYSTEM */

function scanDirection() {
    const volume = getVolumeLevel();
    if (volume > maxVolume) {
        maxVolume = volume;
        strongestAngle = currentAngle;
    }
}

function getDirectionZone() {
    if (strongestAngle < 60) return "left";
    if (strongestAngle < 120) return "center";
    return "right";
}

/* PRIORITY COLOR */

function getColor(label) {
    if (!label) return "white";

    if (label.includes("siren") || label.includes("alarm")) {
        return "#ff2e2e"; // emergency red
    }
    if (label.includes("door")) {
        return "#ffd633"; // yellow
    }
    if (label.includes("baby")) {
        return "#ff8800"; // orange
    }
    return "#00ffcc"; // default teal
}

/* EMERGENCY FLASH MODE */

function flashScreen(color) {
    ctx.fillStyle = color;
    ctx.globalAlpha = 0.15;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.globalAlpha = 1;
}

/* DRAW ARROW */

function drawArrow(x, y, direction, color) {
    ctx.fillStyle = color;
    ctx.strokeStyle = color;
    ctx.lineWidth = 6;

    ctx.beginPath();

    if (direction === "left") {
        ctx.moveTo(x, y);
        ctx.lineTo(x - 40, y - 30);
        ctx.lineTo(x - 40, y + 30);
    } else if (direction === "right") {
        ctx.moveTo(x, y);
        ctx.lineTo(x + 40, y - 30);
        ctx.lineTo(x + 40, y + 30);
    } else {
        ctx.moveTo(x - 30, y - 40);
        ctx.lineTo(x + 30, y - 40);
        ctx.lineTo(x, y);
    }

    ctx.closePath();
    ctx.fill();
}

/* PULSE ANIMATION */

function animatePulse() {
    pulseSize += pulseDirection * 0.8;
    if (pulseSize > 20 || pulseSize < 0) pulseDirection *= -1;
}

/* RENDER LOOP */

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
window.addEventListener("resize", resizeCanvas);
resizeCanvas();

async function updateAR() {
    const prediction = await fetchPrediction();
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    if (prediction.label && prediction.accepted) {
        scanDirection();
        animatePulse();
        const zone = getDirectionZone();
        const color = getColor(prediction.label);
        let x;
        if (zone === "left") x = canvas.width * 0.2;
        else if (zone === "center") x = canvas.width * 0.5;
        else x = canvas.width * 0.8;
        const y = canvas.height / 2;
        // Glow effect
        ctx.shadowColor = color;
        ctx.shadowBlur = 25;
        // Pulsing circle
        ctx.beginPath();
        ctx.arc(x, y, 60 + pulseSize, 0, 2 * Math.PI);
        ctx.fillStyle = color;
        ctx.globalAlpha = 0.4;
        ctx.fill();
        ctx.globalAlpha = 1;
        ctx.shadowBlur = 0;
        // Draw arrow
        drawArrow(x, y - 100, zone, color);
        // Label text
        ctx.fillStyle = "white";
        ctx.font = "bold 36px Arial";
        ctx.textAlign = "center";
        ctx.fillText(prediction.label.toUpperCase(), x, y + 120);
        // Emergency flash
        if (color === "#ff2e2e") {
            flashScreen("#ff2e2e");
        }
    } else {
        maxVolume = 0;
    }
    requestAnimationFrame(updateAR);
}
updateAR();
