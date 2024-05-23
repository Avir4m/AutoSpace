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
    .catch((e) => alert('Could not join forum.'))
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

function setAlert(comp, message, type) {
  comp.classList.remove('alert-danger', 'alert-success');
  comp.classList.add(type);
  comp.innerText = message;
  comp.classList.remove('hidden');
}

function deleteAccount() {
  const card = document.getElementById('overlay-card-messages-delete-account');
  const username = document.getElementById('username').value;
  const password = document.getElementById('password-delete').value;

  if (username === '' || password === '') {
    setAlert(card, 'Flieds are not allowed to be empty.', 'alert-danger');
  } else {
    fetch(`/api/user/delete_account/${username}/${password}`, {method : "POST"})
    .then((res) => res.json())
    .then((data) => {
        if (data.type === 'error') {
          setAlert(card, data.message, 'alert-danger')
        } else if (data.type === 'success') {
          window.location.reload();
        }
    })
    .catch((e) => alert("Could not delete account."));
  }
}

function changePassword() {
  const card = document.getElementById('overlay-card-messages-change-password');
  const password = document.getElementById('password');
  const password1 = document.getElementById('password1');
  const password2 = document.getElementById('password2');

  if (password1.value !== password2.value) {
    setAlert(card, 'Passwords don\'t match, please try again.', 'alert-danger')

  } else if (password1.value === '' && password1.value.length < 7) {
    setAlert(card, 'Passwords need to be at least 7 characters long.', 'alert-danger')

  } else {
    fetch(`/api/user/change_password/${password.value}/${password1.value}`, {method : "POST"})
    .then((res) => res.json())
    .then((data) => {
      if (data.type === "error") {
        var type = 'alert-danger'
      } else {
        var type = 'alert-success'
        password.value = '';
        password1.value = '';
        password2.value = '';
      }
      setAlert(card, data.message, type)
    })
    .catch((e) => alert("Couldn't change password."));
  }
}

function friend(id) {
  var btn = document.getElementById('friend-req-btn');
  fetch(`/api/friend/${id}`, {method : "POST"})
  .then((res) => res.json())
  .then((data) => {
    btn.textContent = data.button;
    if (data.type === 'success') {
      try {
        var cancelBtn = document.getElementById('friend-req-remove-btn');
        cancelBtn.remove();
      } catch (e) {
      }
    }
  })
}

function removeRequest(id) {
  var acceptBtn = document.getElementById('friend-req-btn');
  var cancelBtn = document.getElementById('friend-req-remove-btn');
  fetch(`/api/remove_request/${id}`, {method : "POST"})
  .then((res) => res.json())
  .then((data) => {
    acceptBtn.textContent = data.button;
    if (data.type === 'success') {
      try {
        cancelBtn.remove();
      } catch (e) {
      }
    }
  })
}