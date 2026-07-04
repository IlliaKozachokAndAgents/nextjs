"use client"

import { Form } from "@heroui/form";
import { Input } from "@heroui/input";
import { Button } from "@heroui/button";
import React, { useState } from "react";
import { loginUser } from "../actions/login";
import { cookies } from "next/headers";

interface IProps {
    onClose: () => void
}

const LoginForm = ({onClose}: IProps) => {
    const [formData, setFormData] = useState({
        email: "",
        password: "",
    })
    const handleSubmit =async (e:React.FormEvent) => {
        e.preventDefault()

        const cookieStore = await cookies()
        const token = await loginUser(formData.email, formData.password)
        cookieStore.set('session', token, {httpOnly: true})
        
        console.log('Logged In!')
        onClose()
    }
    return (
        <Form className="w-full max-w-xs" onSubmit={handleSubmit}>
            <Input
                aria-label="Email"
                isRequired
                name="email"
                placeholder="Enter your email"
                type="email"
                value={formData.email}
                classNames={{
                    inputWrapper: "bg-default-100",
                    input: "text-sm focus:outline-none"
                }}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                validate={
                    (value) => { 
                        if (!value) return 'Email is required!';
                        return null;
                    }
                }
            />
            <Input
                isRequired
                name="password"
                placeholder="Enter your password"
                type="password"
                value={formData.password}
                classNames={{
                    inputWrapper: "bg-default-100",
                    input: "text-sm focus:outline-none"
                }}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                validate={
                    (value) => { 
                        if (!value) return 'Password is required!';
                        return null;
                    }
                }
            />
            <div className="flex w-[100%] gap-4 items-center pt-8 justify-end">
                <Button variant="light" onPress={onClose}>Close</Button>
                <Button color="primary" type="submit">Login</Button>
            </div>
        </Form>
    );
}

export default LoginForm;
