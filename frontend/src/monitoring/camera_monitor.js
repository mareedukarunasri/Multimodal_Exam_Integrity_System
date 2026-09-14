let cameraStream = null;
let microphoneStream = null;
let detectionInterval = null;

let faceApiReady = false;
let cocoModel = null;

// ===============================
// CONFIGURATION
// ===============================

const STUDENT_ID = "S001";
const BACKEND_URL = "http://127.0.0.1:8000";

const HEAD_MOVEMENT_THRESHOLD = 0.18;

const FACE_CONFIRMATIONS = 2;
const PHONE_CONFIRMATIONS = 2;
const TALK_CONFIRMATIONS = 3;

const TALKING_THRESHOLD = 0.025;


// ===============================
// STATE VARIABLES
// ===============================

let noFaceCount = 0;
let multipleFaceCount = 0;
let phoneCount = 0;

let leftCount = 0;
let rightCount = 0;

let talkCount = 0;

let currentFaceState = "normal";
let currentPhoneState = false;
let currentTalkingState = false;

let lastSentEvent = "";


// ===============================
// AUDIO / MICROPHONE
// ===============================

let audioContext = null;

let microphoneSource = null;
let microphoneAnalyser = null;

let microphoneData = null;

let microphoneActive = false;


// ===============================
// SIREN
// ===============================

let sirenOscillator = null;
let sirenGain = null;
let sirenInterval = null;

let sirenActive = false;


// ===============================
// HELPER
// ===============================

function updateStatus(id, text) {

    const element =
        document.getElementById(id);

    if (element) {
        element.textContent = text;
    }
}


// ===============================
// FULL SCREEN WARNING
// ===============================

function showRedWarning(message) {

    let warning =
        document.getElementById(
            "suspiciousWarning"
        );

    if (!warning) {

        warning =
            document.createElement("div");

        warning.id =
            "suspiciousWarning";

        warning.innerHTML = `
            <div class="warningBox">

                <div class="warningMarks">
                    !!
                </div>

                <div class="warningTitle">
                    SUSPICIOUS ACTIVITY DETECTED
                </div>

                <div class="warningMessage"
                     id="warningMessage">
                </div>

            </div>
        `;

        warning.style.position = "fixed";
        warning.style.top = "0";
        warning.style.left = "0";
        warning.style.width = "100vw";
        warning.style.height = "100vh";

        warning.style.background =
            "rgba(220, 0, 0, 0.96)";

        warning.style.zIndex =
            "999999";

        warning.style.display =
            "flex";

        warning.style.alignItems =
            "center";

        warning.style.justifyContent =
            "center";

        warning.style.textAlign =
            "center";

        warning.style.color =
            "white";

        warning.style.fontFamily =
            "Arial, sans-serif";

        warning.style.boxSizing =
            "border-box";

        document.body.appendChild(
            warning
        );
    }

    const messageElement =
        document.getElementById(
            "warningMessage"
        );

    if (messageElement) {

        messageElement.textContent =
            message;
    }

    warning.style.display =
        "flex";
}


// ===============================
// HIDE RED WARNING
// ===============================

function hideRedWarning() {

    const warning =
        document.getElementById(
            "suspiciousWarning"
        );

    if (warning) {

        warning.style.display =
            "none";
    }
}


// ===============================
// AUDIO INITIALIZATION
// ===============================

async function initializeAudio() {

    try {

        if (!audioContext) {

            audioContext =
                new (
                    window.AudioContext ||
                    window.webkitAudioContext
                )();
        }

        if (
            audioContext.state ===
            "suspended"
        ) {

            await audioContext.resume();
        }

        return true;

    } catch (error) {

        console.error(
            "Audio initialization failed:",
            error
        );

        return false;
    }
}


// ===============================
// VOICE WARNING
// ===============================

function speakWarning(message) {

    if (
        !("speechSynthesis" in window)
    ) {
        return;
    }

    window.speechSynthesis.cancel();

    const speech =
        new SpeechSynthesisUtterance(
            message
        );

    speech.rate = 0.9;
    speech.pitch = 1;
    speech.volume = 1;

    window.speechSynthesis.speak(
        speech
    );

    updateStatus(
        "voiceStatus",
        "Active"
    );

    console.log(
        "VOICE WARNING:",
        message
    );
}


// ===============================
// START SIREN
// ===============================

