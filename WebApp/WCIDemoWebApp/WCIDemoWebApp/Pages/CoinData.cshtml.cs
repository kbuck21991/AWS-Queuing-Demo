using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using WCIDemoWebApp.Models;

namespace WCIDemoWebApp.Pages
{
    public class CoinDataModel : PageModel
    {
        public string CoinData { get; set; }
        public void OnGet()
        {
            DBContext context = HttpContext.RequestServices.GetService(typeof(DBContext)) as DBContext;
            CoinData = context.GetCoinData()[0].Text;

        }
    }
}