

export async function loginUser(email: string, password: string) {
    try {
        var result = await fetch(
            'http://127.0.0.1:8000/auth/authorize',
            {
                "method": "POST",
                "headers": { "Content-Type": "application/x-www-form-urlencoded" },

                "body": new URLSearchParams({
                    "username": email,
                    "password": password,
                    "grant_type": "password"
                })
            }
        )
        if (result.status == 200) {
            return await result.json()
        } else {
            console.error('FastAPI Server Error Response: ', await result.text())
            return { "error": 'Registration Error!' }
        }
    } catch (error) {
        console.error('Registration Error! ', error)
        return { "error": 'Registration Error!' }
    }
}