async function startSiren() {

    if (sirenActive) {
        return;
    }

    try {

        const ready =
            await initializeAudio();

        if (!ready) {
            return;
        }

        sirenActive = true;

        updateStatus(
            "sirenStatus",
            "Active"
        );

        sirenOscillator =
            audioContext.createOscillator();

        sirenGain =
            audioContext.createGain();

        sirenOscillator.type =
            "sawtooth";

        sirenGain.gain.setValueAtTime(
            0.18,
            audioContext.currentTime
        );

        sirenOscillator.connect(
            sirenGain
        );

        sirenGain.connect(
            audioContext.destination
        );

        sirenOscillator.start();

        let highTone = false;

        function changeTone() {

            if (
                !sirenOscillator ||
                !audioContext
            ) {
                return;
            }

            const frequency =
                highTone ? 950 : 550;

            sirenOscillator.frequency.setValueAtTime(
                frequency,
                audioContext.currentTime
            );

            highTone =
                !highTone;
        }

        changeTone();

        sirenInterval =
            setInterval(
                changeTone,
                450
            );

    } catch (error) {

        console.error(
            "Siren error:",
            error
        );
    }
}


// ===============================
// STOP SIREN
// ===============================

function stopSiren() {

    if (!sirenActive) {
        return;
    }

    sirenActive = false;

    updateStatus(
        "sirenStatus",
        "Not active"
    );

    if (sirenInterval) {

        clearInterval(
            sirenInterval
        );

        sirenInterval = null;
    }

    try {

        if (sirenGain) {

            sirenGain.gain.setValueAtTime(
                0,
                audioContext.currentTime
            );
        }

        if (sirenOscillator) {

            sirenOscillator.stop();

            sirenOscillator.disconnect();

            sirenOscillator = null;
        }

        if (sirenGain) {

            sirenGain.disconnect();

            sirenGain = null;
        }

    } catch (error) {

        console.warn(
            "Siren stop:",
            error
        );
    }
}


// ===============================
// START ALERT
// ===============================

async function startAlert(
    message
) {

    console.log(
        "ALERT:",
        message
    );

    showRedWarning(
        message
    );

    speakWarning(
        message
    );

    await startSiren();
}


// ===============================
// STOP ALERT
// ===============================

function stopAlert() {

    if (
        "speechSynthesis" in
        window
    ) {

        window.speechSynthesis.cancel();
    }

    updateStatus(
        "voiceStatus",
        "Not active"
    );

    stopSiren();

    hideRedWarning();
}


// ===============================
// SEND CAMERA EVENT
// ===============================

async function sendCameraEvent(
    eventType
) {

    if (
        lastSentEvent ===
        eventType
    ) {

        return;
    }

    lastSentEvent =
        eventType;


    // ===============================
    // GET CURRENT EXAM SESSION
    // ===============================

    const sessionId =
        window.currentExamSessionId || null;


    const eventData = {

        student_id:
            STUDENT_ID,

        event_type:
            eventType,

        event_time:
            new Date().toISOString(),

        session_id:
            sessionId
    };


    console.log(
        "Sending camera event:",
        eventData
    );


    try {

        const response =
            await fetch(
                `${BACKEND_URL}/api/camera-events`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(
                            eventData
                        )
                }
            );


        if (!response.ok) {

            throw new Error(
                `HTTP ${response.status}`
            );
        }


        updateStatus(
            "backendStatus",
            "Connected"
        );


    } catch (error) {

        console.error(
            "Backend event error:",
            error
        );

        updateStatus(
            "backendStatus",
            "Not connected"
        );
    }
}


// ===============================
// BACKEND CHECK
// ===============================

async function checkBackend() {

    try {

        const response =
            await fetch(
                `${BACKEND_URL}/health`
            );

        if (response.ok) {

            updateStatus(
                "backendStatus",
                "Connected"
            );

            return true;
        }

    } catch (error) {

        console.error(
            "Backend check failed:",
            error
        );
    }

    updateStatus(
        "backendStatus",
        "Not connected"
    );

    return false;
}


// ===============================
// LOAD FACE MODELS
// ===============================

async function loadFaceModels() {

    try {

        updateStatus(
            "cameraStatus",
            "Loading face detection models..."
        );

        const MODEL_URL =
            "https://justadudewhohacks.github.io/face-api.js/models";


        await faceapi.nets.tinyFaceDetector.loadFromUri(
            MODEL_URL
        );


        await faceapi.nets.faceLandmark68Net.loadFromUri(
            MODEL_URL
        );


        faceApiReady = true;


        console.log(
            "Face detection + landmark models loaded"
        );

    } catch (error) {

        console.error(
            "Face model error:",
            error
        );

        faceApiReady = false;

        updateStatus(
            "cameraStatus",
            "Face model failed to load."
        );
    }
}


// ===============================
// LOAD COCO MODEL
// ===============================

