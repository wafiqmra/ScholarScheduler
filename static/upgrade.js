// upgrade.js - Interactive elements for Upgrade Page

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scroll for anchor links (if any)
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Highlight current plan in comparison table
    const currentPlan = 'Free'; // You can change this dynamically based on user
    highlightCurrentPlan(currentPlan);

    // Add animation to pricing cards on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
            }
        });
    }, observerOptions);

    // Observe pricing cards and FAQ items
    document.querySelectorAll('.pricing-card, .faq-item').forEach(element => {
        observer.observe(element);
    });

    // Upgrade button animation
    const upgradeButtons = document.querySelectorAll('.upgrade-button, .cta-button');
    upgradeButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Add click animation
            this.style.transform = 'scale(0.95)';
            
            // If it's a submit button, show loading state
            if (this.type === 'submit') {
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
                this.disabled = true;
                
                // Reset after 3 seconds (in case form submission fails)
                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.disabled = false;
                    this.style.transform = '';
                }, 3000);
            }
            
            // Reset animation
            setTimeout(() => {
                this.style.transform = '';
            }, 200);
        });
    });

    // FAQ accordion functionality (optional - uncomment if needed)
    /*
    const faqQuestions = document.querySelectorAll('.faq-question');
    faqQuestions.forEach(question => {
        question.addEventListener('click', function() {
            const answer = this.nextElementSibling;
            const icon = this.querySelector('i');
            
            // Toggle answer visibility
            answer.style.display = answer.style.display === 'block' ? 'none' : 'block';
            
            // Rotate icon
            icon.style.transform = answer.style.display === 'block' ? 'rotate(180deg)' : 'rotate(0)';
            
            // Add animation class
            answer.classList.toggle('show');
        });
    });
    */

    // Price toggle animation (if you add monthly/yearly toggle)
    const priceToggle = document.getElementById('price-toggle');
    if (priceToggle) {
        priceToggle.addEventListener('change', function() {
            const monthlyPrices = document.querySelectorAll('.monthly-price');
            const yearlyPrices = document.querySelectorAll('.yearly-price');
            const periodTexts = document.querySelectorAll('.pricing-period');
            
            if (this.checked) {
                // Show yearly prices
                monthlyPrices.forEach(price => price.style.display = 'none');
                yearlyPrices.forEach(price => price.style.display = 'block');
                periodTexts.forEach(text => text.textContent = '/year');
            } else {
                // Show monthly prices
                monthlyPrices.forEach(price => price.style.display = 'block');
                yearlyPrices.forEach(price => price.style.display = 'none');
                periodTexts.forEach(text => text.textContent = '/month');
            }
        });
    }

    // Add floating animation to recommended badge
    const recommendedBadge = document.querySelector('.recommended-badge');
    if (recommendedBadge) {
        setInterval(() => {
            recommendedBadge.style.transform = 'translateY(-5px)';
            setTimeout(() => {
                recommendedBadge.style.transform = 'translateY(0)';
            }, 1000);
        }, 3000);
    }

    // Form submission handling
    const upgradeForm = document.querySelector('.upgrade-form');
    if (upgradeForm) {
        upgradeForm.addEventListener('submit', function(e) {
            // Optional: Add form validation here
            console.log('Upgrade form submitted');
            
            // You can add AJAX form submission here if needed
            /*
            e.preventDefault();
            
            const formData = new FormData(this);
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
            submitBtn.disabled = true;
            
            fetch('/process_upgrade', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    submitBtn.innerHTML = '<i class="fas fa-check"></i> Success!';
                    // Redirect to payment or success page
                    setTimeout(() => {
                        window.location.href = data.redirect_url;
                    }, 1500);
                } else {
                    throw new Error(data.message || 'Payment failed');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
                alert('Payment failed: ' + error.message);
            });
            */
        });
    }
});

// Function to highlight current plan in comparison table
function highlightCurrentPlan(planName) {
    const table = document.querySelector('.comparison-table');
    if (!table) return;
    
    const rows = table.querySelectorAll('tbody tr');
    const planIndex = planName === 'Free' ? 1 : 2; // 1 for Free, 2 for Premium
    
    rows.forEach(row => {
        const cell = row.children[planIndex];
        if (cell) {
            cell.style.backgroundColor = 'var(--notion-green-light)';
            cell.style.fontWeight = '600';
        }
    });
}

// Add CSS for animations
function addUpgradeAnimations() {
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .pricing-card.animated {
            animation: fadeInUp 0.6s ease forwards;
        }
        
        .faq-item.animated {
            animation: fadeInUp 0.4s ease forwards;
        }
        
        .recommended-badge {
            transition: transform 1s ease-in-out;
        }
        
        /* FAQ accordion styles (if enabled) */
        .faq-answer {
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease-out;
        }
        
        .faq-answer.show {
            max-height: 500px;
            transition: max-height 0.5s ease-in;
        }
        
        .faq-question i {
            transition: transform 0.3s ease;
        }
        
        /* Price toggle animation */
        .price-toggle-container {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1rem;
            margin-bottom: 2rem;
        }
        
        .toggle-switch {
            position: relative;
            display: inline-block;
            width: 60px;
            height: 30px;
        }
        
        .toggle-switch input {
            opacity: 0;
            width: 0;
            height: 0;
        }
        
        .toggle-slider {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #ccc;
            transition: .4s;
            border-radius: 34px;
        }
        
        .toggle-slider:before {
            position: absolute;
            content: "";
            height: 22px;
            width: 22px;
            left: 4px;
            bottom: 4px;
            background-color: white;
            transition: .4s;
            border-radius: 50%;
        }
        
        input:checked + .toggle-slider {
            background-color: #3b82f6;
        }
        
        input:checked + .toggle-slider:before {
            transform: translateX(30px);
        }
    `;
    document.head.appendChild(style);
}

// Initialize animations
addUpgradeAnimations();