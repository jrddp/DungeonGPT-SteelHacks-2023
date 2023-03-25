const player_response_container = document.getElementById("player-response");
const player_response_form = document.getElementById("player-response-form");
const player_response_input = document.getElementById("player-response-input");
const story_content_container = document.getElementById("story-content");
const loading_spinner = document.getElementById("loading-spinner");
const dm_message_container = document.getElementById("dm-message");
const img_container = document.getElementById("img-container");
const load_text = document.getElementById("load-text");
const mic_button = document.getElementById("record-speech");
const stop_button = document.getElementById("stop-speech");
const player_image = document.getElementById("player-img");

document.addEventListener("DOMContentLoaded", function () {
  sendResponse("Where am I?");
  fetchPlayerImage();
});

async function synthesizeAndPlaySpeech(text) {
  const formData = new FormData();
  formData.append("text", text);
  await fetch("/synthesize_speech", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      text: text,
    }),
  })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      fetchAudio();
    })
    .catch(error => {
      console.error("Error:", error);
    });
}

player_response_form.addEventListener("submit", function (event) {
  event.preventDefault();
  let player_response = player_response_input.value;

  sendResponse(player_response);
});

function sendResponse(player_response) {
  loading_spinner.style.display = "block";
  story_content_container.replaceChildren(loading_spinner);
  player_response_container.replaceChildren(load_text);
  player_response_input.value = "";

  fetch("/play", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      player_response: player_response,
    }),
  })
    .then(response => response.json())
    .then(data => {
      dm_message_container.innerText = data.dungeon_master_message;
      story_content_container.replaceChildren(dm_message_container, img_container);
      player_response_container.replaceChildren(mic_button, player_response_form);
      synthesizeAndPlaySpeech(data.dungeon_master_message);

      fetchImage(data);
    })
    .catch(error => {
      console.error("Error:", error);
    });
}

async function fetchImage(data) {
  fetch("/process-image", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      dungeon_message: data.dungeon_master_message,
    }),
  })
    .then(response => response.json())
    .then(data => {
      img_container.src = data.state_image;
    })
    .catch(error => {
      console.error("Error:", error);
    });
}

async function fetchPlayerImage() {
  fetch("/player_image", {
    method: "POST",
  })
    .then(response => response.json())
    .then(data => {
      // console.log("Player image: " + data.player_image);
      player_image.src = data.player_image;
    })
    .catch(error => {
      console.error("Error", error);
    });
}

async function fetchAudio() {
  fetch("/get-audio")
    .then(response => response.blob())
    .then(blob => {
      // create a blob URL from the blob
      const blobUrl = URL.createObjectURL(blob);

      // create an Audio element and set its source to the blob URL
      const audio = new Audio(blobUrl);

      // play the audio
      audio.play();
    });
}

const constraints = { audio: true };
let mediaRecorder;
let chunks = [];

navigator.mediaDevices
  .getUserMedia(constraints)
  .then(function (stream) {
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = function (e) {
      chunks.push(e.data);
    };

    mediaRecorder.onstop = function () {
      const blob = new Blob(chunks, { type: "audio/wav" });
      const formData = new FormData();
      formData.append("audio", blob, "audio.wav");

      fetch("/process-audio", {
        method: "POST",
        body: formData,
      })
        .then(response => response.json())
        .then(data => {
          console.log(data);
          let player_message = data.player_message;
          sendResponse(player_message)
        })
        .catch(error => console.error(error));

      chunks = [];
    };
  })
  .catch(function (err) {
    console.error("Error accessing microphone", err);
  });

console.log(mic_button);

mic_button.addEventListener("click", function () {
  console.log(mediaRecorder.state);

  if (mediaRecorder.state == "inactive") {
    // start recording
    mediaRecorder.start();
    mic_button.innerText = "Stop"
    stop_button.display = "block";
  } else if (mediaRecorder.state == "recording") {
    console.log("stop recording");
    mediaRecorder.stop();
    mic_button.innerText = "Rec"
    mic_button.display = "block";
  }

  // if (mediaRecorder.state == "inactive" || mediaRecorder.state == "paused") {
  //   console.log("start recording");
  //   mediaRecorder.start();
  //   this.display = "none";
  //   stop_button.display = "block";
  // }
});

stop_button.addEventListener("click", function () {
  if (mediaRecorder.state == "recording") {
    console.log("stop recording");
    mediaRecorder.stop();
    this.id = "record-speech";
    this.display = "none";
    mic_button.display = "block";
  }
});
