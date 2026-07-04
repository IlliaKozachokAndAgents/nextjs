"use client"

import { Form } from "@heroui/form";
import { Input } from "@heroui/input";
import { Button } from "@heroui/button";
import React, { useState } from "react";
import { registerUser } from "../actions/register";


interface IProps {
    onClose: () => void
}

const RegistrationForm = ({onClose}: IProps) => {
    const [formData, setFormData] = useState({
        email: "",
        password: "",
        confirmPassword: "",
    })
    const validateEmail = (email: string) => {
        const emailRegEx = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegEx.test(email);
    };
    const handleSubmit =async (e:React.FormEvent) => {
        e.preventDefault()
        const result = await registerUser(formData)
        console.log('Form Submitted! ', result)

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
                        if (!validateEmail(value)) return 'Email is not correct!';
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
                        if (value.length < 6) return 'Password must by longer then 6 symbols!';
                        return null;
                    }
                }
            />
            <Input
                isRequired
                name="confirmPassword"
                placeholder="Confirm your password"
                type="password"
                value={formData.confirmPassword}
                classNames={{
                    inputWrapper: "bg-default-100",
                    input: "text-sm focus:outline-none"
                }}
                onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                validate={
                    (value) => { 
                        if (!value) return 'Password is required!';
                        if (value !== formData.password) return 'Passwords does not match!';
                        return null;
                    }
                }
            />
            <div className="flex w-[100%] gap-4 items-center pt-8 justify-end">
                <Button variant="light" onPress={onClose}>Close</Button>
                <Button color="primary" type="submit">Register</Button>
            </div>
        </Form>
    );
}

export default RegistrationForm;
