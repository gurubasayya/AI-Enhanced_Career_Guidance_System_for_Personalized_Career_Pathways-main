// Navigate to guidance page when button is clicked
function showGuidance(button) {
    // Get data from button attributes
    const careerId = button.getAttribute('data-career-id');
    const matchPercentage = button.getAttribute('data-match');
    const growth = button.getAttribute('data-growth');
    
    // Update button state
    const originalText = button.innerHTML;
    button.disabled = true;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
    
    // Get the career title from the ID
    const careerTitle = careerId.replace(/-/g, ' ');
    
    // Show loading state briefly for better UX
    setTimeout(() => {
        // Navigate to the career guidance page
        window.location.href = `/career-guidance/${encodeURIComponent(careerTitle)}?match=${matchPercentage}&growth=${growth}`;
    }, 300);
}

// Add event listeners when the page loads
document.addEventListener('DOMContentLoaded', function() {
    // Add click event to all guidance buttons
    document.querySelectorAll('.guidance-btn').forEach(button => {
        button.addEventListener('click', function() {
            showGuidance(this);
        });
    });
});
