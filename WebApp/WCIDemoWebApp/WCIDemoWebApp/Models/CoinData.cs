using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace WCIDemoWebApp.Models
{
    public class CoinData
    {
        private DBContext context;

        public int Id { get; set; }

        public string Label { get; set; }

        public string Name { get; set; }

        public Decimal Price { get; set; }

        public Decimal Volume { get; set; }

        public DateTime Timestamp { get; set; }
    }
}
