const videoElement = document.getElementById('input_video');
const gestureDisplayGD = document.getElementById('gesture-display'); // Renamed to avoid conflicts

const hands = new Hands({
    locateFile: (file) => {
        return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
    }
});

hands.setOptions({
    maxNumHands: 2,
    modelComplexity: 1,
    minDetectionConfidence: 0.7,
    minTrackingConfidence: 0.7
});

let lastAvgX = null;
let lastAvgY = null;
let actionCooldown = 0;
let activeGesture = "None";
let activeGestureStartTime = 0;
let swipeStartX = null;
const SWIPE_THRESHOLD = 0.15;

hands.onResults(onResults);



function getDistance(lm1, lm2) {
    return Math.sqrt(Math.pow(lm1.x - lm2.x, 2) + Math.pow(lm1.y - lm2.y, 2) + Math.pow(lm1.z - lm2.z, 2));
}

const cameraObj = new Camera(videoElement, {
    onFrame: async () => {
        await hands.send({ image: videoElement });
    },
    width: 640,
    height: 480
});
cameraObj.start();

const handCanvas = document.getElementById('hand-canvas');
const handCtx = handCanvas.getContext('2d');
const monitorGesture = document.getElementById('monitor-gesture');

function drawLandmarks(landmarks) {
    handCtx.clearRect(0, 0, handCanvas.width, handCanvas.height);

    // Set canvas internal size if needed
    if (handCanvas.width !== handCanvas.clientWidth) {
        handCanvas.width = handCanvas.clientWidth;
        handCanvas.height = handCanvas.clientHeight;
    }

    if (!landmarks) return;

    handCtx.fillStyle = '#00f3ff';
    handCtx.shadowBlur = 5;
    handCtx.shadowColor = '#00f3ff';

    landmarks.forEach(landmark => {
        const x = landmark.x * handCanvas.width;
        const y = landmark.y * handCanvas.height;

        handCtx.beginPath();
        handCtx.arc(x, y, 2, 0, 2 * Math.PI);
        handCtx.fill();
    });

    // Optional: Draw connections
    handCtx.strokeStyle = 'rgba(0, 243, 255, 0.2)';
    handCtx.lineWidth = 1;
    handCtx.beginPath();
    // Simplified connections for sci-fi look
    for (let i = 0; i < landmarks.length; i++) {
        for (let j = i + 1; j < landmarks.length; j++) {
            const d = Math.hypot(landmarks[i].x - landmarks[j].x, landmarks[i].y - landmarks[j].y);
            if (d < 0.1) {
                handCtx.moveTo(landmarks[i].x * handCanvas.width, landmarks[i].y * handCanvas.height);
                handCtx.lineTo(landmarks[j].x * handCanvas.width, landmarks[j].y * handCanvas.height);
            }
        }
    }
    handCtx.stroke();
}

