"use client"

import { Button } from "@heroui/button";
import Link from "next/link";

const NotPoundPage = () => {
    return (
        <div className="flex flex-col items-center justify-center ">
            <div className="text-8xl font-bold text-gray-300">404</div>
            <h1 className="text-3xl font-bold tracking-tight">Page Not Found</h1>

            <div className="pt-6">
                <Button as={Link} color="primary" variant="shadow" href="/">
                Return To Main
                </Button>
            </div>    
        </div>
    );
}

export default NotPoundPage;
