import type { Metadata } from 'next';
import './globals.css'
import { Providers } from "./providers";
import Header from "../components/UI/header"
import { siteConfig } from '../config/site.config';
import { layoutConfig } from '../config/layout.config';

export const metadata: Metadata = {
    title: siteConfig.title,
    description: siteConfig.description
};

export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html>
            <body>
                <Providers>
                    <Header />
                    <main className={
                        `flex flex-col 
                        h-[calc(100vh-${layoutConfig.headerHeight}-${layoutConfig.footerHeight})] 
                        w-full justify-start items-center`
                    }>
                        {children}
                    </main>
                    <footer className={`flex h-[${layoutConfig.footerHeight}] justify-center items-center`}>
                        <p>
                            {siteConfig.description}
                        </p>
                    </footer>
                </Providers>
            </body>
        </html>
    )
}
