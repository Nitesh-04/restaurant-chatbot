'use client'

import { useState } from 'react'
import { MessageCircle, X } from 'lucide-react'

export default function Chatbot() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <div className="fixed bottom-4 right-4 z-50">
      <div className="flex flex-col">
        <div 
          className={`transition-all duration-300 ease-in-out ${
            isOpen ? 'h-[430px] opacity-100' : 'h-0 opacity-0'
          } overflow-hidden`}
        >
          <iframe
            allow="microphone"
            width="350"
            height="430"
            src="https://console.dialogflow.com/api-client/demo/embedded/92939191-397a-4094-b9c2-79af8147d002"
            className="border rounded-t-lg bg-white"
          />
        </div>

        <button
          onClick={() => setIsOpen(!isOpen)}
          className="flex items-center justify-between w-[350px] px-4 py-3 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors"
          style={{
            borderRadius: isOpen ? '0 0 0.5rem 0.5rem' : '0.5rem'
          }}
        >
          <div className="flex items-center gap-2">
            <MessageCircle size={20} />
            <span className="font-medium">Chat with us</span>
          </div>
          {isOpen && <X size={20} />}
        </button>
      </div>
    </div>
  )
}
