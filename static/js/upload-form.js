document.addEventListener('DOMContentLoaded', function() {
  const mobileMenuButton = document.getElementById("mobile-menu-button");
  const mobileMenu = document.getElementById("mobile-menu");
  const fileInput = document.getElementById("fileInput");
  const imagePreview = document.getElementById("imagePreview");
  const imagePreviewContainer = document.getElementById("imagePreviewContainer");
  const uploadArea = document.getElementById("uploadArea");
  const removeImageBtn = document.getElementById("removeImage");
  const analyzeButton = document.getElementById("analyzeButton");
  const fileTypeError = document.getElementById("fileTypeError");

  const ALLOWED_TYPES = ["image/jpeg", "image/png"];
  const ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png"];

  function isValidFileType(file) {
    const ext = file.name.slice(file.name.lastIndexOf('.')).toLowerCase();
    return ALLOWED_TYPES.includes(file.type) && ALLOWED_EXTENSIONS.includes(ext);
  }

  function showFileTypeError() {
    if (fileTypeError) fileTypeError.classList.remove("hidden");
  }

  function hideFileTypeError() {
    if (fileTypeError) fileTypeError.classList.add("hidden");
  }

  console.log('Upload form script loaded');
  console.log('File input:', fileInput);
  console.log('Upload area:', uploadArea);

  // Mobile menu toggle
  if (mobileMenuButton && mobileMenu) {
    mobileMenuButton.addEventListener("click", () => {
      mobileMenu.classList.toggle("hidden");
    });
  }

  // File input change handler
  if (fileInput) {
    fileInput.addEventListener("change", (e) => {
      console.log('File input changed');
      const file = e.target.files[0];
      if (file) {
        if (!isValidFileType(file)) {
          showFileTypeError();
          fileInput.value = "";
          return;
        }
        hideFileTypeError();
        console.log('File selected:', file.name);
        const reader = new FileReader();
        reader.onload = (event) => {
          imagePreview.src = event.target.result;
          imagePreviewContainer.classList.remove("hidden");
          uploadArea.classList.add("hidden");
          analyzeButton.disabled = false;
          analyzeButton.classList.remove(
            "bg-gray-700",
            "text-gray-400",
            "cursor-not-allowed",
          );
          analyzeButton.classList.add(
            "bg-green-500",
            "text-black",
            "hover:bg-green-400",
            "cursor-pointer",
          );
          document.getElementById("fileStatus").textContent = file.name;
        };
        reader.readAsDataURL(file);
      }
    });
  }

  // Remove image handler
  if (removeImageBtn) {
    removeImageBtn.addEventListener("click", () => {
      fileInput.value = "";
      imagePreview.src = "";
      hideFileTypeError();
      imagePreviewContainer.classList.add("hidden");
      uploadArea.classList.remove("hidden");
      analyzeButton.disabled = true;
      analyzeButton.classList.add(
        "bg-gray-700",
        "text-gray-400",
        "cursor-not-allowed",
      );
      analyzeButton.classList.remove(
        "bg-green-500",
        "text-black",
        "hover:bg-green-400",
        "cursor-pointer",
      );
      document.getElementById("fileStatus").textContent = "No Image Selected";
    });
  }

  // Click to open file picker
  if (uploadArea) {
    uploadArea.addEventListener("click", () => {
      console.log('Upload area clicked');
      fileInput.click();
    });
  }

  // Drag and drop functionality
  if (uploadArea) {
    uploadArea.addEventListener("dragover", (e) => {
      e.preventDefault();
      uploadArea.style.borderColor = "rgba(34, 197, 94, 0.8)";
    });

    uploadArea.addEventListener("dragleave", () => {
      uploadArea.style.borderColor = "";
    });

    uploadArea.addEventListener("drop", (e) => {
      e.preventDefault();
      uploadArea.style.borderColor = "";

      const file = e.dataTransfer.files[0];
      if (file) {
        if (!isValidFileType(file)) {
          showFileTypeError();
          return;
        }
        hideFileTypeError();
        fileInput.files = e.dataTransfer.files;
        const event = new Event("change");
        fileInput.dispatchEvent(event);
      }
    });
  }
});
