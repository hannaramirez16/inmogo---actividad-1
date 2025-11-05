import { useState, useEffect } from 'react'
import bgImage from '../assets/img/inicio.jpg'

export const Main = () => {
	const [scrollY, setScrollY] = useState(0)

	useEffect(() => {
		const onScroll = () => setScrollY(window.scrollY || window.pageYOffset)
		window.addEventListener('scroll', onScroll)
		return () => window.removeEventListener('scroll', onScroll)
	}, [])

	return (
		<div className="w-full">
			{/* Hero Section */}
			<section className="h-screen pt-28 relative bg-cover bg-center bg-no-repeat" style={{ backgroundImage: `url(${bgImage})` }}>
				{/* subtle overlay for better contrast */}
				<div className="absolute inset-0 bg-white/20" />
				<div className="relative z-10 container mx-auto px-4">
					<div className="flex flex-col items-center md:items-start justify-center gap-8 md:gap-12 py-40">
						{/* Text block (image removed) */}
						<div className="w-full md:w-2/3 text-center md:text-left">
							<h1
								className="text-4xl md:text-6xl lg:text-8xl font-extrabold mb-4 text-green-900"
								style={{ textShadow: '0 8px 24px rgba(34,197,94,0.18)' }}
							>
								Encuentra tu lugar ideal
							</h1>

							<div className="mt-8 md:mt-12">
								<button className="bg-white text-green-800 px-8 py-3 rounded-full font-semibold shadow-lg">Explora nuestras Propiedades</button>
							</div>
						</div>
					</div>
				</div>

				{/* Decorative silhouettes */}
				<div className="absolute bottom-0 left-0 right-0 mx-auto w-full max-w-6xl h-40">
					<div className="relative w-full h-full">
						<div className="absolute bottom-0 left-1/6 w-24 h-36 bg-white/20 rounded-t-md" />
						<div className="absolute bottom-0 left-2/6 w-32 h-44 bg-white/20 rounded-t-md" />
						<div className="absolute bottom-0 left-3/6 w-28 h-52 bg-white/20 rounded-t-md" />
						<div className="absolute bottom-0 left-4/6 w-24 h-36 bg-white/20 rounded-t-md" />
					</div>
				</div>
			</section>
		</div>
	)
}