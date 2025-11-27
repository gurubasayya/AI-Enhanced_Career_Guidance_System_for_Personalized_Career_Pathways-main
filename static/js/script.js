// Upload area functionality
document.addEventListener("DOMContentLoaded", () => {
  const uploadArea = document.getElementById("uploadArea")
  const fileInput = document.getElementById("resume")

  if (uploadArea && fileInput) {
    uploadArea.addEventListener("click", () => fileInput.click())

    uploadArea.addEventListener("dragover", (e) => {
      e.preventDefault()
      uploadArea.style.borderColor = "#667eea"
      uploadArea.style.background = "rgba(102, 126, 234, 0.1)"
    })

    uploadArea.addEventListener("dragleave", (e) => {
      e.preventDefault()
      uploadArea.style.borderColor = "#d1d5db"
      uploadArea.style.background = "transparent"
    })

    uploadArea.addEventListener("drop", (e) => {
      e.preventDefault()
      uploadArea.style.borderColor = "#d1d5db"
      uploadArea.style.background = "transparent"

      const files = e.dataTransfer.files
      if (files.length > 0) {
        fileInput.files = files
        updateUploadDisplay(files[0])
      }
    })

    fileInput.addEventListener("change", (e) => {
      if (e.target.files.length > 0) {
        updateUploadDisplay(e.target.files[0])
      }
    })

    function updateUploadDisplay(file) {
      const uploadIcon = uploadArea.querySelector(".upload-icon")
      const uploadText = uploadArea.querySelector("h3")
      const uploadSubtext = uploadArea.querySelector("p")

      uploadIcon.innerHTML = '<i class="fas fa-file-alt"></i>'
      uploadText.textContent = file.name
      uploadSubtext.textContent = `File size: ${(file.size / 1024 / 1024).toFixed(2)} MB`
    }
  }

  // Test navigation
  const testForm = document.getElementById("testForm")
  if (testForm) {
    let currentQuestion = 1
    const totalQuestions = 5

    const nextBtn = document.getElementById("nextBtn")
    const prevBtn = document.getElementById("prevBtn")
    const submitBtn = document.getElementById("submitBtn")
    const progressBar = document.querySelector(".progress-fill")
    const progressText = document.querySelector(".progress-text")

    function updateProgress() {
      const progress = (currentQuestion / totalQuestions) * 100
      progressBar.style.width = `${progress}%`
      progressText.textContent = `Question ${currentQuestion} of ${totalQuestions}`
    }

    function showQuestion(questionNum) {
      document.querySelectorAll(".question-card").forEach((card) => {
        card.classList.remove("active")
      })
      document.querySelector(`[data-question="${questionNum}"]`).classList.add("active")

      // Update navigation buttons
      prevBtn.style.display = questionNum > 1 ? "inline-flex" : "none"
      nextBtn.style.display = questionNum < totalQuestions ? "inline-flex" : "none"
      submitBtn.style.display = questionNum === totalQuestions ? "inline-flex" : "none"

      updateProgress()
    }

    nextBtn.addEventListener("click", () => {
      if (currentQuestion < totalQuestions) {
        currentQuestion++
        showQuestion(currentQuestion)
      }
    })

    prevBtn.addEventListener("click", () => {
      if (currentQuestion > 1) {
        currentQuestion--
        showQuestion(currentQuestion)
      }
    })

    // Initialize
    showQuestion(1)
  }

  // Smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault()
      const target = document.querySelector(this.getAttribute("href"))
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        })
      }
    })
  })

  // Form validation
  const forms = document.querySelectorAll("form")
  forms.forEach((form) => {
    form.addEventListener("submit", (e) => {
      const requiredFields = form.querySelectorAll("[required]")
      let isValid = true

      requiredFields.forEach((field) => {
        if (!field.value.trim()) {
          isValid = false
          field.style.borderColor = "#ef4444"
        } else {
          field.style.borderColor = "#e5e7eb"
        }
      })

      if (!isValid) {
        e.preventDefault()
        alert("Please fill in all required fields.")
      }
    })
  })
})
