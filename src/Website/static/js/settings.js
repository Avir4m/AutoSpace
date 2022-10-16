function privateAccount(username) {

    var checkBox = document.getElementById("privateAccount");
    
    fetch(`/api/user/${username}/settings/private_account`, {method: 'POST'})
    .then((res) => res.json())
    .then((data) => {
        if (data['private_account'] === true) {
            
            checkBox.checked = true
        } else {
            checkBox.checked = false
        }
    })
    .catch((e) => alert('opss..'));
  }


function getPreferences(username) {
    var checkBox = document.getElementById("privateAccount");

    fetch(`/api/user/${username}/settings/get_preferences`, {method: 'POST'})
    .then((res) => res.json())
    .then((data) => {
        if (data['private_account'] === true) {
            
            checkBox.checked = true
        } else {
            checkBox.checked = false
        }
    })
    .catch((e) => alert('opss..'));
}