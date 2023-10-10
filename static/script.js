document.addEventListener('DOMContentLoaded', function () {
    // Tu código JavaScript aquí
    // Obtén referencias a los elementos HTML
    const modoBoton = document.getElementById('modoBoton');
    const modoImagen = document.getElementById('modoImagen');
    const logo = document.getElementById('logo');
    const loginlogo = document.getElementById('loginlogo');
    const configImg = document.getElementById('config-img');
    const htmlElement = document.documentElement;

    // Variable para rastrear el estado actual (modo oscuro o claro)
    let modoActual = 'light';

    // Función para alternar entre las imágenes
    function alternarImagen() {
        if (modoActual === 'dark') {
            // Cambia a la imagen de light mode
            modoImagen.src = '/static/img/light-mode.png';
            modoImagen.alt = 'light-mode';
            logo.src = '/static/img/logo-darkmode.png';
            logo.alt = 'contacts-logo-light';
            if (!document.getElementById('loginlogo')) {
                // Si no existe el elemento loginlogo, no hacemos nada
            }
            else{
                loginlogo.src = '/static/img/logo-darkmode.png'
                loginlogo.alt = 'contacts-logo-light'
            }

            if (!document.getElementById('configImg')) {
                // Si no existe el elemento loginlogo, no hacemos nada
            }
            else{
                configImg.src = '/static/img/config-darkmode.png'
                configImg.alt = 'config-dark'
            }          
            htmlElement.classList.remove('light');
            htmlElement.classList.add('dark');
            modoActual = 'light';
        } else {
            // Cambia a la imagen de dark mode
            modoImagen.src = '/static/img/dark-mode.png';
            modoImagen.alt = 'dark-mode';
            logo.src = '/static/img/logo.png';
            logo.alt = 'contacts-logo-dark';
            if (!document.getElementById('loginlogo')) {
                // Si no existe el elemento loginlogo, no hacemos nada
            }
            else{
                loginlogo.src = '/static/img/logo.png'
                loginlogo.alt = 'contacts-logo-dark'
            }

            if (!document.getElementById('configImg')) {
                // Si no existe el elemento loginlogo, no hacemos nada
            }
            else{
                configImg.src = '/static/img/config-lightmode.png'
                configImg.alt = 'config-light'
            }
                       
            htmlElement.classList.remove('dark');
            htmlElement.classList.add('light');
            modoActual = 'dark';
        }
    }

    // Agrega un evento de clic al botón para activar la función de alternarImagen
    modoBoton.addEventListener('click', alternarImagen);

    // Config Menu y Profile Menu
    const configButton = document.getElementById("config-menu-button")
    const profileButton = document.getElementById("profile-menu-button")
    const configMenu = document.getElementById("config-menu")
    const profileMenu = document.getElementById("profile-menu")

    function showMenu(menu) {  
        // Verificar si la clase "hidden" está presente
        if (menu.classList.contains("hidden")) {
          // Si está oculto, mostrarlo
          menu.classList.remove("hidden");
          menu.classList.add("block");
        } else {
          // Si está visible, ocultarlo
          menu.classList.remove("block");
          menu.classList.add("hidden");
        }
      }

      // Agregar eventos de clic a los botones correspondientes
    configButton.addEventListener("click", function (e) {
        e.stopPropagation(); // Evita que el clic en el botón se propague al documento
        showMenu(configMenu); // Alternar la clase en configMenu
    });
    
    profileButton.addEventListener("click", function (e) {
        e.stopPropagation(); // Evita que el clic en el botón se propague al documento
        showMenu(profileMenu); // Alternar la clase en profileMenu
    });

      // Función para ocultar los menús si están visibles
    function ocultarMenus() {
        if (!configMenu.classList.contains("hidden")) {
        showMenu(configMenu);
        }
        if (!profileMenu.classList.contains("hidden")) {
        showMenu(profileMenu);
        }
    }

    // Agregar un controlador de clic al documento para ocultar los menús cuando se hace clic fuera de ellos
    document.addEventListener("click", function () {
        ocultarMenus();
    });


});

