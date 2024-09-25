// js to update theme, updated styles of selected board in sidebar
// get local storage
// wait for dom to load theme toggle

let theme_toggle = '';

// Set an interval to check cyclically for the presence of theme toggle element
let waitForContentLoad = setInterval(function () {

    // Look for the value
    theme_toggle = document.querySelector('.theme-toggle .switch input')

    // Check if the value is present
    if (theme_toggle !== null && theme_toggle !== 'undefined') {

        let storedTheme = localStorage.getItem('theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');

        if (storedTheme) {
            document.documentElement.setAttribute('data-theme', storedTheme);
            // check input if theme
            if (storedTheme === 'dark') {
                theme_toggle.checked = 'true'
            }
        }

        // event listener on change theme toggle
        theme_toggle.addEventListener('change', () => {
            let currentTheme = document.documentElement.getAttribute('data-theme');

            let targetTheme = 'light';


            if (currentTheme === 'light') {
                targetTheme = 'dark';
            }

            document.documentElement.setAttribute('data-theme', targetTheme);
            localStorage.setItem('theme', targetTheme);
        });

        // set cs-active on selected board in sidebar
        // currently selected board
        let selected_board = document.querySelector('.board-name h2');

        // if there a board selected
        if (selected_board !== null && selected_board !== 'undefined') {
            // board list items
            let user_boards_items = document.querySelectorAll('.board-list li');
            // element containing name of boards
            let user_boards_names = document.querySelectorAll('.board-list li a span');

            user_boards_names.forEach((el, index) => {
                if (el.textContent === selected_board.textContent) {
                    user_boards_items[index].classList.add('cs-active');
                }
            });
        }

        // add focus to sidebar when active
        let sidebar_el = document.querySelector('.sidebar .new-board-btn');
        let mobile_nav_btn = document.querySelector('.nav-toggle-btn');
        let desktop_nav_btn = document.querySelector('.desktop-nav-toggle');

        mobile_nav_btn.addEventListener('click', () => {
            if (sidebar_el !== null && sidebar_el !== 'undefined') {
                sidebar_el.focus()
            }
        });

        desktop_nav_btn.addEventListener('click', () => {
            if (sidebar_el !== null && sidebar_el !== 'undefined') {
                sidebar_el.focus()
            }
        });


        // Clear the interval
        clearInterval(waitForContentLoad);
    }

}, 50);  // milliseconds.

// form submissions success - reload the page
document.addEventListener('htmx:beforeSwap', (e) => {
    if (e.detail.target.id == 'form-wrapper' && !e.detail.xhr.response) {
        location.reload()
    }
});

// htmx.on("boardChanged", (e) => {
//     location.reload()
// });