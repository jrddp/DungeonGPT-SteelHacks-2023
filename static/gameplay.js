const player_response_form = document.getElementById("player-response-form");
const story_content_container = document.getElementById("story-content");
const loading_spinner = document.getElementById("loading-spinner");
const dm_message_container = document.getElementById("dm-message");
const img_container = document.getElementById("img-container");

player_response_form.addEventListener("submit", function (event) {
  event.preventDefault();
  let player_response = document.getElementById("player_response").value;

  console.log("Posting with response " + player_response)

  loading_spinner.style.display = "block";
  story_content_container.replaceChildren(loading_spinner);

  fetch("{{ url_for('gameplay') }}", {
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
    })
    .catch(error => {
      console.error("Error:", error);
    });
});


// Create a new MediaRecorder object
const mediaRecorder = new MediaRecorder(stream);

// Set event handlers
mediaRecorder.ondataavailable = function(event) {
  // Send recorded data to Flask backend
  const formData = new FormData();
  formData.append('audio', event.data, 'recorded-audio.webm');
  fetch('/process-audio', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    dm_message_container.innerText = data.dungeon_master_message;
    story_content_container.replaceChildren(dm_message_container, img_container);
  })
  .catch(error => {
    console.error("Error:", error);
  });
}

// Start recording
mediaRecorder.start();

// Stop recording after 5 seconds
setTimeout(function() {
  mediaRecorder.stop();
}, 5000);

