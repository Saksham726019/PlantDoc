document.addEventListener("DOMContentLoaded", function () {
    const selectImageBtn = document.getElementById("selectImage");
    const fileInput = document.getElementById("fileInput");
  
    if (selectImageBtn) {
      selectImageBtn.addEventListener("click", function () {
        if (fileInput) fileInput.click();
      });
    }
  
    if (fileInput) {
      fileInput.addEventListener("change", function () {
        if (this.files.length > 0) {
          const file = this.files[0];
          predictDisease(file);
        } else {
          alert("Please select an image file first.");
        }
      });
    }
  
    const videos = document.querySelectorAll('.video-section video');
    
    if (videos.length > 0) {
      videos.forEach(video => {
        video.muted = true; // Programmatically mute each video
        video.setAttribute('muted', ''); // Ensures the video is muted to comply with autoplay policies
        video.setAttribute('playsinline', ''); // Plays the video inline on mobile devices without entering fullscreen
        video.removeAttribute('controls'); // Attempts to play the video, catching any errors due to autoplay restrictions
        video.play().catch(error => console.error('Error attempting to play video:', error));
  
        const videoObserver = new IntersectionObserver((entries) => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              entry.target.play().then(() => {
                entry.target.loop = true; // Ensures the video keeps looping
              }).catch(error => console.error('Error playing the video:', error));
            } else {
              entry.target.pause(); // Pauses the video when it is not in view
            }
          });
        }, {
          threshold: 0.3 // Trigger when at least 50% of the video is visible
        });
  
        videoObserver.observe(video); // Observes each video for visibility changes
      });
    }
  });
  