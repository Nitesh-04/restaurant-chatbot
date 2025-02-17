'use client'

import { useState, useEffect } from 'react'
import Navbar from '../_components/Navbar'
import { MenuItem, CartItem } from '../_types'

export default function Menu() {
  const [menuItems, setMenuItems] = useState<MenuItem[]>([])
  const [cartItems, setCartItems] = useState<CartItem[]>([])

  useEffect(() => {
    async function fetchMenu() {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/menu`)
        if (!response.ok) {
          throw new Error('Network response was not ok')
        }
        const data = await response.json()
        setMenuItems(data.menu)
      } catch (error) {
        console.error('Error fetching menu:', error)
      }
    }

    fetchMenu()
  }, [])

  const addToCart = async (menuItem: MenuItem) => {
    setCartItems(prevItems => {
      const existingItem = prevItems.find(item => item.id === menuItem.id);
      
      if (existingItem) {
        return prevItems.map(item =>
          item.id === menuItem.id
            ? { ...item, quantity: item.quantity + 1 }
            : item
        );
      }
      
      return [...prevItems, { ...menuItem, quantity: 1 }];
    });
  
    const payload = {
      user_id: 11, // replace this with dynamic user_id
      item_id: menuItem.id,
      quantity: 1,
    };
  
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/cart/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'admin-key': `${process.env.NEXT_PUBLIC_AUTH_KEY}`,
        },
        body: JSON.stringify(payload),
      });
  
      if (!response.ok) {
        throw new Error('Failed to add item to the cart');
      }
      
      console.log('Item added to cart successfully');
    } catch (error) {
      console.error('Error adding item to cart:', error);
    }
  };
  

  return (
    <div className="min-h-screen bg-white">
      <Navbar cartItems={cartItems} />
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-orange-500 mb-8">Our Menu</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {menuItems.slice(3).map((item) => (
            <div 
              key={item.id} 
              className="border rounded-lg p-4 shadow-md hover:shadow-lg transition"
            >
              <h2 className="text-xl text-gray-600 font-semibold mb-2">{item.item_name}</h2>
              <p className="text-gray-600 mb-4">Rs.{item.price.toFixed(2)}</p>
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
