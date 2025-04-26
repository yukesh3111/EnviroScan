// Function to show the loading screen
function showLoadingScreen() {
  document.getElementById("loadingScreen").style.display = "block";
}

// Function to hide the loading screen
function hideLoadingScreen() {
  document.getElementById("loadingScreen").style.display = "none";
}

// Function to reload content and show loading screen
function reloadContent() {
  showLoadingScreen();
  // Simulate reloading content (replace with your actual content loading logic)
  setTimeout(function () {
    // Hide loading screen after content is loaded
    hideLoadingScreen();
  }, 200000); // Simulating 2 seconds loading time
}
