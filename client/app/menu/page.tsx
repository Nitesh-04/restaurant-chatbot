'use client'

import { useState } from 'react'
import Navbar from '../_components/Navbar'
import { MenuItem, CartItem } from '../_types'

const menuItems: MenuItem[] = [
  { id: 8, name: 'Margherita Pizza', price: 9.99 },
  { id: 9, name: 'Veg Burger', price: 5.49 },
  { id: 10, name: 'Pasta Alfredo', price: 7.99 }
]

export default function Menu() {
  const [cartItems, setCartItems] = useState<CartItem[]>([])

  const addToCart = (menuItem: MenuItem) => {
    setCartItems(prevItems => {
      const existingItem = prevItems.find(item => item.id === menuItem.id)
      if (existingItem) {
        return prevItems.map(item =>
          item.id === menuItem.id
            ? { ...item, quantity: item.quantity + 1 }
            : item
        )
      }
      return [...prevItems, { ...menuItem, quantity: 1 }]
    })
  }

  return (
    <div className="min-h-screen bg-white">
      <Navbar cartItems={cartItems} />
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-orange-500 mb-8">Our Menu</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {menuItems.map((item) => (
            <div 
              key={item.id} 
              className="border rounded-lg p-4 shadow-md hover:shadow-lg transition"
            >
              <h2 className="text-xl text-gray-600 font-semibold mb-2">{item.name}</h2>
              <p className="text-gray-600 mb-4">${item.price.toFixed(2)}</p>
              <button
                onClick={() => addToCart(item)}
                className="bg-orange-500 text-white px-4 py-2 rounded hover:bg-orange-600"
              >
                Add to Cart
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