function onResults(results) {
    let totalFingers = 0;
    let isPinching = false;
    let pinchDist = 0;
    let isOpenPalm = false;
    let palmCenterX = null;
    let palmCenterY = null;
    let isIndexOnly = false;
    let isThumbOnly = false;

    // Draw landmarks if available
    if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
        drawLandmarks(results.multiHandLandmarks[0]);
        for (let i = 0; i < results.multiHandLandmarks.length; i++) {
            const landmarks = results.multiHandLandmarks[i];

            const WRIST = 0;
            const THUMB_TIP = 4, THUMB_MCP = 2;
            const INDEX_TIP = 8, INDEX_PIP = 6;
            const MIDDLE_TIP = 12, MIDDLE_PIP = 10;
            const RING_TIP = 16, RING_PIP = 14;
            const PINKY_TIP = 20, PINKY_PIP = 18;
            const PINKY_BASE = 17;

            const distThumbIndex = getDistance(landmarks[THUMB_TIP], landmarks[INDEX_TIP]);
            const middleClosed = getDistance(landmarks[MIDDLE_TIP], landmarks[WRIST]) < getDistance(landmarks[MIDDLE_PIP], landmarks[WRIST]);
            const ringClosed = getDistance(landmarks[RING_TIP], landmarks[WRIST]) < getDistance(landmarks[RING_PIP], landmarks[WRIST]);
            const pinkyClosed = getDistance(landmarks[PINKY_TIP], landmarks[WRIST]) < getDistance(landmarks[PINKY_PIP], landmarks[WRIST]);

            if (middleClosed && ringClosed && pinkyClosed && distThumbIndex < 0.25) {
                isPinching = true;
                pinchDist = distThumbIndex;
            }

            let fingersOpen = [false, false, false, false, false];
            if (getDistance(landmarks[THUMB_TIP], landmarks[PINKY_BASE]) > getDistance(landmarks[THUMB_MCP], landmarks[PINKY_BASE])) fingersOpen[0] = true;
            if (getDistance(landmarks[INDEX_TIP], landmarks[WRIST]) > getDistance(landmarks[INDEX_PIP], landmarks[WRIST])) fingersOpen[1] = true;
            if (!middleClosed) fingersOpen[2] = true;
            if (!ringClosed) fingersOpen[3] = true;
            if (!pinkyClosed) fingersOpen[4] = true;

            const openFingersCount = fingersOpen.filter(v => v).length;
            totalFingers += openFingersCount;

            if (openFingersCount >= 4) {
                isOpenPalm = true;
                palmCenterX = landmarks[9].x;
                palmCenterY = landmarks[9].y;
            }

            if (fingersOpen[0] && !fingersOpen[1] && !fingersOpen[2] && !fingersOpen[3] && !fingersOpen[4]) {
                isThumbOnly = true;
                palmCenterX = landmarks[THUMB_TIP].x;
            }

            if (!fingersOpen[0] && fingersOpen[1] && !fingersOpen[2] && !fingersOpen[3] && !fingersOpen[4]) {
                isIndexOnly = true;
                palmCenterX = landmarks[INDEX_TIP].x;
            }
        }
    } else {
        drawLandmarks(null);
    }

    let rawGesture = "None";
    if (isPinching) rawGesture = "PINCH";
    else if (isThumbOnly) rawGesture = "THUMB_ONLY";
    else if (isIndexOnly) rawGesture = "INDEX_ONLY";
    else if (isOpenPalm) rawGesture = "MANUAL_ROTATE";
    else if (totalFingers === 0 && results.multiHandLandmarks && results.multiHandLandmarks.length > 0) rawGesture = "STOP";

    if (rawGesture !== activeGesture) {
        activeGesture = rawGesture;
        activeGestureStartTime = Date.now();
        swipeStartX = (rawGesture === "THUMB_ONLY" || rawGesture === "INDEX_ONLY") ? palmCenterX : null;
        monitorGesture.innerText = rawGesture;
    }

    let holdTime = Date.now() - activeGestureStartTime;
    const INTENT_DELAY = 600; // Increased for stability

    if (activeGesture === "PINCH") {
        gestureDisplayGD.innerText = `Pinch Zoom`;
        let zoomVal = 15 - ((pinchDist - 0.02) / 0.18) * 12;
        zoomVal = Math.max(3, Math.min(15, zoomVal));
        if (window.setZoomValue) window.setZoomValue(zoomVal);
    } else if (activeGesture === "THUMB_ONLY" || activeGesture === "INDEX_ONLY") {
        if (holdTime >= INTENT_DELAY) {
            const now = Date.now();
            if (now > actionCooldown) {
                // Detect Swipe movement
                let dx = palmCenterX - swipeStartX;
                if (Math.abs(dx) > SWIPE_THRESHOLD) {
                    if (dx > 0) window.processCommand(activeGesture === "THUMB_ONLY" ? 'NEXT_OBJECT' : 'PREV_OBJECT');
                    else window.processCommand(activeGesture === "THUMB_ONLY" ? 'PREV_OBJECT' : 'NEXT_OBJECT');
                    actionCooldown = now + 1000;
                }
            }
        }
    } else if (activeGesture === "MANUAL_ROTATE") {
        gestureDisplayGD.innerText = `Manual Rotate`;
        if (lastAvgX !== null && lastAvgY !== null && palmCenterX !== null && palmCenterY !== null) {
            let dx = palmCenterX - lastAvgX;
            let dy = palmCenterY - lastAvgY;
            if (Math.abs(dx) < 0.1 && Math.abs(dy) < 0.1) {
                if (window.manualRotate) window.manualRotate(dx, dy);
            }
        }
        lastAvgX = palmCenterX; lastAvgY = palmCenterY;
    } else if (activeGesture === "STOP") {
        gestureDisplayGD.innerText = activeGesture;
        if (window.processCommand) window.processCommand('STOP');
    } else {
        gestureDisplayGD.innerText = "Searching...";
    }
}

