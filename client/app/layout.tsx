import type { Metadata } from "next";
import "./globals.css";
import Chatbot from "./_components/Chatbot";

export const metadata: Metadata = {
  title: "Resturant-Chatbot",
  description: "Order with a chatbot!",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        {children}
          <Chatbot/>
      </body>
    </html>
  )
}
