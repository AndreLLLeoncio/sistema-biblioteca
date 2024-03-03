function visualizarLivro(livro_id) {
    $.ajax({
        url: '/adm/livros/' + livro_id,
        type: 'GET',
        success: function(data) {
            $('#modal-nome').text(data.nome);
            $('#modal-isbn').text(data.isbn);
            $('#visualizar-livro-modal').modal('show');
        }
    });
}