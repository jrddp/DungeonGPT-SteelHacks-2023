const player_response_container = document.getElementById("player-response")
const player_response_form = document.getElementById("player-response-form");
const story_content_container = document.getElementById("story-content");
const loading_spinner = document.getElementById("loading-spinner");
const dm_message_container = document.getElementById("dm-message");
const img_container = document.getElementById("img-container");
const load_text = document.getElementById("load-text");

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
  let player_response = document.getElementById("player_response").value;

  sendResponse(player_response);
});

function sendResponse(player_response) {
  loading_spinner.style.display = "block";
  story_content_container.replaceChildren(loading_spinner);
  player_response_container.replaceChildren(load_text);

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
      player_response_container.replaceChildren(player_response_form);
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
      console.log(data.state_image);
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
    console.log("Player image: " + data.player_image);
  })
  .catch(error => {
    console.error("Error", error);
  })
}

async function fetchAudio(){
  fetch('/get-audio')
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