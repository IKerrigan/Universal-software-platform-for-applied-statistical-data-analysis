const token = localStorage.getItem('auth');

if (['/', '/index.html'].includes(window.location.pathname) && !token) {
    if (!token) {
        window.location = '/login.html';
    }
}

if (['/login.html', '/register.html'].includes(window.location.pathname) && token) {
    window.location = '/'
}

axios.defaults.headers.common['Authorization'] = token;