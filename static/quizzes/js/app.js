
function toggleUserInfo() {
    const userInfo = document.getElementById('user-info');
    if (userInfo.style.display === 'none' || userInfo.style.display === '') {
        userInfo.style.display = 'block';
    } else {
        userInfo.style.display = 'none';
    }
}

