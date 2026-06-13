import { IFormData } from "../types/form-data"

export async function registerUser(formData: IFormData) {
    try {
        const { email, password, confirmPassword } = formData
        var result = await fetch(
            'http://127.0.0.1:8000/users',
            {
                "method": "POST",
                "headers": {"Content-Type": "application/json"},

                "body": JSON.stringify({
                    "email": email,
                    "password": password
                })
            }
        )
        if(result.status == 200){
            return await result.json()
        } else {
            return { "FastAPI Server Error Response:": await result.text }
        }  
    } catch (error) {
        return { "error": 'Registration Error!' }
    }
}
