const BROWSER_BACKEND_URL =
    "http://127.0.0.1:8000/api/browser-events";

console.log("================================");
console.log("BROWSER MONITOR SCRIPT LOADED");
console.log("================================");


function getSessionId() {

    if (window.currentExamSessionId) {
        return window.currentExamSessionId;
    }

    const storedSession =
        sessionStorage.getItem("currentExamSessionId");

    if (storedSession) {
        return storedSession;
    }

    console.warn("No active exam session ID found.");

    return null;
}


window.sendBrowserEvent = function (eventType) {

    const sessionId = getSessionId();

    const eventData = {
        student_id: "S001",
        event_type: eventType,
        event_time: new Date().toISOString(),
        session_id: sessionId
    };

    console.log("================================");
    console.log("BROWSER EVENT DETECTED");
    console.log("Event:", eventType);
    console.log("Session:", sessionId);
    console.log("Event Data:", eventData);
    console.log("================================");


    if (!sessionId) {

        console.warn(
            "Browser event NOT sent because no active exam session exists."
        );

        return;
    }


    fetch(BROWSER_BACKEND_URL, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(eventData)

    })

    .then(response => {

        if (!response.ok) {

            throw new Error(
                "Backend returned HTTP " + response.status
            );
        }

        return response.json();

    })

    .then(data => {

        console.log(
            "BROWSER EVENT SAVED:",
            data
        );

    })

    .catch(error => {

        console.error(
            "BROWSER EVENT FAILED:",
            error
        );

    });

};


/* =========================
   COPY
========================= */

document.addEventListener("copy", function () {

    console.log("COPY DETECTED");

    window.sendBrowserEvent("copy");

});


/* =========================
   PASTE
========================= */

document.addEventListener("paste", function () {

    console.log("PASTE DETECTED");

    window.sendBrowserEvent("paste");

});


/* =========================
   CUT
========================= */

document.addEventListener("cut", function () {

    console.log("CUT DETECTED");

    window.sendBrowserEvent("cut");

});


/* =========================
   RIGHT CLICK
========================= */

document.addEventListener("contextmenu", function () {

    console.log("RIGHT CLICK DETECTED");

    window.sendBrowserEvent("right_click");

});


/* =========================
   TAB VISIBILITY
========================= */

document.addEventListener("visibilitychange", function () {

    if (document.hidden) {

        console.log("TAB HIDDEN");

        window.sendBrowserEvent("tab_hidden");

    } else {

        console.log("TAB VISIBLE");

        window.sendBrowserEvent("tab_visible");

    }

});


/* =========================
   WINDOW BLUR
========================= */

window.addEventListener("blur", function () {

    console.log("WINDOW BLUR");

    window.sendBrowserEvent("window_blur");

});


/* =========================
   WINDOW FOCUS
========================= */

window.addEventListener("focus", function () {

    console.log("WINDOW FOCUS");

    window.sendBrowserEvent("window_focus");

});


/* =========================
   FULLSCREEN EXIT
========================= */

document.addEventListener("fullscreenchange", function () {

    if (!document.fullscreenElement) {

        console.log("FULLSCREEN EXIT");

        window.sendBrowserEvent("fullscreen_exit");

    }

});


console.log(
    "Browser monitoring initialized successfully."
);