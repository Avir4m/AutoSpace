function toggleComments(postId) {
    const comments = document.getElementById(`comments-${postId}`);

    if (comments.style.display === 'none') {
        comments.style.display = 'block';
    } else {
        comments.style.display = 'none';
    }
}