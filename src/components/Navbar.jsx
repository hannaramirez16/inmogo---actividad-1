import { useState } from 'react'
import burguerMenu from '../assets/img/icon-hamburger.svg'

export const Navbar = () => {
  const [open, setOpen] = useState(false)

  return (
    <div className="relative">
      {/* Hamburger (mobile) - inline SVG so we can color it */}
      <button
        onClick={() => setOpen(!open)}
        aria-label="Toggle menu"
        className="md:hidden p-2 text-blue-800"
      >
        <svg xmlns="http://www.w3.org/2000/svg" className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>

      {/* Desktop links */}
      <div className="hidden md:flex md:items-center md:gap-6">
        <ul className="hidden md:flex md:items-center md:gap-8 hover:text-blue-900 font-medium">
          <li className="cursor-pointer">Inicio</li>
          <li className="cursor-pointer">Propiedades</li>
          <li className="cursor-pointer">Contáctanos</li>
        </ul>

        {/* Icons on the right */}
        <div className="hidden md:flex items-center gap-4 ml-4">
          <button aria-label="Ver carrito" className="text-green-900 p-2 hover:text-green-700">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2 6m5-6v6m6-6v6m-9 0h10" />
            </svg>
          </button>
 
          <button aria-label="Mi cuenta" className="text-green-900 p-2 hover:text-green-700">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5.121 17.804A13.937 13.937 0 0112 15c2.485 0 4.805.62 6.879 1.704M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v2" opacity="0" />
            </svg>
          </button>
        </div>
      </div>

      {/* Mobile panel */}
      {open && (
        <>
          {/* overlay to close menu when clicking outside */}
          <div
            onClick={() => setOpen(false)}
            className="fixed inset-0 z-20 bg-black/20"
          />

          <div className="absolute right-4 top-full mt-3 w-80 bg-white rounded-lg shadow-lg z-30 p-6 text-center">
            {/* little pointer */}
            <div className="absolute -top-3 right-6 w-4 h-4 bg-white rotate-45 shadow-sm" />

            <ul className="flex flex-col gap-4">
              <li className="text-gray-700">Inicio</li>
              <li className="text-gray-700">Propiedades</li>
              <li className="text-gray-700">Contáctanos</li>
            </ul>

            <button className="mt-6 bg-green-500 hover:bg-green-600 px-6 py-2 rounded-full font-bold">
              Inicio de Sesión
            </button>
          </div>
        </>
      )}
    </div>
  )
}