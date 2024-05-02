// Supongamos que tienes un array de comentarios
var comments = [
    { name: 'Usuario 1', comment: 'Este es el comentario del usuario 1' },
    { name: 'Usuario 2', comment: 'Este es el comentario del usuario 2' },
    // Añade más comentarios aquí
];

// Encuentra el contenedor de comentarios en la página
var commentsContainer = document.getElementById('existing-reviews');

// Itera sobre los comentarios y añade cada uno al contenedor de comentarios
comments.forEach(function(comment) {
    // Crea un nuevo elemento div para el comentario
    var commentDiv = document.createElement('div');

    // Añade el nombre y el comentario al div
    commentDiv.innerHTML = '<h3>' + comment.name + '</h3>' +
                           '<p>' + comment.comment + '</p>';

    // Añade el div del comentario al contenedor de comentarios
    commentsContainer.appendChild(commentDiv);
});