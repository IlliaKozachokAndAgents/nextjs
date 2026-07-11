"use client"

import { Button } from "@heroui/button";
import { Navbar, NavbarBrand, NavbarContent, NavbarItem } from "@heroui/navbar";
import Image from "next/image";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { siteConfig } from "../../../config/site.config";
import { layoutConfig } from "../../../config/layout.config";
import RegistrationModal from "../modals/registration.modal";
import LoginModal from "../modals/login.modal";
import { useState } from "react";
import { logoutUser } from "../../../actions/logout";


export const Logo = () => {
    return <Image
        src="/logo.png"
        alt={siteConfig.title}
        width={26}
        height={26}
        priority
    />;
};

export default function Header() {
    const pathname = usePathname()

    const [session, setSession] = useState(null);
    const [status, setStatus] = useState(null);

    console.log('session', session)
    console.log('status', status)

    const getNavItems = () => {
        return siteConfig.navItems.map((item) => {
            const isActive = pathname === item.href

            return (
                <NavbarItem key={item.href}>
                    <Link
                        color="foreground"
                        href={item.href}
                        className={`px-3 pu-1
                            ${isActive ? "text-blue-500" : "text-foreground"}
                            hover:text-blue-300 hover:border
                            hover:border-blue-300 hover:rounded-md
                            transition-colors
                            transition-border
                            duration-200
                        `}
                    >
                        {item.label}
                    </Link>
                </NavbarItem>)
        })
    }

    const [isLoginOpen, setIsLoginOpen] = useState(false)
    const [isRegistrationOpen, setIsRegistrationOpen] = useState(false)

    const handleLogout = async () => {
        await logoutUser()
    }

    return (
        <Navbar style={{ height: layoutConfig.headerHeight }}>
            <NavbarBrand>
                <Link href="/" className="flex gap-1">
                    <Logo />
                    <p className="font-bold text-inherit">{siteConfig.title}</p>
                </Link>
            </NavbarBrand>
            <NavbarContent className="hidden sm:flex gap-4" justify="center">
                {getNavItems()}
            </NavbarContent>
            <NavbarContent justify="end">
                <NavbarItem className="hidden lg:flex">
                    <Button
                        as={Link}
                        href="#"
                        variant="flat"
                        onPress={handleLogout}
                    >
                        Logout
                    </Button>
                </NavbarItem>
                <NavbarItem className="hidden lg:flex">
                    <Button
                        as={Link}
                        href="#"
                        variant="flat"
                        onPress={() => { setIsLoginOpen(true) }}
                    >
                        Login
                    </Button>
                </NavbarItem>
                <NavbarItem>
                    <Button
                        as={Link}
                        color="primary"
                        href="#"
                        variant="flat"
                        onPress={() => { setIsRegistrationOpen(true) }}
                    >
                        Sign Up
                    </Button>
                </NavbarItem>
            </NavbarContent>

            <RegistrationModal
                isOpen={isRegistrationOpen}
                onClose={() => { setIsRegistrationOpen(false) }}
            />
            <LoginModal
                isOpen={isLoginOpen}
                onClose={() => { setIsLoginOpen(false) }}
            />
        </Navbar>
    );
}