async function loadObjectModel() {

    try {

        updateStatus(
            "cameraStatus",
            "Loading object detection model..."
        );

        cocoModel =
            await cocoSsd.load();

        console.log(
            "COCO-SSD model loaded"
        );

    } catch (error) {

        console.error(
            "COCO model error:",
            error
        );

        cocoModel = null;
    }
}


// ===============================
// START MICROPHONE
// ===============================

async function startMicrophone() {

    try {

        microphoneStream =
            await navigator.mediaDevices.getUserMedia(
                {
                    audio: {
                        echoCancellation: true,
                        noiseSuppression: true,
                        autoGainControl: true
                    },
                    video: false
                }
            );


        if (!audioContext) {

            audioContext =
                new (
                    window.AudioContext ||
                    window.webkitAudioContext
                )();
        }


        microphoneSource =
            audioContext.createMediaStreamSource(
                microphoneStream
            );


        microphoneAnalyser =
            audioContext.createAnalyser();


        microphoneAnalyser.fftSize =
            1024;


        microphoneAnalyser.smoothingTimeConstant =
            0.8;


        microphoneData =
            new Uint8Array(
                microphoneAnalyser.fftSize
            );


        microphoneSource.connect(
            microphoneAnalyser
        );


        microphoneActive = true;


        updateStatus(
            "speechStatus",
            "Monitoring"
        );


        console.log(
            "Microphone monitoring started"
        );


    } catch (error) {

        console.error(
            "Microphone access failed:",
            error
        );

        updateStatus(
            "speechStatus",
            "Microphone permission denied"
        );
    }
}


// ===============================
// DETECT VOICE ACTIVITY
// ===============================

function detectTalking() {

    if (
        !microphoneActive ||
        !microphoneAnalyser ||
        !microphoneData
    ) {

        return false;
    }


    microphoneAnalyser.getByteTimeDomainData(
        microphoneData
    );


    let sum = 0;


    for (
        let i = 0;
        i < microphoneData.length;
        i++
    ) {

        const normalized =
            (
                microphoneData[i] -
                128
            ) / 128;

        sum +=
            normalized *
            normalized;
    }


    const rms =
        Math.sqrt(
            sum /
            microphoneData.length
        );


    console.log(
        "Microphone level:",
        rms.toFixed(4)
    );


    return (
        rms >
        TALKING_THRESHOLD
    );
}


// ===============================
// STOP MICROPHONE
// ===============================

function stopMicrophone() {

    microphoneActive = false;


    if (microphoneStream) {

        microphoneStream
            .getTracks()
            .forEach(
                track => track.stop()
            );

        microphoneStream = null;
    }


    microphoneSource = null;

    microphoneAnalyser = null;

    microphoneData = null;


    updateStatus(
        "speechStatus",
        "Not active"
    );
}


// ===============================
// START CAMERA
// ===============================

async function startCamera(
    videoElement
) {

    try {

        if (!videoElement) {

            console.error(
                "Video element not found"
            );

            return false;
        }


        await initializeAudio();


        cameraStream =
            await navigator.mediaDevices.getUserMedia(
                {
                    video: true,
                    audio: false
                }
            );


        videoElement.srcObject =
            cameraStream;


        await videoElement.play();


        updateStatus(
            "cameraStatus",
            "Camera is running."
        );


        console.log(
            "Camera started successfully"
        );


        await checkBackend();


        if (!faceApiReady) {

            await loadFaceModels();
        }


        if (!cocoModel) {

            await loadObjectModel();
        }


        await startMicrophone();


        startDetection(
            videoElement
        );


        return true;


    } catch (error) {

        console.error(
            "Camera start failed:",
            error
        );

        updateStatus(
            "cameraStatus",
            "Camera failed to start."
        );

        return false;
    }
}


// ===============================
// STOP CAMERA
// ===============================

function stopCamera() {

    console.log(
        "Stopping camera..."
    );


    if (detectionInterval) {

        clearInterval(
            detectionInterval
        );

        detectionInterval = null;
    }


    stopMicrophone();


    if (cameraStream) {

        cameraStream
            .getTracks()
            .forEach(
                track => track.stop()
            );

        cameraStream = null;
    }


    stopAlert();


    currentFaceState =
        "normal";

    currentPhoneState =
        false;

    currentTalkingState =
        false;


    noFaceCount = 0;
    multipleFaceCount = 0;
    phoneCount = 0;

    leftCount = 0;
    rightCount = 0;

    talkCount = 0;


    lastSentEvent = "";


    updateStatus(
        "cameraStatus",
        "Camera is not running."
    );


    updateStatus(
        "faceCount",
        "0"
    );


    updateStatus(
        "headMovement",
        "Not active"
    );


    updateStatus(
        "phoneStatus",
        "Not detected"
    );


    updateStatus(
        "speechStatus",
        "Not active"
    );
}


