console.log('navigation.js loaded')

document.addEventListener('DOMContentLoaded', function() {
    const menuIcon = document.querySelector('.menu-icon');
    const navigation = document.querySelector('#navigation');
    const navigationTexts = document.querySelectorAll('.navigation-text');
    const navigationHeadings = document.querySelectorAll('.navigation-heading');
    const contentContainer = document.querySelector('#content-container');

    // Function to apply styles based on navigation size
    function applyNavigationSize(size) {
        if (size === 'large') {
            navigation.style.width = '250px';
            setTimeout(() => {
                navigationHeadings.forEach(heading => heading.style.justifyContent = 'start');
            }, 50); 
            setTimeout(() => {
                navigationTexts.forEach(text => text.style.display = 'inline');
                navigationHeadings.forEach(heading => heading.style.fontSize = '1rem');
                contentContainer.style.marginLeft = '282px';
            }, 100); 
        } else { // Assume 'small'
            navigation.style.width = '76px';
            navigationTexts.forEach(text => text.style.display = 'none');
            navigationHeadings.forEach(heading => heading.style.fontSize = '0.9rem');
            contentContainer.style.marginLeft = '108px';
            // Add a delay to center the heading otherwise it looks weird
            navigationHeadings.forEach(heading => {
                setTimeout(() => {
                    heading.style.justifyContent = 'center';
                }, 600); // Delay in milliseconds
            });
        }
    }

    // Apply saved navigation size or default to 'large'
    const savedSize = localStorage.getItem('navigationSize') || 'large';
    applyNavigationSize(savedSize);

    menuIcon.addEventListener('click', function() {
        // Toggle navigation size
        const newSize = navigation.style.width === '76px' ? 'large' : 'small';
        applyNavigationSize(newSize);
        // Save the new size to localStorage
        localStorage.setItem('navigationSize', newSize);
    });

    // ----------------------------------------------------------------------------------------
    // ----------------------------------------------------------------------------------------
    // ----------------------------------------------------------------------------------------

    // Mobile navigation
    const mobileMenuIcon = document.querySelector('.mobile-menu-icon');
    
    // Function to toggle mobile navigation
    function toggleMobileNavigation() {
        navigation.style.display = navigation.style.display === 'block' ? 'none' : 'block';
        navigation.style.width = '100%';
        navigationTexts.forEach(text => text.style.display = 'inline');
    }

    // Add click event listener to the mobile menu icon
    mobileMenuIcon.addEventListener('click', toggleMobileNavigation);
});