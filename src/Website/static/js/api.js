function like(postId) {
    const likeCount = document.getElementById(`likes-count-${postId}`);
    const likeButton = document.getElementById(`like-button-${postId}`);

    fetch(`/api/like-post/${postId}/`, {method: 'POST'})
    .then((res) => res.json())
    .then((data) => {
        likeCount.innerHTML = data['likes'];
        if (data['liked'] === true) {
          likeButton.src = "/static/images/icons/heart_b.png";
        } else {
          likeButton.src = "/static/images/icons/heart.png";
        }
    })
    .catch((e) => alert('Could not like post.'));

}

function save(postId) {
    const saveButton = document.getElementById(`save-button-${postId}`);

    fetch(`/api/save-post/${postId}/`, {method: 'POST'})
    .then((res) => res.json())
    .then((data) => {
        if (data['saved'] === true) {
          saveButton.src = "/static/images/icons/bookmark_b.png";
        } else {
          saveButton.src = "/static/images/icons/bookmark.png";
        }
    })
    .catch((e) => alert('Could not like post.'));

}

function joinForum(forumId) {
    const joinButton = document.getElementById(`join-button`);
    const memberCount = document.getElementById(`member-count`);
    
    fetch(`/api/join-forum/${forumId}/`, {method: 'POST'})
    .then((res) => res.json())
    .then((data) => {
      if (data['joined'] === true) {
        joinButton.innerHTML = 'Joined';
        memberCount.innerHTML = data['members'];
      } else {
        joinButton.innerHTML = 'Join';
        memberCount.innerHTML = data['members'];
      }
    })
    .catch((e) => alert(e))
  }
  
  function removeProfilePic(username) {
    const picture = document.getElementById('Picture');
  
    fetch(`/api/remove-profile-picture/${username}`, {method: 'POST'})
    .then((res) => res.json())
    .then((data) => {
        picture.src = '/static/images/upload_folder/users/'+ data['picture'];
    })
    .catch((e) => alert('Could not remove profile picture.'));
  }
  
  function follow(username) {
    const followCount = document.getElementById(`followers-count-${username}`);
    const followButton = document.getElementById(`follow-button-${username}`);
  
    fetch(`/api/follow/${username}/`, {method: 'POST'})
    .then((res) => res.json())
    .then((data) => {
        followCount.innerHTML = data['followers'];
        if (data['followed'] === true) {
          followButton.innerHTML = "Following";
        } else {
          followButton.innerHTML = "Follow";
        }
    })
    .catch((e) => alert('Could not follow user.'));
  }