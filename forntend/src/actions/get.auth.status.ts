export async function isAuthorize() {
    try {
        var result = await fetch(
            'http://127.0.0.1:8000/auth/users/me', { method: "GET", credentials: "include" }
        )
        if (result.status == 200) {
            return [await result.json(), 'Authorized']
        } else {
            return [null, 'Authorized']
        }
    } catch (error) {
        return [null, 'Authorized']
    }
}
