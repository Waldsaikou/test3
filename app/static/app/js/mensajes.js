function test(){
    Swal.fire({
        icon: 'error',
        title: 'Oops...',
        text: 'Something went wrong!',
        footer: '<a href="">Why do I have this issue?</a>'
      })

}
function mensajes() {
  alert('123');
}

function eliminarProducto(id) {
  Swal.fire({
    title: 'Confirmar',
    text: 'Desea eliminar el producto?',
    icon: 'question',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'Confirmar'
  }).then((result) => {
    if (result.isConfirmed) {
      Swal.fire('Eliminado!','Producto Eliminado Correctamente','success').then(function() {
          window.location.href = "/delete/"+id+"/";
      })
    }
  })
} 