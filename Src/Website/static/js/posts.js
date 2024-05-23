function deletePost(postId) {
    fetch(`/api/delete-post/${postId}`, {method : "POST"})
    .then((res) => res.json())
    .then((data) => {
      if (data.type === "success") {
        const card = document.getElementById(`post-${postId}`);
        card.remove();
      }
    })
    .catch((e));
}