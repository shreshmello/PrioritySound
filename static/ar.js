const video = document.getElementById("camera");
const canvas = document.getElementById("overlay");
const ctx = canvas.getContext("2d");

let audioContext;
let analyser;
let dataArray;

let currentAngle = 90;
let maxVolume = 0;
let strongestAngle = 90;

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

// Use mouse movement as directional scanning
window.addEventListener("mousemove", (e) => {
    currentAngle = (e.clientX / window.innerWidth) * 180;
});

/* FETCH BACKEND PREDICTION */
async function fetchPrediction() {
    const response = await fetch("/latest_prediction");
    return await response.json();
}

/* DIRECTION LOGIC */

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
/* PRIORITY COLORS */

function getColor(label) {
    if (!label) return "white";

    if (label.includes("siren") || label.includes("alarm")) {
        return "red";
    }
    if (label.includes("door")) {
        return "yellow";
    }
    if (label.includes("baby")) {
        return "orange";
    }
    return "green";
}
/* AR RENDER LOOP */

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
        const zone = getDirectionZone();
        const color = getColor(prediction.label);
        ctx.fillStyle = color;
        ctx.font = "bold 40px Arial";
        let x;
        if (zone === "left") x = canvas.width * 0.15;
        else if (zone === "center") x = canvas.width * 0.45;
        else x = canvas.width * 0.75;
        ctx.fillText(prediction.label.toUpperCase(), x, canvas.height / 2);
        // Pulsing circle
        ctx.beginPath();
        ctx.arc(x + 80, canvas.height / 2 - 60, 50, 0, 2 * Math.PI);
        ctx.globalAlpha = 0.6;
        ctx.fill();
        ctx.globalAlpha = 1;
    } else {
        // Reset scanning if no active sound
        maxVolume = 0;
    }
    requestAnimationFrame(updateAR);
}

updateAR();
