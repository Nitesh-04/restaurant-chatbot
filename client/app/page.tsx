import Navbar from './_components/Navbar'
import Link from 'next/link'

export default function Home() {
  return (
    <main className="min-h-screen bg-white">
      <Navbar cartItems={[]} />
      <div className="container mx-auto px-4 py-16">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-orange-500 mb-4">
            Welcome to Restaurant with Chatbot
          </h1>
          <p className="text-gray-600 mb-8">
            Delicious food delivered fast to your doorstep
          </p>
          <Link 
            href="/menu"
            className="bg-orange-500 text-white px-6 py-3 rounded-lg hover:bg-orange-600 inline-block"
          >
            Order Now
          </Link>
        </div>
      </div>
    </main>
  )
}