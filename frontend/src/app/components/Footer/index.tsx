import React from 'react';

const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();
  
  const socialLinks = [
    { label: 'Facebook', letter: 'F' },
    { label: 'Twitter', letter: 'T' },
    { label: 'Instagram', letter: 'I' },
    { label: 'YouTube', letter: 'Y' },
  ];

  return (
    <footer className="bg-[#F9F9F9] text-gray-700 py-8">
      <div className="container mx-auto px-6">
        <div className="flex flex-col md:flex-row justify-between items-center">
          {/* Logo and company name */}
          <div className="flex items-center gap-2 mb-4 md:mb-0">
            <div className="w-8 h-8 bg-gray-700 rounded-lg"></div>
            <span className="font-semibold text-gray-700">TheCompany</span>
          </div>

          {/* Navigation links */}
          <nav className="flex gap-6 mb-4 md:mb-0">
            <a href="/privacy" className="text-sm text-gray-700 hover:text-gray-900 transition-colors">
              Privacy
            </a>
            <a href="/about" className="text-sm text-gray-700 hover:text-gray-900 transition-colors">
              About
            </a>
            <a href="/terms" className="text-sm text-gray-700 hover:text-gray-900 transition-colors">
              Terms
            </a>
            <a href="/contact" className="text-sm text-gray-700 hover:text-gray-900 transition-colors">
              Contact Us
            </a>
          </nav>

          {/* Social icons */}
          <div className="flex gap-3">
            {socialLinks.map((social, index) => (
              <button
                key={index}
                className="w-8 h-8 bg-gray-700 rounded-full flex items-center justify-center hover:bg-gray-600 transition-colors"
                aria-label={social.label}
              >
                <span className="text-xs font-semibold text-white">{social.letter}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Copyright */}
        <div className="text-center mt-6 pt-6 border-t border-gray-300">
          <p className="text-sm text-gray-700">
            © {currentYear} All right reserved
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;