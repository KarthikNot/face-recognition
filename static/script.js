function saveFace() {
  let name = prompt("Enter a name for the face:");
  if (name) {
    fetch("/save_face", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: name }),
    })
      .then((response) => response.json())
      .then((data) => {
        alert(data.message);
        loadSavedFaces(); // Refresh saved faces
      })
      .catch((error) => console.error("Error:", error));
  }
}

function handleAction(url) {
  fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  })
    .then((response) => response.json())
    .then((data) => alert(data.message))
    .catch((error) => console.error("Error:", error));
}

function loadSavedFaces() {
  fetch("/get_saved_faces")
    .then((response) => response.json())
    .then((data) => {
      let container = document.getElementById("savedFacesContainer");
      container.innerHTML = ""; // Clear previous data
      data.forEach((face) => {
        let faceDiv = document.createElement("div");
        faceDiv.classList.add("saved-face");

        let img = document.createElement("img");
        img.src = "data:image/jpeg;base64," + face.face_img;
        img.alt = face.name;

        let name = document.createElement("p");
        name.textContent = face.name;

        faceDiv.appendChild(img);
        faceDiv.appendChild(name);
        container.appendChild(faceDiv);
      });
    })
    .catch((error) => console.error("Error fetching saved faces:", error));
}

// Load saved faces when the page loads
window.onload = loadSavedFaces;
