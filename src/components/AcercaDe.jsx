import React from 'react';

const AcercaDe = () => {
  return (
    <div className="property-card max-w-6xl mx-auto p-6 bg-white shadow-lg rounded-lg">
      <div className="grid md:grid-cols-2 gap-8">
        <div className="property-image">
          {/* Placeholder for the property image */}
          <img 
            src="/src/assets/img/casas.jpg" 
            alt="Modern house with pool"
            className="w-full h-[600px] object-cover rounded-lg"
          />
        </div>
        
        <div className="property-details flex flex-col justify-between">
          <div>
            <div className="location-info flex items-center gap-2 mb-4">
              <div className="location-icon text-purple-400">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
                </svg>
              </div>
              <div>
                <h2 className="text-2xl font-bold">87 Mishaum Point Rd,</h2>
                <p className="text-gray-600">Dartmouth, MA 02748</p>
              </div>
            </div>

            <p className="text-gray-700 mb-6">
              On the best lot at Phuket is situated the Kaihu Residence. It features Ipe 
              hardwood flooring on the interior and granite stone flooring on the lanais, high 
              vaulted cedar ceilings.
            </p>

            <div className="features grid grid-cols-2 gap-4 mb-8">
              <div className="feature flex items-center gap-2">
                <span className="w-2 h-2 bg-red-400 rounded-full"></span>
                <span>Quiet Neighbourhood</span>
              </div>
              <div className="feature flex items-center gap-2">
                <span className="w-2 h-2 bg-red-400 rounded-full"></span>
                <span>Fabulous Views</span>
              </div>
              <div className="feature flex items-center gap-2">
                <span className="w-2 h-2 bg-red-400 rounded-full"></span>
                <span>Great Local Community</span>
              </div>
              <div className="feature flex items-center gap-2">
                <span className="w-2 h-2 bg-red-400 rounded-full"></span>
                <span>Large Play Center In Yard</span>
              </div>
            </div>
          </div>

          <div className="property-stats flex items-center justify-between bg-white p-4 rounded-lg shadow-sm">
            <div className="price">
              <span className="text-3xl font-bold text-red-400">$1,249,000</span>
            </div>
            <div className="stats flex gap-6">
              <div className="stat flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5 text-gray-600">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
                </svg>
                <span>1,286 sqft</span>
              </div>
              <div className="stat flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5 text-gray-600">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 21v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21m0 0h4.5V3.545M12.75 21h7.5V10.75M2.25 21h1.5m18 0h-18M2.25 9l4.5-1.636M18.75 3l-1.5.545m0 6.205l3 1m1.5.5l-1.5-.5M6.75 7.364V3h-3v18m3-13.636l10.5-3.819" />
                </svg>
                <span>2</span>
              </div>
              <div className="stat flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5 text-gray-600">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75" />
                </svg>
                <span>3</span>
              </div>
              <div className="stat flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5 text-gray-600">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
                </svg>
                <span>2</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AcercaDe
