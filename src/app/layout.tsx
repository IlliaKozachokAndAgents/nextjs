import './globals.css'
import { Providers } from "./providers";
import Header from "../components/UI/header"

export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html>
            <body><Providers><Header/>{children}</Providers></body>
        </html>
    )
}
