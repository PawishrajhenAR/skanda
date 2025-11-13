// Main JavaScript for Credit Management System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Form validation
    initializeFormValidation();
    
    // Number formatting
    initializeNumberFormatting();
    
    // Table enhancements
    initializeTableEnhancements();
    
    // Smooth animations
    initializeAnimations();
    
    // Collection rate animations
    animateCollectionRate();
});

// Form Validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

// Number Formatting
function initializeNumberFormatting() {
    const numberInputs = document.querySelectorAll('input[type="number"]');
    
    numberInputs.forEach(function(input) {
        input.addEventListener('blur', function() {
            if (this.value && !isNaN(this.value)) {
                this.value = parseFloat(this.value).toFixed(2);
            }
        });
    });
}

// Table Enhancements
function initializeTableEnhancements() {
    const tables = document.querySelectorAll('.table');
    
    tables.forEach(function(table) {
        // Add hover effects
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach(function(row) {
            row.addEventListener('mouseenter', function() {
                this.style.backgroundColor = 'rgba(0, 123, 255, 0.05)';
            });
            
            row.addEventListener('mouseleave', function() {
                this.style.backgroundColor = '';
            });
        });
    });
}

// Utility Functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        minimumFractionDigits: 2
    }).format(amount);
}

function formatDate(date) {
    return new Intl.DateTimeFormat('en-IN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    }).format(new Date(date));
}

function showLoading(element) {
    element.classList.add('loading');
    element.disabled = true;
}

function hideLoading(element) {
    element.classList.remove('loading');
    element.disabled = false;
}

// Confirmation Dialogs
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Delete Invoice Confirmation
function deleteInvoice(invoiceId) {
    confirmAction('Are you sure you want to delete this invoice? This action cannot be undone.', function() {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/invoices/${invoiceId}/delete`;
        
        document.body.appendChild(form);
        form.submit();
    });
}

// Export Functions
function exportToExcel() {
    const table = document.getElementById('reportTable');
    if (!table) {
        alert('No data to export');
        return;
    }
    
    let csv = '';
    const rows = table.querySelectorAll('tr');
    
    for (let i = 0; i < rows.length; i++) {
        const cells = rows[i].querySelectorAll('td, th');
        const row = [];
        
        for (let j = 0; j < cells.length; j++) {
            let cellText = cells[j].textContent.trim();
            // Escape commas and quotes
            if (cellText.includes(',') || cellText.includes('"')) {
                cellText = '"' + cellText.replace(/"/g, '""') + '"';
            }
            row.push(cellText);
        }
        
        csv += row.join(',') + '\n';
    }
    
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', 'credit_report_' + new Date().toISOString().split('T')[0] + '.csv');
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function exportToPDF() {
    // This would require a library like jsPDF
    alert('PDF export functionality requires additional setup. For now, you can use the Excel export and convert to PDF.');
}

// Search and Filter Functions
function filterTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const table = document.getElementById(tableId);
    
    if (!input || !table) return;
    
    const filter = input.value.toLowerCase();
    const rows = table.querySelectorAll('tbody tr');
    
    rows.forEach(function(row) {
        const text = row.textContent.toLowerCase();
        if (text.includes(filter)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

// Real-time Search
function initializeSearch() {
    const searchInputs = document.querySelectorAll('.search-input');
    
    searchInputs.forEach(function(input) {
        input.addEventListener('keyup', function() {
            const tableId = this.getAttribute('data-table');
            filterTable(this.id, tableId);
        });
    });
}

// Progress Bar Animation
function animateProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar');
    
    progressBars.forEach(function(bar) {
        const width = bar.style.width;
        bar.style.width = '0%';
        
        setTimeout(function() {
            bar.style.transition = 'width 1s ease-in-out';
            bar.style.width = width;
        }, 100);
    });
}

// Smooth Animations
function initializeAnimations() {
    // Animate cards on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe all cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(function(card) {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'all 0.6s ease';
        observer.observe(card);
    });

    // Animate stats numbers
    animateStatsNumbers();
}

// Animate collection rate
function animateCollectionRate() {
    const progressBars = document.querySelectorAll('.collection-progress-bar .progress-bar');
    
    progressBars.forEach(function(bar) {
        const width = bar.style.width;
        bar.style.width = '0%';
        
        setTimeout(function() {
            bar.style.transition = 'width 1.5s cubic-bezier(0.4, 0, 0.2, 1)';
            bar.style.width = width;
        }, 300);
    });
}

// Animate stats numbers
function animateStatsNumbers() {
    const statsNumbers = document.querySelectorAll('.stats-number');
    
    statsNumbers.forEach(function(element) {
        const finalValue = element.textContent;
        const isPercentage = finalValue.includes('%');
        const numericValue = parseFloat(finalValue.replace(/[^\d.]/g, ''));
        
        if (!isNaN(numericValue)) {
            animateNumber(element, 0, numericValue, 2000, isPercentage);
        }
    });
}

// Number animation function
function animateNumber(element, start, end, duration, isPercentage = false) {
    const startTime = performance.now();
    
    function updateNumber(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function
        const easeOutCubic = 1 - Math.pow(1 - progress, 3);
        const currentValue = start + (end - start) * easeOutCubic;
        
        if (isPercentage) {
            element.textContent = currentValue.toFixed(1) + '%';
        } else {
            element.textContent = Math.round(currentValue);
        }
        
        if (progress < 1) {
            requestAnimationFrame(updateNumber);
        }
    }
    
    requestAnimationFrame(updateNumber);
}

// Initialize animations when page loads
window.addEventListener('load', function() {
    animateProgressBars();
    initializeSearch();
});

// Sidebar Toggle Functionality
document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebarClose = document.getElementById('sidebarClose');
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    const userMenuBtn = document.getElementById('userMenuBtn');
    const userMenu = document.getElementById('userMenu');

    // Toggle sidebar
    function toggleSidebar() {
        if (sidebar) {
            sidebar.classList.toggle('active');
        }
        if (sidebarOverlay) {
            sidebarOverlay.classList.toggle('active');
        }
    }

    // Close sidebar
    function closeSidebar() {
        if (sidebar) {
            sidebar.classList.remove('active');
        }
        if (sidebarOverlay) {
            sidebarOverlay.classList.remove('active');
        }
    }

    // Event listeners
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', toggleSidebar);
    }

    if (sidebarClose) {
        sidebarClose.addEventListener('click', closeSidebar);
    }

    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', closeSidebar);
    }

    // User menu toggle
    if (userMenuBtn && userMenu) {
        userMenuBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            userMenu.classList.toggle('show');
        });

        // Close user menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!userMenuBtn.contains(e.target) && !userMenu.contains(e.target)) {
                userMenu.classList.remove('show');
            }
        });
    }

    // Set active menu item based on current URL
    const currentPath = window.location.pathname;
    const menuLinks = document.querySelectorAll('.menu-link');
    
    menuLinks.forEach(function(link) {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // Close sidebar on window resize if desktop
    window.addEventListener('resize', function() {
        if (window.innerWidth > 992) {
            closeSidebar();
        }
    });
});

// Responsive Table
function makeTableResponsive() {
    const tables = document.querySelectorAll('.table');
    
    tables.forEach(function(table) {
        if (!table.closest('.table-responsive')) {
            const wrapper = document.createElement('div');
            wrapper.className = 'table-responsive';
            table.parentNode.insertBefore(wrapper, table);
            wrapper.appendChild(table);
        }
    });
}

// Initialize responsive tables
document.addEventListener('DOMContentLoaded', function() {
    makeTableResponsive();
});

// Form Auto-save (for long forms)
function initializeAutoSave() {
    const forms = document.querySelectorAll('form[data-autosave]');
    
    forms.forEach(function(form) {
        const inputs = form.querySelectorAll('input, textarea, select');
        
        inputs.forEach(function(input) {
            input.addEventListener('change', function() {
                const formData = new FormData(form);
                const data = Object.fromEntries(formData);
                
                // Save to localStorage
                localStorage.setItem('autosave_' + form.id, JSON.stringify(data));
            });
        });
        
        // Restore saved data
        const savedData = localStorage.getItem('autosave_' + form.id);
        if (savedData) {
            const data = JSON.parse(savedData);
            Object.keys(data).forEach(function(key) {
                const input = form.querySelector(`[name="${key}"]`);
                if (input) {
                    input.value = data[key];
                }
            });
        }
    });
}

// Initialize auto-save
document.addEventListener('DOMContentLoaded', function() {
    initializeAutoSave();
});

// Print Functionality
function printPage() {
    window.print();
}

// Keyboard Shortcuts
document.addEventListener('keydown', function(event) {
    // Ctrl/Cmd + S to save forms
    if ((event.ctrlKey || event.metaKey) && event.key === 's') {
        event.preventDefault();
        const form = document.querySelector('form');
        if (form) {
            form.submit();
        }
    }
    
    // Ctrl/Cmd + N for new invoice
    if ((event.ctrlKey || event.metaKey) && event.key === 'n') {
        event.preventDefault();
        const newInvoiceLink = document.querySelector('a[href*="new_invoice"]');
        if (newInvoiceLink) {
            window.location.href = newInvoiceLink.href;
        }
    }
    
    // Escape to close modals
    if (event.key === 'Escape') {
        const modals = document.querySelectorAll('.modal.show');
        modals.forEach(function(modal) {
            const bsModal = bootstrap.Modal.getInstance(modal);
            if (bsModal) {
                bsModal.hide();
            }
        });
    }
});

// Error Handling
window.addEventListener('error', function(event) {
    console.error('JavaScript Error:', event.error);
    // You could send this to a logging service
});

// Performance Monitoring
function measurePerformance() {
    if ('performance' in window) {
        window.addEventListener('load', function() {
            setTimeout(function() {
                const perfData = performance.getEntriesByType('navigation')[0];
                console.log('Page Load Time:', perfData.loadEventEnd - perfData.loadEventStart, 'ms');
            }, 0);
        });
    }
}

// Initialize performance monitoring
measurePerformance();
