// payment.js - Enhanced card input handling
document.addEventListener('DOMContentLoaded', function() {
    // Format card number with spaces
    const cardNumberInput = document.getElementById('cardNumber');
    
    if (cardNumberInput) {
        cardNumberInput.addEventListener('input', formatCardNumber);
        cardNumberInput.addEventListener('keydown', handleCardNumberKeydown);
        cardNumberInput.addEventListener('paste', handleCardNumberPaste);
    }
    
    function formatCardNumber(e) {
        let value = e.target.value.replace(/\D/g, '');
        
        // Add space after every 4 digits
        let formatted = '';
        for (let i = 0; i < value.length; i++) {
            if (i > 0 && i % 4 === 0) {
                formatted += ' ';
            }
            formatted += value[i];
        }
        
        // Limit to 19 characters (16 digits + 3 spaces)
        e.target.value = formatted.substring(0, 19);
        
        // Update card type indicator
        updateCardType(value);
    }
    
    function handleCardNumberKeydown(e) {
        // Allow: backspace, delete, tab, escape, enter
        if ([46, 8, 9, 27, 13].includes(e.keyCode) ||
            // Allow: Ctrl+A, Ctrl+C, Ctrl+V, Ctrl+X
            (e.keyCode === 65 && e.ctrlKey === true) ||
            (e.keyCode === 67 && e.ctrlKey === true) ||
            (e.keyCode === 86 && e.ctrlKey === true) ||
            (e.keyCode === 88 && e.ctrlKey === true) ||
            // Allow: home, end, left, right
            (e.keyCode >= 35 && e.keyCode <= 39)) {
            return;
        }
        
        // Ensure that it is a number and stop the keypress
        if ((e.keyCode < 48 || e.keyCode > 57) && (e.keyCode < 96 || e.keyCode > 105)) {
            e.preventDefault();
        }
    }
    
    function handleCardNumberPaste(e) {
        // Get pasted data via clipboard API
        const pastedData = e.clipboardData.getData('Text');
        
        // Check if pasted data is numeric
        if (!/^\d+$/.test(pastedData)) {
            e.preventDefault();
            return;
        }
        
        // Format after paste
        setTimeout(() => {
            formatCardNumber({ target: cardNumberInput });
        }, 10);
    }
    
    function updateCardType(cardNumber) {
        const icons = {
            visa: document.querySelector('.fa-cc-visa'),
            mastercard: document.querySelector('.fa-cc-mastercard'),
            amex: document.querySelector('.fa-cc-amex')
        };
        
        // Reset all icons
        Object.values(icons).forEach(icon => {
            if (icon) {
                icon.style.color = 'var(--notion-text-light)';
                icon.style.opacity = '0.5';
            }
        });
        
        // Detect card type
        if (cardNumber.startsWith('4')) {
            if (icons.visa) {
                icons.visa.style.color = 'var(--notion-primary)';
                icons.visa.style.opacity = '1';
            }
        } else if (cardNumber.startsWith('5')) {
            if (icons.mastercard) {
                icons.mastercard.style.color = 'var(--notion-primary)';
                icons.mastercard.style.opacity = '1';
            }
        } else if (cardNumber.startsWith('34') || cardNumber.startsWith('37')) {
            if (icons.amex) {
                icons.amex.style.color = 'var(--notion-primary)';
                icons.amex.style.opacity = '1';
            }
        }
    }
    
    // Format expiry date
    const expiryInput = document.getElementById('expiryDate');
    if (expiryInput) {
        expiryInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            
            if (value.length >= 2) {
                let month = value.substring(0, 2);
                let year = value.substring(2, 4);
                
                // Validate month
                month = Math.min(12, Math.max(1, parseInt(month) || 1)).toString().padStart(2, '0');
                
                e.target.value = month + (year ? '/' + year : '');
            }
        });
    }
    
    // Auto-advance from month to year
    if (expiryInput) {
        expiryInput.addEventListener('keyup', function(e) {
            if (e.target.value.length === 2 && /^\d{2}$/.test(e.target.value)) {
                e.target.value += '/';
            }
        });
    }
    
    // Auto-fill demo card (optional)
    const autoFillBtn = document.createElement('button');
    autoFillBtn.type = 'button';
    autoFillBtn.innerHTML = '<i class="fas fa-magic"></i> Fill Demo Card';
    autoFillBtn.style.cssText = `
        background: var(--notion-primary-light);
        color: var(--notion-primary);
        border: 1px solid var(--notion-primary);
        padding: 0.5rem 1rem;
        border-radius: 6px;
        cursor: pointer;
        font-size: 0.9rem;
        margin-top: 0.5rem;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    `;
    
    autoFillBtn.onclick = function() {
        cardNumberInput.value = '4111 1111 1111 1111';
        expiryInput.value = '12/25';
        document.getElementById('cvvNumber').value = '123';
        document.getElementById('cardName').value = 'John Doe';
        updateCardType('4111111111111111');
        this.innerHTML = '<i class="fas fa-check"></i> Demo Card Filled';
        this.style.background = 'var(--notion-green-light)';
        this.style.color = 'var(--notion-green)';
        this.style.borderColor = 'var(--notion-green)';
    };
    
    // Add button after demo info
    const demoInfo = document.querySelector('.demo-info');
    if (demoInfo) {
        demoInfo.appendChild(autoFillBtn);
    }
});