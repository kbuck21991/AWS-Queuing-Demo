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

        public string Text { get; set; }
    }
}
