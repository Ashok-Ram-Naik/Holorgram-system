const voiceDisplay = document.getElementById('voice-display');
const statusText = document.getElementById('status-text');
const voiceStatus = document.getElementById('voice-status');

// Define processCommand since we are removing websocket_client.js
window.processCommand = function (cmd, extra = null) {
    switch (cmd) {
        case 'ROTATE':
        case 'ROTATE_RIGHT':
            window.rotateRight ? window.rotateRight() : window.rotateObject();
            break;

        case 'ROTATE_LEFT':
            window.rotateLeft ? window.rotateLeft() : window.rotateObject();
            break;

        case 'STOP':
        case 'CLOSED_FIST':
            window.stopObject();
            break;

        case 'NEXT_OBJECT':
        case 'SWIPE_LEFT':
            window.nextObject();
            break;

        case 'PREV_OBJECT':
        case 'SWIPE_RIGHT':
            window.previousObject();
            break;

        case 'ZOOM':
        case 'PINCH':
            window.zoomObject ? window.zoomObject() : null;
            break;

        case 'JUMP':
            if (extra) window.jumpToObject(extra);
            break;
    }
};

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (SpeechRecognition) {
    const recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true; // Use interim for faster feedback
    recognition.lang = 'en-US';

    recognition.onstart = function () {
        console.log("Browser Voice Recognition started.");
        statusText.innerText = 'CORE ONLINE';
        statusText.classList.remove('offline');
        statusText.classList.add('online');
    };

    recognition.onresult = function (event) {
        let interimTranscript = '';
        let finalTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
                finalTranscript += event.results[i][0].transcript.toLowerCase();
            } else {
                interimTranscript += event.results[i][0].transcript.toLowerCase();
            }
        }

        const transcript = finalTranscript || interimTranscript;
        if (!transcript) return;

        voiceStatus.innerText = `Voice: ${transcript.length > 20 ? '...' + transcript.slice(-20) : transcript}`;

        if (finalTranscript) {
            console.log("🎤 Final Heard: ", finalTranscript);
            let command = null;
            let extra = null;

            // Direct Object Selection
            const objectNames = ["cube", "sphere", "pyramid", "torus", "dna knot", "dodecahedron", "icosahedron", "cylinder", "octahedron", "ring"];
            for (let name of objectNames) {
                if (finalTranscript.includes(name)) {
                    command = 'JUMP';
                    extra = name;
                    break;
                }
            }

            if (!command) {
                if (finalTranscript.match(/rotate right|spin right|turn right/)) command = 'ROTATE_RIGHT';
                else if (finalTranscript.match(/rotate left|spin left|turn left/)) command = 'ROTATE_LEFT';
                else if (finalTranscript.match(/rotate|spin|turn|start/)) command = 'ROTATE';
                else if (finalTranscript.match(/zoom|closer|bigger/)) command = 'ZOOM';
                else if (finalTranscript.match(/previous|back|before/)) command = 'PREV_OBJECT';
                else if (finalTranscript.match(/next|change|switch|another/)) command = 'NEXT_OBJECT';
                else if (finalTranscript.match(/stop|halt|pause|wait/)) command = 'STOP';
            }

            if (command) {
                voiceDisplay.innerText = command + (extra ? `: ${extra}` : '');
                window.processCommand(command, extra);

                // Visual Pulse
                voiceDisplay.parentElement.style.boxShadow = "0 0 20px var(--accent)";
                setTimeout(() => {
                    voiceDisplay.parentElement.style.boxShadow = "none";
                }, 500);
            }
        }
    };

    let isPermissionDenied = false;

    recognition.onerror = function (event) {
        console.error("Speech recognition error", event.error);
        if (event.error === 'not-allowed' || event.error === 'service-not-allowed') {
            isPermissionDenied = true;
            voiceDisplay.innerText = "Mic Permission Blocked";
            statusText.innerText = "CLICK HUD TO ENABLE MIC";
            statusText.classList.remove('online');
            statusText.classList.add('offline');
        }
    };

    recognition.onend = function () {
        // Auto-restart listening if it stops, but ONLY if not explicitly denied by user
        if (!isPermissionDenied) {
            setTimeout(() => {
                try {
                    recognition.start();
                } catch (e) { }
            }, 2000); // 2 second buffer to prevent aggressive re-prompting
        }
    };

    let voiceInitialized = false;

    // Start it up - Browsers require user interaction to use the mic reliably!
    const startVoice = () => {
        isPermissionDenied = false; // Reset denial state on click
        try {
            recognition.start();
            voiceInitialized = true;
            statusText.innerText = 'System Online (Listening)';
        } catch (e) { }
    };

    // Try starting immediately
    startVoice();

    // Fallback: Start on any click if blocked by browser policy
    document.body.addEventListener('click', startVoice);

} else {
    console.warn("Speech Recognition API not supported in this browser.");
    voiceDisplay.innerText = "Voice unsupported in this browser";
}