// ===============================
// FACE DETECTION
// ===============================

async function detectFaces(
    videoElement
) {

    if (!faceApiReady) {

        return [];
    }


    try {

        const detections =
            await faceapi
                .detectAllFaces(
                    videoElement,
                    new faceapi.TinyFaceDetectorOptions(
                        {
                            inputSize: 320,
                            scoreThreshold: 0.45
                        }
                    )
                )
                .withFaceLandmarks();


        return detections;


    } catch (error) {

        console.error(
            "Face detection error:",
            error
        );

        return [];
    }
}


// ===============================
// PHONE DETECTION
// ===============================

async function detectPhone(
    videoElement
) {

    if (!cocoModel) {

        return false;
    }


    try {

        const predictions =
            await cocoModel.detect(
                videoElement
            );


        const phones =
            predictions.filter(
                prediction =>
                    prediction.class ===
                    "cell phone" &&
                    prediction.score >=
                    0.35
            );


        return phones.length > 0;


    } catch (error) {

        console.error(
            "Phone detection error:",
            error
        );

        return false;
    }
}


// ===============================
// HEAD MOVEMENT
// ===============================

function detectHeadMovement(
    detection
) {

    if (
        !detection ||
        !detection.landmarks
    ) {

        return "Normal";
    }


    const landmarks =
        detection.landmarks.positions;


    if (
        !landmarks ||
        landmarks.length < 31
    ) {

        return "Normal";
    }


    const leftEye =
        landmarks.slice(36, 42);

    const rightEye =
        landmarks.slice(42, 48);

    const nose =
        landmarks[30];


    const leftEyeX =
        leftEye.reduce(
            (sum, point) =>
                sum + point.x,
            0
        ) / leftEye.length;


    const rightEyeX =
        rightEye.reduce(
            (sum, point) =>
                sum + point.x,
            0
        ) / rightEye.length;


    const eyeCenterX =
        (
            leftEyeX +
            rightEyeX
        ) / 2;


    const eyeDistance =
        Math.abs(
            rightEyeX -
            leftEyeX
        );


    if (eyeDistance === 0) {

        return "Normal";
    }


    const offset =
        (
            nose.x -
            eyeCenterX
        ) / eyeDistance;


    if (
        offset >
        HEAD_MOVEMENT_THRESHOLD
    ) {

        return "Looking Right";
    }


    if (
        offset <
        -HEAD_MOVEMENT_THRESHOLD
    ) {

        return "Looking Left";
    }


    return "Normal";
}


// ===============================
// PROCESS FACE
// ===============================

async function processFaceState(
    detections
) {

    const faceCount =
        detections.length;


    updateStatus(
        "faceCount",
        faceCount.toString()
    );


    if (faceCount === 0) {

        noFaceCount++;

        multipleFaceCount = 0;

        leftCount = 0;
        rightCount = 0;


        updateStatus(
            "headMovement",
            "No face detected"
        );


        if (
            noFaceCount >=
            FACE_CONFIRMATIONS
        ) {

            if (
                currentFaceState !==
                "no_face_detected"
            ) {

                currentFaceState =
                    "no_face_detected";


                await sendCameraEvent(
                    "no_face_detected"
                );


                await startAlert(
                    "Face not detected. Please remain in front of the camera."
                );
            }
        }


        return;
    }


    if (faceCount > 1) {

        multipleFaceCount++;

        noFaceCount = 0;

        leftCount = 0;
        rightCount = 0;


        updateStatus(
            "headMovement",
            "Multiple faces detected"
        );


        if (
            multipleFaceCount >=
            FACE_CONFIRMATIONS
        ) {

            if (
                currentFaceState !==
                "multiple_faces_detected"
            ) {

                currentFaceState =
                    "multiple_faces_detected";


                await sendCameraEvent(
                    "multiple_faces_detected"
                );


                await startAlert(
                    "Multiple faces detected."
                );
            }
        }


        return;
    }


    noFaceCount = 0;
    multipleFaceCount = 0;


    const movement =
        detectHeadMovement(
            detections[0]
        );


    updateStatus(
        "headMovement",
        movement
    );


    if (
        movement ===
        "Looking Left"
    ) {

        leftCount++;

        rightCount = 0;


        if (
            leftCount >=
            FACE_CONFIRMATIONS
        ) {

            if (
                currentFaceState !==
                "looking_left"
            ) {

                currentFaceState =
                    "looking_left";


                await sendCameraEvent(
                    "looking_left"
                );


                await startAlert(
                    "Please look at the screen."
                );
            }
        }


        return;
    }


    if (
        movement ===
        "Looking Right"
    ) {

        rightCount++;

        leftCount = 0;


        if (
            rightCount >=
            FACE_CONFIRMATIONS
        ) {

            if (
                currentFaceState !==
                "looking_right"
            ) {

                currentFaceState =
                    "looking_right";


                await sendCameraEvent(
                    "looking_right"
                );


                await startAlert(
                    "Please look at the screen."
                );
            }
        }


        return;
    }


    leftCount = 0;
    rightCount = 0;


    if (
        currentFaceState !==
        "normal"
    ) {

        currentFaceState =
            "normal";


        await sendCameraEvent(
            "face_detected"
        );
    }


    checkOverallAlert();
}


