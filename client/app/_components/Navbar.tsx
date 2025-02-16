import Link from 'next/link'
import { ShoppingCart } from 'lucide-react'
import { CartItem } from '../_types'

interface NavbarProps {
  cartItems: CartItem[];
}

export default function Navbar ({ cartItems }: NavbarProps) {
  const cartItemCount = cartItems.reduce((sum, item) => sum + item.quantity, 0)

  return (
    <nav className="bg-orange-500 p-4">
      <div className="container mx-auto flex justify-between items-center">
        <Link href="/" className="text-white text-2xl font-bold">
          FastFood
        </Link>
        <div className="flex gap-4">
          <Link href="/menu" className="text-white hover:text-orange-200">
            Menu
          </Link>
          <Link href="/cart" className="text-white hover:text-orange-200 relative">
            <ShoppingCart />
            {cartItemCount > 0 && (
              <span className="absolute -top-2 -right-2 bg-white text-orange-500 rounded-full px-2 text-sm">
                {cartItemCount}
              </span>
            )}
          </Link>
        </div>
      </div>
    </nav>
  )
}