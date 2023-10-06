const crypto = require('crypto');
const fs = require('fs');

//input: mac address(lowercase) and salt 
function computeHashMac(mac_add, salt){
    const hash = crypto.createHash('sha224');
    //space between mac and salt 
    data = hash.update(mac_add + ' ' + salt, 'utf-8');
    gen_hash = data.digest('hex');
    console.log('hash: ' + gen_hash);
}

function readMacAddressesFromCSV(csvFilePath, salt) {
    fs.readFile(csvFilePath, 'utf-8', (err, data) => {
      if (err) {
        console.error('Error reading CSV file:', err);
        return;
      }
  
      const macAddresses = data.split('\n').map((line) => line.trim());
  
      macAddresses.forEach((mac) => {
        computeHashMac(mac, salt);
      });
    });
  }

  readMacAddressesFromCSV('./macs.csv', 'f405e1ca3c303ff374fcceb647c54d4915a242663f66f6f0a8d4a1ad')