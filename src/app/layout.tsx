import type { Metadata } from 'next';
import './globals.css'
import { Providers } from "./providers";
import Header from "../components/UI/layout/header"
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
                    <main 
                        className="flex flex-col w-full justify-start items-center"
                        style={{height: `calc(100vh - ${layoutConfig.headerHeight} - ${layoutConfig.footerHeight})`}}
                    >
                        {children}
                    </main>
                    <footer
                        className="flex justify-center items-center"
                        style={{height: layoutConfig.footerHeight}}
                    >
                        <p>
                            {siteConfig.description}
                        </p>
                    </footer>
                </Providers>
            </body>
        </html>
    )
}