// ===============================
// PROCESS PHONE
// ===============================

async function processPhoneState(
    detected
) {

    if (detected) {

        phoneCount++;


        updateStatus(
            "phoneStatus",
            "⚠ MOBILE PHONE DETECTED"
        );


        if (
            phoneCount >=
            PHONE_CONFIRMATIONS
        ) {

            if (!currentPhoneState) {

                currentPhoneState =
                    true;


                await sendCameraEvent(
                    "mobile_phone_detected"
                );


                await startAlert(
                    "Mobile phone detected. Please remove the phone."
                );
            }
        }


    } else {

        phoneCount = 0;


        updateStatus(
            "phoneStatus",
            "Not detected"
        );


        if (currentPhoneState) {

            currentPhoneState =
                false;
        }


        checkOverallAlert();
    }
}


// ===============================
// PROCESS TALKING
// ===============================

async function processTalkingState(
    talking
) {

    if (talking) {

        talkCount++;


        updateStatus(
            "speechStatus",
            "⚠ VOICE DETECTED"
        );


        if (
            talkCount >=
            TALK_CONFIRMATIONS
        ) {

            if (!currentTalkingState) {

                currentTalkingState =
                    true;


                await sendCameraEvent(
                    "speech_detected"
                );


                await startAlert(
                    "Talking detected. Please remain silent during the examination."
                );
            }
        }


    } else {

        talkCount = 0;


        updateStatus(
            "speechStatus",
            "Monitoring"
        );


        if (currentTalkingState) {

            currentTalkingState =
                false;
        }


        checkOverallAlert();
    }
}


// ===============================
// CHECK OVERALL ALERT
// ===============================

function checkOverallAlert() {

    const suspicious =
        currentFaceState !==
            "normal" ||
        currentPhoneState ||
        currentTalkingState;


    if (!suspicious) {

        stopAlert();
    }
}


// ===============================
// DETECTION LOOP
// ===============================

function startDetection(
    videoElement
) {

    if (detectionInterval) {

        clearInterval(
            detectionInterval
        );
    }


    console.log(
        "AI detection started"
    );


    detectionInterval =
        setInterval(
            async () => {

                if (
                    !cameraStream ||
                    videoElement.readyState <
                    2
                ) {

                    return;
                }


                try {

                    const detections =
                        await detectFaces(
                            videoElement
                        );


                    await processFaceState(
                        detections
                    );


                    const phoneDetected =
                        await detectPhone(
                            videoElement
                        );


                    await processPhoneState(
                        phoneDetected
                    );


                    const talking =
                        detectTalking();


                    await processTalkingState(
                        talking
                    );


                } catch (error) {

                    console.error(
                        "Detection loop error:",
                        error
                    );
                }

            },
            700
        );
}


// ===============================
// BUTTON SETUP
// ===============================

function setupButtons() {

    const startButton =
        document.getElementById(
            "startCamera"
        );


    const stopButton =
        document.getElementById(
            "stopCamera"
        );


    const videoElement =
        document.getElementById(
            "camera"
        );


    if (startButton) {

        startButton.addEventListener(
            "click",
            async () => {

                await startCamera(
                    videoElement
                );
            }
        );
    }


    if (stopButton) {

        stopButton.addEventListener(
            "click",
            () => {

                stopCamera();
            }
        );
    }
}


// ===============================
// PAGE LOAD
// ===============================

function initializeMonitoringModule() {

    console.log(
        "CameraMonitor.js loaded successfully"
    );

    setupButtons();
    checkBackend();
}


if (document.readyState === "loading") {

    document.addEventListener(
        "DOMContentLoaded",
        initializeMonitoringModule,
        { once: true }
    );

} else {

    initializeMonitoringModule();
}


// ===============================
// GLOBAL FUNCTIONS
// ===============================

window.startCamera =
    startCamera;

window.stopCamera =
    stopCamera;