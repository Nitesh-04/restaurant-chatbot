'use client'

import { useState, useEffect } from 'react'
import Navbar from '../_components/Navbar'
import { Trash2 } from 'lucide-react'
import { CartItem } from '../_types'
import Link from 'next/link'

export default function Cart() {
  const [cartItems, setCartItems] = useState<CartItem[]>([])
  
  useEffect(() => {
    async function fetchCart() {
      try {
        const response = await fetch('http://127.0.0.1:8000/cart/11',{
          headers: {
            'admin-key': `${process.env.NEXT_PUBLIC_AUTH_KEY}`,
          },
        })
        const data = await response.json()

        if (data.cart) {
          setCartItems(data.cart)
        }
      } catch (error) {
        console.error('Error fetching cart:', error)
      }
    }

    fetchCart()
  }, [])

  async function removeFromCart (itemId: number) {
    const newCart = cartItems.filter(item => item.id !== itemId)
    setCartItems(newCart)
    localStorage.setItem('cart', JSON.stringify(newCart))
  
    const userId = 11
  
    try {
      await fetch(`http://127.0.0.1:8000/cart?user_id=${userId}&item_id=${itemId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'admin-key': `${process.env.NEXT_PUBLIC_AUTH_KEY}`,
        },
      })
      console.log('Item removed from cart')
    } catch (error) {
      console.error('Error removing item from cart on the server:', error)
    }
  }

  async function placeOrder()
  {
      const userId = 11; 
      const payload = {
        user_id: userId,
      };

      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/orders/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'admin-key': `${process.env.NEXT_PUBLIC_AUTH_KEY}`,
          },
          body: JSON.stringify(payload),
        });
    
        if (!response.ok) {
          throw new Error('Failed to order');
        }
        
        console.log('Order placed successfully');
      }
      catch (error) {
        console.error('Error placing order:', error)
      }

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
                  {item.id}<h2 className="text-xl text-gray-600 font-semibold"> {item.item_name}</h2>
                  <p className="text-gray-600">
                    Rs.{item.price.toFixed(2)} x {item.quantity}
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
            
            <div className="mt-8 flex justify-start gap-10 items-center">
              <p className="text-xl text-gray-600 font-semibold">
                Total: Rs.{total.toFixed(2)}
              </p>
              <button onClick={placeOrder}
                className="bg-orange-500 text-white px-6 py-3 rounded-lg hover:bg-orange-600"
              >
                Order
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
