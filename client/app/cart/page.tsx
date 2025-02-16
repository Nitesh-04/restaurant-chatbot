'use client'

import { useState, useEffect } from 'react'
import Navbar from '../_components/Navbar'
import { Trash2 } from 'lucide-react'
import { CartItem } from '../_types'
import Link from 'next/link'

export default function Cart() {
  const [cartItems, setCartItems] = useState<CartItem[]>([])

  useEffect(() => {
    const savedCart = localStorage.getItem('cart')
    if (savedCart) {
      setCartItems(JSON.parse(savedCart))
    }
  }, [])

  const removeFromCart = (itemId: number) => {
    const newCart = cartItems.filter(item => item.id !== itemId)
    setCartItems(newCart)
    localStorage.setItem('cart', JSON.stringify(newCart))
  }

  const total = cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0)

  return (
    <div className="min-h-screen bg-white">
      <Navbar cartItems={cartItems} />
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-orange-500 mb-8">Your Cart</h1>
        
        {cartItems.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-gray-600 mb-4">Your cart is empty</p>
            <Link 
              href="/menu"
              className="bg-orange-500 text-white px-6 py-3 rounded-lg hover:bg-orange-600 inline-block"
            >
              Browse Menu
            </Link>
          </div>
        ) : (
          <div>
            {cartItems.map((item) => (
              <div 
                key={item.id}
                className="flex justify-between items-center border-b py-4"
              >
                <div>
                  <h2 className="text-xl font-semibold">{item.name}</h2>
                  <p className="text-gray-600">
                    ${item.price.toFixed(2)} x {item.quantity}
                  </p>
                </div>
                <button
                  onClick={() => removeFromCart(item.id)}
                  className="text-red-500 hover:text-red-600"
                >
                  <Trash2 />
                </button>
              </div>
            ))}
            
            <div className="mt-8 flex justify-between items-center">
              <p className="text-xl font-semibold">
                Total: ${total.toFixed(2)}
              </p>
              <button
                className="bg-orange-500 text-white px-6 py-3 rounded-lg hover:bg-orange-600"
              >
                Checkout
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}