import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Resturant-Chatbot",
  description: "Order with a chatbot!",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className="antialiased"
      >
        {children}
      </body>
    </html>
  );
}
