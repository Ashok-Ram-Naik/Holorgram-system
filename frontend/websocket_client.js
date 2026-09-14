const ws = new WebSocket('ws://localhost:8765');

const gestureDisplay = document.getElementById('gesture-display');
const voiceDisplay = document.getElementById('voice-display');
const statusText = document.getElementById('status-text');

let lastGestureTime = 0;
let lastVoiceTime = 0;

ws.onopen = () => {
    console.log('Connected to Hologram Backend');
    statusText.innerText = 'System Online';
    statusText.classList.remove('offline');
    statusText.classList.add('online');
};

ws.onclose = () => {
    console.log('Disconnected from Hologram Backend');
    statusText.innerText = 'System Offline';
    statusText.classList.remove('online');
    statusText.classList.add('offline');
    
    // Try to reconnect
    setTimeout(() => {
        window.location.reload();
    }, 5000);
};

ws.onerror = (error) => {
    console.error('WebSocket Error: ', error);
};

ws.onmessage = (event) => {
    try {
        const data = JSON.parse(event.data);
        const now = Date.now();
        
        if (data.type === 'GESTURE') {
            gestureDisplay.innerText = data.command;
            
            // Debounce gestures to avoid multiple rapid fires
            if (now - lastGestureTime > 1000 || data.command === 'OPEN_PALM' || data.command === 'CLOSED_FIST') {
                processCommand(data.command);
                if (data.command !== 'None') {
                    lastGestureTime = now;
                }
            }
        } else if (data.type === 'VOICE') {
            voiceDisplay.innerText = `"${data.raw_text}" -> ${data.command}`;
            
            if (now - lastVoiceTime > 1000) {
                processCommand(data.command);
                lastVoiceTime = now;
            }
        }
    } catch (e) {
        console.error("Error parsing websocket message", e);
    }
};

function processCommand(cmd) {
    switch(cmd) {
        case 'ROTATE':
        case 'OPEN_PALM':
            window.rotateObject();
            break;
            
        case 'STOP':
        case 'CLOSED_FIST':
            window.stopObject();
            break;
            
        case 'NEXT_OBJECT':
        case 'PEACE_SIGN':
            window.nextObject();
            break;
            
        case 'ZOOM':
        case 'PINCH':
            window.zoomObject();
            break;
    }
}
