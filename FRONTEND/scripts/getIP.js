const os = require('os');
const fs = require('fs');

const getLocalIp = () => {
  const interfaces = os.networkInterfaces();
  for (const name of Object.keys(interfaces)) {
    for (const iface of interfaces[name]) {
      if (iface.family === 'IPv4' && !iface.internal) {
        return iface.address;
      }
    }
  }
  return '127.0.0.1'; // Fallback
};

const ip = getLocalIp();
fs.writeFileSync(
  '.env.development.local',
  `VUE_APP_API_BASE_URL=http://${ip}:5001\n`,
  { flag: 'w' }
);