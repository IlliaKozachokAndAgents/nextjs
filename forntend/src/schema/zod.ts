import { email, object, string } from "zod"

export const loginSchema = object({
    email: email({ error: "Invalid email" })
        .min(1, "Email is required"),
    password: string({ error: "Password is required" })
        .min(1, "Password is required")
        .min(8, "Password must be more than 8 characters")
        .max(32, "Password must be less than 32 characters"),
})
