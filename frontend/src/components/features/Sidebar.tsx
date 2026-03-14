import { NavLink } from 'react-router-dom';
import { MessageSquare, User, History, MapIcon } from 'lucide-react';
import { motion } from 'framer-motion';

const Sidebar = () => {
  const navItems = [
    { to: '/', icon: MessageSquare, label: 'Chat' },
    { to: '/trips', icon: History, label: 'Lịch sử' },
    { to: '/profile', icon: User, label: 'Hồ sơ' },
  ];

  return (
    <motion.div
      initial={{ x: -20, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      className="w-64 border-r bg-card flex flex-col h-full"
    >
      {/* Logo */}
      <div className="p-6 border-b">
        <div className="flex items-center gap-2">
          <div className="w-10 h-10 rounded-lg gradient-hero flex items-center justify-center">
            <MapIcon className="h-6 w-6 text-white" />
          </div>
          <div>
            <h1 className="font-bold text-xl">TravelAI</h1>
            <p className="text-xs text-muted-foreground">Trợ lý du lịch thông minh</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-2">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                isActive
                  ? 'bg-primary text-primary-foreground'
                  : 'hover:bg-muted'
              }`
            }
          >
            <item.icon className="h-5 w-5" />
            <span className="font-medium">{item.label}</span>
          </NavLink>
        ))}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t">
        <div className="bg-muted rounded-lg p-4">
          <p className="text-sm font-medium mb-2">💡 Mẹo</p>
          <p className="text-xs text-muted-foreground">
            Hãy cho tôi biết sở thích của bạn để có gợi ý tốt hơn!
          </p>
        </div>
      </div>
    </motion.div>
  );
};

export default Sidebar;
