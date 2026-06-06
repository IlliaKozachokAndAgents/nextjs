import { IFormData } from "../types/form-data"

export async function registerUser (formData: IFormData) {
    const {email, password, confirmPassword} = formData
    console.log('Extracted data from form', email, password, confirmPassword)

    // Отут має бути запит на FastAPI сервер!
    var result = await fetch('http://127.0.0.1:8000')
    console.log('Data from FastAPI Server: ', await result.json())
}
