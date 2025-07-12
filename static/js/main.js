document.addEventListener('DOMContentLoaded', function() {
  // Enable Bootstrap tooltips
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
  })

  // Form validation
  const forms = document.querySelectorAll('.needs-validation')
  
  Array.from(forms).forEach(form => {
    form.addEventListener('submit', event => {
      if (!form.checkValidity()) {
        event.preventDefault()
        event.stopPropagation()
      }

      form.classList.add('was-validated')
    }, false)
  })

  // Add focus styles to form inputs
  const inputs = document.querySelectorAll('.form-control')
  inputs.forEach(input => {
    input.addEventListener('focus', function() {
      this.parentElement.classList.add('focused')
    })
    
    input.addEventListener('blur', function() {
      this.parentElement.classList.remove('focused')
    })
  })

  // Password toggle functionality
  const passwordToggles = document.querySelectorAll('.password-toggle')
  passwordToggles.forEach(toggle => {
    toggle.addEventListener('click', function() {
      const input = this.previousElementSibling
      const icon = this.querySelector('i')
      
      if (input.type === 'password') {
        input.type = 'text'
        icon.classList.remove('bi-eye')
        icon.classList.add('bi-eye-slash')
      } else {
        input.type = 'password'
        icon.classList.remove('bi-eye-slash')
        icon.classList.add('bi-eye')
      }
    })
  })
})