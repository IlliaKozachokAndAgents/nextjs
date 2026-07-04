import { loginSchema } from "../schema/zod"
import { IFormData } from "../types/form-data"

export async function registerUser(formData: IFormData) {
    if (formData.email !== formData.confirmPassword) {
        return { error: "Passwords does not match!" }
    }

    try {
        const { email, password } = loginSchema.parse(formData)

        var result = await fetch(
            'http://127.0.0.1:8000/users',
            {
                "method": "POST",
                "headers": { "Content-Type": "application/json" },

                "body": JSON.stringify({
                    "email": email,
                    "password": password
                })
            }
        )
        if (result.status == 201) {
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
