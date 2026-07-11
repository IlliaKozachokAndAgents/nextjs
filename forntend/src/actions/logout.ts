export async function logoutUser() {
   await fetch('http://127.0.0.1:8000/auth/logout', {'method': 'DELETE'})
}
