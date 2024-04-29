var reviews = [
    { name: 'Usuario 1', review: 'Esta es la reseña del usuario 1', rating: 5 },
    { name: 'Usuario 2', review: 'Esta es la reseña del usuario 2', rating: 4 },
];

var reviewsContainer = document.getElementById('existing-reviews');

reviews.forEach(function(review) {
    var reviewDiv = document.createElement('div');

    reviewDiv.innerHTML = '<h3>' + review.name + '</h3>' +
                          '<p>' + review.review + '</p>' +
                          '<p>Calificación: ' + review.rating + '/5</p>';

    reviewsContainer.appendChild(reviewDiv);
});