
  $(document).ready(function () {
      $('#sidebarCollapse').on('click', function () {
          $('#sidebar').toggleClass('active');
      });
  });
  



function seleccionarOpcion(opcion) {
    var opciones = document.querySelectorAll('.opcion');
    
    for (var i = 0; i < opciones.length; i++) {
      opciones[i].classList.remove('active');
    }
    
    opcion.classList.add('active');
  }
   